# -*- coding: utf-8 -*-
# -------------------------------

# @软件：PyCharm
# @项目：自己的库

# -------------------------------

# @文件：tools.py
# @时间：2024/12/20 下午10:56
# @作者：小峰
# @邮箱：ling_don@qq.com

# ------------------------------
import psutil
import pygetwindow as gw
import ctypes
import urllib.parse
from PIL import Image
import io
import base64
def Cookie转字典(cookies:str):
    cookies_dict = {}
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        cookies_dict[key.strip()] = value.strip()
    return cookies_dict
def Cookie字典转字符串(cookies:dict):
    cookies_str = ''
    for key, value in cookies.items():
        cookies_str += f'{key}={value};'
    return cookies_str
def 获取浏览器端口():
    def get_pid_from_handle(handle):
        # 使用 ctypes 来调用 Windows API 获取进程ID
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))
        return pid.value

    def get_window_handle(program_name):
        # 获取所有窗口
        windows = gw.getWindowsWithTitle(program_name)
        if windows:
            # 返回第一个匹配的窗口句柄
            return windows[0]._hWnd
        else:
            return None

    def get_ports_by_pid(pid):
        # 获取所有连接
        connections = psutil.net_connections(kind='inet')
        ports = []
        for conn in connections:
            if conn.pid == pid:
                ports.append(conn.laddr.port)
        return ports

    program_name = "chrome.exe"
    handle = get_window_handle(program_name)

    if handle:
        print(f"程序 '{program_name}' 的窗口句柄是: {handle}")
        pid = get_pid_from_handle(handle)
        print(f"程序 '{program_name}' 的进程ID是: {pid}")
        ports = get_ports_by_pid(pid)
        if ports:
            print(f"程序 '{program_name}' 的进程ID {pid} 使用的端口有: {ports}")
            print(int(ports[0]))
        else:
            print(f"未找到程序 '{program_name}' 的进程ID {pid} 使用的端口。")
    else:
        print(f"未找到名称为 '{program_name}' 的程序窗口。")
def url参数转字典(url:str):
    query = urllib.parse.urlparse(url).query
    return urllib.parse.parse_qs(query)
def 验证码图片缩放_b64(图片, 大小):
    image_data = base64.b64decode(图片)
    image = Image.open(io.BytesIO(image_data))
    图片 = image.resize((大小))
    图片 = 图片.convert("RGB")
    buffered = io.BytesIO()
    图片.save(buffered, format="JPEG")  # 可以根据实际情况选择保存格式
    b64_str = base64.b64encode(buffered.getvalue()).decode()
    return b64_str