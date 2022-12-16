# -*- coding: utf-8 -*-
import time
import requests
import base64
import ddddocr
import yagmail
from datetime import datetime


# -----------请在这里填写您的信息-------------
USERNAME = ""                        # 学号
PASSWORD = ""                      # 工软校园密码
SCHOOL = ""                           # 学校
PROVINCE = ""                        # 省
CITY = ""                                 # 市
DISTRICT = ""                           # 区
XM = ""                                   # 姓名
XUEYUAN = ""                   	# 学院
OPENID = ""        			# openid
QQMAIL = ""                       # 负责发送邮件的QQ邮箱
MAILAUTH = ""                  # QQ邮箱登录 POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 的验证码
RECEIVEMAIL = ""             # 负责接受邮件的邮箱
# -----------请在这里填写您的信息-------------

TIME = datetime.today().strftime('%Y-%m-%d')
USERAGENT = "Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) > AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 > Chrome/37.0.0.0 Mobile Safari/537.36 > MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI"
PROCESS = ["-------日志-------"]

# 获取JESSIONID
def getJESSIONID():
    header = {
        'User-Agent': USERAGENT,
    }
    Url = "http://xy.4009955.com/sfrzwx/auth/login"
    data = {
        "openid": OPENID,
        "dlfs": "zhmm"
    }
    responseRes = requests.get(Url, data=data, headers=header)
    jid = responseRes.headers['Set-Cookie'].split(';')[0]
    print(jid)
    PROCESS.append(jid)
    return jid


# 图像识别验证码，调用ddddocr库
def getYzm(jid):
    header = {
        'User-Agent': USERAGENT,
        'cookie': jid
    }
    postUrl = "http://xy.4009955.com/sfrzwx/wxsq/getYzm"
    responseRes = requests.post(postUrl, headers=header)
    base64code = responseRes.content.decode().split('"')[7].split(',')[1]
    imagedata = base64.b64decode(base64code)
    ocr = ddddocr.DdddOcr()
    yzm = ocr.classification(imagedata)
    x = "验证码：" + yzm
    print(x)
    PROCESS.append(x)
    return yzm


# 模拟登录
def login(jid, yzm):
    header = {
        'User-Agent': USERAGENT,
        "cookie": jid
    }
    postUrl = "http://xy.4009955.com/sfrzwx/wx/login"
    data = {
        "openid": OPENID,
        "dlfs": "zhmm",
        "sjschool": "",
        "sjh": "",
        "yzm:": "",
        "zhschool": SCHOOL,
        "username": USERNAME,
        "password": PASSWORD,
        "code": yzm
    }
    requests.post(postUrl, data=data, headers=header)

# 获取code,code会用来获取微信服务大厅token
def getCode1(jid):
    header = {
        'User-Agent': USERAGENT,
        "cookie": jid
    }
    Url = "http://xy.4009955.com/sfrzwx/oauth/authorize?response_type=code&scope=read&client_id=wxfwdt&redirect_uri=http://xy.4009955.com/wxfwdt/&state=tysfrz"
    responseRes = requests.get(Url, headers=header, allow_redirects=False)
    code = responseRes.headers['Location'].split('?')[1].split('=')[1].split('&')[0]
    x = "code1:" + code
    print(x)
    PROCESS.append(x)
    return code


# 获取微信服务大厅token
def getWxfwdttoken(jid,code):
    header = {
        'User-Agent': USERAGENT,
        "cookie": jid
    }
    data = {
        "code": code
    }
    postUrl = "http://xy.4009955.com/wxfwdt-api/layout_01_01/login/loginYdBycode"
    responseRes = requests.post(postUrl, json=data, headers=header)
    x = "wxtoken:" + responseRes.json()["data"]["content"]["token"]
    print(x)
    PROCESS.append(x)
    return responseRes.json()["data"]["content"]["token"]



def getCode2(jid,wxtoken):
    header = {
        'User-Agent': USERAGENT,
        "cookie": f"{jid};wxfwdtToken={wxtoken}"
    }
    postUrl = "http://xy.4009955.com/sfrzwx/oauth/authorize?response_type=code&scope=read&client_id=jktb&redirect_uri=http://xy.4009955.com/jktb/&state=tysfrz"
    responseRes = requests.get(postUrl, headers=header, allow_redirects=False)
    code = responseRes.headers['Location'].split('?')[1].split('=')[1].split('&')[0]
    x = "code2:" + code
    print(x)
    PROCESS.append(x)
    return code


def getJktbtoken(jid, wxtoken, code):
    header = {
        'User-Agent': USERAGENT,
        "cookie": f"{jid};wxfwdtToken={wxtoken}"
    }
    data = {
        "code": code
    }
    postUrl = "http://xy.4009955.com/jktb-api/jktb_01_01/login/loginYdBycode"
    responseRes = requests.post(postUrl, json=data, headers=header)
    x = "jktoken:" + responseRes.json()["data"]["content"]["token"]
    print(x)
    PROCESS.append(x)
    return responseRes.json()["data"]["content"]["token"]


def getTodayForms(jid, wxtoken, jktoken):
    header = {
        'User-Agent': USERAGENT,
        "cookie": f"{jid};wxfwdtToken={wxtoken};jktb_token={jktoken}"
    }
    postUrl = "http://xy.4009955.com/jktb-api/jktb_01_01/homePage/getToadyForms"
    responseRes = requests.post(postUrl, headers=header)
    x = "todayid:" + responseRes.content.decode().split('"')[17]
    print(x)
    PROCESS.append(x)
    return responseRes.content.decode().split('"')[17]


def submit(jid, jktoken, todayid):
    header = {
        'User-Agent': USERAGENT,
        "cookie": f"{jid};jktb_token={jktoken}"
    }
    data = {
        "list": [{"zjlx": 3, "list": [{"column": "c001", "content": "校内"}, {"column": "c002", "content": "校外"}],
                  "value": ["c001"]}, {"zjlx": 5, "list": [{"column": "gSheng", "content": PROVINCE},
                                                           {"column": "gShi", "content": CITY},
                                                           {"column": "gQu", "content": DISTRICT}], "value": ""},
                 {"zjlx": 3, "list": [{"column": "c010", "content": "37.2℃及以下"},
                                      {"column": "c012", "content": "37.3℃-38.4℃（请及时就医并在3天内进行3次核酸检测）"},
                                      {"column": "c013", "content": "38.5℃及以上（请及时就医并在3天内进行3次核酸检测）"}],
                  "value": ["c010"]}, {"zjlx": 3, "list": [{"column": "c014", "content": "没有出现不适症状"},
                                                           {"column": "c015", "content": "乏力、咳嗽、流涕等感冒症状"},
                                                           {"column": "c016", "content": "呕吐、腹泻等消化道不适"},
                                                           {"column": "c017", "content": "与传染病无关的不适症状"}],
                                       "value": ["c014"]}, {"zjlx": 3, "list": [{"column": "c018", "content": "未被隔离"},
                                                                                {"column": "c019",
                                                                                 "content": "居家隔离观察（需要医护人员上门核酸采样）"},
                                                                                {"column": "c020",
                                                                                 "content": "校外集中隔离点隔离观察"}],
                                                            "value": ["c018"]}, {"zjlx": 3, "list": [
                {"column": "c003", "content": "未接种"}, {"column": "c004", "content": "已接种第一针"},
                {"column": "c005", "content": "已接种第二针"}, {"column": "c006", "content": "已接种第三针"}], "value": ["c006"]},
                 {"zjlx": 3, "list": [{"column": "c007", "content": "绿码"},
                                      {"column": "c008", "content": "灰码（请在到威海后第1、第2、第4天各完成1次核酸检测）"},
                                      {"column": "c009", "content": "黄码"}, {"column": "c010", "content": "红码"}],
                  "value": ["c007"]}, {"zjlx": 3, "list": [{"column": "c028", "content": "未出校"},
                                                           {"column": "c029", "content": "出校，未离开威海（须填报出行方式和外出地点）"},
                                                           {"column": "c030", "content": "离威"}], "value": ["c028"]},
                 {"zjlx": 2, "list": [{"column": "c031", "content": ""}], "value": ""},
                 {"zjlx": 3, "list": [{"column": "c021", "content": "是"}, {"column": "c022", "content": "否"}],
                  "value": ["c022"]}, {"zjlx": 1, "list": [{"column": "c023", "content": ""}], "value": ""},
                 {"zjlx": 3, "list": [{"column": "c024", "content": "是"}, {"column": "c025", "content": "否"}],
                  "value": ["c025"]}, {"zjlx": 1, "list": [{"column": "c026", "content": ""}], "value": ""},
                 {"zjlx": 2, "list": [{"column": "c027", "content": ""}], "value": ""}], "isEdit": 1, "tbzt": 0,
        "syxgcs": 3, "tbrq": TIME, "mrtbjzsj": "22:10", "xm": XM, "zzjgmc": XUEYUAN,
        "bdtbslid": todayid, "bdmc": "学生每日健康填报"
    }
    postUrl = "http://xy.4009955.com/jktb-api/jktb_01_01/homePage/saveForm"
    responseRes = requests.post(postUrl, json=data, headers=header)
    x = "finalRes:" + responseRes.content.decode()
    print(x)
    PROCESS.append(x)

def sendmail(res):
    print('正在发送邮件。。。')
    # 登录你的邮箱
    yag = yagmail.SMTP(user=QQMAIL, password=MAILAUTH, host='smtp.qq.com')
    # 发送邮件
    yag.send(to=[RECEIVEMAIL], subject=f'{TIME} 工软校园填报情况', contents=f"{res}")
    print('完成')

def tianbao():
    while True:
        try:
            jid = getJESSIONID()
            yzm = getYzm(jid)
            login(jid, yzm)
            wxcode = getCode1(jid)
            wxtoken = getWxfwdttoken(jid, wxcode)
            jkcode = getCode2(jid, wxtoken)
            jktoken = getJktbtoken(jid, wxtoken, jkcode)
            todayid = getTodayForms(jid, wxtoken, jktoken)
            submit(jid, jktoken, todayid)
        except IndexError:
            PROCESS.append("❌ fail,retrying......\n")
            time.sleep(5)
            continue
        else:
            PROCESS.append("✔ success\n填报已完成")
            res = '\n'.join(PROCESS)
            sendmail(res)
            break

def main_handler(event, context):
	tianbao()
