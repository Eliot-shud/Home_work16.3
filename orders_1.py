import json
import model
from flask import request
from app import app
from setup_db import db


""" вывод заказов """
@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in model.Order.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = model.User(**order_data)

        db.session.add(new_order)
        db.session.commit()

        return "Order Created", 201


""" вывод заказа """
@app.route("/order/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
    if request.method == "GET":
        return json.dumps(model.Order.query.get(uid).to_dict()), 200
    if request.method == "POST":
        order_data = json.loads(request.data)
        u = model.Order.query.get(uid)
        u.name = order_data["name"]
        u.description = order_data["description"]
        u.start_date = order_data["start_date"]
        u.end_date = order_data["end_date"]
        u.address = order_data["address"]
        u.price = order_data["price"]
        u.customer_id = order_data["customer_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Order updated", 204
    if request.method == "DELETE":
        u = model.Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order Deleted", 204