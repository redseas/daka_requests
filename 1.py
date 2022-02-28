import re
a="xxx西华大学"
if re.match(r".*?西华大学.*?",a):
    print("匹配成功")