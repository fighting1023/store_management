# import pymysql
# pymysql.connect(
# host='47.105.91.77',
# user='store_manager',
# password='store_manager',
# database='store_management',
# charset='utf8'#注意不是utf-8
# )
import os
import time  # 含有sleep()的库
import pymysql  # python连接数据库的库
import logging
# import pandas as pd
import datetime  # 获取时间的库

db_name = 'store_management'
db_user = 'store_manager'
db_pass = 'store_manager'
db_ip = '47.105.91.77'
db_port = 3306


# 写入数据到数据库中
def writeDb(sql, db_data=()):
    """
    连接mysql数据库（写），并进行写的操作
    """

    try:
        cursor.execute(sql, db_data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error('数据写入失败:%s' % e)
        return False



while True:
    times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = """ INSERT INTO test(test_time,test_name) VALUES(%s,%s) """
    data = (times, 'ha')
    result = writeDb(sql, data)
    time.sleep(1)

