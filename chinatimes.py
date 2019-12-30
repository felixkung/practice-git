import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

def news(page):
    num = (page - 1)*10
    url = 'https://www.chinatimes.com/newspapers/260118?page =' +str(1) + '&chdtv'
    #url = 'https://www.chinatimes.com/newspapers/2601?chdtv'
    res = requests.get(url, headers=headers).text
    #print(res)

    p_title = '<h3 class="title">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    # print(title)
    # print(len(title))
    p_href = '<h3 class="title">.*?<a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    # print(href)
    # print(len(href))

    source = []
    for i in range(len(title)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        source.append(title[i].split('&nbsp;&nbsp;')[0])
        source[i] = source[i].strip()
        print(str(i + 1) + '.' + title[i] + source[i])
        print("https://www.chinatimes.com" + href[i])


for i in range(20):
    news(i+1)
    print('第' + str(i+1) + '頁爬取成功')





