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