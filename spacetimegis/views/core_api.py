# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from spacetimegis import app, db
from spacetimegis.models import core
from spacetimegis.utils.logging_mixin import logger

from flask import request
from .utils import json_result

@app.route('/helloworld')
def helloworld():
    return json_result(200, 'Hello World!')


@app.route('/', methods=['GET'])
def index():
    return json_result(200, 'Hello Space Time GIS!')


@app.route('/getdbs', methods=['GET'])
def get_dbs():
    try:
        session = db.session
        databases = session.query(core.Database).all()
        res = []
        for database in databases:
            temp = dict()
            temp['name'] = database.database_name
            temp['id'] = database.id
            res.append(temp)
        session.close()
        return json_result(result=res)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(code=500, msg=str(e))


@app.route('/adddbs', methods=['POST'])
def adddbs():
    try:
        session = db.session
        dict_rep = dict(request.json)
        core.Database.import_from_dict(session=session, dict_rep=dict_rep)
        session.commit()
        session.close()
        return json_result(result=dict_rep)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(code=500, result=str(e))

@app.route('/deletedbs', methods=['DELETE'])
def deletedbs():
    try:
        id = dict(request.json).get('id')
        session = db.session
        o = session.query(core.Database).filter_by(id=id).first()
        session.delete(o)
        session.commit()
        session.close()
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(code=500, result=str(e), msg='failue')
    return json_result(result=None)