from flask import Flask
from flask import jsonify, request, render_template, send_file, send_from_directory
from setting import MYSQL_USER, MYSQL_PORT, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE
import random
import db
from DBUtils.PersistentDB import PersistentDB
import pymysql
from flask_cors import CORS
import time, os, shutil

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决跨域请求

# https://blog.csdn.net/weixin_40976261/article/details/89057633
POOL = PersistentDB(
    creator=pymysql,
    maxusage=None,
    setsession=[],  # 开始会话前执行的命令列表.
    ping=1,
    closeable=False,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    charset='utf8'
)

conn = POOL.connection()
cursor = conn.cursor()


def resultmsg(code, msg, data, pageDetail):
    """

    :param code: 响应码
    :param msg: 联通信息
    :param data: {...}
    :param pageDetail: {page:1,perpage:15,pageCount:113}
    :return:
    """
    result = {
        "msg": msg,
        "code": code,
        "data": data,
        "pageDetail": pageDetail
    }
    return result


def insert_sql():
    for i in range(2):
        year = int(random.uniform(2001, 2010))
        month = int(random.uniform(10, 12))
        day = int(random.uniform(10, 28))
        hour = int(random.uniform(10, 23.5))
        minute = int(random.uniform(10, 59.5))
        second = int(random.uniform(10, 59.5))
        if i == 0:
            time = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(
                second)
        else:
            date_produced = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(
                minute) + ':' + str(second)
    i = random.randint(0, 1)
    print(i)
    j = random.randint(0, 1)
    k = random.randint(0, 1)
    warehouse = ['怀柔', '中科院']
    out_in = [1, -1]
    print('out_in:', out_in[j])
    product = ['羊腿', '猪肉']
    num = random.randint(10, 100)
    p = random.randint(0, 4)
    people = ['张三', '李四', '王五', '赵六', '钱七']
    cost = random.randint(10, 200) + (random.randint(1, 99)) / 100

    s = (warehouse[i], out_in[j], product[k], date_produced, num, people[p], time, cost)
    print(s)
    # 行数据插入语法,增加新字段之后还没修正此语句.
    sql1 = 'insert into warehouse(warehouse_name, out_in, product_name, date_produced,num, operator, date_managed, cost) values ("%s","%d","%s","%s","%d","%s","%s","%2f")' % s
    # sql = 'insert into warehouse(warehouse_name, out_in, product_name, num, operator, datetime, cost) values ("%s","%d","%s","%d","%s","%s","%2f")'% ('大红门',1,'肥牛',25,'撒苦辣','2033-12-07 12:45:23',12.34)

    return sql1


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == '' or request.form['password'] == '':
        return jsonify(resultmsg(400, "input wrong", "", ''))

    sql = 'select username,`right` from users where username="%s" and password="%s"' % (
        request.form['username'], request.form['password'])
    db_result = db.db_execute(conn, cursor, sql)
    if len(db_result) == 0:
        return jsonify(resultmsg(400, "账号或密码错误,请重新输入!", "", ''))
    result = {"username": db_result[0][0], "right": db_result[0][1]}
    return jsonify(resultmsg(200, 'ok', result, 'page'))


@app.route('/productlist', methods=['GET'])
def get_productlist():
    sql = 'select id,product_name from product_category'
    productlist = db.db_execute(conn, cursor, sql)
    result = []
    for i in range(len(productlist)):
        result.append({'id': productlist[i][0], 'product_name': productlist[i][1]})
    return resultmsg(200, '成功', result, '已全部返回.')


@app.route('/addproduct', methods=['POST'])
def addproduct():
    if len(str(request.form['product_name'])) == 0 or len(str(request.form['add_date'])) == 0:
        return resultmsg(400, '信息添加错误,请重新添加.', '', '')
    add_product_info = (str(request.form['product_name']), str(request.form['add_date']))
    sql = 'insert into product_category(product_name,add_product_name_date) values ("%s","%s")' % add_product_info
    result = db.db_execute(conn, cursor, sql)
    return resultmsg(200, '成功', result, '产品名称已添加.')


@app.route('/stock', methods=['POST'])
def stroe_management():
    warehouse_name = request.form['seat']
    warehouse_name_condation = 'warehouse_name="%s"'
    if warehouse_name == '0':
        warehouse_name_condation = '%s'
        warehouse_name = ''

    product_name = request.form['product_name']
    product_name_condation = ' and product_name="%s"'
    if product_name == '0':
        product_name_condation = '%s'
        product_name = ''

    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' and DATE_FORMAT(date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 仅入库
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and cost=%d'

    page = request.form['page']
    perPage = request.form['perPage']
    query_num = (int(page) - 1) * int(perPage)
    limit_condation = ' limit %d,%d'

    sql = 'select id,warehouse_name,out_in,product_name,num,operator,DATE_FORMAT(date_managed,"%Y-%m-%d %H:%i:%s"),cost from warehouse where ' \
          + warehouse_name_condation % warehouse_name \
          + product_name_condation % (product_name) \
          + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
          + field_condation % term \
          + limit_condation % (int(query_num), int(perPage))

    sql2 = 'select count(*) from warehouse where ' \
           + warehouse_name_condation % warehouse_name \
           + product_name_condation % (product_name) \
           + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
           + field_condation % term

    count = db.db_execute(conn, cursor, sql2)
    print(count)

    print(sql)
    result = db.db_execute(conn, cursor, sql)
    print(result)
    data_ = []
    if result == None:
        pass
    else:
        for i in range(len(result)):
            data_.append({
                'id': result[i][0],
                'product_name': result[i][3],
                'operation': result[i][2],
                'number': result[i][4],
                'opttime': result[i][6],
                'stock': result[i][1],
                'fare': result[i][7],
                'operator': result[i][5],
            })
    print("result:\n", result)
    data = {
        "dataList": data_,
        "pageCount": int(count[0][0])
    }

    return resultmsg(200, '', data, '')


@app.route('/operateStock', methods=['POST'])
def warehouse_manage():
    warehouse_name = request.form['seat']
    product_name = request.form['produce_name']
    out_in = request.form['out_in']
    num = request.form['num']
    date_managed = request.form['date']
    cost = request.form['fare']  # 此处必须限制小数点后两位
    operator = request.form['operator']
    s = (warehouse_name, int(out_in), product_name, int(num), operator, date_managed, float(cost))
    if out_in == '-1':
        sql_sum_remaining = 'select sum(num) from warehouse where warehouse_name="%s"' % (warehouse_name) + \
                            ' and product_name="%s"' % product_name
        print(sql_sum_remaining)
        product_name_sum_num = db.db_execute(conn, cursor, sql_sum_remaining)[0][0]
        print("product_name_sum_num:", product_name_sum_num)

        if product_name_sum_num >= int(num):

            sql = 'insert into warehouse(warehouse_name, out_in, product_name,num, operator, date_managed, cost) ' \
                  'values ("%s",%d,"%s",%d,"%s","%s",%2f)' % s
            # print(sql)
            result = db.db_execute(conn, cursor, sql)
            return resultmsg(200, 'OK', result, '数据插入成功')
        else:
            return resultmsg(422, '当前产品库存量不足出库量,请重新输入!', '', '')
    else:
        # 数量超过11位数,不能插入数据
        if len(str(num)) > 11:
            return resultmsg(422, '入库数量超限!', '', '')
        elif int(num) > 0:
            sql = 'insert into warehouse(warehouse_name, out_in, product_name,num, operator, date_managed, cost)' \
                  'values ("%s",%d,"%s",%d,"%s","%s",%2f)' % s
            print(sql)
            result = db.db_execute(conn, cursor, sql)
            return resultmsg(200, 'OK', result, '数据插入成功')
        else:
            return resultmsg(422, '入库数量不可小于1!')


@app.route('/total', methods=['POST'])
def total():
    warehouse_name1 = request.form['seat1']
    print(warehouse_name1)
    warehouse_name2 = request.form['seat2']
    print(warehouse_name2)
    sql1 = 'select sum(num*out_in) from warehouse where warehouse_name="%s"' % (warehouse_name1)
    sql2 = 'select sum(num*out_in) from warehouse where warehouse_name="%s"' % (warehouse_name2)
    print(sql1)
    result1 = db.db_execute(conn, cursor, sql1)
    result2 = db.db_execute(conn, cursor, sql2)

    warehouse1_name_total = int(result1[0][0])
    warehouse2_name_total = int(result2[0][0])
    all_total = warehouse1_name_total + warehouse2_name_total
    result = {"allstock": all_total, "seat1_stock": warehouse1_name_total, "seat2_stock": warehouse2_name_total}
    return resultmsg(200, 'ok', result, '')


@app.route('/warehouse', methods=['POST'])
def warehouse():
    warehouse_name = request.form['seat']
    sql1 = 'select product_name from product_category'
    product_names = db.db_execute(conn, cursor, sql1)
    print(product_names)
    result = []
    for i in range(len(product_names)):
        sql2 = 'select sum(num*out_in) from warehouse where product_name="%s"' % product_names[i][
            0] + ' and warehouse_name="%s"' % warehouse_name
        print(sql2)
        data = db.db_execute(conn, cursor, sql2)
        if data[0][0] == None:
            data = 0
        else:
            data = data[0][0]
        print(data)
        result.append({'product_name': product_names[i][0], "product_num": int(data)})
    return resultmsg(200, 'ok', result, '')


@app.route('/sum', methods=['POST'])
def sum():
    warehouse_name = request.form['seat']
    warehouse_name_condation = 'warehouse_name="%s"'

    product_name = request.form['product_name']
    product_name_condation = ' and product_name="%s"'
    if product_name == '0':
        product_name_condation = '%s'
        product_name = ''
    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' and DATE_FORMAT(date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 仅入库
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and cost=%d'

    sql_all_in = 'select sum(num) from warehouse where ' \
                 + warehouse_name_condation % warehouse_name \
                 + product_name_condation % product_name \
                 + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
                 + ' and out_in=%d' % 1 \
                 + field_condation % term
    print('sql_all_in:\n', sql_all_in)
    sql_all_out = 'select sum(num) from warehouse where ' \
                  + warehouse_name_condation % warehouse_name \
                  + product_name_condation % product_name \
                  + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
                  + ' and out_in=%d' % -1 \
                  + field_condation % term
    print('sql_all_out:\n', sql_all_out)
    sql_all_cost = 'select sum(cost) from warehouse where ' \
                   + warehouse_name_condation % warehouse_name \
                   + product_name_condation % product_name \
                   + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
                   + field_condation % term
    print('sql_all_cost:\n', sql_all_cost)

    all_in = db.db_execute(conn, cursor, sql_all_in)
    all_out = db.db_execute(conn, cursor, sql_all_out)
    all_cost = db.db_execute(conn, cursor, sql_all_cost)
    values = [all_in[0][0], all_out[0][0], all_cost[0][0]]
    for i in range(len(values)):
        if values[i] == None:
            values[i] = 0
    data = {"allinstock": str(values[0]), "alloutstock": str(values[1]), "allfare": str(values[2])}
    return resultmsg(200, 'ok', data, '')


@app.route('/edit', methods=['POST'])
def edit():
    id = int(request.form['id'])
    product_name = request.form['product_name']
    out_in = int(request.form['out_in'])

    num = int(request.form['num'])
    date_managed = request.form['date']
    cost = float(request.form['fare'])

    sql = 'update warehouse set num=%d,date_managed="%s",cost=%2f,product_name="%s",out_in=%d' % (
    num, date_managed, cost, product_name, out_in) + ' where id=%d' % (id)
    # sql = 'update warehouse set num=%d,date_managed="%s",cost=%2f'%(num,date_managed,cost) + ' where id=%d'%(id)
    print(sql)
    result = db.db_execute(conn, cursor, sql)
    return resultmsg(200, 'ok', result, '')


@app.route('/download', methods=['POST'])
def download():
    print('进入下载程序!')
    warehouse_name = request.form['seat']
    warehouse_name_condation = 'warehouse_name="%s"'
    if warehouse_name == '0':
        warehouse_name_condation = '%s'
        warehouse_name = ''

    product_name = request.form['product_name']
    product_name_condation = ' and product_name="%s"'
    if product_name == '0':
        product_name_condation = '%s'
        product_name = ''

    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' and DATE_FORMAT(date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 仅入库
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and cost=%d'

    # page = request.form['page']
    # perPage = request.form['perPage']
    # query_num = (int(page) -1)* int(perPage)
    # limit_condation = ' limit %d,%d'

    file_name = str(int(time.time())) + '.xlsx'
    print(file_name)

    sql = 'select warehouse_name,out_in,product_name,num,operator,DATE_FORMAT(date_managed,"%Y-%m-%d %H:%i:%s"),cost from warehouse where ' \
          + warehouse_name_condation % warehouse_name \
          + product_name_condation % (product_name) \
          + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
          + field_condation % term \
          + 'into outfile ' + '/var/lib/mysql-files/"%s"' % file_name
    print(sql)
    result = db.db_execute(conn, cursor, sql)
    print(result)
    # basepath = os.path.abspath(os.getcwd()
    file_list = os.listdir("/var/lib/mysql-files/")
    if len(file_name) > 0:
        for file in file_list:
            if file[-4:] == 'xlsx':
                shutil.move("/var/lib/mysql-files/" + file, '/home/store_flask/')
    dirpath = os.path.join(app.root_path, '')
    return send_from_directory(dirpath, file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    ## 数据库中有226条数据
    # sql = insert_sql()
    # db.db_execute(conn,cursor,sql)
    # app.run(debug=True)
