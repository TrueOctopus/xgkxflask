from flask_mail import Message
from flask import render_template
from app import mail
import app

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[XGKX]'
app.config['FLASKY_MAIL_SENDER'] = '18368876370@163.com'


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)
