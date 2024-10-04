# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 */3 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('Linux系统状态监控')

import os
import psutil
import platform
import socket
import requests
import time

# PushPlus Token
PUSHPLUS_TOKEN = "你的token"

# 推送消息函数
def pushplus_message(title, content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "json"
    }
    response = requests.post(url, json=data)
    return response.json()

# 获取内存使用情况
def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "总内存": f"{memory.total / (1024 ** 3):.2f} GB",
        "已用内存": f"{memory.used / (1024 ** 3):.2f} GB ({memory.percent}%)",
        "可用内存": f"{memory.available / (1024 ** 3):.2f} GB"
    }

# 获取磁盘使用情况
def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    return {
        "总硬盘": f"{disk_usage.total / (1024 ** 3):.2f} GB",
        "已用硬盘": f"{disk_usage.used / (1024 ** 3):.2f} GB ({disk_usage.percent}%)",
        "可用硬盘": f"{disk_usage.free / (1024 ** 3):.2f} GB"
    }

# 获取网络流量
def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "发送字节": f"{net_io.bytes_sent / (1024 ** 3):.2f} GB",
        "接收字节": f"{net_io.bytes_recv / (1024 ** 3):.2f} GB"
    }

# 获取系统运行时间
def get_uptime():
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    return time.strftime("%H:%M:%S", time.gmtime(uptime))

# 获取系统负载
def get_load_average():
    load_avg = os.getloadavg()
    return {
        "1分钟负载": load_avg[0],
        "5分钟负载": load_avg[1],
        "15分钟负载": load_avg[2]
    }

# 获取TCP连接
def get_tcp_connections():
    return len(psutil.net_connections(kind='tcp'))

# 获取系统温度（如果支持）
def get_temperature():
    try:
        temp = psutil.sensors_temperatures()
        return {key: f"{value[0].current} °C" for key, value in temp.items() if value}
    except Exception as e:
        return {"温度信息": "无法获取温度数据"}

# 获取系统信息
def get_system_info():
    uname = platform.uname()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    

    system_info = {
        "系统": f"{uname.system} {uname.release}",
        "主机名": hostname,
        "IP地址": ip_address,
    }
    system_info.update(get_memory_info())
    system_info.update(get_disk_info())
    system_info.update(get_network_info())
    system_info["系统运行时间"] = get_uptime()
    system_info.update(get_load_average())
    system_info["活跃TCP连接数"] = get_tcp_connections()
    system_info.update(get_temperature())

    return system_info

# 主函数
def main():
    system_info = get_system_info()
    title = "系统状态推送"
    content = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
    result = pushplus_message(title, content)
    print(f"PushPlus推送结果: {result}")

if __name__ == "__main__":
    main()
