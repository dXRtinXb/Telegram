import mysql.connector
from Api_id_key import *
from DDL import *

def insert_customer_data( CID , FIRST_NAME, LAST_NAME=None):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO CUSTOMER (CID , FIRST_NAME, LAST_NAME) VALUES (%s, %s, %s)"
    cursor.execute(SQL_QUERY, (CID , FIRST_NAME, LAST_NAME))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'customer "{FIRST_NAME}" data inserted successfully with id: {CID}')

def insert_product_data(NAME , DESCRIPTION =None , PRICE = None , INVENTORY = None , MID = None , PRODUCT_CAPTION = None) :
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO PRODUCT ( NAME , DESCRIPTION  , PRICE , INVENTORY , MID , PRODUCT_CAPTION) VALUES (%s , %s , %s , %s , %s , %s )"
    cursor.execute(SQL_QUERY , (NAME ,DESCRIPTION , PRICE, INVENTORY , MID , PRODUCT_CAPTION ))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'product "{NAME}" inserted successfully')

def insert_category( CATEGORY_NAME, CATEGORY_INFO = None):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO CATEGORY (CATEGORY_NAME, CATEGORY_INFO ) VALUES (%s, %s)"
    cursor.execute(SQL_QUERY, ( CATEGORY_NAME, CATEGORY_INFO))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'category "{CATEGORY_NAME}" inserted successfully')

def insert_sale(CID):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO SALE (CUST_ID) VALUES (%s)"
    cursor.execute(SQL_QUERY , (CID,) )
    conn.commit()
    cursor.close()
    conn.close()
    print(f'sale "{CID}" inserted successfully')

def insert_SALE_ROW_data( PRODUCT_ID , QUANTITY ,SALE_ID):
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    SQL_QUERY = "INSERT INTO SALE_ROW (PRODUCT_ID , QUANTITY ,SALE_ID) VALUES (%s, %s, %s)"
    cursor.execute(SQL_QUERY, (PRODUCT_ID , QUANTITY ,SALE_ID ,  ))
    conn.commit()
    cursor.close()
    conn.close()
    print(f'SALE ROW  data inserted successfully')


if __name__ == "__main__":
    insert_customer_data(546456685, "test")
    insert_product_data( 'test' , 'TEST DESC' , 5888 , 5 , 55151498451 )
    insert_category('test')               
    insert_sale(546456685)                         
    insert_SALE_ROW_data(100 , 5 , 1)