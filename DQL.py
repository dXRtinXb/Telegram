import mysql.connector
from Api_id_key import *


def get_customers_data():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT CID FROM CUSTOMER;")
    result = cursor.fetchall()
    customers = [i['CID'] for i in result]
    print(customers)
    cursor.close()
    conn.close()

def get_product_data():
    
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID FROM PRODUCT ")
    result = cursor.fetchall()
    products = [i['ID'] for  i  in result]
    return (products)

def get_category_info():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID FROM CATEGORY ")
    result = cursor.fetchall()
    category  = [i['ID'] for  i  in result]
    return (category)

def get_sale_data():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID FROM SALE ;")
    result = cursor.fetchall()
    sales = [i['ID'] for i in result]
    print(sales)
    cursor.close()
    conn.close()
    return sales
def get_sale_row_data():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SALE_ID FROM SALE_ROW ;")
    result = cursor.fetchall()
    sale_ids = [i['SALE_ID'] for i in result]
    print(sale_ids)
    cursor.close()
    conn.close()
    return(sale_ids)


def custom_get_data( DATA_BASE ,  wanted  , ID):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT {wanted} FROM {DATA_BASE} WHERE ID ={ID}  ;")
    result = cursor.fetchall()
    sale_ids = [i[wanted] for i in result]
    (sale_ids)
    cursor.close()
    conn.close()


def custom_get_customer_data( wanted  , CID):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT {wanted} FROM CUSTOMER WHERE CID ={CID}  ;")
    result = cursor.fetchall()
    sale_ids = [i[wanted] for i in result]
    return(sale_ids)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get_customers_data()
    get_product_data()
    get_category_info()
    get_sale_data()
    get_sale_row_data()
