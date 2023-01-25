from flask import Flask

import model
import join
from setup_db import db


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# база данных
def init_database():
    db.drop_all()
    db.create_all()

    for user_data in join.raw_data.users:
        new_user = model.User(**user_data)

        db.session.add(new_user)


    for order_data in join.raw_data.orders:
        new_order = model.Order(**order_data)

        db.session.add(new_order)


    for offer_data in join.raw_data.offers:
        new_offer = model.Offer(**offer_data)

        db.session.add(new_offer)

    db.session.commit()

if __name__ == '__main__':
    app.run()


