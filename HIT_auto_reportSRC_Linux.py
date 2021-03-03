#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/2/18 18:42
# @Author: f
# @File  : main.py

import platform
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException, \
    JavascriptException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Report(object):

    def __init__(self):
        self.user_id = id
        self.password = Password
        self.daily_report_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx'
        self.temperature_report_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsTwsb'
        self.home_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome'
        self.login_url = 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange'

        self.log("开始上报")
        chrome_options = Options()
        sysstr = platform.system()
        # 根据系统类型配置chrome_options

        if (sysstr == "Linux"):
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.log("调用浏览器")

        while self.home_url != self.driver.current_url:
            self.log("登陆账户")
            try:
                self.login()
            except Exception as e:
                print(str(e))
                Report.log(str(e))
                self.driver.refresh()
            time.sleep(0.5)

        self.Report()
        # self.temperature_report()
        self.log("------------")
        self.driver.quit()
        return

    def login(self):
        self.load_url(self.login_url)
        time.sleep(0.5)
        if self.home_url == self.driver.current_url:
            return
        self.driver.find_element_by_xpath("/html/body/div/div[2]/button[1]").click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[1]/input").send_keys(
            id)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]").send_keys(Password)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]").send_keys(Keys.ENTER)
        time.sleep(0.5)
        if self.home_url == self.driver.current_url:
            self.log("登陆成功")
        else:
            self.log("登陆失败")
        return

    def Report(self):
        self.load_url(self.daily_report_url)
        if self.driver.title.__contains__("404"):
            self.log("当前不在上报时间")
            return
        self.log("尝试首次载入上报界面")
        while self.daily_report_url != self.driver.current_url:
            self.wait_url(self.daily_report_url)
            self.log("再次尝试载入上报界面")
            time.sleep(1)

        try:
            status_text = self.wait_element_path("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]").text
            if "审核状态：未提交" == status_text or "审核状态：待辅导员审核" == status_text:
                self.log(status_text)
                self.wait_and_click_path("/html/body/div[1]/div[2]/div[2]/div[2]")

            else:
                self.driver.execute_script("add()")

        except JavascriptException:
            self.log("当前不在上报时间！")
            return

        while True:
            try:
                self.log("添加新的上报")
                location = self.wait_element_path("/html/body/div[1]/div[3]/div[1]/input")
                cur_loc = location.get_attribute('value')
                if cur_loc == '获取位置失败，请打开位置权限！':
                    cur_loc = '哈尔滨工业大学'
                time.sleep(1)

                checkbox = self.wait_element_id("checkbox")
                if not checkbox.is_selected():
                    self.driver.find_element_by_id("checkbox").click()
                    self.log("已勾选checkbox")

                time.sleep(0.5)
                self.log("设置地理位置")
                location.clear()
                location.send_keys(cur_loc)
                self.driver.execute_script("save()")
                time.sleep(3)
                Weui_confirm_btn = self.wait_element_path("/html/body/div[13]/div[3]/a[2]")
                try:
                    if Weui_confirm_btn.is_enabled():
                        Weui_confirm_btn.click()
                        self.log("上报成功")
                        break
                except StaleElementReferenceException as e:
                    self.log("没有上报成功，可能是地理位置出现了问题")
                    self.driver.refresh()

                time.sleep(5)

            except UnexpectedAlertPresentException as e:
                #如果出现拒绝地理位置授权
                alert = self.driver.switch_to.alert
                alert.accept()
                self.log("出现弹窗，可能是有关地理授权的原因")
                continue

            except NoSuchElementException as e:
                self.log("检测到今日已生成疫情上报")
                print(str(e))
                return

        time.sleep(1)
        return

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

    def wait_and_click_id(self, element_id):
        """
        等待相应id的元素加载完成后点击元素
        :param element_id: 元素id
        :return:
        """
        element = self.wait_element_id(element_id)
        element.click()
        return element

    def wait_and_click_path(self, element_path):
        """
        等待相应id的元素加载完成后点击元素
        :param element_id: 元素id
        :return:
        """
        element = self.wait_element_path(element_path)
        element.click()
        return element

    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def log(self, msg):
        print(id + " " + msg)
        f.write(id)
        f.write(time.strftime(" %Y-%m-%d %H:%M:%S ", time.localtime(time.time())))
        f.write(msg + "\n")


if __name__ == '__main__':
    id = ""
    Password = ""
    f = open('log', 'a')
    if len(sys.argv) >= 3:
        id = sys.argv[1]
        Password = sys.argv[2]
        r = Report()
        sys.exit(-1)
    try:
        file = open('./账户密码.txt', 'r')
        id = file.readline()
        Password = file.readline()
    except FileNotFoundError:
        print("未检测到缓存账户密码，您可以尝试在可执行文件同目录下创建 账户密码.txt 在本地保存您的账户密码以实现自动化登陆\n"
              "尝试手动登陆统一身份认证")
    except PermissionError:
        print("权限不足，尝试使用管理员权限进行访问")

    try:
        r = Report()
        sys.exit(0)

    except Exception as e:
        print(str(e))
        Report.log(str(e))
