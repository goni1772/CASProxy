from jpype import *
from flask import Flask, request
from urllib import parse
import requests
import logging as log
import configparser

config = configparser.ConfigParser() #configparser 객체 생성
config.read('./config.ini') #config파일 리드
Service = config['SERVICE'] #SERVICE필드 정의
Secure = config['KEY'] #KEY필드 정의
Url = config['CASURL'] # CAS Url 필드 정의

CPID = Service['CPID'] #CAS 연동 시스템 CP계정 ID - 신청 후 할당
CPPW = Service['CPPW']  #CAS 연동 시스템 CP PW - 신청 후 할당
#SERVICECODE = Service['CloudGame_ServiceCode'] 
CASECODE = Service['CloudGame_CaseCode'] #CAS 신청 CASECODE - 신청 후 할당
INPUT = Service['input'] #CASECODE 발급시 신청한 Input값(ex. CTN or SUB_NO)

KEY1 = Secure['KEY1'] #CAS 암호화 KEY값 - 신청 후 할당
KEY2 = Secure['KEY2'] #CAS 암호화 KEY값 - 신청 후 할당
KEY3 = Secure['KEY3'] #CAS 암호화 KEY값 - 신청 후 할당
KEY4 = Secure['KEY4'] #CAS 암호화 KEY값 - 신청 후 할당
apiURL = Url['CASserver'] #CAS URL

classpath = "./CASIFJAVACodec.jar"  # jar 파일 경로 정의
startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)  # Python JVM 실행
DefaultExtractor = JPackage("com").lgtel.mmdb  # CAS 전문 암호화 패키지 정의
PyCasCryptoEncode = DefaultExtractor.CasCrypto.casCryptoEncode  # Encode Class.method 정의
PyCasCryptoDecode = DefaultExtractor.CasCrypto.casCryptoDecode  # Decode Class.method 정의

log.basicConfig(filename='./log.txt', level=log.DEBUG) #로그파일 생성 및 저장

app = Flask(__name__)
@app.route('/') # defualt router
def default():
    return 'please send CTN!'

@app.after_request
def apply_caching(response): # response header 값 추가
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/CASINFO', methods=['POST']) #CASINFO router
def getCASInfo():
    Arg = request.get_json('body') #request 전문에서 body 값 추출
    print(Arg)
    InArg = Arg[INPUT] #body에서 CASECODE에 정의된 INPUT값 추출(ex. CTN or SUB_NO)
    print(InArg)
    enCPPW = PyCasCryptoEncode(KEY1, KEY2, KEY3, KEY4, CPPW) #Password 암호화 method 호출(Python -> JVM -> jar)
    param = {'CPTYPE': 'I', 'CPID': CPID, 'CPPWD': enCPPW, 'CASECODE': CASECODE, INPUT : InArg} #CAS로 요청할 URL 파라미터 생성
    enparam = parse.urlencode(param) #생성된 파라미터 URL 인코딩
    URL = apiURL + enparam #암호화->인코딩된 파라미터를 CAS URL과 조합
    print(URL)
    CASinfo = requests.get(URL).headers #최종 생성된 URL로 get 하여 header 값 수신
    print(CASinfo)
    res = CASinfo['RESP'] #header에서 'RESP' 필드 추출
    deres = parse.parse_qs(res) #응답값 URL 디코딩
    # final = deres['RESPMSG'] 
    return(deres)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # 5000번 미만 포트는 sudo 권한 필요
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')
