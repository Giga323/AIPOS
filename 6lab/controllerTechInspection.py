from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST employee

@app.route('/tech_inspection/post/', methods=["GET", "POST"])
def create_tech_inspection():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_inspection/post/')

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
                curs.execute('INSERT INTO tech_inspection (cause, result, data, equipmentid, employee_id)'
                             ' VALUES (%s, %s, %s, %s, %s)',
                             [cause, result, data, employee_id, equipment_id])
                conn.commit()
            return render_template('tech_inspection/tech_inspection_post.html', data='New tech inspection was created')

    logger.debug('GET REQUEST FROM /tech_inspection/post/')
    return render_template('tech_inspection/tech_inspection_post.html')


# GET all employees

@app.route('/tech_inspection/', methods=["GET"])
def get_all_tech_inspections():
    logger.debug('POST REQUEST FROM /tech_inspection/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM tech_inspection')
        all_tech_inspection = curs.fetchall()
    return render_template('tech_inspection/tech_inspection.html', data=all_tech_inspection)


# GET chosen employee

@app.route('/tech_inspection/get_tech_inspection/', methods=["GET", "POST"])
def get_one_tech_inspection():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_inspection/get_tech_inspection/')

        tech_inspection_id = request.form.get('tech_inspection_id')

        if not tech_inspection_id:
            print('there is no tech inspection id')
            flash('there is no tech inspection id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM tech_inspection WHERE id = ' + str(tech_inspection_id))
                tech_inspection = curs.fetchone()
                if not tech_inspection:
                    tech_inspection = 'There is no tech inspection with this id'
            return render_template('tech_inspection/get_tech_inspection.html', data=tech_inspection)

    logger.debug('GET REQUEST FROM /tech_inspection/get_tech_inspection/')
    return render_template('tech_inspection/get_tech_inspection.html')


# PUT chosen employee

@app.route('/tech_inspection/update_tech_inspection/', methods=["GET", "POST"])
def update_tech_inspection():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_inspection/update_tech_inspection/')

        tech_failure_id = request.form.get('tech_failure_id')
        cause = request.form.get('cause')
        result = request.form.get('result')
        data = request.form.get('data')
        employee_id = request.form.get('employee_id')
        equipment_id = request.form.get('equipment_id')

        name_values = ['cause', 'result', 'data', 'employee_id', 'equipmentid']
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
                        return redirect(url_for('tech_inspection/update_tech_inspection'))

    logger.debug('GET REQUEST FROM /tech_inspection/update_tech_inspection/')
    return render_template('tech_inspection/update_tech_inspection.html')


# DELETE chosen employee

@app.route('/tech_inspection/delete_tech_inspection/', methods=["GET", "POST"])
def delete_tech_inspection():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /tech_inspection/delete_tech_inspection/')
        tech_failure_id = request.form.get('id')

        if not tech_failure_id:
            print('there is no tech failure id')
            flash('there is no tech failure id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM tech_inspection WHERE id = ' + str(tech_failure_id))
                conn.commit()
        return redirect(url_for('tech_inspection/delete_tech_inspection'))

    logger.debug('POST REQUEST FROM /tech_inspection/delete_tech_inspection/')
    return render_template('tech_inspection/delete_tech_inspection.html')
