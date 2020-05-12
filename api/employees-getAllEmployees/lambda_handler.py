#! /usr/bin/env python
import os
import sys
import pymysql
import rds_config

def getAllEmployees(event, context):
    employeesList = []
    return_result =[]
    connection = pymysql.connect(host=rds_config.db_hostname,
                                     user=rds_config.db_username,
                                     password=rds_config.db_password,
                                     db=rds_config.db_dbname,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    try: 
        with connection.cursor() as cursor:
            sqlSize = "SELECT COUNT(*) AS count FROM employees;"
            cursor.execute(sqlSize)
            size = cursor.fetchone()
        
            for i in range(0, size["count"], 1000):
                sqlEmployees = "SELECT emp_no, email, first_name, last_name FROM employees LIMIT %s, %s;"
                cursor.execute(sqlEmployees, (i, 1000, ))
                employees = cursor.fetchall()
                employeesList += employees
    except:
        sys.exit() 
        
    finally:
        connection.close()
            
    return employeesList

