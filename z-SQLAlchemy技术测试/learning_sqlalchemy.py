from sqlalchemy import Column,String,INT,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象基类
Base = declarative_base()

# 定义User对象
class User(Base):
    # 表名字：
    __tablename__ = 'user'

    # 表结构
    id = Column(INT,primary_key=True)
    name = Column(String(20))
    password = Column(String(256))

# 初始化数据库连接
# engine = create_engine('mysql + store_management://stroe_manager.stroe_manager@47.105.91.77:5000/store_managemgnt')
engine = create_engine('mysql + mysqlconnector://stroe_manager.stroe_manager@47.105.91.77:5000/store_managemgnt')
DBSession = sessionmaker(bind=engine)

# 创建session对象：
session = DBSession()
