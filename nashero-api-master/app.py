from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cache import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS
from celery import Celery
import logging
from celery import Celery
from ut import run


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
CORS(
    app,
    origins=[
        "https://nas.cryptohero.pro/*",
        "http://nas.cryptohero.pro/*",
        "http://localhost:8080",
        "http://test.dapdap.io/*",
        "http://hero-otc.etherfen.com/*",
        "https://hero-otc.etherfen.com/*",
    ],
)
app.config.from_pyfile("config.py")
api = Api(app)
celery = make_celery(app)
mongo = PyMongo(app)
cache = Cache(app, config={"CACHE_TYPE": "redis"})


class Heros(Resource):

    # @cache.cached(timeout=60 * 5)
    def get(self):
        dapp = mongo.db.hero.find({}, {"_id": 0})
        return {"data": sorted(dapp, key=lambda x: float(x["price"]), reverse=False)}


class Hero(Resource):

    def get(self, heroId):
        dapp = mongo.db.hero.find({"heroId": heroId}, {"_id": 0})
        if dapp:
            return {
                "data": sorted(dapp, key=lambda x: float(x["price"]), reverse=False)
            }
        else:
            return {"error": 1, "msg": "该英雄目前没有售卖"}


api.add_resource(Heros, "/nasapi/hero")
api.add_resource(Hero, "/nasapi/hero/<string:heroId>")


@celery.task
def runcelery():
    "每小时跑一次数据"
    run()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8003, threaded=True)
