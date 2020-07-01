import MySQLdb
from sqlalchemy import types, create_engine

# MySQL Connection
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'asipong123456'
MYSQL_HOST_IP = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'gisweb'


engine = create_engine('mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST_IP + ':' + str(
    MYSQL_PORT) + '/' + MYSQL_DATABASE+'?charset=utf8', echo=False)

con = MySQLdb.connect(user=MYSQL_USER, passwd=MYSQL_PASSWORD, host=MYSQL_HOST_IP, db=MYSQL_DATABASE, auth_plugin='mysql_native_password')
