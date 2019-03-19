from bs4 import BeautifulSoup
import mechanicalsoup

import time
import sched

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
    # print(soup.text.find("FULL")!= -1)
    # return td.text.strip() == 'FULL'
    return soup.text.find("FULL")!= -1

def send_email (code):
    subject = 'UCI Course Master: The course ({}) you are watching is not full anymore'.format(code)
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

    fromaddr = "jasonliuofficial@gmail.com"
    toaddr = ["haosonl@uci.edu","liulhs1998@gmail.com"]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "112131415161lhs")

    for to in toaddr:
        msg['To'] = to
        server.sendmail(fromaddr, to, msg.as_string())
        print (str("Email sent to \"" + to + "\"."))

    server.quit()

if __name__ == '__main__':
    course_list = [34165,34166,34167,34168,34169,34170,34171,34172]
    sent = False
    while not sent:
        for code in course_list:
            if not is_full(code):
                send_email(code)
                sent = True
        if not sent:
            print('ALLFULL')
        time.sleep(300)