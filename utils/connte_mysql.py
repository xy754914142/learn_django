import pymysql
from pymysql.cursors import DictCursor

def mysql_commit(sql,value=[]):
    '''
    提交sql语句
    :param sql: mysql语句
    :param value: 格式化mysql语句的参数，可为空
    :return: 无返回值
    '''
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='754914142', db='studentmanagementsystem')
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql,value)
    conn.commit()
    cursor.close()
    conn.close()

def mysql_result(sql,value=[]):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='754914142', db='studentmanagementsystem')
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql,value)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def mysql_fetchone(sql,value=[]):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='754914142', db='studentmanagementsystem')
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql, value)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result




class Mysql_Connet():
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='754914142',
                               db='studentmanagementsystem')
        self.cursor = self.conn.cursor(DictCursor)


    def mysql_commit(self,sql,value):

        self.cursor.execute(sql,value)
        self.conn.commit()

    def mysql_result(self, sql, value):
        self.cursor.execute(sql, value)
        result = self.cursor.fetchall()
        return result

    def mysql_fetchone(self, sql, value):
        self.cursor.execute(sql, value)
        result = self.cursor.fetchone()
        self.conn.commit()
        return result

    def mysql_commit_return_id(self,sql,value):

        self.cursor.execute(sql,value)
        self.conn.commit()
        id = self.cursor.lastrowid
        return id


    def mysql_many_commit(self,sql,value):
        self.cursor.executemany(sql,value)
        self.conn.commit()

    def mysql_colse(self):
        self.cursor.close()
        self.conn.close()



