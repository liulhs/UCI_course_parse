from bs4 import BeautifulSoup
import mechanicalsoup
url = 'https://www.reg.uci.edu/perl/WebSoc'

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'lxml'},
    raise_on_404=True,
)

browser.open(url)
browser.select_form('form[action="{}"]'.format(url))
browser["CourseCodes"] = '34310'
##
response = browser.submit_selected()
##
soup = BeautifulSoup(response.text, 'lxml')

##td = soup.find_all(attrs={'bgcolor':'#D5E5FF'})[-1]
##

