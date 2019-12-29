#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'felixkung'

# 导入urllib中的request模块，用来发送http/https请求
from urllib import request
from bs4 import BeautifulSoup
import pymysql
from openpyxl import Workbook
import redis


# 获取数据
def get_data():
    url = 'https://search.51job.com/list/070200,000000,0000,00,9,99,java%25E5%25BC%2580%25E5%258F%2591,2,1.html'
    # 创建Request对象，指定url和请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    # print(type(response))  # HTTPResponse类型
    # print(response.getcode())  # 响应状态码
    # print(response.info())

    if response.getcode() == 200:
        data = response.read()  # 读取响应结果
        # print(type(data)) # bytes类型
        data = str(data, encoding='gbk')  # 转换为str
        # print(data)

        # 将数据写入文件中
        with open('index.html', mode='w', encoding='gbk') as f:
            f.write(data)


# 处理数据
def parse_data():
    with open('index.html', mode='r', encoding='gbk') as f:
        html = f.read()

    #  创建BeautifulSoup实例，解析html数据
    bs = BeautifulSoup(html, 'html.parser')  # 指定使用html解析器parser
    # 获取职位信息
    divs = bs.select('#resultList .el')
    result = []
    for div in divs[1:]:
        title = div.select('.t1')[0].get_text(strip=True)
        company = div.select('.t2')[0].get_text(strip=True)
        addr = div.select('.t3')[0].get_text(strip=True)
        salary = div.select('.t4')[0].get_text(strip=True)
        pubDate = div.select('.t5')[0].get_text(strip=True)
        # print(title, company, addr, salary, pubDate)
        row = {
            'title': title,
            'company': company,
            'addr': addr,
            'salary': salary,
            'pubDate': pubDate
        }
        result.append(row)
    return result

# 存储数据到Excel
def save_to_excel(data):
    # 创建工作薄Workbook
    book = Workbook()

    # 创建工作表Sheet
    sheet = book.create_sheet('南京Java招聘信息', 0)

    # 向工作表中添加数据
    sheet.append(['职位名', '公司名', '工作地点', '薪资', '发布时间'])
    for item in data:
        row = [item['title'], item['company'], item['addr'], item['salary'], item['pubDate']]
        sheet.append(row)

    # 输出保存
    book.save('51job.xlsx')


if __name__ == '__main__':
     #get_data()
    # save_to_mysql(parse_data())
    save_to_excel(parse_data())
    # save_to_redis(parse_data())
    #read_from_redis()
