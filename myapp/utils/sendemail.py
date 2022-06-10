#-*- codeing = utf-8 -*-
#@Time: 2022/5/29 20:54
#@Author: 怪盗LLYL
#@File: sendemail.py
#@Software: PyCharm
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from django_wx import  settings
import smtplib
class MyEmail(object):
    def sendemail(self,code,to_addr):
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        from_addr = settings.SEND_EMAIL# 发邮件的邮箱
        password = settings.EMAIL_PASSWORD#授权码
        to_addr =  to_addr #目标
        smtp_server ='smtp.163.com'# input('SMTP server: ')
        msg = MIMEText('<html><body><p>验证码：'  + code  +  '</p>' +    '</body></html>', 'html', 'utf-8')
        msg['From'] = _format_addr('测试开发真货 <%s>' % from_addr)
        msg['To'] = _format_addr('登录用户 <%s>' % to_addr)
        msg['Subject'] = Header('登录验证码', 'utf-8').encode() #邮件主题
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
if __name__ == '__main__':
    myemai = MyEmail()
    myemai.sendemail('qwea','441565547@qq.com')