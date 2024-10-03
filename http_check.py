import os
import requests

# 环境变量：WEBSITES   逗号隔开

# 从环境变量中读取网站列表
def get_websites_from_env():
    websites = os.getenv("WEBSITES", "")
    return websites.split(",") if websites else []

# 检测网站是否正常
def check_website_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"{url} 正常工作"
        else:
            return f"{url} 返回状态码: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"{url} 访问失败，错误: {str(e)}"

# PushPlus 推送消息
def send_pushplus_message(token, title, content):
    url = "http://www.pushplus.plus/send"
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "txt"
    }
    response = requests.post(url, json=data)
    return response.json()

if __name__ == "__main__":
    # 从青龙面板环境变量中获取 PushPlus Token 和网站列表
    pushplus_token = os.getenv("PUSHPLUS_TOKEN")
    websites = get_websites_from_env()

    if not websites:
        print("未找到网站列表")
    else:
        result_message = ""
        for website in websites:
            status_message = check_website_status(website.strip())
            result_message += status_message + "\n"
        
        # 推送结果到 PushPlus
        if pushplus_token:
            send_pushplus_message(pushplus_token, "网站状态监控", result_message)
        else:
            print("未找到 PushPlus Token")
        
        # 打印监控结果
        print(result_message)
