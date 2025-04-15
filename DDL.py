import mysql.connector
from Api_id_key import *

# config = {'user': 'root', 'password': 'password', 'host': 'localhost'}
# conn = mysql.connector.connect(user='root', password='password', host='localhost')
# conn = mysql.connector.connect(**config)

# cursor = conn.cursor()

# cursor.execute("DROP DATABASE IF EXISTS Store;")

# conn.close()
# cursor.close()

def drop_n_create_database(db_name):
    config = configDict
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'database {db_name} created succesfully')

def create_customer_table():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE CUSTOMER (
        CID             BIGINT UNSIGNED NOT NULL PRIMARY KEY,
        FIRST_NAME      VARCHAR(20) NOT NULL,
        LAST_NAME       VARCHAR(20),
        PHONE           VARCHAR(14),
        REGISTER_DTAE   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        LAST_UPDATE     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );""")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'customer table created succesfully')

def create_table_cat():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(''' 
    CREATE TABLE CATEGORY( ID        INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   
                    CATEGORY_NAME    VARCHAR(30) NOT NULL , 
                   
                    CATEGORY_INFO    TEXT          
                   
                   );''')
    conn.commit()
    cursor.close()
    conn.close()
    print(f'CATEGORY table created succesfully')

def create_product_table():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE PRODUCT (
        ID              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        NAME            VARCHAR(50),
        DESCRIPTION     TEXT,
        PRICE           DOUBLE(10, 2) NOT NULL,
        INVENTORY       MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
        MID             VARCHAR(150) NOT NULL,
        PRODUCT_CAPTION TEXT ,
        REGISTER_DATE   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        LAST_UPDATE     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (ID));""")
    cursor.execute("ALTER TABLE PRODUCT AUTO_INCREMENT=100")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'product table created succesfully')

def create_sale_table():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE SALE (
        ID              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        DATE            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CUST_ID         BIGINT UNSIGNED NOT NULL ,
        LAST_UPDATE     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (ID ), 
        FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER (CID)
        );""")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'sale table created succesfully')

def create_sale_row_table():
    config = configDictionary
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE SALE_ROW (
        PRODUCT_ID      BIGINT UNSIGNED NOT NULL,
        QUANTITY        SMALLINT UNSIGNED NOT NULL,
        SALE_ID         BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (PRODUCT_ID, SALE_ID),
        FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT (ID),
        FOREIGN KEY (SALE_ID) REFERENCES SALE (ID)
        );""")
    conn.commit()
    cursor.close()
    conn.close()
    print(f'sale_row table created succesfully')


if __name__ == '__main__':
    drop_n_create_database('project')
    create_customer_table()
    create_table_cat()
    create_product_table()
    create_sale_table()
    create_sale_row_table()
