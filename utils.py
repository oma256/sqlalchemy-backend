import json
from copy import copy
import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import Flask, Response
from flask_migrate import Migrate
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    return app


def init_app(app):
    db.init_app(app)
    Migrate(app, db)


def json_response(data):
    return Response(
        json.dumps(data, cls=JSONEncoderCore),
        mimetype='application/json; charset=utf-8',
    )

def orm_to_json(orm):
    if not orm:
        return None
    if isinstance(orm, list):
        ret = []
        for o in orm:
            if hasattr(o, '__dict__'):
                d = copy(o.__dict__)
            else:
                d = o._asdict()
            d.pop('_sa_instance_state', None)
            ret.append(d)
        return ret
    else:
        if hasattr(orm, '__dict__'):
            d = copy(orm.__dict__)
        else:
            d = orm._asdict()
        d.pop('_sa_instance_state', None)
        return d


class JSONEncoderCore(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = str(o)[:19]
            return r
        elif isinstance(o, datetime.date):
            return str(o)
        elif isinstance(o, datetime.time):
            r = str(o)
            return r
        elif isinstance(o, datetime.timedelta):
            return o.total_seconds()
        elif isinstance(o.__class__, DeclarativeMeta):
            return orm_to_json(o)
        else:
            return super(JSONEncoderCore, self).default(o)