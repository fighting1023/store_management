# -*- coding:utf-8 -*-
from flask import Flask
from flask import jsonify, request, render_template, send_file, send_from_directory
from setting import MYSQL_USER, MYSQL_PORT, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE
import random
import db
from DBUtils.PersistentDB import PersistentDB
import pymysql
from flask_cors import CORS
import time, os, shutil
import pandas as pd

app = Flask(__name__)

# 解决跨域请求
CORS(app, supports_credentials=True)

# 添加进程池
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


def warehouse_category_info():
    sql = 'select id, warehouse_name from warehouse_category'
    result = db.db_execute(conn, cursor, sql)
    id_product_category = []
    name_product_category = []
    for i in range(len(result)):
        id_product_category.append(str(result[i][0]))
        name_product_category.append(result[i][1])
    return id_product_category, name_product_category


def product_category_info():
    sql = 'select id, product_name from product_category where product_name_be_del is null'
    result = db.db_execute(conn, cursor, sql)
    id_product_category = []
    name_product_category = []
    for i in range(len(result)):
        id_product_category.append(result[i][0])
        name_product_category.append(result[i][1])
    return id_product_category, name_product_category


@app.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return:
    """
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
    """
    查询产品列表（猪肉、羊肉。。。）
    :return:
    """
    sql_productlist = 'select id,product_name,DATE_FORMAT(add_product_name_date,"%Y-%m-%d %H:%i:%s"),batch,`size`,mark,note ' \
                      'from product_category ' \
                      'where product_name_be_del is null'
    productlist = db.db_execute(conn, cursor, sql_productlist)
    print(productlist)
    if productlist == None:
        resultmsg(200, 'ok', '', '查询结果为空！')
    result = []
    for i in range(len(productlist)):
        result.append({'id': str(productlist[i][0]),
                       'product_name': str(productlist[i][1]),
                       'add_product_name_date': str(productlist[i][2]),
                       'batch': productlist[i][3],
                       'size': productlist[i][4],
                       'mark': productlist[i][5],
                       'note': productlist[i][6]
                       })
    return resultmsg(200, '产品名录详情', result, '已全部返回.')


@app.route('/product_del_list', methods=['GET'])
def get_product_del_list():
    """
    查询已删除产品的列表
    :return:
    """
    sql_product_del_list = 'select id,product_name,DATE_FORMAT(product_name_be_del_time,"%Y-%m-%d %H:%i:%s"),product_name_be_del_operator,batch,`size`,mark,note ' \
                           'from product_category ' \
                           'where product_name_be_del is not null'
    product_del_list = db.db_execute(conn, cursor, sql_product_del_list)
    print(product_del_list)
    if product_del_list == None:
        product_del_list = []
    result = []
    for i in range(len(product_del_list)):
        result.append({'id': str(product_del_list[i][0]),
                       'product_name': str(product_del_list[i][1]),
                       'product_name_be_del_time': str(product_del_list[i][2]),
                       'product_name_be_del_operator': str(product_del_list[i][3]),
                       'batch': str(product_del_list[i][4]),
                       'size': str(product_del_list[i][5]),
                       'mark': str(product_del_list[i][6]),
                       'note': str(product_del_list[i][7])
                       })
    return resultmsg(200, '已删除产品名录详情', result, '已全部返回.')


@app.route('/reuse_product_name', methods=['POST'])
def reuse_product_name():
    id = int(request.form['id'])
    sql_reuse_product_name = 'update product_category ' \
                             'set product_name_be_del=NULL,product_name_be_del_time=NULL,product_name_be_del_operator=NULL ' \
                             'where id=%d' % id
    result = db.db_execute(conn, cursor, sql_reuse_product_name)
    print(result)
    return resultmsg(200, '恢复成功！', '', '')


@app.route('/addproduct', methods=['POST'])
def addproduct():
    """
    在产品名录product_category中添加产品
    :return:
    """
    if len(str(request.form['product_name'])) == 0 or len(str(request.form['add_date'])) == 0:
        return resultmsg(400, '信息添加错误,请重新添加.', '', '')
    sql = 'select id,product_name from product_category where product_name_be_del is null'
    productlist = db.db_execute(conn, cursor, sql)
    result = []
    for i in range(len(productlist)):
        result.append(productlist[i][1])
    if request.form['product_name'] in result:
        return resultmsg(200, '产品已存在（或者从已删除列表中恢复）！', '', '')
    add_product_info = (str(request.form['product_name']),
                        str(request.form['add_date']),
                        str(request.form['batch']),
                        str(request.form['size']),
                        str(request.form['mark']),
                        str(request.form['note'])
                        )
    sql = 'insert into product_category(product_name,add_product_name_date,batch,`size`,mark,note) ' \
          'values ("%s","%s","%s","%s","%s","%s")' % add_product_info
    result = db.db_execute(conn, cursor, sql)
    return resultmsg(200, '成功', result, '产品名称已添加.')


@app.route('/stock', methods=['POST'])
def stroe_management():
    """
    条件查询操作记录  (A->warehouse, B->warehouse_category, C->product_category)
    :return:
    """
    warehouse_name = int(request.form['seat'])
    warehouse_name_condation = ' A.warehouse_name=%d'
    if warehouse_name == 0:
        warehouse_name_condation = '%s'
        warehouse_name = ''

    product_name = int(request.form['product_name'])
    product_name_condation = ' and A.product_name=%d'
    if product_name == 0:
        product_name_condation = '%s'
        product_name = ''

    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' and DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 仅入库
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and A.cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and A.cost=%d'

    page = request.form['page']
    perPage = request.form['perPage']
    query_num = (int(page) - 1) * int(perPage)
    limit_condation = ' limit %d,%d'

    sql = 'select A.id,B.warehouse_name,A.out_in,C.product_name,A.num,A.operator,DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s"),A.cost,C.id,A.correct,C.batch,C.size,C.mark,C.note ' \
          'from warehouse A,warehouse_category B,product_category C ' \
          'where' + warehouse_name_condation % warehouse_name \
          + product_name_condation % (product_name) \
          + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
          + field_condation % term \
          + ' and A.warehouse_name=B.id' \
          + ' and C.id=A.product_name' \
          + limit_condation % (int(query_num), int(perPage))
    # sql = """
    # select A.id,B.warehouse_name,C.product_name from warehouse A,warehouse_category B,product_category C where A.product_name=C.id and A.warehouse_name=B.id and A.warehouse_name=1 and DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s") BETWEEN "2000-06-23 00:00:00" AND "2020-07-23 23:59:59";
    # """

    sql2 = 'select count(*) from warehouse A,warehouse_category B,product_category C where ' \
           + warehouse_name_condation % warehouse_name \
           + product_name_condation % (product_name) \
           + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
           + ' and A.warehouse_name=B.id' \
           + ' and C.id=A.product_name' \
           + field_condation % term
    count = db.db_execute(conn, cursor, sql2)
    print(count)

    print('sql:\n', sql)
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
                'p_id': result[i][8],
                'correct': result[i][9],
                'batch': result[i][10],
                'size': result[i][11],
                'mark': result[i][12],
                'note': result[i][13]
            })
    print("result:\n", result)
    data = {
        "dataList": data_,
        "pageCount": int(count[0][0])
    }

    return resultmsg(200, '', data, '')


@app.route('/operateStock', methods=['POST'])
def warehouse_manage():
    """
    出入库操作(出库时需要判断余量是否满足条件)
    :return:
    """
    warehouse_name = int(request.form['seat'])
    product_name = int(request.form['produce_name'])
    out_in = request.form['out_in']
    num = request.form['num']
    date_managed = request.form['date']
    cost = request.form['fare']  # 此处必须限制小数点后两位
    operator = request.form['operator']
    s = (warehouse_name, int(out_in), product_name, int(num), operator, date_managed, float(cost))
    if out_in == '-1':
        sql_sum_remaining = 'select sum(num*out_in) from warehouse where warehouse_name=%d' % warehouse_name + ' and product_name=%d' % product_name
        print(sql_sum_remaining)
        product_name_sum_num = db.db_execute(conn, cursor, sql_sum_remaining)[0][0]
        if product_name_sum_num == None:
            product_name_sum_num = 0
        else:
            product_name_sum_num = int(product_name_sum_num)
        print("product_name_sum_num:\n", product_name_sum_num)

        if product_name_sum_num >= int(num) > 0:

            sql = 'insert into warehouse(warehouse_name, out_in, product_name,num, operator, date_managed, cost) ' \
                  'values ("%s",%d,"%s",%d,"%s","%s",%2f)' % s
            # print(sql)
            result = db.db_execute(conn, cursor, sql)
            return resultmsg(200, 'OK', result, '数据插入成功')
        else:
            return resultmsg(422, '数值错误，请重新输入!', '', '')

    elif out_in == '1':
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
    """
    查询 各个库的产品总存量，并累加成为所有的库存量
    :return:
    """
    warehouse_name1 = int(request.form['seat1'])
    print(warehouse_name1)
    warehouse_name2 = int(request.form['seat2'])
    print(warehouse_name2)
    sql1 = 'select sum(num*out_in) from warehouse where warehouse_name=%d' % warehouse_name1
    sql2 = 'select sum(num*out_in) from warehouse where warehouse_name=%d' % warehouse_name2
    print(sql1)
    result1 = db.db_execute(conn, cursor, sql1)
    result2 = db.db_execute(conn, cursor, sql2)
    datas = [result1, result2]
    print(datas)
    for i in range(len(datas)):
        if datas[i][0][0] == None:
            datas[i] = 0
        else:
            datas[i] = datas[i][0][0]
    print(datas)

    print(result1)
    print(result2)
    warehouse1_name_total = int(str(datas[0]))
    warehouse2_name_total = int(str(datas[1]))
    all_total = warehouse1_name_total + warehouse2_name_total
    result = {"allstock": all_total, "seat1_stock": warehouse1_name_total, "seat2_stock": warehouse2_name_total}
    return resultmsg(200, 'ok', result, '')


@app.route('/warehouse', methods=['POST'])
def warehouse():
    """
    查询指定库下的所有产品种类及对应数量
    :return:
    """
    warehouse_name = int(request.form['seat'])
    sql1 = 'select id,product_name,batch,`size`,mark,note from product_category where product_name_be_del is null'
    product_names = db.db_execute(conn, cursor, sql1)
    print('product_names:\n', product_names)
    if product_names == None:
        product_names = []
    result = []
    for i in range(len(product_names)):
        sql2 = 'select sum(num*out_in) from warehouse ' \
               'where product_name=%d' % int(product_names[i][0]) + ' and warehouse_name=%d' % warehouse_name
        data = db.db_execute(conn, cursor, sql2)
        if data[0][0] == None:
            data = 0
        else:
            data = data[0][0]
        print(data)
        result.append({'id': product_names[i][0],
                       "name": product_names[i][1],
                       "batch": product_names[i][2],
                       "size": product_names[i][3],
                       "mark": product_names[i][4],
                       "note": product_names[i][5],
                       "value": int(data)
                       })
    return resultmsg(200, 'ok', result, '')


@app.route('/allwarehouse', methods=['GET'])
def allwarehouse():
    """
    计算所有库中各个产品的总余量
    :return:
    """
    sql1 = 'select id,product_name from product_category where product_name_be_del is Null'
    product_names = db.db_execute(conn, cursor, sql1)
    result = []
    for i in range(len(product_names)):
        sql3 = 'select sum(num*out_in) from warehouse where product_name=%d' % product_names[i][0]
        print(sql3)
        data = db.db_execute(conn, cursor, sql3)
        if data[0][0] == None:
            data = 0
        else:
            data = data[0][0]
        print(data)
        result.append({'id': product_names[i][0], "name": product_names[i][1], "value": int(data)})
    return resultmsg(200, 'ok', result, '')


@app.route('/sum', methods=['POST'])
def sum():
    """
    条件查询所有操作记录中的某产品出入库总量及对应的费用
    :return:
    """
    warehouse_name = int(request.form['seat'])
    warehouse_name_condation = 'warehouse_name=%d'

    product_name = int(request.form['product_name'])
    product_name_condation = ' and product_name=%d'
    if product_name == 0:
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
                 + field_condation % term \
                 + 'and out_in=1'

    print('sql_all_in:\n', sql_all_in)

    sql_all_out = 'select sum(num) from warehouse where ' \
                  + warehouse_name_condation % warehouse_name \
                  + product_name_condation % product_name \
                  + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
                  + field_condation % term \
                  + 'and out_in=-1'

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
    datas = [all_in, all_out, all_cost]
    print(datas)
    for i in range(len(datas)):
        if datas[i] == None:
            datas[i] = 0
        else:
            datas[i] = datas[i][0][0]

    values = datas
    print(datas)
    for i in range(len(values)):
        if values[i] == None:
            values[i] = 0
    data = {"allinstock": str(values[0]), "alloutstock": str(values[1]), "allfare": str(values[2])}
    return resultmsg(200, 'ok', data, '')


@app.route('/edit', methods=['POST'])
def edit():
    """
    修改操作记录
    :return:
    """
    id = int(request.form['id'])
    product_name = int(request.form['product_name'])
    out_in = int(request.form['out_in'])
    num = int(request.form['num'])
    date_managed = request.form['date']
    cost = float(request.form['fare'])

    sql = 'update warehouse set num=%d,date_managed="%s",cost=%2f,product_name=%d,out_in=%d' % (
        num, date_managed, cost, product_name, out_in) + ' where id=%d' % (id)
    print(sql)
    result = db.db_execute(conn, cursor, sql)
    return resultmsg(200, 'ok', result, '')


@app.route('/download', methods=['POST'])
def download():
    """
    下载操作记录
    :return:
    """
    warehouse_name = request.form['seat']
    warehouse_name_condation = 'A.warehouse_name=%d'
    if warehouse_name == '0':
        warehouse_name_condation = '%s'
        warehouse_name = ''

    product_name = request.form['product_name']
    product_name_condation = ' and A.product_name=%d'
    if product_name == '0':
        product_name_condation = '%s'
        product_name = ''

    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 无条件
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and A.cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and A.cost=%d'

    correct = int(request.form['correct'])
    correct_condation = ' and A.correct=%d'
    if -1 > correct or correct > 1:
        return resultmsg(200, 'correct值错误！', '', '')
    if correct == 0:
        correct_condation = '%s'
        correct = ''
    sql = 'select B.warehouse_name,A.out_in,C.product_name,A.num,C.batch,C.size,C.mark,C.note,A.operator,DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s"),A.cost,A.correct ' \
          'from warehouse A, warehouse_category B, product_category C where ' \
          + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
          + warehouse_name_condation % warehouse_name \
          + product_name_condation % (product_name) \
          + correct_condation % correct \
          + field_condation % term \
          + ' and A.warehouse_name=B.id and A.product_name=C.id ' \
        # + ' limit 0,15'
    # + 'into outfile ' + '/var/lib/mysql-files/"%s"' % file_name \
    # + 'CHARACTER SET gbk'
    print(sql)
    result = db.db_execute(conn, cursor, sql)
    print(pd.DataFrame(result))
    index = []
    for i in range(1, len(result) + 1):
        index.append(str(i))
    # xlsx = pd.DataFrame(result,columns=['所属仓库','出入库','产品名','数量','操作员','时间','运费','修正'],index=None)
    xlsx = pd.DataFrame(result, columns=['所属仓库', '出入库', '产品名', '数量', '批次', '规格', '条形码', '备注', '操作员', '时间', '运费', '修正'],
                        index=index)
    path = '/www/wwwroot/fyw/store_management/excel_files/'
    path = ''
    url = 'http://www.fangyangwang.cn/store_management/excel_files/'
    warehouse_name_xlsx = 'select B.warehouse_name from warehouse_category B,watrhouse A where A.warehouse_name=B.id'
    print(warehouse_name_xlsx)

    filename = str(int(time.time())) + '.xlsx'
    xlsx.to_excel(path + filename)

    url = url + filename
    return resultmsg(200, 'ok', url, '')


@app.route('/warehouse_info', methods=['GET'])
def warehouseinfo():
    """
    查询仓库信息
    :return:
    """
    sql = 'select id, warehouse_name,`position`,telphone,master from warehouse_category'
    result = db.db_execute(conn, cursor, sql)
    print(result)
    data = []
    for i in range(len(result)):
        data.append({"id": result[i][0],
                     "name": result[i][1],
                     "position": result[i][2],
                     "telphone": result[i][3],
                     "master": result[i][4],
                     })
    return resultmsg(200, '', data, '')


@app.route('/del_product_name', methods=['POST'])
def del_product_name():
    """
    删除产品
    :return:
    """
    product_name_be_del = int(request.form['tag'])
    if product_name_be_del != 1:
        return resultmsg(400, '删除标记错误！', '', '')
    product_name_be_del_time = request.form['time']
    id = int(request.form['id'])
    operator = request.form['user']
    sql_find_id = 'select id from product_category where product_name_be_del is null'
    pids = db.db_execute(conn, cursor, sql_find_id)
    print(pids)
    pisd_list = []
    for i in range(len(pids)):
        pisd_list.append(pids[i][0])
    if id in pisd_list:
        # sql_del_product_name = 'delete from product_category where id=%d' % id
        sql_del_product_name = 'update product_category set product_name_be_del=%d,' % product_name_be_del + ' product_name_be_del_time="%s", ' % product_name_be_del_time + 'product_name_be_del_operator="%s"' % operator + ' where id=%d ' % id
        print(sql_del_product_name)
        result = db.db_execute(conn, cursor, sql_del_product_name)
        print(result)
        if len(result) == 0:
            return resultmsg(200, '操作成功！', result, '')
        else:
            return resultmsg(500, '服务器错误，请重新尝试！', result, '')
    else:
        return resultmsg(200, '当前产品不存在！', [], '')


@app.route('/correct', methods=['POST'])
def correct():
    """
    修正仓库中某产品的信息
    :return:
    """
    warehouse_name = int(request.form['seat'])
    out_in = int(request.form['out_in'])
    product_name = int(request.form['name'])
    num = int(request.form['num'])
    operator = request.form['operator']
    date_managed = request.form['time']
    cost = float(request.form['fare'])
    correct = int(request.form['correct'])
    correct_data = (warehouse_name, out_in, product_name, num, operator, date_managed, cost, correct)
    sql_correat = 'insert into warehouse(warehouse_name,out_in,product_name,num,operator,date_managed,cost,correct) ' \
                  'values (%d,%d,%d,%d,"%s","%s",%2f,%d)' % correct_data
    print(sql_correat)
    result = db.db_execute(conn, cursor, sql_correat)
    if len(result) == 0:
        print(result)
        return resultmsg(200, '修正完成。', result, '')
    else:
        return resultmsg(500, '服务器错误，请重新尝试！', result, '')


@app.route('/correct_log', methods=['POST'])
def correct_log():
    """
    查询所有的修正记录
    :return:
    """
    # warehouse_name = int(request.form['seat'])
    warehouse_name = int(request.form['seat'])
    warehouse_name_condation = ' A.warehouse_name=%d'
    if warehouse_name == 0:
        warehouse_name_condation = '%s'
        warehouse_name = ''

    product_name = int(request.form['product_name'])
    product_name_condation = ' and A.product_name=%d'
    if product_name == 0:
        product_name_condation = '%s'
        product_name = ''

    date_start = request.form['startdate'] + ' 00:00:00'
    date_end = request.form['enddate'] + ' 23:59:59'
    time_span_condation1 = ' and DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s")'
    time_span_condation2 = ' BETWEEN "%s" AND "%s"'
    # print(time_span_condation2)

    term = request.form['condation']
    if str(term) == '0':  # 仅入库
        term = ''
        field_condation = '%s'
    elif str(term) == '1':  # 仅入库
        term = 1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '2':  # 仅出库
        term = -1
        field_condation = ' and A.out_in=%d'
    elif str(term) == '3':  # 有运费
        term = 0.01
        field_condation = ' and A.cost>=%2f'
    elif str(term) == '4':  # 无运费
        term = 0
        field_condation = ' and A.cost=%d'

    page = request.form['page']
    perPage = request.form['perPage']
    query_num = (int(page) - 1) * int(perPage)
    limit_condation = ' limit %d,%d'

    sql = 'select A.id,B.warehouse_name,A.out_in,C.product_name,A.num,A.operator,DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s"),A.cost,C.id,A.correct ' \
          'from warehouse A,warehouse_category B,product_category C ' \
          'where correct is not null and ' + warehouse_name_condation % warehouse_name \
          + product_name_condation % (product_name) \
          + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
          + field_condation % term \
          + ' and A.warehouse_name=B.id' \
          + ' and C.id=A.product_name' \
          + limit_condation % (int(query_num), int(perPage))
    # sql = """
    # select A.id,B.warehouse_name,C.product_name from warehouse A,warehouse_category B,product_category C where A.product_name=C.id and A.warehouse_name=B.id and A.warehouse_name=1 and DATE_FORMAT(A.date_managed,"%Y-%m-%d %H:%i:%s") BETWEEN "2000-06-23 00:00:00" AND "2020-07-23 23:59:59";
    # """

    sql2 = 'select count(*) from warehouse A,warehouse_category B,product_category C where  correct is not null and ' \
           + warehouse_name_condation % warehouse_name \
           + product_name_condation % (product_name) \
           + time_span_condation1 + time_span_condation2 % (date_start, date_end) \
           + ' and A.warehouse_name=B.id' \
           + ' and C.id=A.product_name' \
           + field_condation % term
    count = db.db_execute(conn, cursor, sql2)
    print(count)

    print('sql:\n', sql)
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
                'p_id': result[i][8],
                'correct': result[i][9]
            })
    print("result:\n", result)
    data = {
        "dataList": data_,
        "pageCount": int(count[0][0])
    }

    return resultmsg(200, '', data, '')


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    添加用户
    :return:
    """
    usernames = db.db_execute(conn, cursor, 'select username from users')
    print(usernames)
    usernames_list = []
    for i in range(len(usernames)):
        usernames_list.append(usernames[i][0])

    username = request.form['name']
    if username in usernames_list:
        return resultmsg(200, '用户名已存在！', '', '')

    password = request.form['pwd']
    right = 2
    phone = request.form['phone']
    if len(phone) != 11:
        return resultmsg(200, '手机号错误', '', '')
    realname = request.form['realname']
    data_user = (username, password, right, phone, realname)
    sql_add_user = 'insert into users(username,password,`right`,phone,realname) values ("%s","%s",%d,"%s","%s")' % data_user
    print(sql_add_user)
    result = db.db_execute(conn, cursor, sql_add_user)
    print(result)
    if len(result) == 0:
        return resultmsg(200, 'ok', result, '')
    else:
        return resultmsg(500, '服务器错误，请重新尝试！', result, '')


@app.route('/userlist', methods=['GET'])
def userlist():
    """
    查询所有的用户信息
    :return:
    """
    sql_userlist = 'select id,username,`right`,phone,realname from users'
    result = db.db_execute(conn, cursor, sql_userlist)
    print(result)
    data = []
    for i in range(len(result)):
        data.append({'id': result[i][0], 'username': result[i][1], 'right': result[i][2], 'phone': result[i][3],
                     'realname': result[i][4]})
    return resultmsg(200, 'ok', data, '')


@app.route('/del_user', methods=['POST'])
def del_user():
    """
    删除用户
    :return:
    """
    id = int(request.form['id'])
    sql_del_user = 'delete from users where id=%d' % id
    result = db.db_execute(conn, cursor, sql_del_user)
    if len(result) == 0:
        return resultmsg(200, '账号已删除！', result, '')
    else:
        return resultmsg(500, '服务器错误，请重新尝试！', result, '')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5003)
    # app.run(host='0.0.0.0', debug=True, port=5000)
