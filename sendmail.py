#coding:utf-8
import smtplib
from email.mime.text import MIMEText

class SendEmail:
    global send_user
    global email_host
    global password
    password = "Nissan.com9090niubi"
    email_host = "smtp.exmail.qq.com"
    send_user = "security@mljr.com"

    def send_mail(self,user_list,sub,content):
        user = "美利安全中心" + "<" + send_user + ">"
        message = MIMEText(content,_subtype='html',_charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP_SSL()
        server.connect(email_host,465)
        server.login(send_user,password)
        server.sendmail(user,user_list,message.as_string())
        server.close()

if __name__ == '__main__':
    send = SendEmail()
    user_list = ['hebei.zhang01@mljr.com']
    sub = "测试邮件"
    content = "ceshi看看"
    send.send_mail(user_list,sub,content)
