import os
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from olympic import get_olympic_medal_tally

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return """
        <h1>Paris 2024 Olympic Medal Tally Unofficial API</h1>
        <p>All trademarks, data, and other relevant properties are the copyright and
        property of the International Olympic Committee (IOC).</p>
        """


@app.route("/medals", methods=["GET"])
def get_medal_tally():
    ioc_noc_code = request.args.get("country")
    fetch_all = bool(request.args.get("all"))

    results = get_olympic_medal_tally(fetch_all=fetch_all, ioc_noc_code=ioc_noc_code)
    response = make_response(jsonify(results))
    # https://vercel.com/docs/edge-network/caching
    response.headers["Cache-Control"] = "public, s-maxage=1800"
    return response


if __name__ == "__main__":
    app.run(debug=os.environ.get("VERCEL_ENV") is None)
