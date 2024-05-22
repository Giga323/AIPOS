from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST employee

@app.route('/tech_failure/post/', methods=["GET", "POST"])
def create_tech_failure():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_failure/post/')

        cause = request.form.get('cause')
        result = request.form.get('result')
        data = request.form.get('data')
        employee_id = request.form.get('employee_id')
        equipment_id = request.form.get('equipment_id')

        if not cause:
            print('not cause')
            flash('Cause is required')
        elif not result:
            print('not result')
            flash('Result is required')
        elif not data:
            print('not data')
            flash('Data is required')
        elif not employee_id:
            print('Not employee id')
            flash('Employee id is required')
        elif not equipment_id:
            print('not equipment id')
            flash('Equipment id is required')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('INSERT INTO tech_failure (cause, result, data, employeeid, equipmentid)'
                             ' VALUES (%s, %s, %s, %s, %s)',
                             [cause, result, data, employee_id, equipment_id])
                conn.commit()
            return render_template('tech_failure/tech_failure_post.html', data='New tech failure was created')

    logger.debug('GET REQUEST FROM /tech_failure/tech_failure_post/')
    return render_template('tech_failure/tech_failure_post.html')


# GET all employees

@app.route('/tech_failure/', methods=["GET"])
def get_all_tech_failure():
    logger.debug('GET REQUEST FROM /tech_failure/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM tech_failure')
        all_tech_failures = curs.fetchall()
    return render_template('tech_failure/tech_failure.html', data=all_tech_failures)


# GET chosen employee

@app.route('/tech_failure/get_tech_failure/', methods=["GET", "POST"])
def get_one_tech_failure():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_failure/get_tech_failure/')

        tech_failure_id = request.form.get('tech_failure_id')

        if not tech_failure_id:
            print('there is no tech failure id')
            flash('there is no tech failure id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM tech_failure WHERE id = %s', [tech_failure_id])
                tech_failure = curs.fetchone()
                if not tech_failure:
                    tech_failure = 'There is no tech failure with this id'
            return render_template('tech_failure/get_tech_failure.html', data=tech_failure)

    logger.debug('GET REQUEST FROM tech_failure/get_tech_failure.html/')
    return render_template('tech_failure/get_tech_failure.html')


# PUT chosen employee

@app.route('/tech_failure/update_tech_failure/', methods=["GET", "POST"])
def update_tech_failure():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM tech_failure/update_tech_failure.html/')

        tech_failure_id = request.form.get('tech_failure_id')
        cause = request.form.get('cause')
        result = request.form.get('result')
        data = request.form.get('data')
        employee_id = request.form.get('employeeid')
        cursor = conn.cursor()
        with cursor as curs:
            equipment_id = curs.execute('SELECT * FROM tech_failure WHERE tech_failure.employeeid = %s',
                                        [employee_id])
            conn.commit()

        name_values = ['cause', 'result', 'data', 'employeeid', 'equipmentid']
        values = [cause, result, data, employee_id, equipment_id]

        if not cause and not result and not data and not employee_id and not equipment_id:
            print('You need to fill at least one window')
            flash('You need to fill at least one window')
        else:
            i = 0
            for value in values:
                if not value:
                    i = i + 1
                else:
                    cursor = conn.cursor()
                    with cursor as curs:
                        curs.execute(f'UPDATE tech_failure SET {name_values[i]} = %s WHERE id = %s',
                                     [value, tech_failure_id])
                        conn.commit()
                        return render_template('tech_failure/update_tech_failure.html')

    logger.debug('GET REQUEST FROM tech_failure/update_tech_failure/')
    return render_template('tech_failure/update_tech_failure.html')


# DELETE chosen employee

@app.route('/tech_failure/delete_tech_failure/', methods=["GET", "POST"])
def delete_tech_failure():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM tech_failure/delete_tech_failure/')

        tech_failure_id = request.form.get('tech_failure_id')

        if not tech_failure_id:
            print('there is no tech failure id')
            flash('there is no tech failure id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM tech_failure WHERE id = ' + str(tech_failure_id))
                conn.commit()
        return render_template('tech_failure/delete_tech_failure.html')

    logger.debug('GET REQUEST FROM tech_failure/delete_tech_request/')
    return render_template('tech_failure/delete_tech_failure.html')
