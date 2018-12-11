# 自动跑阳光体育平台(原汉姆运动)脚本
## 本脚本仅供研究，使用者造成的任何后果由使用者自行承担。

该脚本参考[S-Ex1t/SunnyRunningPy](https://github.com/S-Ex1t/SunnyRunningPy)的脚本

## 新增功能
- 修改手动输入IMEI，直接在脚本中输入
- 可以配置SMTP，当汉姆出现问题时（一般都是IMEI过期引起的问题），可以自动发送邮件提醒
- 能放在服务器上，设置定时执行该脚本，如 Ubuntu16.04+ 的 crontab。

## 获取IMEI
安卓：使用抓包软件，查找http协议，寻找imeicode
ios：打开飞行模式，打开app，有报错信息，可以看到imeicode

## 使用
修改文件头部的`IMEI`，输入自己的IMEI。
配置'mail'函数，将其中的配置转换为对应的服务商。
请使用python3运行该脚本

## 注意
配置smtp时，请尽量不要使用没有经过ssl加密的25端口。因为阿里云是直接封了该端口的。
填写	message['From']和message['To']时，请按照我的方式写，如果使用网上的Header(...)方法，会被163拦截为垃圾邮件

