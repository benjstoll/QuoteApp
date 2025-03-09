from flask import Flask
import logging
logger = logging.getLogger(__name__)

def create_app():
    # Set up logging
    log_format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO)

    app = Flask(__name__)

    # Load the standard app blueprint (quote.py)
    logger.info('Initializing quote app...')
    from . import quote
    app.register_blueprint(quote.bp)

    return app
