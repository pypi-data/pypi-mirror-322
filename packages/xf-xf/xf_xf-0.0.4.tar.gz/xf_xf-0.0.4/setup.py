# -*- coding: utf-8 -*-
# -------------------------------

# @软件：PyCharm
# @项目：自己的库

# -------------------------------

# @文件：setup.py
# @时间：2024/12/20 下午10:53
# @作者：小峰
# @邮箱：ling_don@qq.com

# -------------------------------
# setup.py

from setuptools import setup, find_packages

setup(
    name='xffunk',               # 库的名称
    version='0.0.4',                 # 版本号
    author='小峰',              # 作者
    author_email='ling_don@qq.com',  # 邮箱
    package_data={
        'xffunk': ['*','xffunk/DP浏览器/Porxy/*', 'xffunk/DP浏览器/*'],  # 添加这行，确保包含所有文件
    },
    description='实用到的的功能',  # 描述
    classifiers=[
        'Programming Language :: Python :: 3',  # Python版本要求
    ],
)