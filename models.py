from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)

    def __init__(self, pname, email):
        self.name = pname
        self.email = email


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(512))


    def __init__(self, title, description):
        self.title = title
        self.description = description


class PeoplePosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))
    position_id = db.Column(db.Integer, db.ForeignKey(Position.id))
