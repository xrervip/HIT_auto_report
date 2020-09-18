#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 本脚本在git@github.com:1180300211/HIT_auto_report.git的基础上修改而成，改善了因不恰当地各种强制等待导致的效率问题
from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Reporter(object):
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

        self.daily_report_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx'
        self.temperature_report_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsTwsb'
        self.home_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
        self.login_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange'
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        print("reporting")
        self.login()
        self.daily_report()
        self.temperature_report()
        self.driver.close()

    def login(self):
        """
        自动登录
        :return:
        """
        self.driver.get(self.login_url)

        self.driver.execute_script("tongyishenfen()")
        self.wait_and_send_keys('username', self.user_id)
        self.wait_and_send_keys('password', self.password)
        self.wait_and_send_keys('password', Keys.ENTER)

        self.wait_url(self.home_url)

        print("logged in")

    def daily_report(self):
        """
        自动每日上报
        :return:
        """
        self.driver.get(self.daily_report_url)
        self.wait_url(self.daily_report_url)

        self.driver.execute_script("add()")
        try:
            self.wait_and_click('txfscheckbox')
        except UnexpectedAlertPresentException:
            self.driver.get(self.home_url)
            self.wait_url(self.home_url)
            print("daily report already done")
            return

        self.driver.execute_script("save()")
        print("daily report done")

    def temperature_report(self):
        """
        自动体温上报
        :return:
        """
        self.driver.get(self.temperature_report_url)
        self.wait_url(self.temperature_report_url)

        self.driver.execute_script("add()")
        # self.wait_and_click('twsb_tx')

        try:
            self.wait_url_redirect(self.temperature_report_url, 5)
        except UnexpectedAlertPresentException:
            print("daily temperature report already done")
            return

        self.wait_and_click('edit1')
        old_temperature = self.wait_element_path('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]')
        new_temperature = self.wait_element_path('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]')
        time.sleep(1)
        ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
        time.sleep(1)
        self.wait_and_click('weui-picker-confirm')
        self.driver.execute_script("save(1)")
        time.sleep(3)

        self.wait_and_click('edit2')
        time.sleep(1)
        self.wait_and_click('weui-picker-confirm')
        self.driver.execute_script("save(2)")
        time.sleep(3)

        print("daily temperature report done")

    def wait_url(self, target_url, timeout=10.0):
        """
        等待直到url更新为目标url
        :param target_url: 预计更新后的目标url
        :param timeout: 超时时间
        :return:
        """
        while target_url != self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_url_redirect(self, origin_url, timeout=10.0):
        """
        等待直到url更新为另一个url
        :param origin_url: 更新前的url
        :param timeout: 超时时间
        :return:
        """
        while origin_url == self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_element_id(self, element_id):
        """
        等待相应id的元素加载完成
        :param element_id: 元素id
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return element

    def wait_element_path(self, element_xpath):
        """
        等待相应xpath的元素加载完成
        :param element_xpath: 元素xpath
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return element

    def wait_and_send_keys(self, element_id, keys):
        """
        等待相应id的元素加载完成后输入字符
        :param element_id: 元素id
        :param keys: 需要输入的字符
        :return:
        """
        element = self.wait_element_id(element_id)
        element.send_keys(keys)

    def wait_and_click(self, element_id):
        """
        等待相应id的元素加载完成后点击元素
        :param element_id: 元素id
        :return:
        """
        element = self.wait_element_id(element_id)
        element.click()


if __name__ == '__main__':
    input_id = ""
    input_password = ""
    if len(sys.argv) == 3:
        input_id = sys.argv[1]
        input_password = sys.argv[2]
    else:
        try:
            file = open('./账户密码.txt', 'r')
            input_id = file.readline()
            Password = file.readline()
        except FileNotFoundError:
            print("未检测到缓存账户密码，您可以尝试在可执行文件同目录下创建 账户密码.txt 在本地保存您的账户密码以实现自动化登陆\n"
                  "尝试手动登陆统一身份认证")
        except PermissionError:
            print("权限不足，尝试使用管理员权限进行访问")

    print("starting reporter")
    r = Reporter(input_id, input_password)
