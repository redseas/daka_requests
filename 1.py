import re 
str="30.780882,10.947853"

# pattern = re.compile(r"3\d{1}.\d{6},1\d{2}.\d{6}")
# print(pattern.search(str))
if re.match(r"3\d{1}.\d{6},1\d{2}.\d{6}",str):
    print(1)