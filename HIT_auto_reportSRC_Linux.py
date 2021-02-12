#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2020/2/18 18:42
#@Author: f
#@File  : main.py

import platform
import traceback

from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoSuchElementException,JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

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
        #根据系统类型配置chrome_options

        if (sysstr == "Linux"):
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.log("调用chrome")

        while self.home_url != self.driver.current_url:
            self.log("尝试登陆")
            try:
                self.login()
            except Exception as e:
                print(str(e))
                Report.log(str(e))
                self.driver.refresh()
            time.sleep(0.5)

        self.Report()
        #self.temperature_report()
        self.log("------------")
        self.driver.quit()
        return

    def login(self):
        self.load_url('http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/shsj/loginChange')
        time.sleep(0.5)
        if 'http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome' == self.driver.current_url:
            return
        self.driver.find_element_by_xpath("/html/body/div/div[2]/button[1]").click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[1]/input").send_keys(id)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]").send_keys(Password)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]"). send_keys(Keys.ENTER)
        time.sleep(0.5)
        if 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsHome' == self.driver.current_url:
            self.log("登陆成功")
        else:
            self.log("登陆失败")
        return


    def Report(self):
        self.load_url('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
        self.log("尝试首次载入上报界面")
        while 'https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx' != self.driver.current_url:
            self.wait_url('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
            self.log("再次尝试载入上报界面")
            time.sleep(1)

        try:
            if "审核状态：未提交" == self.wait_element_path("/html/body/div[1]/div[2]/div[2]/div[1]/div[2]").text:
                self.log("当前状态：未成功提交")
                self.wait_and_click_path("/html/body/div[1]/div[2]/div[2]/div[2]")

            else:
                self.driver.execute_script("add()")

            #self.load_url("https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/editYqxx?id=B38F09AD700BB738E053663CA8C0AB9D&zt=00")
        except JavascriptException:
            self.log("当前不在上报时间！")
            return

        self.log("添加新的上报")
        location = self.wait_element_path("/html/body/div[1]/div[3]/div[1]/input")
        cur_loc = location.get_attribute('value')
        while True:
                time.sleep(5)
                self.log("设置地理位置")
                location.clear()
                location.send_keys(cur_loc)
                try:


                    # try:
                    #     """
                    #     体温按钮1
                    #     """
                    #     self.wait_and_click_id('tw')
                    #     old_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[8]')
                    #     new_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[2]')
                    #     time.sleep(0.5)
                    #     ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
                    #     time.sleep(0.5)
                    #     self.wait_and_click_id('weui-picker-confirm')
                    #     time.sleep(0.5)
                    #
                    #     self.wait_and_click_id('tw1')
                    #     old_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[8]')
                    #     new_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[2]')
                    #     time.sleep(0.5)
                    #
                    #     ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
                    #     time.sleep(0.5)
                    #     self.wait_and_click_id('weui-picker-confirm')
                    #     self.log("成功设置体温")
                    #
                    # except TimeoutException as te:
                    #     self.log("按钮控件出现问题")
                    #     self.driver.refresh()
                    #     pass

                    if self.driver.find_element_by_id("checkbox"):
                        self.driver.find_element_by_id("checkbox").click()
                        self.log("勾选checkbox")
                        break

                except UnexpectedAlertPresentException as e:
                    self.log("检测到今日已生成疫情上报")
                    print(str(e))
                    return

                except NoSuchElementException as e:
                    self.log("检测到今日已生成疫情上报")
                    print(str(e))
                    return

        time.sleep(0.5)
        location.clear()
        location.send_keys(cur_loc)
        self.driver.execute_script("save()")
        time.sleep(3)
        self.wait_and_click_path("/html/body/div[13]/div[3]/a[2]")
        self.log("上报成功")
        time.sleep(20)
        return

    # def temperature_report(self):
    #     """
    #     自动体温上报
    #     :return:
    #     """
    #     self.log("进行体温上报")
    #     self.driver.get(self.temperature_report_url)
    #     self.wait_url(self.temperature_report_url)
    #
    #     self.driver.execute_script("add()")
    #     # self.wait_and_click('twsb_tx')
    #
    #     try:
    #         self.wait_url_redirect(self.temperature_report_url, 5)
    #     except UnexpectedAlertPresentException:
    #         self.log("今日已经生成了体温上报")
    #         return
    #
    #     self.wait_and_click_id('edit1')
    #     old_temperature = self.wait_element_path('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]')
    #     new_temperature = self.wait_element_path('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div[4]')
    #     time.sleep(1)
    #     try:
    #         ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
    #     except Exception as te:
    #         self.log("按钮控件出现问题")
    #         pass
    #
    #     time.sleep(1)
    #     self.wait_and_click_id('weui-picker-confirm')
    #     self.driver.execute_script("save(1)")
    #     time.sleep(3)
    #
    #     self.wait_and_click_id('edit2')
    #     time.sleep(1)
    #     self.wait_and_click_id('weui-picker-confirm')
    #     self.driver.execute_script("save(2)")
    #     time.sleep(3)
    #     time.sleep(1)
    #
    #     self.log("体温上报成功")

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

    def log(self,msg):
        print(id+" "+msg)
        f.write(id)
        f.write(time.strftime(" %Y-%m-%d %H:%M:%S ", time.localtime(time.time())))
        f.write(msg+"\n")



if __name__ == '__main__':
    id=""
    Password=""
    f = open('log', 'a')
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

    try:
        r=Report()
    except Exception as e:
        print(str(e))
        Report.log(str(e))


