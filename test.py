from bs4 import BeautifulSoup
from requests_html import HTMLSession
# a = {'a': 1}
# print(list(a.keys())[0])

session = HTMLSession()

url = session.get('http://neonai.rf.gd/test.txt')

print(url.text)