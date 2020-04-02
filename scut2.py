from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

root = 'http://jw.scut.edu.cn/zhinan/cms/toPosts.do'
name = ''
api = "https://sc.ftqq.com/SCU55712T9c248ed4b9847cc948c0534020b532e75d330f368d84e.send"

def get_urls(root):
    driver = webdriver.Chrome()
    driver.get(root)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    k = soup.ul
    kk = k.find_all('a')
    urls = []
    for kkk in kk:
        urls.append('http://jw.scut.edu.cn' + kkk.attrs['href'])
    driver.close()
    return urls


def get_content(url):
    html = requests.get(url)
    html.encoding = 'utf-8'
    htm = BeautifulSoup(html.text, 'html.parser')
    content = {
        'title': htm.select('.content-title')[0].text,
        'time': htm.select('.content-date')[0].text}
    article = []
    for p in htm.select('.content span')[:-1]:
        article.append(p.text.strip())
    article_all = ' '.join(article)
    content['Notice'] = article_all
    return content


def sendbyWeiChat(content):
    data = {'text': content['title'], 'desp': content['Notice']}
    req = requests.post(api, data=data)


def main():
    urls = get_urls(root)
    old_urls = urls
    requests.get(api + '?text=监控开启成功')
    while True:
        urls = get_urls(root)
        if urls != old_urls:
            new = get_content(urls[0])
            sendbyWeiChat(new)
            old_urls = urls
        time.sleep(3600)


main()


