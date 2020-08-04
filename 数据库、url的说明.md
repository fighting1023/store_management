# 数据库说明
## product_category 产品名录表
字段 | 含义 | 类型 | 备注 
---|---|---|---|
id |   | int | 非空，自增 | 
product_name | 产品名称 | varchar | 非空
add_product_name_date | 添加产品名称时间 | datetime | 非空
product_name_be_del  | 删除产品标记 | int | 1表示删除，0表示未删除
product_name_be_del_time | 删除产品时间 | datetime | 
batch | 批次 | varchar | 非空
size  | 规格 | varchar | 非空
mark  | 条形码 | varchar | 非空
note  | 备注  | varchar  | 

## users 用户表
字段 | 含义 | 类型 | 备注 
---|---|---|---|
id |   | int | 非空，自增
username | 用户名 | varchar | 非空
password | 密码   | varchar | 非空
righ     |        | int     | 非空权限级别
phone    | 手机号码 | varchar | 
realname | 真名   | varchar | 

## warehouse 操作记录表
字段 | 含义 | 类型 | 备注 
---|---|---|---|
id |   | int | 非空，自增
warehouse_name | 仓库编号 | int | 非空，warehouse_category中对应id
out_in | 出入库类型 | int | 非空，1入库，-1出库
product_name |   | int | 非空，product_category中对应id
num | 出入库数量 | int | 非空
operator | 操作员 | varchar | 非空
date_managed | 操作时间 | datetime | 非空
cost | 运费 | float | 非空
correct | 修正记录标记 | int | 空为非修正记录，1增加库存，-1减少库存

## warehouse_category 仓库名录表
字段 | 含义 | 类型 | 备注 
---|---|---|---|
id |   | int | 非空，自增
warehouse_name | 仓库名称 | varchar | 非空
position | 仓库位置 | varchar | 
telphone | 负责人电话 | varchar | 
master | 负责人姓名 | varchar | 

# url说明
### /login
用户登录 

### /productlist
查询产品列表（猪肉、羊肉。。。）
