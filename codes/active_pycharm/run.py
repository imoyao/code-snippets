import os
import delegator

"""
本代码只在 Python3.7 & Windows 环境中测试通过，激活过程中如何路径包含中文名，可能会失败；
如果没有相应文件，肯定会失败；
如果找不到pycharm安装路径，建议直接在相应函数位置写入指定的路径。
"""


class ActivePycharm:
    PYCHARM_VMOPTIONS_FN = 'pycharm.exe.vmoptions'
    PYCHARM_VMOPTIONS_64_FN = 'pycharm64.exe.vmoptions'
    CRACK_NAME = 'JetbrainsCrack-release-enc.jar'
    CRACK_FP = os.path.normpath(os.path.join('./src', CRACK_NAME))
    AFTER_ACTIVE_STR = '''
Please paste those strings on activation code:
    
ThisCrackLicenseId-{
“licenseId”:”11011″,
“licenseeName”:”别院牧志”,
“assigneeName”:”masantu.com”,
“assigneeEmail”:”immoyao@gmail.com”,
“licenseRestriction”:””,
“checkConcurrentUse”:false,
“products”:[
{“code”:”II”,”paidUpTo”:”2099-12-31″},
{“code”:”DM”,”paidUpTo”:”2099-12-31″},
{“code”:”AC”,”paidUpTo”:”2099-12-31″},
{“code”:”RS0″,”paidUpTo”:”2099-12-31″},
{“code”:”WS”,”paidUpTo”:”2099-12-31″},
{“code”:”DPN”,”paidUpTo”:”2099-12-31″},
{“code”:”RC”,”paidUpTo”:”2099-12-31″},
{“code”:”PS”,”paidUpTo”:”2099-12-31″},
{“code”:”DC”,”paidUpTo”:”2099-12-31″},
{“code”:”RM”,”paidUpTo”:”2099-12-31″},
{“code”:”CL”,”paidUpTo”:”2099-12-31″},
{“code”:”PC”,”paidUpTo”:”2099-12-31″}
],
“hash”:”2911276/0″,
“gracePeriodDays”:7,
“autoProlongated”:false}
    '''

    def __init__(self):
        pass

    @staticmethod
    def which_pycharm():
        """
        找到pyCharm所在目录
        see also: https://stackoverflow.com/questions/304319/is-there-an-equivalent-of-which-on-the-windows-command-line
        :return:
        """
        cmd = 'where pycharm.exe'
        c = delegator.run(cmd)
        real_path = os.path.dirname(c.out)
        return real_path

    def modify_vmoptions(self, pycharm_bin_fp):
        """
        修改配置文件的内容
        :param pycharm_bin_fp:
        :return:
        """
        pycharm_vmoptions_fp = os.path.join(pycharm_bin_fp, self.PYCHARM_VMOPTIONS_FN)
        pycharm_vmoptions_64_fp = os.path.join(pycharm_bin_fp, self.PYCHARM_VMOPTIONS_64_FN)
        make_line = os.path.join(pycharm_bin_fp, self.CRACK_NAME)
        w_line = f'-javaagent:{make_line}\n'
        for file in [pycharm_vmoptions_fp, pycharm_vmoptions_64_fp]:
            if os.path.exists(file):
                with open(file, 'a+') as f:
                    f.write(w_line)
            else:
                raise FileExistsError(f'Sorry! I can not find {file}')

    def copy_crack(self):
        """
        拷贝破解器
        :return:
        """
        py_fp = self.which_pycharm()
        if os.path.exists(self.CRACK_FP):

            cmd = f'copy {self.CRACK_FP} {py_fp}'
            c = delegator.run(cmd)
            return c.return_code
        else:
            raise FileExistsError(f'File not Found:{self.CRACK_FP}')

    def active(self):
        """
        找到pycharm路径
        将破解器拷贝到指定目录
        修改配置文件
        最后填入激活码信息
        """
        pycharm_bin_path = self.which_pycharm()
        self.copy_crack()
        self.modify_vmoptions(pycharm_bin_path)
        print(f'{self.AFTER_ACTIVE_STR}')


if __name__ == '__main__':
    try_obj = ActivePycharm()
    try_obj.active()
