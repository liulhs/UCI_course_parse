from bs4 import BeautifulSoup
import mechanicalsoup

import time
import logging
import datetime

import smtplib
try:
    from email.MIMEText import MIMEText
except:
    from email.mime.text import MIMEText
try:
    from email.MIMEMultipart import MIMEMultipart
except:
    from email.mime.multipart import MIMEMultipart

def is_full (code):

    url = 'https://www.reg.uci.edu/perl/WebSoc'

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
    )
    browser.open(url)
    browser.select_form('form[action="{}"]'.format(url))
    browser["CourseCodes"] = code

    response = browser.submit_selected()

    soup = BeautifulSoup(response.text, 'lxml')
    td = soup.find_all(attrs={'bgcolor':'#D5E5FF'})[-1]

    return td.text.strip() == 'FULL'

def send_email (code):
    subject = 'Course ({}) is not full!'.format(code)
    body = """\
    <html>
    <head></head>
    <body>
    <p>
       The course {} has either an open spot or opened a waitlist.
    </p>
    </body>
    </html>
    """.format(code)

    fromaddr = "pythonscripts@caiobatista.com"
    toaddr = [""]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.yandex.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "Senh@123")

    for to in toaddr:
        msg['To'] = to
        server.sendmail(fromaddr, to, msg.as_string())
        print (str("Email sent to \"" + to + "\"."))

    server.quit()

if __name__ == '__main__':
    while True:
        code = input('Please input your class code: ')
        if is_full(code):
            print("Sorry, this class is full...")
        else:
            print("Your class still have avaliable spots!")
