import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'csv_file' in request.files:
        # handle CSV upload…
        return redirect(url_for('index'))
    if request.method == 'POST' and 'specialties' in request.form:
        # handle Apollo search…
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
