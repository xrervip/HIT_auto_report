# HIT_auto_report
工大自动疫情上报程序(Win32-64)

依赖于python运行环境+chorme+selenium chrome驱动

selenium chrome驱动 镜像地址: [http://npm.taobao.org/mirrors/selenium](http://npm.taobao.org/mirrors/selenium)

> 谁还不是一条懒狗呢?



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

# python脚本代码
在`Auto_report`目录中执行
```bash
vim HIT_auto_reportSRC_Linux.py
```
会在当前目录新建一个 `HIT_auto_reportSRC_Linux.py`  并用vim编辑器打开

然后在 `HIT_auto_reportSRC_Linux.py` 中添加代码（复制粘贴）


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

添加多个上报计划如下：
```powershell
30 9  * * * reboot
19 10 * * * root sh /Auto_report目录中/autoLinuxA.sh
25 11 * * * root sh /Auto_report目录中/autoLinuxB.sh
30 12 * * * root sh /Auto_report目录中/autoLinuxC.sh
```
如上文所示，三个.sh的上报(执行)时间分别为 `10:19,11:25,12:30`
按照学校开放的时间自己调整即可，推荐放在上午，因为如果放在下午的话有时候受到短信不知道是没到点执行脚本还是上报失败
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200716215022899.png)
（因为有时候chorme会抽风，我设置每天定时重启服务器`30 9  * * * reboot`）
然后 在vim界面输入`wq`保存即可
然后再终端输入`crontab -l`就可以看是否成功添加定时任务了
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200716215442669.png)
最后要做的事就是等明天看有没有收到短信，如果收到了说明那一步出了问题，没收到的话恭喜，以后就再也不用管上报的事情了