# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import simplejson as json

from spacetimegis import db
from spacetimegis.models import core, sql_query
from spacetimegis.utils.logging_mixin import logger

from flask import request, Blueprint
from .utils import json_result, json_success

core_bp = Blueprint('core', __name__)

@core_bp.route('/getdbs', methods=['GET'])
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


@core_bp.route('/adddbs', methods=['POST'])
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

@core_bp.route('/deletedbs', methods=['DELETE'])
def deletedbs():
    try:
        id = dict(request.json).get('id')
        session = db.session
        o = session.query(core.Database).filter_by(id=id).first()
        session.delete(o)
        session.commit()
        session.close()
        return json_result(result=None)
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(code=500, result=str(e), msg='failue')


@core_bp.route('/executesql', methods=['GET'])
def executesql():
    try:
        uri = dict(request.json).get('uri')
        sql = dict(request.json).get('sql')
        sqlquery = sql_query.SQLQuery(uri)
        res = sqlquery.executesql(sql)
        return json_success(json.dumps(res))
    except Exception as e:
        logger.writeerrorlog(e)
        return json_result(code=500, result=str(e), msg='failue')