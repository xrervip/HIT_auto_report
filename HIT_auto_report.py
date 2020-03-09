#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2020/2/18 18:42
#@Author: f
#@File  : main.py
#为了对学校网络和api进行保护 有关网站链接和js方法已被删除
#警告：在使用本工具之前请确保您没有感染新冠肺炎或者存在感染的风险或处于医学隔离观察中，代码会根据您之前保留的填写记录自动提交
#本工具开发的目的是为了配合导员工作（作者经常因为没有及时上报被辅导员提醒），对于不遵守使用条例的行为而导致的后果作者不承担责任
#最后祝伟大祖国早日战胜疫情，武汉加油，中国加油！
#2020/03/09 新增命令行读入账号密码 格式： 学号 密码
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sys

class Report(object):
    def __init__(self):
        self.base_url = ''
        self.driver = webdriver.Chrome()
        self.login()
        self.Report()

    def login(self):
        self.load_url('')
        time.sleep(0.5)
        if '' == self.driver.current_url:
            return
        self.driver.execute_script("")
        time.sleep(0.5)
        self.driver.find_element_by_id('username').send_keys(id)
        self.driver.find_element_by_id('password').send_keys(Password)
        self.driver.find_element_by_id('password'). send_keys(Keys.ENTER)
        time.sleep(0.5)

        while True:
            time.sleep(1)
            if '' == self.driver.current_url:
                break

        if '' == self.driver.current_url:
            self.load_url('')
            return

    def Report(self):
        while '' != self.driver.current_url:
            self.load_url('')
            time.sleep(5)
        self.driver.execute_script("")
        if self.driver.find_element_by_id(''):
            self.driver.find_element_by_id('').click()
            self.driver.execute_script("")

        return

    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

if __name__ == '__main__':
    id=""
    Password=""
    if len(sys.argv)==3:
        id=sys.argv[1]
        Password=sys.argv[2]
        r = Report()
        sys.exit(0)
    try:
        file=open('./账户密码.txt', 'r')
        id = file.readline()
        Password = file.readline()
    except FileNotFoundError:
        print("未检测到缓存账户密码，您可以尝试在可执行文件同目录下创建 账户密码.txt 在本地保存您的账户密码以实现自动化登陆\n"
              "尝试手动登陆统一身份认证")
    except PermissionError:
        print("权限不足，尝试使用管理员权限进行访问")

    r=Report()