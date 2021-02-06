import logging

import flask

from downloads.database import db
from downloads.views import api

app = flask.Flask(__name__)
app.logger.setLevel(logging.INFO)

db.init_app(app)

app.register_blueprint(api, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run()
