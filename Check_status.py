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



if __name__ == '__main__':
    code = ''
    while code != 'q':
        try:
            code = input("Please input the course code you would like to check or press q to quit: ").strip()
            if is_full(code):
                print("Sorry, your class is still full.")
            else:
                print("Your class still have spots or it's available for waitlist.")
        except:
            print("Please input a valid course code")