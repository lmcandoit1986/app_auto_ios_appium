#!/usr/bin/python3
# -* - coding: UTF-8 -* -

import pymysql

def sqlexc(sqlstr):

    # 打开数据库连接
    db = connect()

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    # sqlstr = 'select code from CZB.czb_mobile_captcha order by -id limit 1;'
    cursor.execute(sqlstr)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    # 关闭数据库连接
    cursor.close()
    db.close()
    if data:
        return data[0]
    else:
        return data

def sqlexcFetchAll(sqlstr):
    db = connect()
    cursor = db.cursor()
    cursor.execute(sqlstr)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    res = []
    for lines in data:
        # for line in lines:
        #     res.append(line)
        res.append(lines)
    return res

def sqlexcedit(sqlstr):
    # 打开数据库连接
    db = connect()

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    # sqlstr = 'select code from CZB.czb_mobile_captcha order by -id limit 1;'
    try:
        cursor.execute(sqlstr)
        db.commit()
    except:
        db.rollback()
    finally:
        cursor.close()
        db.close()

def connect():
    return pymysql.connect("10.211.4.108", "dev", "ycjf_2018", "CZB")

def delLoginLog(phone):
    selectUerIDsqlStr = 'select user_id from CZB.czb_user where phone in ("{0}")'.format(phone)
    userid = sqlexc(selectUerIDsqlStr)
    delSqlStr = 'delete from CZB.czb_security_log_login where user_id in("{0}")'.format(userid)
    sqlexcedit(delSqlStr)