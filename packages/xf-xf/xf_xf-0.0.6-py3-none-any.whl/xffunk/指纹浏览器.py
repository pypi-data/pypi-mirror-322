# -*- coding: utf-8 -*-
# -------------------------------
import json
from .请求 import *
# @软件：PyCharm
# @项目：自己的库

# -------------------------------

# @文件：指纹浏览器.py
# @时间：2024/12/21 下午6:37
# @作者：小峰
# @邮箱：ling_don@qq.com

# -------------------------------
class ixBrowser:
    def __init__(self, 端口):
        self.端口 = 端口

    def 获取浏览器列表(self):
        data = {
            "page": 1,
            "limit": 10,
            "group_id": 0,
            "tag_id": 0,
            "name": ""
        }
        res = requests.post(f"http://127.0.0.1:{self.端口}/api/v2/profile-list", json=data)
        res = json.loads(res.text)
        return res['data']['data']

    def 打开浏览器(self, 窗口序号):
        data = {
            "profile_id": 窗口序号,
            "args": [
                "--disable-extension-welcome-page"
            ],
            "load_extensions": True,
            "load_profile_info_page": False,
            "cookies_backup": False,
            "cookie": ""
        }
        res = requests.post(f"http://127.0.0.1:{self.端口}/api/v2/profile-open-with-random-fingerprint", json=data)
        print(res.text)
        res = json.loads(res.text)
        return res['data']['debugging_address']

    def 关闭浏览器(self, 窗口序号):
        data = {
            "profile_id": 窗口序号
        }
        res = requests.post(f"http://127.0.0.1:{self.端口}/api/v2/profile-close", json=data)
        res = json.loads(res.text)
        return res['data']
class 比特:
    def __init__(self, 端口=54345):
        # 官方文档地址
        # https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

        # 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档
        self.url = f"http://127.0.0.1:{端口}"
        self.headers = {'Content-Type': 'application/json'}

    def 创建窗口(self,名称:str,备注='',代理方式=2,代理类型='noproxy',host='',port='',proxyUserName=''):  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
        # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
        json_data = {
            'name': 名称,  # 窗口名称
            'remark': 备注,  # 备注
            'proxyMethod': 代理方式,  # 代理方式 2自定义 3 提取IP
            'proxyType': 代理类型,
            'host': host,  # 代理主机
            'port': port,  # 代理端口
            'proxyUserName': proxyUserName,  # 代理账号
            "browserFingerPrint": {  # 指纹对象
                'coreVersion': '112'  # 内核版本 112 | 104，建议使用112，注意，win7/win8/winserver 2012 已经不支持112内核了，无法打开
            }
        }

        res = requests.post(f"{self.url}/browser/update",
                            data=json.dumps(json_data), headers=self.headers)
        res = json.loads(res.text)
        browserId = res['data']['id']
        return browserId

    def 更新窗口(self,ids:list,备注=''):  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
        json_data = {'ids': ids,
                     'remark': 备注, 'browserFingerPrint': {}}
        res = requests.post(f"{self.url}/browser/update/partial",
                            data=json.dumps(json_data), headers=self.headers).json()
        print(res)

    def 打开窗口(self,id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
        json_data = {"id": f'{id}'}
        res = requests.post(f"{self.url}/browser/open",
                            data=json.dumps(json_data), headers=self.headers)
        res = json.loads(res.text)
        return res

    def 关闭窗口(self,id):  # 关闭窗口
        json_data = {'id': f'{id}'}
        return post请求(f"{self.url}/browser/close",data=json.dumps(json_data), headers=self.headers).json()
    def 删除窗口(self,id):  # 删除窗口
        json_data = {'id': f'{id}'}
        return post请求(f"{self.url}/browser/delete",data=json.dumps(json_data), headers=self.headers).json()

    def 分组查询(self):  # 删除窗口
        json_data = {'page': 0, 'pageSize': 10, 'all': True}
        return post请求(f"{self.url}/group/list", data=json.dumps(json_data), headers=self.headers).json()

    def 分组列表(self,z):
        json_data = {'page': 0, 'pageSize': 1, 'seq': int(z)}
        return post请求(f"{self.url}/browser/list", data=json.dumps(json_data), headers=self.headers).json()

    def 分组详细(self,id):
        json_data = {'id': id}
        return post请求(f"{self.url}/group/detail", data=json.dumps(json_data), headers=self.headers).json()

    def 获取所有窗口列(self,num: int, xh):  # 获取所有窗口列
        data = {
            'page': 0,
            'pageSize': num,
            'groupId': xh
        }
        res = requests.post(f"{self.url}/browser/list", json=data)
        res_j = json.loads(res.text)
        return res_j