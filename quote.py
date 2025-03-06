from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def create_quote():
    return render_template('quote/quote.html')