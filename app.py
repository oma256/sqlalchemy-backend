from flask import request

from models import db, People, Position
from utils import create_app, init_app, json_response

app = create_app()
init_app(app)


@app.route('/peoples', methods=['GET', 'POST'])
def peoples():
    if request.method == 'POST':
        people = People(
            pname=request.json.get('name'),
            email=request.json.get('email'),
            phone=request.json.get('phone')
        )

        db.session.add(people)
        db.session.commit()

        return json_response(people)

    elif request.method == 'GET':
        peoples_list = db.session.query(People).all()

        return json_response(peoples_list)


@app.route('/positions', methods=['GET'])
def positions():
    positions_list = db.session.query(Position).all()

    return json_response(positions_list)


if __name__ == '__main__':
    app.run()
