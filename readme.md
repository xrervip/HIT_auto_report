> 谁还不是一条懒狗呢?
工大自动疫情上报程序(Win/Linux)

依赖于python运行环境+chorme+selenium+chrome驱动

---

**2020年11月7日更新**

增加处理新添加体温状态的功能

---

GitHub地址：
[https://github.com/xrervip/HIT_auto_report](https://github.com/xrervip/HIT_auto_report)

每天都要搞学校的上报属实有点烦

目前已经运行了两个多月，基本上没有再管过上报，除了有时候会抽风

首先需要搞到一台云服务器，（阿里云学生身份可以白女票半年机）这些方法不用多说，花钱也好白女票也罢，都不在本文的讨论范围之内。
云服务器推荐做成centos7或者是windows
白女票地址：
[阿里云高校计划](https://developer.aliyun.com/adc/student/?source=5176.11533457&userCode=99tdlj0h&type=copy)

然后需要做的有以下：

 1. 利用ssh连接云服务器 （不用多说）
 2. 为云服务器配置Python3环境[Centos安装python3](https://blog.csdn.net/qq_42196922/article/details/90379239)
 3. 为云服务器配置Chorme+selenium的环境[centos 安装Selenium+Chrome](https://www.cnblogs.com/erhao9767/p/11369876.html)
 4. 传输代码并调试，代码放在后面
 5. 为程序的执行编写.sh文件
 6. 在使用Linux中的crontab 指令添加定时任务，到一个时间点就执行之前的.sh
 
 
 首先，为了拥有更整洁的目录，可以在文件夹里新键一个文件夹用于放脚本之类的东西
 

```bash
mkdir Auto_report
cd Auto_report
```
然后我们就将工作目录切入`Auto_report`目录中了

---
以下内容适用于Linux系统，如果你想用win系统的话，在**计算机-管理中找到task schedule（或直接搜索 task）** ，添加定时任务即可

# python脚本代码
在`Auto_report`目录中执行
```bash
vim HIT_auto_reportSRC_Linux.py
```
会在当前目录新建一个 `HIT_auto_reportSRC_Linux.py`  并用vim编辑器打开

然后在 `HIT_auto_reportSRC_Linux.py` 中添加代码（复制粘贴）

 
```python
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
            self.load_url('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx')
            self.log("再次尝试载入上报界面")
            time.sleep(1)

        try:
            self.driver.execute_script("add()")
            #self.load_url("https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/editYqxx?id=B371C35E13D7665EE053653CA8C0AA52&zt=01")
        except JavascriptException:
            self.log("当前不在上报时间！")
            return


        self.log("添加新的上报")
        while True:
                time.sleep(0.5)
                print("设置体温并检测checkbox勾选状况")
                try:
                    """
                    体温按钮1
                    """
                    self.wait_and_click('tw')
                    old_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[8]')
                    new_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[2]')
                    time.sleep(0.5)
                    ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
                    time.sleep(0.5)
                    self.wait_and_click('weui-picker-confirm')
                    time.sleep(0.5)

                    self.wait_and_click('tw1')
                    old_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[2]')
                    new_temperature = self.wait_element_path('/html/body/div[11]/div[2]/div[2]/div/div[3]/div[2]')
                    time.sleep(0.5)
                    ActionChains(self.driver).drag_and_drop(new_temperature, old_temperature).perform()
                    time.sleep(0.5)
                    self.wait_and_click('weui-picker-confirm')
                    self.log("成功设置体温")

                    if self.driver.find_element_by_id("txfscheckbox"):
                        self.driver.find_element_by_id("txfscheckbox").click()
                        self.log("勾选checkbox")
                        break
                except UnexpectedAlertPresentException:
                    self.log("检测到今日已生成疫情上报")
                    return

                except NoSuchElementException:
                    self.log("检测到今日已生成疫情上报")
                    return


        # self.driver.execute_script("save()")
        self.log("上报成功")

        return

    def temperature_report(self):
        """
        自动体温上报
        :return:
        """
        self.log("进行体温上报")
        self.driver.get(self.temperature_report_url)
        self.wait_url(self.temperature_report_url)

        self.driver.execute_script("add()")
        # self.wait_and_click('twsb_tx')

        try:
            self.wait_url_redirect(self.temperature_report_url, 5)
        except UnexpectedAlertPresentException:
            self.log("今日已经生成了体温上报")
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

        self.log("体温上报成功")

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



```
粘贴完代码后，点击esc 退出编辑节面，键入“：”进入命令 节面，输入“wq” 退出并保存
传输完文件可以传入参数进行测试，如果代码用静默的方式结束或者提示“今日已完成上报”，表示代码正常运作


# 编写shell文件来调用python脚本
对shell文件的编写：
让我们的shell文件可以调用起之前写好的python程序

假设我们的学号为：1180300000，密码为hello123
那么编写shell文件，学号和密码对应两个参数即可：
`autoLinuxA.sh`:
```powershell
#!/bin/sh
python3 /root/Auto_report/HIT_auto_reportSRC_Linux.py 1180300000 hello123
```
然后保存，并添加执行权限

```powershell
chmod 777 autoLinuxA.sh
```
正确赋予权限后，sh处于可执行状态

具体的文件目录结构（test.py没啥用）：
（因为两位hxd将他们的账号委派给我，所以有三个.sh文件）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200716214703585.png)
# 添加定时任务
在终端执行指令：

```powershell
crontab -e 
```
进入一个vim的编辑界面，关于crontab具体如何运作了解：[Linux crontab命令详解](https://www.cnblogs.com/ftl1012/p/crontab.html)
并键入内容：

```powershell
30 9  * * * reboot
19 10 * * * root sh /Auto_report目录中/autoLinuxA.sh
25 11 * * * root sh /Auto_report目录中/autoLinuxB.sh
30 12 * * * root sh /Auto_report目录中/autoLinuxC.sh
```
（因为两位hxd将他们的账号委派给我，我有三个.sh文件，如果只为自己上报的话，添加一条就行）
如上文所示，三个.sh的上报(执行)时间分别为 `10:19,11:25,12:30`
按照学校开放的时间自己调整即可，推荐放在上午，因为如果放在下午的话有时候受到短信不知道是没到点执行脚本还是上报失败
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200716215022899.png)
（因为有时候chorme会抽风，我设置每天定时重启服务器`30 9  * * * reboot`）
然后 在vim界面输入`wq`保存即可
然后再终端输入`crontab -l`就可以看是否成功添加定时任务了
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200716215442669.png)
最后要做的事就是等明天看有没有收到短信，如果收到了说明那一步出了问题，没收到的话恭喜，以后就再也不用管上报的事情了