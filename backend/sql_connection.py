from mysql.connector import connection

__conn = None
def get_sql_connection():
    global __conn
    if __conn is None:
        __conn = connection.MySQLConnection(user='root', password='Root@2025',host='localhost', database='grocery_store')

        # cnx = mysql.connector.connect(user='root', password='Root@2025',host='localhost', database='grocery_store')



        # conn.close()
    return __conn





