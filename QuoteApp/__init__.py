from flask import Flask
import logging
logger = logging.getLogger(__name__)

def create_app(test_config=None):
    log_format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO)

    app = Flask(__name__, instance_relative_config=True)

    from . import quote
    app.register_blueprint(quote.bp)

    return app
