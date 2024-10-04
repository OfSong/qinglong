# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 0 1 1 *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('胖乖获取token')

import requests

# 用户输入手机号
phone_number = input("请输入手机号: ")

# 发送验证码的URL
send_code_url = "https://userapi.qiekj.com/common/sms/sendCode"

# 发送验证码的请求头
send_code_headers = {
    "Host": "userapi.qiekj.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryL7voVAgDfuWd4I4F",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://h5.qiekj.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://h5.qiekj.com/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 发送验证码的请求数据
send_code_data = (
    f"------WebKitFormBoundaryL7voVAgDfuWd4I4F\r\n"
    f"Content-Disposition: form-data; name=\"phone\"\r\n\r\n"
    f"{phone_number}\r\n"
    f"------WebKitFormBoundaryL7voVAgDfuWd4I4F\r\n"
    f"Content-Disposition: form-data; name=\"template\"\r\n\r\n"
    f"reg\r\n"
    f"------WebKitFormBoundaryL7voVAgDfuWd4I4F--\r\n"
)

# 发送验证码
send_code_response = requests.post(send_code_url, headers=send_code_headers, data=send_code_data)
if send_code_response.status_code == 200:
    print(f"验证码已发送到手机: {phone_number}")
else:
    print("发送验证码失败:", send_code_response.text)
    exit()

# 用户输入收到的验证码
verification_code = input("请输入你收到的验证码: ")

# 提交验证码并获取Token的URL
verify_code_url = "https://userapi.qiekj.com/user/reg"

# 提交验证码的请求头
verify_code_headers = {
    "Host": "userapi.qiekj.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryyr34AnsulemOFr4v",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://h5.qiekj.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://h5.qiekj.com/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 提交验证码的请求数据
verify_code_data = (
    f"------WebKitFormBoundaryyr34AnsulemOFr4v\r\n"
    f"Content-Disposition: form-data; name=\"channel\"\r\n\r\n"
    f"h5\r\n"
    f"------WebKitFormBoundaryyr34AnsulemOFr4v\r\n"
    f"Content-Disposition: form-data; name=\"phone\"\r\n\r\n"
    f"{phone_number}\r\n"
    f"------WebKitFormBoundaryyr34AnsulemOFr4v\r\n"
    f"Content-Disposition: form-data; name=\"verify\"\r\n\r\n"
    f"{verification_code}\r\n"
    f"------WebKitFormBoundaryyr34AnsulemOFr4v--\r\n"
)

# 提交验证码并获取Token
verify_code_response = requests.post(verify_code_url, headers=verify_code_headers, data=verify_code_data)

# 打印返回的整个响应内容
print("响应状态码:", verify_code_response.status_code)
print("响应内容:", verify_code_response.text)

# 检查并提取Token
if verify_code_response.status_code == 200:
    response_json = verify_code_response.json()
    print("完整的响应JSON:", response_json)  # 打印完整的JSON响应内容
    token = response_json.get('data', {}).get('token')  # 从'data'字典中获取'token'
    if token:
        print("Token获取成功:", token)
    else:
        print("未能获取到Token")
else:
    print("验证码验证失败:", verify_code_response.text)
