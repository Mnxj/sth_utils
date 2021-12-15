import os
import re
import time

import requests
from bs4 import BeautifulSoup

URL_TEMPLATE = 'https://m.imitui.com'
payload = {}
headers = {
    'authority': 'm.imitui.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '__yjs_duid=1_92c5f9fa380e878536d9a961d176c1121639327444533; UM_distinctid=17daf87b3a9820-023403167188f8-133f6452-1ea000-17daf87b3aa9df; _ga=GA1.1.1654586346.1639327446; click-9574=1; CNZZDATA1280258856=931658379-1639317253-https%253A%252F%252Fwww.baidu.com%252F%7C1639410602; CNZZDATA1279069799=1585978817-1639321760-https%253A%252F%252Fm.imitui.com%252F%7C1639404725; _ga_0245EFVQ0X=GS1.1.1639412915.3.1.1639412963.0'
}


def load_images(urls: str, catalog: int, name: str):
    if urls.startswith('http'):
        response = requests.request("GET", urls, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.findAll('img')[0].get("src")
        p = str(soup.findAll('p')[0].string).split("/")
        if p[0] == p[1]:  # 每章节结尾
            return
        write_images(images, catalog, name)
        for a in soup.findAll('a'):
            href = a['href'].strip()
            if href != '':
                if a.string == '下一章' and str(href).endswith('.html'):
                    catalog += 1
                    load_images(href, catalog, name)
                if a.string == '下一页':
                    load_images(URL_TEMPLATE + href, catalog, name)


def write_images(urls: str, catalog: int, name: str):
    print(urls)
    time.sleep(1)
    path = name + str(catalog)
    if not os.path.exists(path):
        os.makedirs(path)

    img = requests.get(urls, headers=headers)
    with open(path + '/' + str(time.time()) + '.jpg', 'wb') as fd:
        for chunk in img.iter_content():
            fd.write(chunk)


def generate(url: str, num: int, name: str):
    response = requests.request("GET", url, headers=headers, data=payload)
    if re.compile(r'<center><h1>没有找到指定页面！</h1></center>').findall(response.text):
        print('没有找到指定页面')
        return
    soup = BeautifulSoup(str(re.compile(r'<a.*?class=".*?"><span>.*?</span></a>').findall(response.text)),
                         'html.parser')
    urls = soup.findAll('a')
    print(response.text)

    while num < len(urls):
        print("start:" + str(num))
        if str(urls[num]['href']).startswith("javascript"):
            print('漫画结束....')
            return num
        load_images(urls[num]['href'], num, name)
        num += 1
    return num+1
