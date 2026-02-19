from flask import Flask, jsonify, request
import os
import datetime

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")

@app.route("/")
def home():
    return jsonify({
        "service": "Enterprise Bank Transaction API",
        "version": APP_VERSION,
        "status": "running",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/transaction", methods=["POST"])
def transaction():
    data = request.json
    amount = data.get("amount")
    account = data.get("account")

    if not amount or not account:
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify({
        "message": "Transaction processed securely",
        "account": account,
        "amount": amount
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
