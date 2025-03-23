from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"

    uid = db.Column(db.String(50), primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    primogems = db.Column(db.Integer, nullable=False, default=0)
    pity = db.Column(db.Integer, nullable=False, default=0)
    four_star_pity = db.Column(db.Integer, nullable=False, default=0)
    is_rate_on = db.Column(db.Boolean, nullable=False, default=False)
    four_star_rate_on = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
        self,
        uid,
        username,
        email,
        primogems=0,
        pity=0,
        four_star_pity=0,
        is_rate_on=False,
        four_star_rate_on=False,
    ):
        self.uid = uid
        self.username = username
        self.email = email
        self.primogems = primogems
        self.pity = pity
        self.four_star_pity = four_star_pity
        self.is_rate_on = is_rate_on
        self.four_star_rate_on = four_star_rate_on

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "uid",
            "username",
            "email",
            "primogems",
            "pity",
            "four_star_pity",
            "is_rate_on",
            "four_star_rate_on",
        )

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.Enum("3-star", "4-star", "5-star"), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_rate_up = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, id, name, item_type, type, rarity, image_url, is_rate_up):
        self.id = id
        self.name = name
        self.item_type = item_type
        self.type = type
        self.rarity = rarity
        self.image_url = image_url
        self.is_rate_up = is_rate_up

class ItemSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "item_type",
            "type",
            "rarity",
            "image_url",
            "is_rate_up"
        )

class History(db.Model):
    __tablename__ = "history"
    id_result = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    rarity = db.Column(db.Enum("3-star", "4-star", "5-star"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, uid, item_name, rarity, date=None):
        self.uid = uid
        self.item_name = item_name
        self.rarity = rarity
        self.date = date or datetime.now()

class HistorySchema(ma.Schema):
    class Meta:
        fields = (
            "id_result",
            "uid",
            "email",
            "item_name",
            "rarity",
            "date"
        )
