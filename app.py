import logging
from datetime import datetime, timezone

from flask import Flask
from flask_restful import Api

from creator_api.resources.creator_init import CreatorInit

app = Flask(__name__)
api = Api(app)

# add endpoints
api.add_resource(CreatorInit, "/init")

# setup logging for app
app.logger.setLevel(logging.DEBUG)
svc_log_file = (
    f"ansible-creator-svc-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.log"
)
app.logger.debug(
    f"ansible-creator service is starting, logs available in {svc_log_file}"
)
handler = logging.FileHandler(svc_log_file)
app.logger.addHandler(handler)
