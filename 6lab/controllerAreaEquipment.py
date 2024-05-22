from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST equipment

@app.route('/equipment_in_area/post/', methods=["GET", "POST"])
def create_area_to_equipment():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment_in_area/post/')

        area_id = request.form.get('area_id')
        equipment_id = request.form.get('equipment_id')

        if not area_id:
            print('not area_id')
            flash('Area id is required')
        elif not equipment_id:
            print('not equipment_id')
            flash('Equipment id is required')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('INSERT INTO areaequipment (areaid, equipmentid) VALUES (%s, %s)',
                             [area_id, equipment_id])
                conn.commit()
            return render_template('/area_equipment/area_equipment_post.html', data='New relation was created')

    logger.debug('GET REQUEST FROM /equipment_in_area/post/')
    return render_template('/area_equipment/area_equipment_post.html')


# GET all equipment on area

@app.route('/equipment_in_area/', methods=["GET"])
def get_all_equipment_on_area():
    logger.debug('GET REQUEST FROM /equipment_in_area/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT production_area.*, equipment.* ' +
                        'FROM production_area ' +
                        'JOIN areaequipment ON production_area.id = areaequipment.areaid ' +
                        'JOIN equipment ON areaequipment.equipmentid = equipment.id')
        all_equipment_area = curs.fetchall()
    return render_template('area_equipment/equipmentArea.html/', data=all_equipment_area)


# GET chosen employee

@app.route('/equipment_in_area/get_equipment_by_area/', methods=["GET", "POST"])
def get_equipment_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment_in_area/get_equipment_by_area/')

        area_id = request.form.get('area_id')

        if not area_id:
            print('there is no area id')
            flash('there is no area id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM areaequipment WHERE areaid = %s', [area_id])
                equipments = curs.fetchall()
            return render_template('area_equipment/get_equipment_by_area.html', data=equipments)

    logger.debug('GET REQUEST FROM /equipment_in_area/get_equipment_by_area/')
    return render_template('area_equipment/get_equipment_by_area.html')


# PUT chosen employee

@app.route('/equipment_in_area/update_equipment_by_area/', methods=["GET", "POST"])
def update_equipment_by_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment_in_area/update_equipment_by_area/')

        area_id = request.form.get('area_id')
        equipment_id = request.form.get('equipment_name')

        cursor = conn.cursor()

        if not area_id and not equipment_id:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        elif not area_id:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        elif not equipment_id:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        else:
            with cursor as curs:
                curs.execute('UPDATE areaequipment SET equipmentid = %s WHERE areaid = %s',
                             [equipment_id, area_id])
                conn.commit()
            return redirect(url_for('area_equipment/equipmentArea/'))

    logger.debug('GET REQUEST FROM /equipment_in_area/update_equipment_by_area/')
    return render_template('area_equipment/update_equipment_by_area.html')


# DELETE chosen employee

@app.route('/equipment_in_area/delete_equipment_by_area/', methods=["GET", "POST"])
def delete_equipment_by_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /equipment_in_area/delete_equipment_by_area/')

        area_id = request.form.get('area_id')
        equipment_id = request.form.get('equipment_id')

        if not equipment_id:
            print('there is no employee id')
            flash('there is no employee id')
        elif not area_id:
            print('there is no area id')
            flash('there is no area id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM areaequipment WHERE equipmentid = %s AND areaid = %s',
                             [equipment_id, area_id])
                conn.commit()
        return render_template('area_equipment/delete_equipment_by_area.html')

    logger.debug('GET REQUEST FROM /equipment_in_area/delete_equipment_by_area/')
    return render_template('area_equipment/delete_equipment_by_area.html')
