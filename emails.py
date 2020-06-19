from flask_mail import Mail,Message
from secpassword import app,mail


def send_mail(subject,to,body):
    message=Message(subject,recipients=[to],body=body)
    mail.send(Message)
print app.MAIL_USERNAME
send_mail('aa',recipients=['hebei.zhang01@mljr.com'],body='abc')

