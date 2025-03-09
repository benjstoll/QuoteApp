from flask import Blueprint, render_template, redirect, url_for
from os import path
from yaml import safe_load
from requests import get

import logging
logger = logging.getLogger(__name__)

from gemini_handler import genai_gemini
from dynamo_handler import dynamo


config_path = path.abspath(path.join(path.dirname(__file__), 'config.yml'))
with open(config_path, 'r') as f:
    config = safe_load(f)

bp = Blueprint('quote', __name__)
gai = genai_gemini.GenAi(config['prompt'])
db = dynamo.DynamoDb(config['dynamo_table'])

try:
    ip = get('http://169.254.169.254/latest/meta-data/local-ipv4').text.strip()
except:
    logger.error('Could not get IPv4 address from instance.')
    ip = None


# Main page for user interaction
@bp.route('/')
def quote_page():
    # Fetch the current quote and count
    quote_count = db.get_quote_count()
    quote = db.get_last_quote(quote_id=quote_count)

    if not quote:
        quote = "No quotes currently in database, please generate one."

    return render_template('quote/quote.html', quote_count=quote_count, quote=quote, ip=ip)


# POST method to generate a new gemini quote and post it to the database.
@bp.route('/generate', methods=['POST'])
def generate():
    logger.info('Generating quote from Gemini...')
    quote = gai.generate_quote()['quote']

    logger.info('Adding quote to the database...')
    quote_count = db.get_quote_count()
    db.insert_quote(quote_id=quote_count+1, quote=quote)

    return redirect(url_for('quote.quote_page'))


# Clear all entries from the database
@bp.route('/clear', methods=['POST'])
def clear():
    db.clear_all_quotes()
    return redirect(url_for('quote.quote_page'))