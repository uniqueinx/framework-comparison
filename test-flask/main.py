import os
import orjson
from datetime import datetime
from flask import Flask, request
from flask_redis import FlaskRedis

print("=" * 50)
print(os.environ["REDIS_URL"])
print("=" * 50)
app = Flask(__name__)
app.config.update(dict(REDIS_URL=os.environ["REDIS_URL"], DEBUG=False))
redis_client = FlaskRedis()
redis_client.init_app(app)


@app.route("/")
def health_check():
    return "hello healthy"


@app.route("/status", methods=("POST",))
def set_status():
    _id = request.json.get("id")
    data = {"status": "live", "last_time": datetime.utcnow()}
    redis_client.setex(_id, 50, orjson.dumps(data))
    return {"status": True}


@app.route("/status/<id>")
def get_status(id):
    data = redis_client.get(id)
    return orjson.loads(data) if data else {}
