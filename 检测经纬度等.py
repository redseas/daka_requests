#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File    : 检测经纬度等.py
@Time    : 2022/02/18 22:13:19
@Author  : chou
@Contact : chou2079986882@gmail.com
@Version : 0.1
@Desc    : None
'''

import requests
import os
import sys
import time
import json
import pandas as pd
from hashlib import md5
import pymysql
import re
import pandas as pd
import random
print("检测程序开始运行")
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}


def login():
    data_login = {
        "Name": stu_name,
        "PassWord": stu_password,
        "UserType": "1",
        "XGH": stu_xgh,
        "YXDM": "10623"
    }
    login_url = "https://yqfkapi.zhxy.net/api/User/CheckUser"
    # 登陆
    s = requests.Session()
    res = s.post(login_url, json=data_login, headers=headers)

    return res


# 发邮箱提醒账号密码错误
def email_send(stu_xgh, to_addr, password):
    # 密码错误反馈
    import smtplib
    from email.mime.text import MIMEText
    import datetime

    # email 用于构建邮件内容
    from email.header import Header

    # 用于构建邮件头

    email = ""

    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'qnyfMsg@qq.com'
    password = 'eojparquwepvddia'

    # 发信服务器
    smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(msg, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(str(datetime.date.today()) + '青柠打卡反馈')

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    # 发送完成反馈
    print("邮箱发送成功")


def de_one(stu_name):
    # 删除错误
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
    sql = f"delete from user where stu_name='{stu_name}'"
    cursor.execute(sql)
    sql2 = f"delete from fall where stu_name='{stu_name}'"
    cursor.execute(sql2)

    cursor.close()
    print("！！！删除成功")


def loc(location):
    headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56"}
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}
    headers = [headers1, headers2]
    base_url = "https://apis.map.qq.com/jsapi?qt=geoc&addr="
    data = requests.get(base_url+location, headers=random.choice(headers))
    # print(type(data))
    inf = data.json()
    try:
        jwd_x = inf['detail']['pointx']
        jwd_y = inf['detail']['pointy']
        JWD = jwd_y+','+jwd_x
        return JWD
    except:
        print("地址问题")
        email_send(msg="qnyf通知，请注意您的地址是否正确比如：四川省成都市xx区，如果是机器误报请忽略，系统已自动生成随机jwd，但是请您自己重新上传信息以确保信息准确，否则可能无法打卡❤")
        JWD =""
        return JWD


# print(loc("河南省周口市"))


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


def change_jwd():
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
    sql_query2 = f"delete from user where stu_name='{stu_name}'"
    cursor.execute(sql_query2)

    sql = "INSERT INTO user(stu_name,stu_num,password,email,jwd,place) VALUES('%s','%s','%s','%s','%s','%s')" % (
        stu_name, stu_xgh, password, to_addr, jwd, place)
    cursor.execute(sql)

    cursor.close()
    print("执行完成")


if __name__ == '__main__':
    lis = []
    table = all_data()
    for i in range(table.shape[0]):
        data = table.loc[i]
        lis.append(dict(data))
    for i in lis:
        # 姓名
        stu_name = str(i['stu_name'])
        # 学号
        stu_xgh = str(i['stu_num'])
        # 密码
        password = str(i['password'])
        email = str(i['email'])
        to_addr = email
        place = str(i["place"])
        jwd = str(i["jwd"])
        # 验证jwd
        if not re.match(r"3\d{1}.\d{6},1\d{2}.\d{6}", jwd):
            jwd = loc(place)
            change_jwd()
            print("jwd自动更新成功")
        stu_password = md5(password.encode('utf8')).hexdigest()
        try:
            res = login()

            # print(res.json)
            correct = res.json()["info"]
            print(stu_name+":"+correct)
            if correct == "学号或密码错误":
                print("学号或密码错误")
                email_send(stu_xgh, to_addr, password,msg="qnyf通知：学号或者密码错误，如果是机器误报请忽略")
                de_one(stu_name)
            time.sleep(4)
            print("4秒后检测下一个")
            # sys.exit()
        except:
            print("发生错误")