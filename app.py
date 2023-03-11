from flask import Flask, render_template, request

from models import People, db, Position, PeoplePosition
from utils import create_app, init_app

app = create_app()
init_app(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/addperson')
def addperson():
    return render_template('index.html')


@app.route('/addposition')
def addposition():
    return render_template('add_position.html')


@app.route('/positionadd', methods=['POST'])
def positionadd():
    title = request.form['title']
    description = request.form['description']

    position = Position(title, description)
    db.session.add(position)
    db.session.commit()

    return render_template('add_position.html')


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
    query = db.session.query(People)
    peoples = []

    for people in query:
        people_positions_ids = db.session.query(PeoplePosition.position_id).filter(
            PeoplePosition.people_id == people.id
        )

        positions = db.session.query(Position).filter(
            Position.id.in_(people_positions_ids)
        ).all()
        peoples.append({
            'name': people.name,
            'email': people.email,
            'positions': positions
        })

    return render_template('people_list.html', peoples=peoples)


if __name__ == '__main__':
    app.run()
