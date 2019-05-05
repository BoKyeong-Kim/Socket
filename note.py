import pymysql.cursors

def sql(name):
        connection = pymysql.connect(host='localhost', user='root', password='0331', db='network')
        cursor = connection.cursor()
        sql = 'insert into login(nickname) values(%s)'
        cursor.execute(sql, name)
        sql1 = 'select * from login'
        cursor.execute(sql1)
        connection.commit()
        data = cursor.fetchall()
        print(data)
