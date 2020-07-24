# tuples = []
# for i in [1,2,3,'a','e']:
#     tuples.append(i)
# print(tuples)
# print(tuple(tuples))
#
# print('**'*2,'*'*0)

# 向数据库中插入数据
from main import Store_management
import random
import pymysql,logging



db_name = 'store_management'
db_user = 'store_manager'
db_pass = 'store_manager'
db_ip = '47.105.91.77'
db_port = 3306
db = Store_management()

def writeDb(cursor,sql, db_data=()):
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



# for item in range(200):
#     # cursor = db.cursor()
#     year = int(random.uniform(2011, 2020))
#     month = int(random.uniform(1, 12))
#     day = int(random.uniform(1, 28))
#     hour = int(random.uniform(0, 23.5))
#     minute = int(random.uniform(0, 59.5))
#     second = int(random.uniform(0, 59.5))
#
#     time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
#     i = random.randint(0, 1)
#     j = random.randint(0, 1)
#     k = random.randint(0, 1)
#     warehouse = ['怀柔', '中科院'],
#     out_in = [1, -1],
#     product = ['羊腿', '猪肉'],
#     num = random.randint(10, 100)
#     p = random.randint(0, 4)
#     people = ['张三', '李四', '王五', '赵六', '钱七'],
#     cost = random.randint(10, 200) + (random.randint(1, 99)) / 100
#
#     # tuples = (warehouse[i],out_in[j],product[k],num,people[p],time,cost)
#     s =                           (warehouse[i], out_in[j], product[k], num, people[p], time, cost)
#     # sql = 'insert into warehouse(warehouse_name, out_in, product_name, num, operator, datetime, cost) values ("%s","%d","%s","%d","%s","%s","%2f")' % s
#     sql = 'insert into warehouse(warehouse_name, out_in, product_name, num, operator, datetime, cost) values ("%s","%d","%s","%d","%s","%s","%2f")'
#     db.cursor.execute(sql)
#     db.commit()
#     print('插入次数:', item)
#     db.close()

count = 0
while True:
    count += 1
    print(count)
    if count > 200:
        break

    year = int(random.uniform(2011, 2020))
    month = int(random.uniform(10, 12))
    day = int(random.uniform(10, 28))
    hour = int(random.uniform(10, 23.5))
    minute = int(random.uniform(10, 59.5))
    second = int(random.uniform(10, 59.5))

    time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second)
    i = random.randint(0, 1)
    print(i)
    j = random.randint(0, 1)
    k = random.randint(0, 1)
    warehouse = ['怀柔', '中科院']
    out_in = [1, -1]
    product = ['羊腿', '猪肉']
    num = random.randint(10, 100)
    p = random.randint(0, 4)
    people = ['张三', '李四', '王五', '赵六', '钱七']
    cost = random.randint(10, 200) + (random.randint(1, 99)) / 100

    # tuples = (warehouse[i],out_in[j],product[k],num,people[p],time,cost)
    # s = (warehouse[i])
    s = (warehouse[i], out_in[j], product[k], num, people[p], time, cost)
    print(s)
    # sql = 'insert into warehouse(warehouse_name, out_in, product_name, num, operator, datetime, cost) values ("%s","%d","%s","%d","%s","%s","%2f")' % s
    sql = 'insert into warehouse(warehouse_name, out_in, product_name, num, operator, datetime, cost) values ("%s","%d","%s","%d","%s","%s","%2f")'% ('大红门',1,'肥牛',25,'撒苦辣','2033-12-07 12:45:23',12.34)


    result = writeDb(sql, s)
    # time.sleep(1)
# finally:
#     cursor.close()
#     conn.close()
# return True