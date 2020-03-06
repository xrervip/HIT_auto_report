# HIT_auto_report
工大自动疫情上报程序(Win32-64)

依赖于python运行环境+chorme+selenium chrome驱动

selenium chrome驱动 镜像地址: [http://npm.taobao.org/mirrors/selenium](http://npm.taobao.org/mirrors/selenium)

登陆方式

1.手动输入账户密码登陆(效率较低)

2.将 账户+'\n'(换行)+密码 保存在 可执行文件 同目录下的 账户密码.txt 中，实现自动化登陆（推荐） ps:您的密码将被保存到本地，并仅供于登陆使用

3.在执行2的基础上 将该可执行文件添加到Windows定时自动任务中，以实现完全自动化（非常推荐） 添加方式：桌面右键此电脑->管理->计算机管理->系统工具->任务计划程序->任务计划程序库->创建任务