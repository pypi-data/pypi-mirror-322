# -*- coding: utf-8 -*-
# -------------------------------
import os
# @软件：PyCharm
# @项目：自己的库

# -------------------------------

# @文件：DP.py
# @时间：2025/1/11 下午8:43
# @作者：小峰
# @邮箱：ling_don@qq.com

# -------------------------------
import time
from queue import Queue
from DrissionPage._base.driver import Driver
from DrissionPage import WebPage, ChromiumOptions
from DrissionPage.common import Actions
from time import perf_counter, sleep
from .FingerPrint import FingerPrint
from faker import Faker
import websockets
import asyncio
import threading
import json
import random
class 日志监听:
    def __init__(self,page) -> None:
        """
        :param page: ChromiumBase对象
        """
        self._page = page
        self._address = page.address
        self._target_id = page._target_id
        self._driver = None

        self._caught = None

        self.listening = False

    def start(self):
        """
        开启console-api监听
        """
        self.clear()
        self._driver = Driver(self._target_id, "page", self._address)
        self._driver.run("Console.enable")
        self._set_callback()
        self.listening = True


    def stop(self):
        """停止监听，清空已监听到的列表"""
        if self.listening:
            self.pause()
            self.clear()
        self._driver.stop()
        self._driver = None

    def pause(self, clear=True):
        """暂停监听
        :param clear: 是否清空已获取队列
        :return: None
        """
        if self.listening:
            self._driver.set_callback('Console.messageAdded', None)
            self.listening = False
        if clear:
            self.clear()

    def clear(self):
        self._caught = Queue(maxsize=0)

    def steps(self, count=None, timeout=None, gap=1):
        caught = 0
        end = perf_counter() + timeout if timeout else None
        while True:
            if timeout and perf_counter() > end:
                return
            if self._caught.qsize() >= gap:
                yield self._caught.get_nowait() if gap == 1 else [
                    self._caught.get_nowait() for _ in range(gap)
                ]
                if timeout:
                    end = perf_counter() + timeout
                if count:
                    caught += gap
                    if caught >= count:
                        return
            sleep(0.05)

    def _set_callback(self):
        self._driver.set_callback("Console.messageAdded", self._console)

    def _console(self, **kwargs):
        self._caught.put(kwargs)

class WSS监控:
    def __init__(self,page) -> None:
        """
        :param page: ChromiumBase对象
        """
        self._page = page
        self._address = page.address
        self._target_id = page._target_id
        self._driver = None

        self._caught = None

        self.listening = False

    def start(self):
        """
        开启websocker监听
        """
        self.clear()
        self._driver = Driver(self._target_id, "page", self._address)
        self._driver.run("Network.enable")
        self._set_callback()
        self.listening = True


    def stop(self):
        """停止监听，清空已监听到的列表"""
        if self.listening:
            self.pause()
            self.clear()
        self._driver.stop()
        self._driver = None

    def pause(self, clear=True):
        """暂停监听
        :param clear: 是否清空已获取队列
        :return: None
        """
        if self.listening:
            self._driver.set_callback('Network.webSocketClosed', None)
            self._driver.set_callback('Network.webSocketCreated', None)
            self._driver.set_callback('Network.webSocketFrameReceived', None)
            self.listening = False
        if clear:
            self.clear()

    def clear(self):
        self._caught = Queue(maxsize=0)

    def steps(self, count=None, timeout=None, gap=1):
        caught = 0
        end = perf_counter() + timeout if timeout else None
        while True:
            if timeout and perf_counter() > end:
                return
            if self._caught.qsize() >= gap:
                yield self._caught.get_nowait() if gap == 1 else [
                    self._caught.get_nowait() for _ in range(gap)
                ]
                if timeout:
                    end = perf_counter() + timeout
                if count:
                    caught += gap
                    if caught >= count:
                        return
            sleep(0.05)

    def _set_callback(self):
        self._driver.set_callback("Network.webSocketClosed", self._websocket_closed)
        self._driver.set_callback("Network.webSocketCreated", self._websocket_created)
        self._driver.set_callback(
            "Network.webSocketFrameReceived", self._websocket_frame_received
        )

    def _websocket_closed(self, **kwargs):
        print("_websocket_closed", kwargs)

    def _websocket_created(self, **kwargs):
        rid = kwargs.get("requestId")

    def _websocket_frame_received(self, **kwargs):
        self._caught.put(kwargs["response"])

class 手机模式:
    """模拟设备"""

    def __init__(self, page) -> None:
        self.page = page
        self.IphoneSe()

    def IphoneSe(self):
        iphone_se = {
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "width": 375,
            "height": 667,
        }
        self.Eemulation()

    def Eemulation(self):
        self.page.run_cdp("Emulation.resetPageScaleFactor")
        self.page.run_cdp(
            "Emulation.setDeviceMetricsOverride",
            devicePosture={"type": "continuous"},
            deviceScaleFactor=2,
            dontSetVisibleSize=True,
            height=896,
            mobile=True,
            positionX=0,
            positionY=0,
            scale=0.86,
            screenHeight=896,
            screenOrientation={"angle": 0, "type": "portraitPrimary"},
            screenWidth=414,
            width=414,
        )
        self.page.run_cdp(
            "Network.setUserAgentOverride",
            userAgent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        )
        self.page.run_cdp(
            "Emulation.setTouchEmulationEnabled",
            enabled=True,
            maxTouchPoints=1,
        )
        self.page.run_cdp(
            "Overlay.setShowViewportSizeOnResize",
            show=False,
        )
        self.page.run_cdp(
            "Overlay.setShowHinge",
        )
        self.page.run_cdp(
            "Emulation.setEmitTouchEventsForMouse",
            enabled=True,
            configuration="mobile",
        )

class 手机点击:
    def __init__(self, page) -> None:
        self.page = page

    def click(self, node):
        vx, vy = node.rect.viewport_midpoint
        print(vx, vy)
        self.page.run_cdp(
            "Input.emulateTouchFromMouseEvent",
            button="left",
            clickCount=0,
            modifiers=0,
            type="mousePressed",
            x=int(vx),
            y=int(vy),
        )
        # time.sleep(0.5)
        self.page.run_cdp(
            "Input.emulateTouchFromMouseEvent",
            button="left",
            clickCount=0,
            modifiers=0,
            type="mouseReleased",
            x=int(vx),
            y=int(vy),
        )

class 页面滑动:
    def __init__(self, page, startx, starty, movex, movey) -> None:
        self.page = page
        self._move(startx, starty, movex, movey)

    def _move(self, startx, starty, movex, movey):
        self.page.run_cdp(
            "Input.dispatchTouchEvent",
            type="touchStart",
            touchPoints=[{"x": startx, "y": starty}],
        )
        self.page.run_cdp(
            "Input.dispatchTouchEvent",
            type="touchMove",
            touchPoints=[{"x": movex, "y": movey}],
        )
        self.page.run_cdp("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])

class 手机移动:
    def __init__(self, node, movex, movey) -> None:
        self.node = node
        vx, vy = node.rect.viewport_midpoint
        self._move(vx, vy, movex, movey)

    def _move(self, vx, vy, movex, movey):
        self.node.page.run_cdp(
            "Input.dispatchTouchEvent",
            type="touchStart",
            touchPoints=[{"x": vx, "y": vy}],
        )
        for i in range(1, 5):
            self.node.page.run_cdp(
                "Input.dispatchTouchEvent",
                type="touchMove",
                touchPoints=[{"x": i * movex / 5, "y": movey}],
            )
            time.sleep(0.1)
        self.node.page.run_cdp(
            "Input.dispatchTouchEvent", type="touchEnd", touchPoints=[]
        )

class 监控脚本:
    def __init__(self,page) -> None:
        """
        :param page: ChromiumBase对象
        """
        self._page = page
        self._address = page.address
        self._target_id = page._target_id
        self._driver = None

        self._caught = None

        self.listening = False

    def start(self):
        """
        开启console-api监听
        """
        self.clear()
        self._driver = Driver(self._target_id, "page", self._address)
        self._driver.run("Debugger.enable")
        self._set_callback()
        self.listening = True


    def stop(self):
        """停止监听，清空已监听到的列表"""
        if self.listening:
            self.pause()
            self.clear()
        self._driver.stop()
        self._driver = None

    def pause(self, clear=True):
        """暂停监听
        :param clear: 是否清空已获取队列
        :return: None
        """
        if self.listening:
            self._driver.set_callback('Debugger.scriptParsed', None)
            self.listening = False
        if clear:
            self.clear()

    def clear(self):
        self._caught = Queue(maxsize=0)

    def steps(self, count=None, timeout=None, gap=1):
        caught = 0
        end = perf_counter() + timeout if timeout else None
        while True:
            if timeout and perf_counter() > end:
                return
            if self._caught.qsize() >= gap:
                yield self._caught.get_nowait() if gap == 1 else [
                    self._caught.get_nowait() for _ in range(gap)
                ]
                if timeout:
                    end = perf_counter() + timeout
                if count:
                    caught += gap
                    if caught >= count:
                        return
            sleep(0.05)

    def _set_callback(self):
        self._driver.set_callback("Debugger.scriptParsed", self._script)

    def _script(self, **kwargs):
        self._caught.put(kwargs)
class 指纹类:
    def __init__(self,浏览器=None):
        threading.Thread(target=self.监听wss服务, daemon=True).start()
        self.浏览器 = 浏览器

    def 启动浏览器(self):
        fake = Faker()
        platform = random.choice(['android', 'ios',])
        if platform == 'android':
            user_agent = fake.android_platform_token()
        elif platform == 'ios':
            user_agent = fake.ios_platform_token()
            platform = 'iPhone'
        else:
            user_agent = fake.user_agent()
            platform = None
        timezone = fake.timezone()
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        language = fake.locale()
        浏览器配置 = ChromiumOptions(read_file=False).auto_port()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建插件文件的绝对路径
        proxy_path = os.path.join(current_dir, 'Porxy')
        浏览器配置.add_extension(proxy_path)
        # 浏览器配置.add_extension(r"指纹")
        浏览器 = WebPage(chromium_options=浏览器配置, session_or_options=False).latest_tab
        浏览器.set.NoneElement_value(None)
        浏览器.set.window.size(width=360, height=740)
        fp = FingerPrint(浏览器)
        # 设置核心
        fp.set_CPU_core(6)
        # 清楚RPA特征 自动化标记
        fp.clear_rpa_feature()
        # 禁用cookie
        fp.disable_cookies()
        # 设置时区
        fp.set_timezone(timezone)
        # 设置地理位置经纬度
        fp.set_setGeolocation(latitude=latitude, longitude=longitude)
        # 设置UA和语言
        fp.set_user_agent(user_agent=user_agent, platform=platform, acceptLanguage='en-GB')

        # 设置触摸模式
        fp.set_touch_mode(enabled=True, maxTouchPoints=2)

        # 设置浏览器尺寸 设备像素比
        fp.set_size(width=360, height=740, mobile=True, scale=1.1)
        self.浏览器 = 浏览器
        return 浏览器

    async def handle_connection(self, websocket, path):
        global ws
        ws = websocket
        while True:
            try:
                message = await websocket.recv()
                print("Received message:", message)
            except:
                break

    def 监听wss服务(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()

        async def run_server():
            try:
                server = await websockets.serve(self.handle_connection, "localhost", 11111)
                await server.wait_closed()
            except:
                pass

        loop.run_until_complete(run_server())


    def 切换代理(self, host, port):
        self.浏览器.get('chrome-extension://ffbfifgkagcgjbeacllkoginflmioekl/1.html')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, '切换代理.js')
        with open(script_path, 'r', encoding='utf-8') as file:
            script = file.read()
        self.浏览器.run_js(script, host, port)
        return self
    def 实时切换代理(self, host, port):
        if ws is not None:
            send_data = {"task": "set", "host": str(host), "port": port}
            asyncio.run_coroutine_threadsafe(ws.send(json.dumps(send_data)), ws.loop)
    def 实时清空代理(self, host, port):
        if ws is not None:
            send_data = {"task": "clear"}
            asyncio.run_coroutine_threadsafe(ws.send(json.dumps(send_data)), ws.loop)

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def get_tracks_2(self, distance, seconds, ease_func):
        """
        根据轨迹离散分布生成的数学生成  # 参考文档  https://www.jianshu.com/p/3f968958af5a
        成功率很高 90% 往上
        :param distance: 缺口位置
        :param seconds:  时间
        :param ease_func: 生成函数
        :return: 轨迹数组
        """
        tracks = [0]
        offsets = [0]
        for t in range(0, int(seconds * 10), 1):  # 循环10次，相当于每次增加0.1秒
            ease = ease_func
            offset = round(ease(t / 10 / int(seconds)) * float(distance))  # t / 10是当前秒数
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return tracks

    def 过点选(self, 浏览器, x,元素):
        try:
            点选背景 = 元素
            ac = Actions(浏览器)
            #print('点击中')
            for i in x:
                i = i.split(',')
                #print(f"点击位置,x:{i[0]}|y:{i[1]}")
                ac.move_to(ele_or_loc=点选背景, offset_x=int(i[0]), offset_y=int(i[1]) - 30, duration=0).click()
            ac.release(点选背景)
            return True
        except:
            return False
    def 过滑块(self, 浏览器, x,元素):
        try:
            tracks = self.get_tracks_2(x, 2.5, self.ease_out_quart)
            ac = Actions(浏览器)
            滑块按钮 = 元素
            ac.hold(滑块按钮)
            for offset_x in tracks:
                ac.move(offset_x=offset_x, duration=0)
            ac.release()
            return True
        except:
            return False