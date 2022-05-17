import requests
from bs4 import BeautifulSoup
import time

list_ip = []
list_port = []
list_headers_ip = []

for start in range(1, 11):

    url = 'https://www.kuaidaili.com/free/inha/{}/'.format(start)  # 每页15个数据，共爬取10页
    print("正在处理url: ", url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71'}
    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    ip = soup.select('#list > table > tbody > tr > td:nth-child(1)')
    port = soup.select('#list > table > tbody > tr > td:nth-child(2)')

    for i in ip:
        list_ip.append(i.get_text())

    for i in port:
        list_port.append(i.get_text())

    time.sleep(1)  # 防止爬取太快，数据爬取不全

# 代理ip的形式:        'http':'http://119.14.253.128:8088'

for i in range(150):
    IP_http = '{}:{}'.format(list_ip[i], list_port[i])
    IP_https = 'https://{}:{}'.format(list_ip[i], list_port[i])
    proxies = {
        'HTTP': IP_http
        # 'HTTPS': IP_https
    }
    list_headers_ip.append(proxies)
    # print(proxies)

print(list_headers_ip)


# 检查IP的可用性
def check_ip(list_ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
        'Connection': 'close'}
    # url = 'https://www.baidu.com'  # 以百度为例，检测IP的可行性
    url = 'https://movie.douban.com/subject/1292052/'

    can_use = []
    for ip in list_ip:
        try:
            response = requests.get(url=url, headers=headers, proxies=ip, timeout=3)  # 在0.1秒之内请求百度的服务器
            if response.status_code == 200:
                can_use.append(ip)
        except Exception as e:
            print(e)

    return can_use


can_use = check_ip(list_headers_ip)
print('能用的代理IP为：', can_use)
# for i in can_use:
#     print(i)
print('能用的代理IP数量为：', len(can_use))

fo = open('IP代理池.txt', 'w')
for i in can_use:
    fo.write(str(i) + '\n')

fo.close()