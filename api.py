from flask import Flask, jsonify, make_response, request

from olympic import get_olympic_medal_tally

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "<h1>Paris 2024 Olympic Medal Tally Unofficial API</h1>"


@app.route("/medals", methods=["GET"])
def get_medal_tally():
    results = get_olympic_medal_tally(request.args.get("country"))
    response = make_response(jsonify(results))
    # https://vercel.com/docs/edge-network/caching
    response.headers["Cache-Control"] = "public, s-maxage=1800"
    return response


if __name__ == "__main__":
    app.run(debug=True)
