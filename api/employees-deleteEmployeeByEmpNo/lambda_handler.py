#! /usr/bin/env python
import os
import sys
import json
import pymysql
import rds_config

def deleteEmployeeByEmpNo(event, context):
    if not event["email"]:
        return {"Message": "No Email parameter"}
        
    email = event["email"]

    connection = pymysql.connect(host=rds_config.db_hostname,
                                     user=rds_config.db_username,
                                     password=rds_config.db_password,
                                     db=rds_config.db_dbname,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
    
    try: 
        with connection.cursor() as cursor:
            sqlDelete = "DELETE FROM employees WHERE email=%s"
            cursor.execute(sqlDelete, (email,))
            connection.commit();

    except:
        sys.exit() 
    finally:
        connection.close()
    
    return {"message: ": "Delete Successfully"}
