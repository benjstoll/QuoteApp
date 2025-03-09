from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import quote
    app.register_blueprint(quote.bp)

    return app
