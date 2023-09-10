import os
import pymysql.cursors

class MySQLConnection:
    def __init__(self,db):
        connection = pymysql.connect(host=os.environ["MYSQL_HOST"],
                                    user = os.environ["MYSQL_USER"],
                                    password=os.environ["MYSQL_PASSWORD"],
                                    db=db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                #spits out a string, that mogrifies the template & data into a string
                #binary data can NOT be represented as a string
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                    #any method with an insert will give the new available row's ID
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return ((False,))
            finally:
                self.connection.close()
def connectToMySQL(db):
    return MySQLConnection(db)
#this creates an instance and needs db to be passed through
