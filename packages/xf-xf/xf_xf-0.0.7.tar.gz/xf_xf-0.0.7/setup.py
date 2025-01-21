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
    version='0.0.7',                 # 版本号
    author='小峰',              # 作者
    author_email='ling_don@qq.com',  # 邮箱
    include_package_data=True,
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests', '**/__pycache__', '**/__pycache__/*']),
    package_data={
        '': ['*.py', '*.json', '*.txt', '*.html', '*.js'],
        'xffunk.DP浏览器': ['*.py', '*.json', '*.txt', '*.html', '*.js'],
        'xffunk.DP浏览器.Porxy': ['*.html', '*.js'],
    },
    exclude_package_data={
        '': ['*.pyc', '*.pyo', '*.pyd', '*__pycache__', '*__pycache__/*'],
        'xffunk.DP浏览器': ['*.pyc', '*.pyo', '*.pyd', '*__pycache__', '*__pycache__/*'],
        'xffunk.DP浏览器.Porxy': ['*.pyc', '*.pyo', '*.pyd', '*__pycache__', '*__pycache__/*'],
    },
    description='实用到的的功能',  # 描述
    classifiers=[
        'Programming Language :: Python :: 3',  # Python版本要求
    ],
)
