import json
from flask import Flask
from logger import logger
from connect_to_database import ConnectDataBase

NAME = 'equipment_failure'
USER = 'postgres'
PASSWORD = 'Justice32252bb'
HOST = 'localhost'

app = Flask(__name__)
app.secret_key = '123451234554321'
db = ConnectDataBase(NAME, USER, PASSWORD, HOST)
conn = db.connect_to_database()

from controllerEmployee import *
from controllerAreaEquipment import *
from homepage import *
from controllerEquipment import *
from controllerProductionArea import *
from controllerTechFailure import *
from controllerTechInspection import *


if __name__ == "__main__":
    logger.debug('SERVER START')

    app.config["DEBUG"] = True
    app.run(debug=True)


