import base64
import datetime

import yagmail

from webapp import models
from webapp.utils import decodeID


def sent_to_mail(email=None, subject=None, body=None):
    try:
        if email and subject:
            sender_email = "antoanhethongthongtin13@gmail.com"
            receiver_email = email
            password = decodeID("ETUXVUUXVUMyMDQtgjRwMEMClTL8F0C")[0:-1].capitalize()
            content = body or ''
            yag = yagmail.SMTP(user=sender_email, password=password,smtp_ssl=True)
            status = yag.send(
                to=receiver_email,
                subject=subject,
                contents=content
            )
            return False if status == False else True
        raise Exception("email or subject is None")
    except Exception as e:
        print("Error sent_to_mail:", e)
        return False
def sent_mail_login(team, data):
    try:
        if team and data:
            data["time"] = str(datetime.datetime.now().strftime("%X %p - %d %B %Y"))

            subject = f'[QLGVDBDQG] Successful Login From New IP  {data["ip"]} - {data["time"]}'

            prettify_html = f'<h1><strong>Successful Login <span style ="color:#0bff00"> {team.name} </span> From New IP</strong></h1>\
                            <h3><strong>We&#39;ve noticed that you accessed your account from IP address new</strong></h3>\
                            <p>Time: <strong style="color:red">' + data['time'] + '</strong></p>\
                            <p>IP Address: <strong style="color:red">' + data['ip'] + ' - ' + data['location'] + '</strong></p>\
                            <p>Application: <strong style="color:red">' + data[
                'user_agent'].lower().capitalize() + ' - ' + data['os'] + '</strong></p>\
                            '

            return sent_to_mail(team.email, subject=subject, body=prettify_html)
        raise ValueError('team or data không có')
    except Exception as e:
        print('Error Sent_mail_login:', e)
        return False
def sent_account_to_mail(idteam):
    try:
        account = models.Team.query.get(idteam)
        if account:
            subject = f'[QLGVDBDQG] Account Login'
            content = f'<h1>Tài khoản đăng nhập đăng ký tham gia giải vô địch bóng đá quốc gia</h1>\
                                        <p>Username: <strong>' + account.username + '</strong></p>\
                                        <p>Password: <strong >' + base64.urlsafe_b64decode(account.password).decode(
                'utf-8') + '</strong></p>\
                                     '
            return sent_to_mail(account.email, subject=subject, body=content)
        raise Exception('account không hợp lệ')
    except Exception as e:
        print("Error sent_account_to_mail:", e)
        return False
