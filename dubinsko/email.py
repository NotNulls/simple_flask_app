from threading import Thread
from flask import current_app
from flask_mail import Message
from dubinsko import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email( sender, recipients, text_body, html_body=None,subject=None):
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg),daemon=False).start()

