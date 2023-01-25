import json

from flask import request

import model
from app import app
from setup_db import db

"""вывод данных ползователей"""
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


"""вывод данных ползователя"""
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

