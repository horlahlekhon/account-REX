import logging
from flask import g, has_app_context
import uuid
import datetime





class MessageFilter(logging.Filter):
    def filter(self, record):
        # if has_app_context():
        record.uuid = g.get("X-request-id", uuid.uuid4())
        record.timestamp = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
        return True



logger = logging.getLogger(__name__)
loglevels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG
}
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s'
                                      ' uuid=%(uuid)s')
handler.addFilter(MessageFilter())
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(loglevels["debug"])