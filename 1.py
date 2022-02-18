
# 发邮箱提醒账号密码错误
def email_send(stu_xgh, to_addr, password,msg):
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
email_send("1111","2079986882@qq.com","1111","1111")