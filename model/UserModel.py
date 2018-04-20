from .baseModel import baseModel

class UserModel(object):
    __cursor = None

    def __init__(self, app):
        # self.mysql = MySQL( cursorclass = pymysql.cursors.DictCursor )
        # self.mysql.init_app(app)
        # self.mysql.connect()
        # self.__cursor = self.mysql.get_db().cursor()
        dbObj = baseModel(app)
        self.__cursor = dbObj.dbCoursor()


    def user_list(self):
        import random
        fields = 'id uid,cellphone,nickname,sex,age,sign,user_type,init_time'
        sql = 'select %s from qy_user limit %d, 3' % (fields, random.choice(range(1, 90000)))
        self.__cursor.execute(sql)
        # executemany()方法可以一次插入多条值，执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数。
        return self.__cursor.fetchall()
        # __mysql = MySQL( cursorclass = pymysql.cursors.DictCursor )
        # __mysql.init_app(app)
        # cursor = __mysql.get_db().cursor()
        # cursor.execute('select id uid,cellphone,nickname,sex,age,sign,user_type,init_time from qy_user limit 3')
        # # executemany()方法可以一次插入多条值，执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数。
        # data = cursor.fetchall()
        # rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。

        # sqli="insert into student values(%s,%s,%s,%s)"
        # cursor.execute(sqli,('3','Huhu','2 year 1 class','7'))

        # sqli="insert into student values(%s,%s,%s,%s)"
        # cur.executemany(sqli,[
        #     ('3','Tom','1 year 1 class','6'),
        #     ('3','Jack','2 year 1 class','7'),
        #     ('3','Yaheng','2 year 2 class','7'),
        #     ])

    def buy_grab(self, neededArgs):
        return 4156468485
        # pass
