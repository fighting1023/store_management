import pymysql
from setting import MYSQL_DATABASE,MYSQL_USER,MYSQL_PORT,MYSQL_HOST,MYSQL_PASSWORD
from pymysql import connect
from pymysql.cursors import DictCursor


def db_execute(conn,cursor,sql):
    # print('执行sql语句')
    try:
        res1 = cursor.execute(sql)
        # print("执行语句后的返回值:",res1)
        res2 = conn.commit()
        # print('commit的返回值:',res2)
        result = cursor.fetchall()
        # print("fetchall的返回值:",result)
        return result
    except:
        conn.rollback()


# class Store_management(object):
#     def __init__(self):
#         self.conn = connect(
#             host = MYSQL_HOST,
#             port = MYSQL_PORT,
#             user = MYSQL_USER,
#             password = MYSQL_PASSWORD,
#             database = MYSQL_DATABASE,
#             charset = 'utf8'
#         )
#         self.cursor = self.conn.cursor(DictCursor)
#
#     def __del__(self):
#         self.cursor.close()
#         self.conn.close()
#
#     def account_check(self,username,password):
#         # current_login_info = {'username':username,'password':password}
#         sql = 'select username,password,"right" from users where username="%s" and password="%s"'%(username,password)
#         # sql = 'select username,password from users where username="%s"'%(username)
#         self.cursor.execute(sql)
#         return self.cursor.fetchall()
#
#     # def select_keyword(self,warehouse_name,out_in,product_name,num,operator,datetime,cost):
#     def select_keyword(self,warehouse_name,out_in,product_name,num,operator,datetime,cost):
#
#         """
#         按照单个字段进行查询
#
#         假设前端的变量为 house\out\prod\number\people\time\expence
#
#         id
#         warehouse_name:仓库名
#                 out_in:出入(操作类型)
#           product_name:产品名
#                    num:数量
#               operator:操作员
#               datetime:日期
#                   cost:成本
#         """
#
#         var_names =        [warehouse_name,    out_in,   product_name,   num,      operator,   datetime,   cost]
#         var_names_string = ['warehouse_name', 'out_in', 'product_name', 'num',    'operator', 'datetime', 'cost']
#         front_name =       ['house',          'out',    'prod',         'number', 'people',   'time',     'expence' ]
#         tuples = []
#
#
#         for i in range(len(var_names)):
#             if var_names[i] == front_name[i]:
#                 tuples+[var_names_string[i],front_name[i]]
#
#
#         # sql1 = 'select count(*) from store_management'
#         sql2 = 'select * from store_management where "%s"="%s"'+'and "%s"="%s"'*len(tuples)/2%tuple(tuples)
#         self.cursor.execute(sql2)
#         return self.cursor.fetchall()
