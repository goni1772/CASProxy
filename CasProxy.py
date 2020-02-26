from jpype import *
from flask import Flask, request
from urllib import parse
import requests
import logging as log
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
Service = config['SERVICE']
Secure = config['KEY']
Url = config['CASURL']

CPID = Service['CPID'] #CAS 연동 시스템 CP계정 ID - 신청 후 할당
CPPW = Service['CPPW']  #CAS 연동 시스템 CP PW - 신청 후 할당
SERVICECODE = Service['CloudGame_ServiceCode']
CASECODE = Service['CloudGame_CaseCode'] #CAS 신청 CASECODE - 신청 후 할당
INPUT = Service['input']

KEY1 = Secure['KEY1'] #CAS 암호화 KEY값 - 신청 후 할당
KEY2 = Secure['KEY2']
KEY3 = Secure['KEY3']
KEY4 = Secure['KEY4']
apiURL = Url['CASserver'] #CAS URL

classpath = "./CASIFJAVACodec.jar"  # jar 파일 경로 정의
startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)  # Python JVM 실행
DefaultExtractor = JPackage("com").lgtel.mmdb  # CAS 전문 암호화 패키지 정의
PyCasCryptoEncode = DefaultExtractor.CasCrypto.casCryptoEncode  # Encode Class.method 정의
PyCasCryptoDecode = DefaultExtractor.CasCrypto.casCryptoDecode  # Decode Class.method 정의

log.basicConfig(filename='./log.txt', level=log.DEBUG) #로그파일 생성 및 저장

app = Flask(__name__)
@app.route('/')
def default():
    return 'please send CTN!'

@app.route('/CASINFO', methods=['POST'])
def getCASInfo():
    InArg = request.form[INPUT]
    print(InArg)
    enCPPW = PyCasCryptoEncode(KEY1, KEY2, KEY3, KEY4, CPPW)
    param = {'CPTYPE': 'I', 'CPID': CPID, 'CPPWD': enCPPW, 'CASECODE': CASECODE, INPUT : InArg}
    enparam = parse.urlencode(param)
    URL = apiURL + enparam
    print(URL)
    CASinfo = requests.get(URL).headers
    print(CASinfo)
    res = CASinfo['RESP']
    deres = parse.parse_qs(res)
    # final = deres['RESPMSG']
    return(deres)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # 5000번 미만 포트는 sudo 권한 필요
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')