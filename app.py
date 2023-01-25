import json

from flask import Flask, request, jsonify

import model
from join import raw_data
from setup_db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# views users
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in model.User.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = model.User(**user_data)

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201


@app.route("/user/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):

    if request.method == "GET":
        return json.dumps(model.User.query.get(uid).to_dict()), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        u = model.User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = model.User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "User deleted", 204


# views orders
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


# views offers
@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for u in model.Offer.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = model.User(**offer_data)

        db.session.add(new_offer)
        db.session.commit()

        return "Offer Created", 201


@app.route("/offer/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data["order_id"]
        u.executor_id = offer_data["executor_id"]


        db.session.add(u)
        db.session.commit()

        return "Order updated", 204
    if request.method == "DELETE":
        u = model.Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order Deleted", 204


# база данных
def init_database():
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
        new_user = model.User(**user_data)

        db.session.add(new_user)


    for order_data in raw_data.orders:
        new_order = model.Order(**order_data)

        db.session.add(new_order)


    for offer_data in raw_data.offers:
        new_offer = model.Offer(**offer_data)

        db.session.add(new_offer)

    db.session.commit()

if __name__ == '__main__':
    app.run()


