from flask import Flask, render_template, request

from models import People, db
from utils import create_app, init_app

app = create_app()
init_app(app)


@app.route('/')
def index():
    return '<a href="/addperson"><button> Click here </button></a>'


@app.route('/addperson')
def addperson():
    return render_template('index.html')


@app.route("/personadd", methods=['POST'])
def personadd():
    pname = request.form["pname"]
    email = request.form["email"]

    entry = People(pname, email)
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")


@app.route('/people-list')
def people_list():
    peoples = db.session.query(People).all()

    return render_template('people_list.html', peoples=peoples)

if __name__ == '__main__':
    app.run()
