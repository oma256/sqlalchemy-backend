from flask import request

import xlsxwriter

from models import db, People, Position, PeoplePosition
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


@app.route('/positions', methods=['GET', 'POST'])
def positions():

    if request.method == 'POST':
        position = Position(
            title=request.json.get('title'),
            description=request.json.get('description'),
        )

        db.session.add(position)
        db.session.commit()

        return json_response(position)

    elif request.method == 'GET':
        positions_list = db.session.query(Position).all()

        return json_response(positions_list)


@app.route('/people-positions', methods=['GET', 'POST'])
def people_positions():
    if request.method == 'POST':
        people_id = request.json.get('people_id')
        position_id = request.json.get('position_id')

        people = db.session.query(People).filter_by(id=people_id).first()

        if people is None:
            data = {
                'code': -1,
                'message': f'Человек ID c {people_id} не существует в БД'
            }
            return json_response(data=data, status_code=400)

        position = db.session.query(Position).filter_by(id=position_id).first()

        if position is None:
            data = {
                'code': -1,
                'message': f'Должность ID c {position_id} не существует в БД'
            }
            return json_response(data=data, status_code=400)

        people_position = db.session.query(PeoplePosition).filter_by(
            people_id=people.id, position_id=position.id
        ).first()

        if people_position is None:
            people_position = PeoplePosition(
                people_id=people.id,
                position_id=position.id
            )

            db.session.add(people_position)
            db.session.commit()
        else:
            data = {
                'code': -1,
                'message': 'Запись в БД уже существует'
            }

            return json_response(data=data, status_code=400)

        data = {
            'code': 0,
            'message': 'Данные успешно сохранены в БД'
        }
        return json_response(data=data, status_code=201)

    elif request.method == 'GET':
        data = []
        peoples = db.session.query(People).all()

        for people in peoples:
            positions_ids = db.session.query(PeoplePosition.position_id).filter_by(
                people_id=people.id
            )

            positions = db.session.query(Position).filter(
                Position.id.in_(positions_ids)
            ).all()

            data.append({
                'id': people.id,
                'name': people.name,
                'email': people.email,
                'phone': people.phone,
                'positions': positions
            })

        return json_response(data=data)


@app.route('/create-people-excel-file', methods=['POST'])
def create_people_excel_file():
    peoples = db.session.query(People).all()

    workbook = xlsxwriter.Workbook('people_list.xlsx')
    worksheet = workbook.add_worksheet('Список людей')

    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, 'Имя')
    worksheet.write(0, 2, 'Почта')
    worksheet.write(0, 3, 'Номер телефона')

    for i, people in enumerate(peoples, start=1):
        worksheet.write(i, 0, people.id)
        worksheet.write(i, 1, people.name)
        worksheet.write(i, 2, people.email)
        worksheet.write(i, 3, people.phone)

    data = {
        'code': 0,
        'message': 'Файл создан!'
    }

    workbook.close()
    return json_response(data=data, status_code=201)


if __name__ == '__main__':
    app.run()
