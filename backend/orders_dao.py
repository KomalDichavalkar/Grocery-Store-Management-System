from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO grocery_store.orders "
                   "(cname, total, datetime)"
                   "VALUES (%s, %s, %s)")
    order_data = (order['cname'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO grocery_store.order_details "
                           "(order_id, pid, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['pid']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id


def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from grocery_store.order_details where order_id = %s"


    query = """
        SELECT 
            grocery_store.order_details.order_id, 
            grocery_store.order_details.quantity, 
            grocery_store.order_details.total_price, 
            grocery_store.products.pname, 
            grocery_store.products.price_per_unit 
        FROM 
            grocery_store.order_details 
        LEFT JOIN 
            grocery_store.products 
        ON 
            grocery_store.order_details.pid = grocery_store.products.pid 
        WHERE 
            grocery_store.order_details.order_id = %s
    """

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, pname, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'pname': pname,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records


def get_all_orders(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM grocery_store.orders"
    cursor.execute(query)
    response = []
    for (order_id, cname, total, datetime) in cursor:
        response.append({
            'order_id': order_id,
            'cname': cname,
            'total': total,
            'datetime': datetime,
        })
    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])
    return response


if __name__=='__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(insert_order(connection,{
    #     'cname': 'codebasics',
    #     'total': '500',
    #     'order_details':[
    #         {
    #                      'pid': 1,
    #                      'quantity': 2,
    #                      'total_price': 50
    #                  },
    #                  {
    #                      'pid': 3,
    #                      'quantity': 1,
    #                      'total_price': 30
    #                  }
    #     ]
    # }))






