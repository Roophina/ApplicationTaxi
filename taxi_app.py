"""
Веб-приложение для заказа такси.

Реализовано в соответствии с приложенной документацией.

Для отправки тела запроса использовался Postman.
"""
from contextlib import contextmanager

from flask import Flask, jsonify, request
from sqlalchemy.orm import scoped_session, sessionmaker

from functions import valid_json
from schemas import schema_post_order, schema_id, schema_put_order, schema_post_driver, schema_post_client
from taxi_db import Driver, engine, Client, Order

app = Flask(__name__)

Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))


@contextmanager
def session_scope():  # type: ignore
    """Подключение к базе данных."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@app.route('/drivers', methods=['POST'])  # type: ignore
def post_driver():  # type: ignore
    """Добавить в систему водителя."""
    content = request.get_json()
    if not valid_json(content, schema_post_driver):
        return "Неправильный запрос", 400
    with session_scope() as session:
        new_driver = Driver(name=content["name"],
                            car=content["car"])
        session.add(new_driver)
    return jsonify(content), 201


@app.route('/drivers', methods=['GET'])  # type: ignore
def get_driver():  # type: ignore
    """Найти водителя по id."""
    content = request.get_json()
    if not valid_json(content, schema_id):
        return "Неправильный запрос", 400
    with session_scope() as session:
        driver = session.query(Driver).filter(Driver.id == content["id"].first())
        if not driver:
            return "Объект в базе не найден", 404
        driver_list = [driver.serialize]
    return jsonify(driver_list), 200


@app.route('/drivers', methods=['DELETE'])  # type: ignore
def delete_driver():  # type: ignore
    """Удалить водителя из системы."""
    content = request.get_json()
    if not valid_json(content, schema_id):
        return "Неправильный запрос", 400
    with session_scope() as session:
        q = session.query(Driver).filter(Driver.id == content["id"]).one()
        if not q:
            return "Объект в базе не найден", 404
        session.delete(q)
        return "Удалено", 204


@app.route('/clients', methods=['POST'])  # type: ignore
def post_client():  # type: ignore
    """Занести в базу клиента."""
    content = request.get_json()
    if not valid_json(content, schema_post_client):
        return "Неправильный запрос", 400
    with session_scope() as session:
        new_client = Client(name=content["name"],
                            is_vip=content["is_vip"])
        session.add(new_client)
    return jsonify(content), 201


@app.route('/clients', methods=['GET'])  # type: ignore
def get_client():  # type: ignore
    """Найти клиента по ID."""
    content = request.get_json()
    if not valid_json(content, schema_id):
        return "Неправильный запрос", 400
    with session_scope() as session:
        client = session.query(Client).filter(Client.id == content["id"].first())
        if not client:
            return "Объект в базе не найден", 404
        client_list = [client.serialize]
    return jsonify(client_list), 200


@app.route('/clients', methods=['DELETE'])  # type: ignore
def delete_client():  # type: ignore
    """Удалить клиента из базы."""
    content = request.get_json()
    if not valid_json(content, schema_id):
        return "Неправильный запрос", 400
    with session_scope() as session:
        q = session.query(Client).filter(Client.id == content["id"]).one()
        if not q:
            return "Объект в базе не найден", 404
        session.delete(q)
        return "Удалено", 204


@app.route('/orders', methods=['POST'])  # type: ignore
def post_order():  # type: ignore
    """Добавить новый заказ."""
    content = request.get_json()
    if not valid_json(content, schema_post_order):
        return "Плохой json :(", 400
    with session_scope() as session:
        new_order = Order(address_from=content["address_from"],
                          address_to=content["address_to"],
                          client_id=content["client_id"],
                          driver_id=content["driver_id"],
                          date_created=content["date_created"],
                          status=content["status"])
        session.add(new_order)
    return jsonify(content), 201


@app.route('/orders', methods=['GET'])  # type: ignore
def get_order():  # type: ignore
    """Найти заказ."""
    content = request.get_json()
    if not valid_json(content, schema_id):
        return "Неправильный запрос", 400
    with session_scope() as session:
        order = session.query(Order).filter(Order.id == content["id"]).first()
        if not order:
            return "Объект в базе не найден", 404
        order_list = [order.serialize]
    return jsonify(order_list), 200


@app.route('/orders', methods=['PUT'])  # type: ignore
def put_order():  # type: ignore
    """Изменить заказ."""
    content = request.get_json()
    if not valid_json(content, schema_put_order):
        return "Неправильный запрос", 400
    with session_scope() as session:
        q = session.query(Order).filter(Order.id == content["id"]).first()
        if not q:
            return "Объект в базе не найден", 404
        if q.status == "not_accepted" and (content["status"] == "in_progress" or content["status"] == "cancelled"):
            q.status = content["status"]
        elif q.status == "in_progress" and (content["status"] == "done" or content["status"] == "cancelled"):
            q.status = content["status"]
        elif q.status == "not_accepted" and content["status"] == "not_accepted":
            q.date_created = content["date_created"]
            q.driver_id = content["driver_id"]
            q.client_id = content["client_id"]
    return jsonify(content), 200


if __name__ == "__main__":
    app.run()
