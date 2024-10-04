# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 */3 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('监控系统状态')

import psutil
import os
import requests

# pushplus推送环境变量 ：PUSHPLUS_TOKEN

# 获取系统信息
def get_system_info():
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 ** 3)
    used_memory = memory.used / (1024 ** 3)
    memory_info = f"总内存: {total_memory:.2f} GB\n已使用: {used_memory:.2f} GB\n"

    disk = psutil.disk_usage('/')
    total_disk = disk.total / (1024 ** 3)
    used_disk = disk.used / (1024 ** 3)
    disk_info = f"总磁盘: {total_disk:.2f} GB\n已使用: {used_disk:.2f} GB\n"

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_info = f"CPU 使用率: {cpu_usage}%\n"

    # 获取温度信息（假设在Linux系统上）
    try:
        temp_info = psutil.sensors_temperatures()
        if 'coretemp' in temp_info:
            cpu_temp = temp_info['coretemp'][0].current
            temp_info_str = f"CPU 温度: {cpu_temp}°C\n"
        elif 'thermal_zone' in temp_info:
            cpu_temp = temp_info['thermal_zone_0'][0].current
            temp_info_str = f"CPU 温度: {cpu_temp}°C\n"
        else:
            temp_info_str = "无法获取 CPU 温度信息\n"
    except Exception as e:
        temp_info_str = f"获取温度信息时出错: {e}\n"

    return memory_info + disk_info + cpu_info + temp_info_str

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
    # 从青龙面板环境变量中获取 PushPlus Token
    pushplus_token = os.getenv("PUSHPLUS_TOKEN")
    
    if not pushplus_token:
        print("未找到 PushPlus Token")
    else:
        # 获取系统信息并推送
        system_info = get_system_info()
        result = send_pushplus_message(pushplus_token, "宿主机状态监控", system_info)
        print("推送结果:", result)
