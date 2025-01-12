# import mysql.connector
from sql_connection import get_sql_connection

def get_all_products(connection):

    # cursor = cnx.cursor()
    cursor = connection.cursor()

    query = "SELECT products.pid, products.pname, products.um_id,products.price_per_unit, uom.um_name FROM grocery_store.products inner join grocery_store.uom on uom.um_id=products.um_id"

    cursor.execute(query)

    response = []
    for (pid, pname, um_id, price_per_unit, um_name) in cursor:
        response.append({
            'pid':pid,
            'pname':pname,
            'um_it':um_id,
            'price_per_unit':price_per_unit,
            'um_name':um_name
        })
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()

    query = "insert into grocery_store.products(pname, um_id, price_per_unit) values (%s, %s, %s)"
    data = (product['pname'], product['um_id'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection,pid):
    cursor = connection.cursor()
    query = "DELETE FROM grocery_store.products WHERE pid=" + str(pid)
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid



if __name__=='__main__':
    connection = get_sql_connection()
    print(delete_product(connection,7))




