import os
from flask import Flask
from flask_script import Manager
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.exmail.qq.com'
app.config['MAIL_SENDER'] = "security@mljr.com"
app.config['MAIL_DEBUG'] = True  
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'security@mljr.com'
app.config['MAIL_PASSWORD'] = 'Nissan.com9090niubi'
manager = Manager(app)
mail = Mail(app)

if __name__ == '__main__':
    manager.run()
#    message = Message(subject='Hello,World!',recipients=['aa<hebei.zhang01@mljr.com>'],body='111')
#    mail.send(message)
