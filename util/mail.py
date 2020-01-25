# -*- coding: utf-8 -*-
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

FROM_ADDRESS = 'yugenaoki1016@gmail.com'
MY_PASSWORD = 'Nic47746!'
BCC = 'yugenaoki1016@gmail.com'
SUBJECT = '【月末報告】'
BODY = """さんから月末報告がありました。
確認おねがいします。"""


def create_message(user, attendance_pdf_path, fare_pdf_path):
    
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM_ADDRESS
    msg['To'] = user['mail']
    msg['Bcc'] = BCC
    msg['Date'] = formatdate()

    mbody = MIMEText(user['id'] + BODY, _subtype='plain')
    msg.attach(mbody)


    # ファイルを添付する
    with open(attendance_pdf_path, 'rb') as f:
        attendance_pdf = MIMEApplication(f.read(), _subtype="pdf")

    attendance_pdf.add_header('Content-Disposition',
                           'attachment', filename=attendance_pdf_path)

    with open(fare_pdf_path, 'rb') as f:
        fare_pdf = MIMEApplication(f.read(), _subtype="pdf")

    fare_pdf.add_header('Content-Disposition',
                           'attachment', filename=fare_pdf_path)

    msg.attach(attendance_pdf)
    msg.attach(fare_pdf)
    
    return msg.as_string()


def send_mail(user, attendance_pdf_path, fare_pdf_path):
    
    msg = create_message(user, attendance_pdf_path, fare_pdf_path)

    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(FROM_ADDRESS, user['mail'], msg)
    smtpobj.close()
