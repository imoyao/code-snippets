import hashlib
import OpenSSL
import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayOfflineMarketShopCategoryQueryModel import AlipayOfflineMarketShopCategoryQueryModel
from alipay.aop.api.request.AlipayOfflineMarketShopCategoryQueryRequest import \
    AlipayOfflineMarketShopCategoryQueryRequest
import traceback
from alipay.aop.api.response.AlipayOfflineMarketShopCategoryQueryResponse import \
    AlipayOfflineMarketShopCategoryQueryResponse
from functools import partial
logger = logging.getLogger(__name__)
# 常见加密算法
CryptoAlgSet = (
    b'rsaEncryption',
    b'md2WithRSAEncryption',
    b'md5WithRSAEncryption',
    b'sha1WithRSAEncryption',
    b'sha256WithRSAEncryption',
    b'sha384WithRSAEncryption',
    b'sha512WithRSAEncryption'
)

class AliPayCert:
    """
    公钥证书相较RSA2密钥签名多了 app_cert_sn 和 alipay_root_cert_sn 参与签名，需要根据证书内容读出
    """

    def __init__(
            self,
            app_public_key_cert_string,  # 应用公钥证书
            alipay_public_key_cert_string,  # 支付宝公钥证书
            alipay_root_cert_string  # 支付宝根证书
    ):
        self._app_public_key_cert_string = self.cert_to_raw(app_public_key_cert_string)
        self._alipay_public_key_cert_string = self.cert_to_raw(alipay_public_key_cert_string)
        self._alipay_root_cert_string = self.cert_to_raw(alipay_root_cert_string)
        self._alipay_public_key_string = self.load_alipay_public_key_string()

    def load_alipay_public_key_string(self):
        # print(self._alipay_public_key_cert_string, '====11111111=============')
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, self._alipay_public_key_cert_string)
        # print(cert, f'===={cert.get_pubkey()}===========')
        return OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")

    def get_cert_sn(self, cert):
        """
        获取app_cert_sn
        """
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        cert_issues = cert.get_issuer()
        graphy = cert.to_cryptography()
        sn = str(graphy.serial_number)
        sub_with_sn = f'CN={cert_issues.CN},OU={cert_issues.OU},O={cert_issues.O},C={cert_issues.C}{sn}'
        _cert_sn = hashlib.md5(sub_with_sn.encode()).hexdigest()
        return _cert_sn

    def get_root_cert_sn(self, root_cert):
        """
        获取alipay_root_cert_sn
        """
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, root_cert)
        graphy = cert.to_cryptography()
        _subject = graphy.subject
        sn = graphy.serial_number
        # print(str(sn),'====================')
        sub_with_sn = str(_subject) + str(sn)
        root_cert_sn = hashlib.md5(sub_with_sn.encode()).hexdigest()
        return root_cert_sn
    @staticmethod
    def read_pem_cert_chain(certContent):
        """解析根证书"""
        # 根证书中，每个 cert 中间有两个回车间隔
        items = [i for i in certContent.split('\n\n') if i]
        load_cert = partial(OpenSSL.crypto.load_certificate, OpenSSL.crypto.FILETYPE_PEM)
        return [load_cert(c) for c in items]

    def new_get_root_cert_sn(self,rootCert):
        """ 根证书 SN 算法"""
        certs = self.read_pem_cert_chain(rootCert)
        rootCertSN = None
        for cert in certs:
            try:
                sigAlg = cert.get_signature_algorithm()
            except ValueError:
                continue
            if sigAlg in CryptoAlgSet:
                certIssue = cert.get_issuer()
                name = 'CN={},OU={},O={},C={}'.format(
                    certIssue.CN, certIssue.OU, certIssue.O, certIssue.C
                )
                string = name + str(cert.get_serial_number())
                certSN = hashlib.md5(string.encode()).hexdigest()
                if not rootCertSN:
                    rootCertSN = certSN
                else:
                    rootCertSN = rootCertSN + '_' + certSN
        return rootCertSN

    @property
    def app_cert_sn(self):
        return self.get_cert_sn(self._app_public_key_cert_string)

    @property
    def alipay_root_cert_sn(self):
        return self.new_get_root_cert_sn(self._alipay_root_cert_string)

    def cert_to_raw(self, cert_str):
        """
        原本的cert在存入的时候会转化为字符格式，所以需要继续处理成带换行符的格式
        为了区分密钥中的正文和分割符，此处先给替换成带特殊字符的cert，然后重新转化回来成标准格式
        """
        right_begin = '-----BEGIN CERTIFICATE-----'
        for_split_begin = '-----BEGIN--CERTIFICATE-----'
        right_end = '-----END CERTIFICATE-----'
        for_split_end = '-----END--CERTIFICATE-----'
        cert_str = cert_str.replace(right_begin, for_split_begin)
        cert_str = cert_str.replace(right_end, for_split_end)
        join_str = '\n'.join(cert_str.split(' '))
        join_str = join_str.replace(for_split_begin, right_begin)
        join_str = join_str.replace(for_split_end, right_end)
        return join_str


class Alipay:
    def create_client(self, access_infos=None):
        """
        配置客户端
        :param access_infos:
        :return:
        """
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
        if access_infos:
            is_cert_sign_type = self.check_is_cert_sign_type(access_infos)
            # 证书加签
            if is_cert_sign_type:
                alipay_client_config.app_id = access_infos.get('AppId')
                alipay_client_config.app_private_key = access_infos.get('app_private_key')
                alipay_client_config.alipay_public_key = access_infos.get('alipay_public_key_cert_string')
                client = DefaultAlipayClient(alipay_client_config, logger)
            else:
                alipay_client_config.app_id = access_infos.get('AppId')
                alipay_client_config.app_private_key = access_infos.get('api_secret')
                alipay_client_config.alipay_public_key = access_infos.get('api_key')
                client = DefaultAlipayClient(alipay_client_config, logger)
            return client

    def add_cert_params_before_fetch(self, alipay_request, app_cert_sn, alipay_root_cert_sn):
        """
        在发起请求前增加必要的证书签名
        :param alipay_request: 支付宝封装的请求处理
        :param app_cert_sn: 应用公钥参数
        :param alipay_root_cert_sn: 支付宝根证书参数
        :return:
        """
        alipay_request.add_other_text_param("app_cert_sn", app_cert_sn)
        alipay_request.add_other_text_param("alipay_root_cert_sn", alipay_root_cert_sn)
        return alipay_request

    def execute(self, api_client, api_request, api_response):
        """
        执行接口
        :param api_client:
        :param api_request:
        :param api_response:
        :return:
        """
        response_content = False
        try:
            response_content = api_client.execute(api_request)
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
        logger.info(f"result============={response_content}")
        if not response_content:
            logger.debug("failed execute")
            api_response = None
        else:
            # 解析响应结果
            api_response.parse_response_content(response_content)
        return api_response

    def check_is_cert_sign_type(self, access_infos):
        """"""
        # 是否为证书加签方式
        sign_type = access_infos.get('sign_type')
        # 证书加签
        return sign_type and sign_type == 'cert'


class Action(Alipay):
    def action(self, account_infos):
        if account_infos:
            model = AlipayOfflineMarketShopCategoryQueryModel()
            request = AlipayOfflineMarketShopCategoryQueryRequest(biz_model=model)
            api_client = self.create_client(account_infos)
            is_cert_sign_type = self.check_is_cert_sign_type(account_infos)
            if is_cert_sign_type:
                app_public_key_cert_string = account_infos.get('app_public_key_cert_string')
                alipay_public_key_cert_string = account_infos.get('alipay_public_key_cert_string')
                alipay_root_cert_string = account_infos.get('alipay_root_cert_string')

                alipay_cert_sign_instance = AliPayCert(app_public_key_cert_string, alipay_public_key_cert_string,
                                                       alipay_root_cert_string)
                try:
                    app_cert_sn = alipay_cert_sign_instance.app_cert_sn
                    alipay_root_cert_sn = alipay_cert_sign_instance.alipay_root_cert_sn
                    print(f'==is_cert_sign_type=={app_cert_sn}==={alipay_root_cert_sn}=====')
                    request = self.add_cert_params_before_fetch(request, app_cert_sn, alipay_root_cert_sn)
                except Exception as e:
                    logger.info(f'===is_cert_sign_type===error==={str(e)}===========')
                    return False

            response = AlipayOfflineMarketShopCategoryQueryResponse()
            try:
                resp = self.execute(api_client, request, response)
            except Exception as e:
                logger.info(f"AliPay==check_account==error--{str(e)}")
                return {"Code": 4004, "Msg": str(e), "Data": str(e)}
            if resp and resp.is_success():
                return True
            else:
                return 'error'


if __name__ == '__main__':
    account_infos = {"account_type": 274, "sign_type": "cert", "AppId": "20210xxxx697273",
                     "app_private_key": "{content}",
                     "app_public_key_cert_string": "-----BEGIN CERTIFICATE----- {content}-----END CERTIFICATE-----",
                     "alipay_public_key_cert_string": "-----BEGIN CERTIFICATE----- {content} -----END CERTIFICATE-----",
                     "alipay_root_cert_string": "-----BEGIN CERTIFICATE----- {content}-----END CERTIFICATE-----"}
    app_public_key_cert_string = account_infos.get('app_public_key_cert_string')
    alipay_public_key_cert_string = account_infos.get('alipay_public_key_cert_string')
    alipay_root_cert_string = account_infos.get('alipay_root_cert_string')

    alipay_cert = AliPayCert(app_public_key_cert_string, alipay_public_key_cert_string,
                             alipay_root_cert_string)
    print(alipay_cert.app_cert_sn, '=====app_cert_sn==')
    print(alipay_cert.alipay_root_cert_sn, '=====alipay_root_cert_sn==')