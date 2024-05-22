from app import app, conn
from flask import render_template, request, flash, redirect, url_for
from app import logger


# POST employee

@app.route('/production_area/post/', methods=["GET", "POST"])
def create_production_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /production_area/post/')

        name = request.form.get('name')

        if not name:
            print('there is no name')
            flash('Name of production area is required')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('INSERT INTO production_area (name) VALUES (%s)',
                             [name])
                conn.commit()
            return render_template('production_area/production_area_post.html', data='New production area was created')

    logger.debug('GET REQUEST FROM /production_area/post/')
    return render_template('production_area/production_area_post.html')


# GET all employees

@app.route('/production_area/', methods=["GET"])
def get_all_production_areas():
    logger.debug('GET REQUEST FROM /production_area/')
    cursor = conn.cursor()
    with cursor as curs:
        curs.execute('SELECT * FROM production_area')
        all_equipment = curs.fetchall()
    return render_template('production_area/production_area.html', data=all_equipment)


# GET chosen employee

@app.route('/production_area/get_production_area/', methods=["GET", "POST"])
def get_one_production_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /production_area/get_production_area/')
        production_area_id = request.form.get('id')

        if not production_area_id:
            print('there is no production_area id')
            flash('there is no production_area id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('SELECT * FROM production_area WHERE id = %s', [production_area_id])
                production_area = curs.fetchone()
                if not production_area:
                    production_area = 'There is no production area with this id'
            return render_template('/production_area/get_production_area.html', data=production_area)

    logger.debug('GET REQUEST FROM /production_area/get_production_area/')
    return render_template('production_area/get_production_area.html')


# PUT chosen employee

@app.route('/production_area/update_production_area/', methods=["GET", "POST"])
def update_production_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /production_area/update_production_area/')
        production_area_id = request.form.get('production_area_id')
        name = request.form.get('name')

        cursor = conn.cursor()

        if not name:
            print('You need to fill the windows')
            flash('You need to fill the windows')
        else:
            with cursor as curs:
                curs.execute('UPDATE production_area SET name = %s WHERE id = %s',
                             [name, production_area_id])
                conn.commit()
            return render_template('/production_area/update_production_area.html')

    logger.debug('GET REQUEST FROM /production_area/update_production_area/')
    return render_template('production_area/update_production_area.html')


# DELETE chosen employee

@app.route('/production_area/delete_production_area/', methods=["GET", "POST"])
def delete_production_area():
    if request.method == "POST":
        logger.debug('POST REQUEST FROM /production_area/delete_production_area/')
        production_area_id = request.form.get('id')

        if not production_area_id:
            print('there is no production area id')
            flash('there is no production area id')
        else:
            cursor = conn.cursor()
            with cursor as curs:
                curs.execute('DELETE FROM production_area WHERE id = %s', [production_area_id])
                conn.commit()
        return render_template('production_area/delete_production_area.html')

    logger.debug('GET REQUEST FROM /production_area/delete_production_area/')
    return render_template('production_area/delete_production_area.html')
