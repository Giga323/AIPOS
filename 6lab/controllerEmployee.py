from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST employee

@app.route('/employees/post/', methods=["GET", "POST"])
def create_employee():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /employees/post/')

        full_name = request.form.get('name')
        job_title = request.form.get('title')

        print(full_name, job_title)

        if not full_name:
            print('not full_name')
            flash('Full name is required')
        elif not job_title:
            print('not job_title')
            flash('Job title is required')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('INSERT INTO employee (full_name, job_title) VALUES (%s, %s)',
                             [full_name, job_title])
                conn.commit()
            return render_template('employee/employee_post.html', data='New employee was created')

    logger.debug('GET REQUEST FROM /employees/post/')
    return render_template('employee/employee_post.html')


@app.route('/submit/', methods=["GET"])
def submit():
    return render_template('submit.html')


# GET all employees

@app.route('/employees/', methods=["GET"])
def get_employees():
    logger.debug('GET REQUEST FROM /employees/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM employee')
        all_employees = curs.fetchall()
    return render_template('employee/employees.html', data=all_employees)


# GET chosen employee

@app.route('/employees/get_employee/', methods=["GET", "POST"])
def get_employee():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /employees/get_employee/')
        employee_id = request.form.get('id')

        if not employee_id:
            print('there is no employee id')
            flash('there is no employee id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM employee WHERE id = ' + str(employee_id))
                employee = curs.fetchone()
                if not employee:
                    employee = 'There is no employee with this id'
            return render_template('employee/employee_id.html', data=employee)

    logger.debug('GET REQUEST FROM /employees/get_employee/')
    return render_template('employee/employee_id.html')


# PUT chosen employee

@app.route('/employees/update_employee/', methods=["GET", "POST"])
def update_employee():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /employees/update_employee/')
        employee_id = request.form.get('id')
        full_name = request.form.get('name')
        job_title = request.form.get('title')

        cursor = conn.cursor()

        if not full_name and not job_title:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        elif not full_name:
            with cursor as curs:
                curs.execute('UPDATE employee SET job_title = %s WHERE id = %s', [job_title, employee_id])
                conn.commit()
            return redirect(url_for('employee/update_employee'))
        elif not job_title:
            with cursor as curs:
                curs.execute('UPDATE employee SET full_name = %s WHERE id = %s', [full_name, employee_id])
                conn.commit()
            return redirect(url_for('employee/update_employee'))
        else:
            with cursor as curs:
                curs.execute('UPDATE employee SET job_title = %s, full_name = %s WHERE id = %s',
                             [job_title, full_name, employee_id])
                conn.commit()
            return render_template('employee/update_employee.html')

    logger.debug('GET REQUEST FROM /employee/update_employee/')
    return render_template('employee/update_employee.html')


# DELETE chosen employee

@app.route('/employees/delete_employee/', methods=["GET", "POST"])
def delete_employee():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /employees/delete_employee/')
        employee_id = request.form.get('id')

        if not employee_id:
            print('there is no employee id')
            flash('there is no employee id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM employee WHERE id = ' + str(employee_id))
                conn.commit()
        return render_template('employee/delete_employee.html')

    logger.debug('GET REQUEST FROM /employees/delete_employee/')
    return render_template('employee/delete_employee.html')
