# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 */3 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('windows系统状态监控')

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
        "已用内存": f"{memory.used / (1024 ** 3):.2f} GB ({memory.percent}%)"
    }

# 获取磁盘使用情况
def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    return {
        "总硬盘": f"{disk_usage.total / (1024 ** 3):.2f} GB",
        "已用硬盘": f"{disk_usage.used / (1024 ** 3):.2f} GB ({disk_usage.percent}%)"
    }

# 获取网络流量
def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "发送字节": f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
        "接收字节": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB"
    }

# 获取系统运行时间
def get_uptime():
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    return time.strftime("%H:%M:%S", time.gmtime(uptime))

# 获取系统负载
def get_load_average():
    return {
        "1分钟负载": psutil.getloadavg()[0],
        "5分钟负载": psutil.getloadavg()[1],
        "15分钟负载": psutil.getloadavg()[2]
    }

# 获取进程监控
def get_top_processes(sort_by='cpu'):
    if sort_by == 'cpu':
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']),
                           key=lambda p: p.info['cpu_percent'], reverse=True)[:10]
    else:  # sort by memory
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']),
                           key=lambda p: p.info['memory_info'].rss, reverse=True)[:10]
    return processes

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

    # 进程信息
    top_processes_cpu = get_top_processes(sort_by='cpu')
    cpu_process_info = "\n".join([f"{i+1}. {proc.info['name']} (PID: {proc.info['pid']})\n\tCPU: {proc.info['cpu_percent']}% - 内存: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB"
                                   for i, proc in enumerate(top_processes_cpu)])
    
    top_processes_memory = get_top_processes(sort_by='memory')
    memory_process_info = "\n".join([f"{i+1}. {proc.info['name']} (PID: {proc.info['pid']})\n\tCPU: {proc.info['cpu_percent']}% - 内存: {proc.info['memory_info'].rss / (1024 ** 2):.2f} MB"
                                      for i, proc in enumerate(top_processes_memory)])

    system_info["按CPU占用排序的前十个进程"] = cpu_process_info
    system_info["按内存占用排序的前十个进程"] = memory_process_info

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
