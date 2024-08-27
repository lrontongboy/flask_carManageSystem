from flask import Flask
import mysql.connector as connector
from datetime import datetime
from config import db_config
import hashlib
import os

# 管理员工号
id_card = 2
# 管理员姓名
name = 'admin'
# 管理员密码
password = '123456'
real_name = 'admin'
address = 'address'


# 生成密码哈希
def generate_password_hash(password):
    salt = os.urandom(16)
    hash_obj = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt.hex() + hash_obj



# 连接数据库
conn = connector.connect(**db_config)
cursor = conn.cursor()

# 插入数据的SQL语句
sql = 'INSERT INTO `users` (`id`, `username`, `password`, `real_name`, `date_of_birth`, `address`, `is_admin`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
val = (id_card, name, generate_password_hash(password), real_name, datetime.now(), address, 1)

# 执行SQL语句
cursor.execute(sql, val)
conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()