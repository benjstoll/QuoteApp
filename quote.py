from flask import Flask, render_template, redirect, url_for, request
from os import path
from yaml import safe_load


from gemini_handler import genai_gemini
from dynamo_handler import dynamo


config_path = path.abspath(path.join(path.dirname(__file__), 'config.yml'))
with open(config_path, 'r') as f:
    config = safe_load(f)


app = Flask(__name__)
gai = genai_gemini.GenAi(config['gemini_key'], config['prompt'])
db = dynamo.DynamoDb(config['dynamo_table'])


@app.route('/')
def quote_page():
    # Fetch the current quote and count
    quote_count = db.get_quote_count()
    quote = db.get_last_quote(quote_id=quote_count)

    if not quote:
        quote = "No quotes currently in database, please generate one."

    return render_template('quote/quote.html', quote_count=quote_count, quote=quote)


@app.route('/generate', methods=['POST'])
def generate():
    quote = gai.generate_quote()['quote']
    quote_count = db.get_quote_count()
    db.insert_quote(quote_id=quote_count+1, quote=quote)

    return redirect(url_for('quote_page'))


@app.route('/clear', methods=['POST'])
def clear():
    db.clear_all_quotes()
    return redirect(url_for('quote_page'))

if __name__ == '__main__':
    app.run(debug=True)