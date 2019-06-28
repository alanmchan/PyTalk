import pymysql

class DBManager:
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root','123456','test', charset='utf8')
        self.cursor = self.conn.cursor()

    def do_login(self, name, pwd):
        sql = "select * from users where name='%s' and pwd='%s'" % (name, pwd)
        # 执行查询
        self.cursor.execute(sql)
        result = self.cursor.fetchall()  # result = (('zhangsan', '123456'),)
        # print(result)
        if not result:
            result = "用户名或密码不正确"
        else:
            result = 'OK'
        return result

    def do_register(self, name, pwd):
        sql = "insert into users values('%s', '%s')" % (name, pwd)
        # 执行SQL语句
        try:
            self.cursor.execute(sql)  # 返回值为影响的条数，在此即为1
            self.conn.commit()
            return 'OK'
        except:
            self.conn.rollback()
            return '用户名已存在'


if __name__ == '__main__':
    db = DBManager()
    re = db.do_register('lisi', '123456')
    print(re)