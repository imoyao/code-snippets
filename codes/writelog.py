
def get_hostname():
    try:
        hostname = ''
        retcode,proc = utils.cust_popen2([setting.hostname])
        result = proc.stdout.read().strip()
        if result:
            hostname = re.sub('\s+','',result).lower().replace('.','').replace('@','').replace('_','')
        return hostname
    except:
        debug.write_debug(debug.LINE(),"digisan",traceback.print_exc())


def write2log_db(func):
    def wrapper(*args, **kwargs):
        host = 'localhost'
        try:
            hostname = get_hostname()
        except Exception as e:
            traceback.print_exc()
            hostname = 'master'
        if hostname in ['master', 'slave']:
            if hostname == 'slave':
                host = 'master'     # 写入主机
        elif digithirdinfo.checkthirdnode():
            hostname = 'third'
        else:
            pass
        kwargs['host'] = host
        kwargs['hostname'] = hostname
        func(*args, **kwargs)
    return wrapper