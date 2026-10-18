# shopping_cart.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory cart: each replica has its OWN cart (no shared storage in this lab)
cart = []


@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)


@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.json
    cart.append(item)
    return jsonify(cart), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
