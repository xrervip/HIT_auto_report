#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2020/2/18 18:42
#@Author: f
#@File  : main.py
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Report(object):
    def __init__(self):
        self.base_url = 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx'
        self.driver = webdriver.Chrome()
        self.login()
        self.Report()

    def login(self):
        self.load_url('http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange')
        time.sleep(0.5)
        if 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome' == self.driver.current_url:
            return
        self.driver.execute_script("tongyishenfen()")
        time.sleep(0.5)
        self.driver.find_element_by_id('username').send_keys(id)
        self.driver.find_element_by_id('password').send_keys(Password)
        self.driver.find_element_by_id('password'). send_keys(Keys.ENTER)
        time.sleep(0.5)

        while True:
            time.sleep(1)
            if 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome' == self.driver.current_url:
                break

        if 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome' == self.driver.current_url:
            self.load_url('http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
            return

    def Report(self):
        while 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx' != self.driver.current_url:
            self.load_url('http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
            time.sleep(5)
        self.driver.execute_script("add()")
        if self.driver.find_element_by_id('txfscheckbox'):
            self.driver.find_element_by_id('txfscheckbox').click()
            self.driver.execute_script("save()")

        return

    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

if __name__ == '__main__':
    id=""
    Password=""
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