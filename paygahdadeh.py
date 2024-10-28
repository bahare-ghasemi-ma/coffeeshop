import sqlite3 as sdb
import tabulate
import time
import os

con = sdb.Connection("coffeeshop.db")
cur = con.cursor()

def db_connection(cmd):
    try:
        
        data = cur.execute(cmd)
        fdata = data.fetchall()
        con.commit()
        
        return fdata
    except sdb.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"General error: {e}")
        return []



def table_kala_selection():
    cmd = """SELECT kala_id,kala_name,kala_price FROM kala """
    all_data = db_connection(cmd)
    return all_data


def table_kala_insert(item_name,item_price):  
    cmd = f"""INSERT INTO kala (kala_name,kala_price) VALUES ('{item_name}','{item_price}')"""
    all_data = db_connection(cmd)
    return all_data

def table_kala_update(kala_id,kala_name,kala_price):
    cmd = f""" UPDATE kala 
    SET   kala_name  ='{kala_name}', kala_price ='{kala_price}'
    WHERE  kala_id ='{kala_id}'"""  
    all_data = db_connection(cmd)


# ///////////////مشتربان//////////////////////
def table_customer_selection():
    cmd = """SELECT * FROM customer """
    all_data = db_connection(cmd)
    return all_data

def table_customer_insert( customer_name, customer_family,customer_phone):
    cmd = f"""INSERT INTO customer (customer_name,customer_family,customer_phone) VALUES ('{customer_name}','{customer_family}','{customer_phone}')"""
    all_data = db_connection(cmd)
    return all_data


def table_customer_update(customer_id,customer_name,customer_family,customer_phone):
    cmd = f""" UPDATE customer 
    SET   customer_name  ='{customer_name}', customer_family ='{customer_family}' ,customer_phone ='{customer_phone}'
    WHERE  customer_id ='{customer_id}'"""  
    all_data = db_connection(cmd)

# //////////////////پایان مشتریان////////////////


def table_factor_selection():    
    cmd = """SELECT * FROM factor """
    all_data = db_connection(cmd)
    return all_data
   


#تابع مربوط به هدر فاکتور
def insert_into_factor(customer_id,factor_date, customer_factor_sum_price):
    cmd = f"""INSERT INTO factor (customer_id,factor_date, customer_factor_sum_price) 
VALUES ('{customer_id}','{factor_date}','{customer_factor_sum_price}'); """
    
    cmd1="""SELECT last_insert_rowid(); """
    all_data = db_connection(cmd)
    all_data = db_connection(cmd1)
    return all_data[0][0]

#  تابع مربوط به کالاهای هر فاکتور
def insert_into_kalahay_factor(factor_id,kala_id,factor_count_kala,kala_price):
    cmd = f""" INSERT INTO
      kalahay_factor (factor_id,kala_id,factor_count_kala,factor_row_price) 
      VALUES ('{factor_id}','{kala_id}','{factor_count_kala}','{factor_count_kala*kala_price}') """
    all_data = db_connection(cmd)
    return all_data


#تابع مربوط به ثبت کالاهای هر فاکتور
def enter_factor_info(customer_id,factor_date,list_kala):
    factor_id = insert_into_factor(customer_id,factor_date, 0)
    customer_factor_sum_price=0
    for item in list_kala :
        insert_into_kalahay_factor(factor_id,item[0],item[1],item[2])
        customer_factor_sum_price += item[1]*item[2] #قیمت کل هر فاکتور

    cmd = f""" UPDATE factor 
    SET customer_factor_sum_price='{customer_factor_sum_price}'  
    WHERE  factor_id ='{factor_id}'"""  
    all_data = db_connection(cmd)  
    return factor_id

# نمایش کالاهای هر فاکتور
def show_kalahay_factor_db(factor_id):
    cmd=f"""SELECT  kala.kala_name,kalahay_factor.factor_count_kala,kala.kala_price,kalahay_factor.factor_row_price
FROM kala join kalahay_factor on kala.kala_id=kalahay_factor.kala_id WHERE  kalahay_factor.factor_id ='{factor_id}' """
    all_data = db_connection(cmd)  
    return all_data



def show_top10_kala():
    cmd=f"""SELECT kalahay_factor.kala_id, kala.kala_name , count(*) as  occurrence_count 
    FROM kalahay_factor JOIN  kala on kala.kala_id=kalahay_factor.kala_id 
    GROUP BY kalahay_factor.kala_id 
    ORDER BY occurrence_count DESC 
    LIMIT 10 """
    all_data = db_connection(cmd)  
    return all_data

    
# /////////////////////////////////جستجو////////////////////////////////////

def search_customer_db(factor_date1,factor_date2,customer_name):
# جستجوی مشتری برا اساس شماره فاکتور
    cmd=f"""SELECT factor.factor_id,customer.customer_id,customer.customer_name,customer.customer_family,customer.customer_phone FROM factor 
    join customer on customer.customer_id= factor.customer_id WHERE True """
    if len(factor_date1) > 0: 
        cmd += f""" and factor.factor_date >= '{factor_date1}' """
    if len(factor_date2) > 0: 
        cmd += f""" and factor.factor_date <= '{factor_date2}' """
    if len(customer_name) > 0: 
        cmd += f""" and customer.customer_name LIKE '%{customer_name}%' """
    
    all_data = db_connection(cmd)  
    return all_data

# /////////////////////////////////جستجو/////////////////////////////


def con_close():
    con.close()
