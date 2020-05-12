#! /usr/bin/env python
import os
import sys
import json
import pymysql

import rds_config

def getEmployeeByEmail(event, context):
    if not event["email"]:
        return {"Message": "No email parameter"}
        
    email = event["email"]
    employee = {}
    salaryList = []
    departmentList = []
    titleList = []
    try: 
        connection = pymysql.connect(host=rds_config.db_hostname,
                                     user=rds_config.db_username,
                                     password=rds_config.db_password,
                                     db=rds_config.db_dbname,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            sqlEmployee = "SELECT emp.emp_no, \
                                  emp.email, \
                                  emp.first_name, \
                                  emp.last_name, \
                                  emp.birth_date, \
                                  emp.gender, \
                                  emp.hire_date, \
                                  sal.salary, \
                                  sal.from_date, \
                                  sal.to_date \
                          FROM employees emp \
                          INNER JOIN salaries sal ON (emp.emp_no=%s \
                                                   AND emp.emp_no=sal.emp_no);"
            cursor.execute(sqlEmployee, (email,))
            employees = cursor.fetchall()
        
            if not employees:
                return {"message": "No record found"}
            
            emp_no = employees[0]["emp_no"]
            employee["emp_no"] = employees[0]["emp_no"]
            employee["email"] = employees[0]["email"]
            employee["first_name"] = employees[0]["first_name"]
            employee["last_name"] = employees[0]["last_name"]
            employee["birth_date"] = employees[0]["birth_date"].isoformat()
            employee["gender"] = employees[0]["gender"]
            employee["hire_date"] = employees[0]["hire_date"].isoformat()
            for emp in employees:
                salaryDict = {}
                salaryDict["salary"] = emp["salary"]
                salaryDict["from_date"] = emp["from_date"].isoformat()
                salaryDict["to_date"] = emp["to_date"].isoformat()
                salaryList.append(salaryDict)
            employee["salaries"] = salaryList
        
            sqlDepartment = "SELECT dept.dept_no, \
                                    dept.dept_name, \
                                    deptEmp.from_date, \
                                    deptEmp.to_date \
                             FROM departments dept \
                             INNER JOIN dept_emp deptEmp ON (deptEmp.emp_no=%s \
                                                         AND deptEmp.dept_no=dept.dept_no);"
            cursor.execute(sqlDepartment, (emp_no,))
            departments = cursor.fetchall()
        
            sqlDeptManager = "SELECT emp.emp_no,\
                                     emp.first_name,\
                                     emp.last_name, \
                                     emp.email, \
                                     detpManager.from_date, \
                                     detpManager.to_date \
                              FROM dept_manager detpManager \
                              INNER JOIN employees emp ON (detpManager.emp_no=emp.emp_no \
                                                       AND detpManager.dept_no=%s);"
            for department in departments:
                dept_no = department["dept_no"]
                department["from_date"] = department["from_date"].isoformat()
                department["to_date"] = department["to_date"].isoformat()
                cursor.execute(sqlDeptManager, (dept_no,))
                deptManagers = cursor.fetchall()
                for deptManager in deptManagers:
                    deptManager["from_date"] = deptManager["from_date"].isoformat()
                    deptManager["to_date"] = deptManager["to_date"].isoformat()
                department["dept_manager"] = deptManagers
                departmentList.append(department)
            employee["departments"] = departmentList
        
            sqlTitle = "SELECT title, from_date, to_date FROM titles WHERE emp_no=%s"
            cursor.execute(sqlTitle, (emp_no,))
            titles = cursor.fetchall()
            for title in titles:
                title["from_date"] = title["from_date"].isoformat()
                title["to_date"] = title["to_date"].isoformat()
                titleList.append(title)
            employee["title"] = titleList
    except:
        sys.exit() 
    finally:
        connection.close()
    
    return employee 