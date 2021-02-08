import atexit
import logging

import flask

from downloads.database import db
from downloads.tasks import scheduler
from downloads.views import api

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)

db.init_app(app)

atexit.register(lambda: scheduler.shutdown())
scheduler.init_app(app)
scheduler.start()

app.register_blueprint(api, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()
