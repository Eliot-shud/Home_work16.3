import json
import model
from flask import request
from app import app
from setup_db import db



"""вывод предложений """
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

"""вывод предложения """
@app.route("/offer/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    if request.method == "GET":
        return json.dumps(model.Offer.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = model.Offer.query.get(uid)
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