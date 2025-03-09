import flask
from flask import request, jsonify, redirect, url_for
from gacha.gacha import *
from models import *

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/gacha_impact"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
ma.init_app(app)

users_schema = UserSchema(many=True)
history_schema = HistorySchema(many=True)

with app.app_context():
    db.create_all()

# ------------- ROUTES ----------------

# get
@app.route("/", methods=['GET'])
def home():
    return "<h1>HELLO WORLD<h1>"

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("home"))

@app.route("/user", methods=["GET"])
def get_user():
    users = []
    data = User.query.all()
    users = users_schema.dump(data)
    return jsonify(users)

@app.route("/history", methods=['GET'])
def get_history():
    history = []
    _json = request.json
    uid = _json["uid"]
    data = History.query.filter_by(uid=uid).all()
    history = history_schema.dump(data)
    return jsonify(history)

@app.route("/pull", methods=["GET"])
def ten_pull():
    # get request body
    _json = request.json
    type = _json["type"]

    # get user data
    user = User.query.get(_json['uid'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    # get item data
    items = Item.query.all()
    three_star_item = []
    four_star_char = []
    five_star_char = []

    for item in items:
        if item.rarity == "3-star":
            three_star_item.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "rarity": item.rarity,
                    "item_type": item.item_type,
                    "type": item.type,
                    "is_rate_up": item.is_rate_up,
                    "image_url": item.image_url,
                }
            )
        elif item.rarity == "4-star":
            four_star_char.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "rarity": item.rarity,
                    "item_type": item.item_type,
                    "type": item.type,
                    "is_rate_up": item.is_rate_up,
                    "image_url": item.image_url,
                }
            )
        elif item.rarity == "5-star":
            five_star_char.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "rarity": item.rarity,
                    "item_type": item.item_type,
                    "type": item.type,
                    "is_rate_up": item.is_rate_up,
                    "image_url": item.image_url,
                }
            )

    gacha_pool = {
        "3-star": [Item(**item) for item in three_star_item],
        "4-star": [Item(**item) for item in four_star_char],
        "5-star": [Item(**item) for item in five_star_char],
    }

    # gacha
    result = pull(type, user, gacha_pool)
    user.pity = result['current_pity']
    user.four_star_pity = result["current_4star_pity"]
    user.is_rate_on = result['five_star_rateon']
    user.four_star_rate_on = result['four_star_rateon']
    if type == 'ten_pull':
        if user.primogems < 1600:
            return jsonify("Primo harus minimal 1600")
        user.primogems -= 1600
    elif type == 'one_pull':
        if user.primogems < 160:
            return jsonify("Primo harus minimal 160")
        user.primogems -= 160

    # Simpan hasil gacha ke history
    history_entries = []
    for gacha in result["gacha_result"]:
        history_entry = History(
            uid=result["uid"],
            item_name=gacha["item_name"],
            rarity=gacha["rarity"],
        )
        history_entries.append(history_entry)
        
    db.session.add_all(history_entries)
    
    db.session.commit()
    return jsonify(result)

# post

# patch
@app.route("/user/<string:uid>", methods=["PATCH"])
def update_user(uid):
    user = User.query.get(uid)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json

    if not data:
        return jsonify({"message": "No data provided"}), 400

    if "username" in data:
        if not isinstance(data["username"], str) or len(data["username"]) > 20:
            return jsonify({"error": "Invalid username"}), 400
        user.username = data["username"]

    if "email" in data:
        if not isinstance(data["email"], str) or len(data["email"]) > 20:
            return jsonify({"error": "Invalid email"}), 400
        user.email = data["email"]

    if "primogems" in data:
        if not isinstance(data["primogems"], int) or data["primogems"] < 0:
            return jsonify({"error": "Invalid primogems"}), 400
        user.primogems += data["primogems"]

    if "pity" in data:
        if not isinstance(data["pity"], int) or data["pity"] < 0:
            return jsonify({"error": "Invalid pity"}), 400
        user.pity = data["pity"]

    if "four_star_pity" in data:
        if not isinstance(data["four_star_pity"], int) or data["four_star_pity"] < 0:
            return jsonify({"error": "Invalid four_star_pity"}), 400
        user.four_star_pity = data["four_star_pity"]

    if "is_rate_on" in data:
        if data["is_rate_on"] not in ["True", "False"]:
            return jsonify({"error": "Invalid is_rate_on"}), 400
        user.is_rate_on = data["is_rate_on"]

    if "four_star_rate_on" in data:
        if data["four_star_rate_on"] not in ["True", "False"]:
            return jsonify({"error": "Invalid four_star_rate_on"}), 400
        user.four_star_rate_on = data["four_star_rate_on"]

    db.session.commit()

    return (
        jsonify({"message": "User update success"}),
        200,
    )

# delete
# @app.route("/product/<string:uid>", methods=["DELETE"])
# def delete_user(uid):
#     product = Product.query.get(uid)
#     if not product:
#         return jsonify({"message": "Product not found"}), 404

#     db.session.delete(product)
#     db.session.commit()

#     return jsonify({"message": f"Product {uid} deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
