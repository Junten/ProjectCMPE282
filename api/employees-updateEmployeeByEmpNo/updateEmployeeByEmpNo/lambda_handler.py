#! /usr/bin/env python
import os
import sys
import json
import pymysql
import datetime
import rds_config

def updateEmployeeByEmpNo(event, context):
    if not event["email"]:
        return {"Message": "No email parameter!"}

    mTimeZone = datetime.timezone(datetime.timedelta(hours=-7))
    mNow = datetime.datetime.now(mTimeZone)    
    mToday = mNow.strftime("%Y-%m-%d")

    email = event["email"]  
    connection = pymysql.connect(host=rds_config.db_hostname,
                                     user=rds_config.db_username,
                                     password=rds_config.db_password,
                                     db=rds_config.db_dbname,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
    
    try: 
        if "department" in event: 
      
            department = event["department"]                          
            with connection.cursor() as cursor:
                sql = "SELECT emp_no FROM employees WHERE email=%s"
                cursor.execute(sql, (email,))
                empNo = cursor.fetchone();
                if not empNo:
                    return {"Message": "User not Found???"}
                
                sqlDeptEmp = "SELECT deptEmp.emp_no, \
                                deptEmp.dept_no \
                                FROM dept_emp deptEmp \
                                WHERE to_date='9999-01-01' AND \
                                deptEmp.emp_no=(SELECT emp.emp_no FROM employees emp WHERE emp.email=%s);"
                cursor.execute(sqlDeptEmp, (email,))
                deptEmp = cursor.fetchone();
                empNo = deptEmp["emp_no"]
                
                sqlDeptEmp = "UPDATE dept_emp SET to_date = %s WHERE emp_no=%s AND to_date='9999-01-01';"
                cursor.execute(sqlDeptEmp, (mToday, empNo, ));
                
                sqlDeptEmp = "SELECT dept_no FROM departments WHERE dept_name=%s;"
                cursor.execute(sqlDeptEmp, (department,))
                dept = cursor.fetchone();

                if not dept:
                    return {"Message": "Department not Found"}

                deptNo = dept["dept_no"]
                sqlDeptEmp = "INSERT INTO dept_emp \
                                (emp_no, \
                                dept_no, \
                                from_date, \
                                to_date) \
                                VALUES (%s, %s, %s, %s);"
                cursor.execute(sqlDeptEmp, (empNo, deptNo, mToday, '9999-01-01', ))

                connection.commit()
        
        if "title" in event:
            title = event["title"]
            with connection.cursor() as cursor:
                sqlTitle = "SELECT Emp.emp_no FROM employees Emp WHERE Emp.email=%s"
                cursor.execute(sqlTitle, (email,))
                empNo = cursor.fetchone();
                if not empNo:
                    return {"Message": "User not Found"}

                sqlTitle = "UPDATE titles T SET T.to_date=%s WHERE T.emp_no=%s AND T.to_date='9999-01-01';"
                cursor.execute(sqlTitle, (mToday, empNo['emp_no'], ))
            
                sqlTitle = "INSERT INTO titles (emp_no, title, from_date, to_date) VALUES (%s, %s, %s, %s);"
                cursor.execute(sqlTitle, (empNo['emp_no'], title, mToday, '9999-01-01', ))
                
                connection.commit()

        if "salary" in event:
            salary = event["salary"]

            with connection.cursor() as cursor:
                sqlSalary = "SELECT emp_no FROM employees WHERE email=%s"
                cursor.execute(sqlSalary, (email,))
                empNo = cursor.fetchone();
                if not empNo:
                    return {"Message": "User not Found"}
                
                sqlSalary = "UPDATE salaries SET to_date=%s WHERE emp_no=%s AND to_date=%s;"
                cursor.execute(sqlSalary, (mToday, empNo['emp_no'], '9999-01-01', ))

                sqlSalary = "INSERT INTO salaries (emp_no, salary, from_date, to_date) VALUES (%s, %s, %s, %s);"
                cursor.execute(sqlSalary, (empNo['emp_no'], salary, mToday, '9999-01-01', ))

                connection.commit();
    except:
        sys.exit() 
    finally:
        connection.close()

    return {"Message": "Update Successfully"}
