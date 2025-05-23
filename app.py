# app.py
import os
import csv
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page:
    - POST (CSV): parse uploaded CSV into coaches_list
    - GET  (location): fetch coaches_list via Apollo stub
    Renders index.html with `coaches` for the right panel.
    """
    coaches_list = []

    # CSV upload
    if request.method == 'POST' and 'csv_file' in request.files:
        coaches_list = _parse_csv(request.files['csv_file'])

    # Location search
    elif request.method == 'GET' and request.args.get('location'):
        location = request.args.get('location', '').strip()
        coaches_list = _fetch_coaches_from_apollo(location)

    return render_template('index.html', coaches=coaches_list)

@app.route('/activity', methods=['GET'])
def activity():
    """
    Activity page: shows email send/open/click stats.
    """
    activities = []  # TODO: integrate Postmark API
    return render_template('activity.html', activities=activities)

def _parse_csv(csv_file):
    """
    Reads a CSV with headers (id,name,email,thumbnail_url) into a list of dicts.
    """
    text = csv_file.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    coaches = []
    for idx, row in enumerate(reader):
        coaches.append({
            'id': row.get('id', idx),
            'name': row.get('name', '').strip(),
            'email': row.get('email', '').strip(),
            'thumbnail_url': row.get('thumbnail_url', '').strip(),
        })
    return coaches

def _fetch_coaches_from_apollo(location):
    """
    Stub for Apollo API. Replace with real query logic.
    """
    return []

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
