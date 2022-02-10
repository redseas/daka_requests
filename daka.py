import openpyxl
import time
import json
import requests
from hashlib import md5
import random
def main():
    global s
    s = requests.Session()

    #打卡信息检查（务必要这一个步骤）
    def jiancha():
        daka_url = 'https://yqfkapi.zhxy.net/api/ClockIn/IsClockIn?uid={}&usertype=1&yxdm=10623'.format(stu_uid)
        print("专属检查链接为："+str(daka_url))
        daka = s.get(daka_url)
        #print(daka.text)
        json_response = daka.json()
        try:
            a = json_response["data"]["msg"]#打卡情况
            print("打卡信息检查："+a)
        except:
            a = "打卡信息检查：大概率访问频繁"
            print(a)
        return a

        
    #验证码处理系统
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
        return key,code
    
    #主签到程序
    def qiandao(key,code):
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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        health_result = s.post('https://yqfkapi.zhxy.net/api/ClockIn/Save', json=data_health, headers=headers)
        json_response = health_result.json()
        print(json_response)
        b = json_response["info"]#打卡情况
        return str(b)
    
    #pushdeer提醒
    def pushdeer(push_key,sendnews):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        urltxt = "https://api2.pushdeer.com/message/push?pushkey={}&text={}".format(push_key,sendnews)
        page = requests.get(url=urltxt, headers=headers)
        print("已经打卡情况进行pushdeer推送！")
        
    # 管理员通知 
    def send_pusher(times):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        urltxt = "https://api2.pushdeer.com/message/push?pushkey=PDU3996TCdVkJGKXVCdsmq41BhLxGavia0Ir3Fqa&text={}".format(times)
        page = requests.get(url=urltxt, headers=headers)
        return "send_pusher操作结束"
        
    #计算打卡情况
    chenggongtimes = 0
    shibaitimes = 0
    
    #打卡n人，循环n+1
    for i in range (1,8):
        tixing = "正在登录第{}个账号".format(str(i))
        print(tixing)
        book = openpyxl.load_workbook('/www/qingningdaka2/青柠打卡账号.xlsx')
        sheetname = book.worksheets[0]
        #获取信息                   
        cell2 = sheetname.cell(row=i+1, column=1)#名字
        stu_name = cell2.value
        print("名字："+stu_name)
        
        cell5 = sheetname.cell(row=i+1, column=4)#定位
        JWD = cell5.value
        print("经纬度："+str(JWD))
        
        cell6 = sheetname.cell(row=i+1, column=5)#地址
        Place = cell6.value
        print("地址："+str(Place))
        
        cell7 = sheetname.cell(row=i+1, column=6)#UID
        stu_uid = str(cell7.value)
        print("UID："+str(stu_uid))

        cell8 = sheetname.cell(row=i+1, column=7)#KEY
        push_key = str(cell8.value)
        print("push_key："+push_key)
        book.close()
        
        #运行一次打卡情况检查，否则验证码错误
        jiancha()
        
        #运行打卡程序
        try:
            print("-------------执行打卡程序中-------------")
            #验证码识别
            key,code = dddocr()
            #打卡脚本
            time.sleep(5)
            qian = qiandao(key,code)
            if qian == "响应成功" or qian == "今天你已经自诊打过卡了！":
                chenggongtimes += 1
            else:
                m = 0
                while qian == "操怍失败，验证码错误":
                    m += 1
                    print(stu_name+"|打卡出现问题："+qian+"|重试识别验证码第"+str(m)+"次")
                    if m <= 4:
                        jiancha()
                        key,code = dddocr()
                        time.sleep(5)
                        qian = qiandao(key,code)
                    else:
                        shibaitimes += 1
                        qian = "注意！请自己手动去打卡吧|https://wxyqfk.zhxy.net/?yxdm=10623&from=singlemessage#/clockIn"
                        break
                        
            sendnews = "（居家打卡）青柠打卡反馈 |"+stu_name+"："+qian
            print("准备发送pushdeer告知："+sendnews)
            pushdeer(push_key,sendnews)
            print("发送完毕")
        except:
            print("*********遇见问题*********")

            
        randomInt = random.randint(10,55) 
        print("将等待：" + str(randomInt) + " 秒")
        time.sleep(randomInt)
        
    times = "（居家打卡）管理员|本次成功打卡{}人，失败打卡{}人".format(chenggongtimes,shibaitimes)
    print(times)
    pusher_onwer = send_pusher(times)
    print(pusher_onwer)


main()

