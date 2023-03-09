from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, pname, email):
        self.name = pname
        self.email = email
