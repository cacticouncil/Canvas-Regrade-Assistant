import urllib.request
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup, SoupStrainer

def grab_hrefs(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    li = []
    for a in soup.find_all(href=True,):
        li.append(a['href'])

    return li


def login(url, uname, pw, a_url):
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = url
    password_mgr.add_password(None, top_level_url, uname, pw)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    opener.open(a_url)
    urllib.request.install_opener(opener)
    response = urlopen('http://192.168.156.2:3000/courses/1/quizzes/1?module_item_id=1')
    print(response.getcode())
    soup = BeautifulSoup(response, 'html.parser')
    for a in soup.find_all(href=True,):
        print('Found URL:', a['href'])
