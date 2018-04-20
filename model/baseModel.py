from flaskext.mysql import MySQL
import pymysql

class baseModel(object):
    __mysql = None

    def __init__(self, app):
        self.__mysql = MySQL( cursorclass = pymysql.cursors.DictCursor )
        self.__mysql.init_app(app)
        self.__mysql.connect()
        
    def dbCoursor(self):
        return self.__mysql.get_db().cursor()