#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Email functionality for the app."""

from threading import Thread

from flask import render_template
from flask import current_app as app

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Mail:

    def __init__(self):
        # set default attributes
        self.host = app.config['MAIL_SERVER']
        self.sender = app.config['MAIL_SENDER']
        self.port = app.config['MAIL_PORT']
        self.recipient = app.config['MAIL_RECIPIENT']
        self.subject = app.config['MAIL_SUBJECT']
        self.attachment = None

    def __repr__(self):
        return f'<Custom SMTP mail object: attrs=[host, sender, recipient, subject, body, port, attachment]>'

    def send_mail(self):
        # define the message

        try:
            assert self.host
            assert self.sender
            assert self.recipient
            assert self.subject
            assert self.body
            assert self.port
        except AttributeError as e:
            message_part1 = f'{type(e)} {e}.'
            message_part2 = 'Mail objects must include host, sender, recipient, subject, body, and port attributes.'
            message = ' '.join([message_part1, message_part2])
            return message

        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.recipient
        message['Subject'] = self.subject
        message.attach(MIMEText(self.body, 'plain'))

        # format and set the attachment if present
        if self.attachment is not None:
            # set the filename
            if '\\' in self.attachment:
                self.attachment.replace('\\', '/')
            if '/' in self.attachment:
                idx = self.attachment.rfind('/') + 1
                filename = self.attachment[idx:]
            else:
                filename = self.attachment

            # read in the attachment
            with open(self.attachment, 'rb') as file:
                payload = MIMEBase('application', 'octate-stream')
                payload.set_payload(file.read())
                encoders.encode_base64(payload)
                payload.add_header('Content-Disposition', 'attachment', filename=filename)
                message.attach(payload)

        with smtplib.SMTP(self.host, self.port) as smtp:
            text = message.as_string()
            smtp.sendmail(self.sender, self.recipient, text)


# send password reset email
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    mail = Mail()
    mail.recipient = user.email
    mail.subject = ' '.join([app.config['APPLICATION_NAME'], 'Reset Password'])
    mail.body = render_template('email/reset_password.txt', user=user, token=token)
    mail.send_mail()


# send async emails
def create_async_email(app, mail):
    # figure this out for my mail method
    with app.app_context():
        mail.send_mail()


# function to create the thread for async emails
def send_async_email(mail, sync=False):
    if sync:
        mail.send_mail()
    else:
        Thread(target=create_async_email, args=(app._get_current_object(), mail)).start()
