from flask import Flask, request, jsonify
from kite_api import get_ltp, buy_stock, get_portfolio

app = Flask(__name__)

@app.route("/ltp")
def ltp():
    symbol = request.args.get("symbol", "NSE:INFY")
    price = get_ltp(symbol)
    return jsonify({"symbol": symbol, "ltp": price})

@app.route("/buy", methods=["POST"])
def buy():
    data = request.json
    symbol = data.get("symbol", "NSE:INFY")
    qty = data.get("qty", 1)
    result = buy_stock(symbol, qty)
    return jsonify({"message": result})

@app.route("/portfolio")
def portfolio():
    return jsonify(get_portfolio())

if __name__ == "__main__":
    app.run(port=5000)
