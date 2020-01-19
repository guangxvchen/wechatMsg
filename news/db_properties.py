# coding:utf-8

import pymysql

# 获取连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='chen',
    password='chen',
    db='python3',
    charset='utf8'
)
