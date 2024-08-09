import os
from flask import Flask, jsonify, make_response, request
from upstash_ratelimit import FixedWindow, Ratelimit
from upstash_redis import Redis

from olympic import get_olympic_medal_tally

app = Flask(__name__)
redis = Redis(url=os.getenv("KV_REST_API_URL"), token=os.getenv("KV_REST_API_TOKEN"))
ratelimit = Ratelimit(
    redis=redis,
    limiter=FixedWindow(max_requests=5, window=10),
    prefix="@upstash/paris-ratelimit",
)


@app.route("/", methods=["GET"])
def home():
    return """
        <h1>Paris 2024 Olympic Medal Tally Unofficial API</h1>
        <p>All trademarks, data, and other relevant properties are the copyright and
        property of the International Olympic Committee (IOC).</p>
        """


@app.route("/medals", methods=["GET"])
def get_medal_tally():
    ip = request.headers.get("X-Real-Ip")
    ratelimit_gate = ratelimit.limit(ip)

    if not ratelimit_gate.allowed:
        return make_response(jsonify({"error": "Rate limit exceeded"}), 429)

    ioc_noc_code = request.args.get("country")
    results = get_olympic_medal_tally(ioc_noc_code=ioc_noc_code)
    response = make_response(jsonify(results))
    # https://vercel.com/docs/edge-network/caching
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "public, s-maxage=1800"

    return response


@app.route("/medals/all", methods=["GET"])
def get_medal_tally_all():
    # Deprecated
    return get_medal_tally()


if __name__ == "__main__":
    app.run(debug=os.environ.get("VERCEL_ENV") is None)
