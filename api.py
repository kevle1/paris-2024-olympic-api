import logging
import json
import os
from flask import Flask, jsonify, make_response, request
from upstash_ratelimit import FixedWindow, Ratelimit
from upstash_redis import Redis

from olympic import get_olympic_medal_tally

app = Flask(__name__)
redis = Redis(url=os.getenv("KV_REST_API_URL"), token=os.getenv("KV_REST_API_TOKEN"))
ratelimit = Ratelimit(
    redis=redis,
    limiter=FixedWindow(max_requests=10, window=10),
    prefix="@upstash/paris-ratelimit",
)

logger = logging.getLogger(__name__)


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
    logger.info(f"Request from {ip}")

    ioc_noc_code = request.args.get("country")

    ratelimit_gate = ratelimit.limit(ip)
    if not ratelimit_gate.allowed:
        logger.warning(f"Rate limit exceeded for {ip}")
        response = make_response(jsonify({"error": "Rate limit exceeded"}))
        response.status_code = 429
        response.headers["Retry-After"] = 10
        return response

    cache_key = f"medals_cache:{ioc_noc_code}"
    cached_response = redis.get(cache_key)

    if cached_response:
        response = make_response(jsonify(json.loads(cached_response)))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    results = get_olympic_medal_tally(ioc_noc_code=ioc_noc_code)
    response = make_response(jsonify(results))

    redis.setex(cache_key, 1800, response.get_data(as_text=True))

    response.headers["Access-Control-Allow-Origin"] = "*"
    # response.headers["Cache-Control"] = "public, max-age=30"

    return response


@app.route("/medals/all", methods=["GET"])
def get_medal_tally_all():
    # Deprecated
    return get_medal_tally()


if __name__ == "__main__":
    app.run(debug=os.environ.get("VERCEL_ENV") is None)
