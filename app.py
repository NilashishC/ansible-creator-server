import logging

from datetime import datetime, timezone

from flask import Flask, request
from flask_restful import Api

from creator_api.resources.creator_init import CreatorInit


app = Flask(__name__)
api = Api(app)


@app.before_request
def log_request_info():
    """Log every incoming request."""
    headers = " ".join([line.strip() for line in str(request.headers).splitlines()])
    request_log = f"REMOTE_ADDR={request.remote_addr}, METHOD={request.method}, URI={request.full_path}, HEADERS={headers}"
    app.logger.debug(request_log)


# setup logging for app
app.logger.setLevel(logging.DEBUG)
svc_log_file = (
    f"ansible-creator-svc-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.log"
)
app.logger.debug(
    "ansible-creator service is starting, logs available in %s", svc_log_file
)
handler = logging.FileHandler(svc_log_file)
app.logger.addHandler(handler)

# add endpoints
api.add_resource(CreatorInit, "/init")
