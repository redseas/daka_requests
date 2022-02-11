import openpyxl
import sys
import time
import json
import requests
from hashlib import md5
import random
import pandas as pd
import pymysql
global s
s = requests.Session()

# 打卡信息检查（务必要这一个步骤）


def jiancha():
    daka_url = 'https://yqfkapi.zhxy.net/api/ClockIn/IsClockIn?uid={}&usertype=1&yxdm=10623'.format(
        stu_uid)
    print("专属检查链接为："+str(daka_url))
    daka = s.get(daka_url)
    # print(daka.text)
    json_response = daka.json()
    try:
        a = json_response["data"]["msg"]  # 打卡情况
        print("打卡信息检查："+a)
    except:
        a = "打卡信息检查：大概率访问频繁"
        print(a)
    return a


# 验证码处理系统
def dddocr():
    pic1 = s.get('https://yqfkapi.zhxy.net/api/common/getverifycode')
    tex1 = pic1.content
    tex2 = bytes.decode(tex1)
    if json.loads(tex2)['info'] == '非法访问！':
        print(tex2)
        sys.exit(1)
    tex3 = json.loads(tex2)['data']['img']
    key = json.loads(tex2)['data']['key']
    print("获取到验证码key:"+key)
    url = 'data:image/png;base64,' + tex3
    img_url = url
    import ddddocr
    ocr = ddddocr.DdddOcr()
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    filepath = "qrcode_temp.png"
    with open(filepath, 'rb') as f:
        img_bytes = f.read()
        code = str(ocr.classification(img_bytes))
        print("识别到验证码code："+code)
    #code = input("请输入验证码：")
    return key, code

# 主签到程序


def qiandao(key, code):
    data_health = {
        "UID": stu_uid,
        "UserType": "1",
        "JWD": JWD,
        "key": key,
        "code": code,
        "ZZDKID": "37",
        "A1": "正常",
        "A4": "无",
        "A2": "全部正常",
        "A3": Place,
        "A11": "不在校",
        "A12": "未实习",
        "A13": "低风险区",
        "YXDM": "10623",
        "version": "v1.3.2"
    }
    print(data_health)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    health_result = s.post(
        'https://yqfkapi.zhxy.net/api/ClockIn/Save', json=data_health, headers=headers)
    json_response = health_result.json()
    print(json_response)
    b = json_response["info"]  # 打卡情况
    return str(b)


def push(text):
    key = "PDU3765TBs56dzcIw5d6WcV4Qe7qqo9MNTdREyuB"
    # text="无内容"
    url = f"https://api2.pushdeer.com/message/push?pushkey={key}&text={text}"
    requests.get(url)
# pushdeer提醒


def pushdeer(push_key, sendnews):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
    urltxt = "https://api2.pushdeer.com/message/push?pushkey={}&text={}".format(
        push_key, sendnews)
    page = requests.get(url=urltxt, headers=headers)
    print("已经打卡情况进行pushdeer推送！")

# 管理员通知


def send_pusher(times):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
    urltxt = "https://api2.pushdeer.com/message/push?pushkey=PDU3996TCdVkJGKXVCdsmq41BhLxGavia0Ir3Fqa&text={}".format(
        times)
    page = requests.get(url=urltxt, headers=headers)
    return "send_pusher操作结束"


def all_data():
    # 1.连接

    conn = pymysql.connect(host='localhost', user='daka',
                           password='1234c', db='daka')
    sql_query = 'SELECT * FROM user'
    table = pd.read_sql(sql_query, con=conn)
    conn.close()
    table.drop_duplicates(['stu_num', 'stu_name'], keep='last')
    # print(df)
    return table


# 插入数据
def sql_insert(sql_query):
    # 1.连接
    conn = pymysql.connect(host='localhost', user='daka',
                           password='1234c', db='daka')
    if conn:
        print("连接成功")
    else:
        print('连接失败')
    # 2.创建游标
    cursor = conn.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute(sql_query)
    cursor.close()
    print("执行完成")

# 插入数据库


def insert_one():
    # 1.连接
    conn = pymysql.connect(host='localhost', user='daka',
                           password='1234c', db='daka')
    # print(conn)
    if conn:
        print("连接数据库成功")
    else:
        print('连接数据库失败')
    # 2.创建游标
    cursor = conn.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    sql = "INSERT INTO fall(stu_name,stu_num,password,email,jwd,place) VALUES('%s','%s','%s','%s','%s','%s')" % (
        stu_name, stu_xgh, password, to_addr, JWD, Place)
    cursor.execute(sql)

    cursor.close()
    print("执行完成")

# 获取uid


def uid():
    formdata = {
        "YXDM": "10623",
        "UserType": "1",
        "XGH": stu_xgh,
        "Name": stu_name,
        "PassWord": stu_password
    }
    url = "https://yqfkapi.zhxy.net/api/User/CheckUser"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    response = requests.post(url, json=formdata, headers=headers)
    # 使用json()方法，将response对象，转为列表/字典
    json_response = response.json()
    # print(json_response)
    # 获取UID
    UID = json_response['data']['ID']
    # print(UID)
    stu_uid = str(UID)
    return stu_uid


def recode(a):
    # time.sleep(3)
    # 记录日志
    if a == "success":
        print(stu_name + "打卡成功")
        sql_query2 = f"delete from fall where stu_name='{stu_name}'"
        sql_insert(sql_query=sql_query2)
        print("已在fall数据表删除此人数据")

    else:
        print(stu_name + "打卡失败")
        sql_query_de = f"DELETE from fall WHERE(stu_num='{stu_xgh}')"
        sql_insert(sql_query=sql_query_de)
        insert_one()
        push(text=f"{stu_name} 打卡失败😓【主程序通知】")

    print("进入下一个打卡")


lis = []
table = all_data()
print(f"一共{str(table.shape[0])}个账号，开始打卡————————")
for i in range(table.shape[0]):
    data = table.loc[i]
    lis.append(dict(data))
for i in lis:
    a = "fall"
    # 姓名
    stu_name = str(i['stu_name'])
    # 学号
    stu_xgh = str(i['stu_num'])
    # 密码
    password = str(i['password'])
    stu_password = md5(password.encode('utf8')).hexdigest()
    # JWD = str(i['JWD'])
    JWD = str(i['jwd'])
    Place = str(i['place'])
    to_addr = str(i['email'])
    # phone = str(int(i['phone']))
    print("打卡数据载入成功！")
    print("获取uid中----")
    try:
        stu_uid = uid()
        if stu_uid:
            print(stu_name+"UID："+stu_uid)
            stu_sign_password = str(i['password'])  # 登录密码
            # print(stu_name, stu_password, stu_xgh, stu_uid, JWD, Place)
        else:
            print("uid调用频繁")
            a = 'wrong'
    except:
        print("获取uid失败")
        a = 'wrong'
    # 运行一次打卡情况检查，否则验证码错误
    try:
        jiancha()
        a = "success"
    except:
        a = "wrong"
    # 运行打卡程序
    try:
        print("-------------执行打卡程序中-------------")
        # 验证码识别
        key, code = dddocr()
        # 打卡脚本
        time.sleep(5)
        qian = qiandao(key, code)
        if qian == "响应成功" or qian == "今天你已经自诊打过卡了！":
            print(f"{stu_name}今日打卡已打卡")
        else:
            m = 0
            while qian == "操怍失败，验证码错误":
                m += 1
                print(stu_name+"|打卡出现问题："+qian+"|重试识别验证码第"+str(m)+"次")
                if m <= 4:
                    jiancha()
                    key, code = dddocr()
                    time.sleep(5)
                    qian = qiandao(key, code)
                    a="success"
                else:
                    qian = "注意！请自己手动去打卡吧|https://wxyqfk.zhxy.net/?yxdm=10623&from=singlemessage#/clockIn"

    except:
        print("*********遇见问题*********")
        a = "wrong"

    recode(a)  # 记录
    randomInt = random.randint(10, 30)
    print("将等待：" + str(randomInt) + " 秒")
    time.sleep(randomInt)
