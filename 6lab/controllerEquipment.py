from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST employee

@app.route('/equipment/post/', methods=["GET", "POST"])
def create_equipment():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment/post/')
        name = request.form.get('name')

        if not name:
            print('there is no name')
            flash('Name of equipment is required')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('INSERT INTO equipment (name) VALUES (%s)',
                             [name])
                conn.commit()
            return render_template('equipment/equipment_post.html', data='New equipment was created')

    logger.debug('GET REQUEST FROM /equipment/post/')
    return render_template('equipment/equipment_post.html')


# GET all employees

@app.route('/equipment/', methods=["GET"])
def get_all_equipment():
    logger.debug('GET REQUEST FROM /equipment/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM equipment')
        all_equipment = curs.fetchall()
    return render_template('equipment/equipment.html', data=all_equipment)


# GET chosen employee

@app.route('/equipment/get_equipment/', methods=["GET", "POST"])
def get_one_equipment():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment/get_equipment/')

        equipment_id = request.form.get('id')

        if not equipment_id:
            print('there is no equipment id')
            flash('there is no equipment id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM equipment WHERE id = ' + str(equipment_id))
                equipment = curs.fetchone()
                if not equipment:
                    equipment = 'There is no equipment with this id'
            return render_template('equipment/get_equipment.html', data=equipment)

    logger.debug('GET REQUEST FROM /equipment/get_equipment/')
    return render_template('equipment/get_equipment.html')


# PUT chosen employee

@app.route('/equipment/update_equipment/', methods=["GET", "POST"])
def update_equipment():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /employees/delete_employee/')

        equipment_id = request.form.get('id')
        name = request.form.get('name')

        cursor = conn.cursor()

        if not name:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        else:
            with cursor as curs:
                curs.execute('UPDATE equipment SET name = %s WHERE id = %s',
                             [name, equipment_id])
                conn.commit()
            return render_template('equipment/update_equipment.html')

    logger.debug('GET REQUEST FROM equipment/update_equipment/')
    return render_template('equipment/update_equipment.html')


# DELETE chosen employee

@app.route('/equipment/delete_equipment/', methods=["GET", "POST"])
def delete_equipment():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment/delete_equipment/')
        employee_id = request.form.get('id')

        if not employee_id:
            print('there is no employee id')
            flash('there is no employee id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM equipment WHERE id = ' + str(employee_id))
                conn.commit()
        return redirect('equipment/delete_equipment/')

    logger.debug('GET REQUEST FROM /equipment/delete_equipment/')
    return render_template('equipment/delete_equipment.html')
