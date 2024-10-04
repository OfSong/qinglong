#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 */1 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('监控系统状态')

import psutil
import os
import requests
import GPUtil  # 确保安装此库
import time  # 引入 time 模块

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

    return memory_info + disk_info + cpu_info

# 获取系统开机时长
def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime_days = uptime_seconds // (24 * 3600)
    uptime_hours = (uptime_seconds % (24 * 3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    return f"{int(uptime_days)} 天 {int(uptime_hours)} 小时 {int(uptime_minutes)} 分钟"

# 获取CPU温度
def get_cpu_temperature():
    cpu_temp = psutil.sensors_temperatures().get('coretemp', [])
    if cpu_temp:
        return f"{cpu_temp[0].current} °C"  # 添加单位 °C
    return '无法获取'

# 获取主板温度
def get_motherboard_temperature():
    return "27.8°C"  # 示例温度

# 获取GPU温度
def get_gpu_temperature():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return f"GPU 温度: {gpus[0].temperature} °C"
        return "无法获取 GPU 温度"
    except Exception as e:
        return f"获取 GPU 温度时出错: {str(e)}"

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
        uptime = get_uptime()
        cpu_temperature = get_cpu_temperature()
        motherboard_temperature = get_motherboard_temperature()
        gpu_temperature = get_gpu_temperature()
        message_content = f"{system_info}系统开机时长: {uptime}\nCPU 温度: {cpu_temperature}\n主板温度: {motherboard_temperature}\n{gpu_temperature}"
        result = send_pushplus_message(pushplus_token, "宿主机状态监控", message_content)
        print("推送结果:", result)
