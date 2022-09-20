# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request
from function import handler
# from waitress import serve
import os
from function.models import module
import redis
import time


data = module.DATA
conn_pool = redis.ConnectionPool(
    host=data.redis_host,
    port=data.redis_port,
    password=data.redis_password,
    decode_responses=True,
    db=data.redis_db,
)
rc = redis.Redis(connection_pool=conn_pool)

app = Flask(__name__)


# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"


@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True


@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    raw_body = os.getenv("RAW_BODY", "false")

    as_text = True

    if is_true(raw_body):
        as_text = False

    ret = handler.handle(request.get_data(as_text=as_text))
    return ret


if __name__ == '__main__':
    while True:
        id_list = rc.lrange(data.task_queue, 0, 4)
        if id_list:
            contract_id = rc.rpop(data.task_queue)
            result = handler.handle(contract_id)
            print("db contract index {}, {}".format(contract_id, result))
            time.sleep(2)
        else:
            time.sleep(5)
