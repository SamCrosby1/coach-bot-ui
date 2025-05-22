import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Home page: shows CSV uploader and custom search form.
    """
    return render_template('index.html')


@app.route('/coaches', methods=['GET', 'POST'])
def coaches():
    """
    Coaches page:
      - POST (CSV): parses uploaded CSV into a list of coaches
      - GET (form): uses query params (location, specialty) to fetch coaches
    Renders coaches.html with `coaches` = list of dicts [{id, name, email, thumbnail_url}, …]
    """
    coaches_list = []

    # CSV upload
    if request.method == 'POST' and 'csv_file' in request.files:
        csv_file = request.files['csv_file']
        coaches_list = _parse_csv(csv_file)

    # Custom search
    else:
        location = request.args.get('location', '').strip()
        specialty = request.args.get('specialty', '').strip()
        # TODO: replace this stub with your Apollo API integration
        coaches_list = _fetch_coaches_from_apollo(location, specialty)

    return render_template('coaches.html', coaches=coaches_list)


@app.route('/activity', methods=['GET'])
def activity():
    """
    Activity page: shows email send/open/click stats.
    Renders activity.html with `activities` = list of dicts
      [{ to_email, status, opened, clicked }, …]
    """
    # TODO: replace with real Postmark API calls
    activities = [
        # example:
        # {'to_email': 'alice@example.com', 'status': 'sent', 'opened': '3', 'clicked': '1'},
    ]
    return render_template('activity.html', activities=activities)


@app.route('/generic', methods=['GET'])
def generic():
    """
    A simple placeholder you can delete or repurpose.
    """
    return render_template('generic_body.html')


def _parse_csv(csv_file):
    """
    Reads a CSV file (expects columns like name,email,thumbnail_url)
    and returns a list of coach dicts.
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


def _fetch_coaches_from_apollo(location, specialty):
    """
    Stub for Apollo API search. Returns [] until you wire in your API calls.
    """
    # Example structure you’ll eventually populate:
    # return [
    #   {'id': 1, 'name': 'Jane Doe', 'email': 'jane@coach.com', 'thumbnail_url': 'https://…'},
    #   …
    # ]
    return []


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # debug=True is handy during development; turn it off in production.
    app.run(host='0.0.0.0', port=port, debug=True)
