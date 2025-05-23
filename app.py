import os
import csv
import random
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Coach Hub:
      - POST: parse uploaded CSV into coaches_list
      - GET : fetch coaches_list via Apollo stub by location
    Always display only the first 5 coaches.
    """
    coaches_list = []

    # 1) CSV upload
    if request.method == 'POST' and 'csv_file' in request.files:
        coaches_list = _parse_csv(request.files['csv_file'])

    # 2) Location search
    elif request.method == 'GET' and request.args.get('location'):
        loc = request.args.get('location', '').strip()
        coaches_list = _fetch_coaches_from_apollo(loc)

    # 3) (Optional) apply additional in-memory filters or sorting here
    #    e.g. coaches_list = [c for c in coaches_list if c['rating'] >= 4.0]

    # 4) Limit to first 5 for display
    displayed_coaches = coaches_list[:5]

    # 5) Render the coach hub
    return render_template('index.html', coaches=displayed_coaches)


@app.route('/activity')
def activity():
    """
    Email Hub: Campaign analytics dashboard
    """
    # Stub analytics data
    # Trend: last 7 days
    trend = []
    for i in range(7):
        trend.append({
            'date':        f'Day-{7-i}',
            'open_rate':   round(random.uniform(20, 80), 1),
            'click_rate':  round(random.uniform(5, 30), 1),
            'bounce_count': random.randint(0, 5)
        })

    # Top-performing subject lines
    subjects = [
        {'subject': 'Quick Question',         'count': random.randint(20, 100)},
        {'subject': 'Opportunity for You',    'count': random.randint(20, 100)},
        {'subject': 'Let’s Connect',          'count': random.randint(20, 100)},
    ]

    # Geo data for map (not used here, but kept for compatibility)
    geo = [
        {'name': 'New York, USA', 'lat': 40.7, 'lng': -74, 'clicks': random.randint(0, 50)},
        {'name': 'London, UK',    'lat': 51.5, 'lng': -0.1, 'clicks': random.randint(0, 50)},
        {'name': 'Sydney, AUS',   'lat': -33.9, 'lng': 151.2, 'clicks': random.randint(0, 50)},
    ]

    analytics = {'trend': trend, 'subjects': subjects, 'geo': geo}
    return render_template('activity.html', analytics=analytics)


@app.route('/dashboard')
def dashboard():
    """
    Dashboard: render 3D globe and list of coaches who opened emails.
    """
    coaches = []
    for i in range(20):
        coaches.append({
            'name':       f'Coach {i+1}',
            'lat':        random.uniform(-60, 80),
            'lng':        random.uniform(-180, 180),
            'open_count': random.randint(0, 10),
            'bounce_count': random.randint(0, 3)
        })
    return render_template('dashboard.html', coaches=coaches)


def _parse_csv(csv_file):
    """
    Reads a CSV file with headers (name,email,experience,rating,lat,lng)
    into a list of coach dicts.
    """
    text = csv_file.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    coaches = []
    for idx, row in enumerate(reader):
        coaches.append({
            'id':          idx,
            'name':        row.get('name', '').strip(),
            'email':       row.get('email', '').strip(),
            'experience':  float(row.get('experience') or 0),
            'rating':      float(row.get('rating') or 0),
            'lat':         float(row.get('lat') or 0),
            'lng':         float(row.get('lng') or 0),
            'open_count':  int(row.get('open_count') or 0),
            'bounce_count':int(row.get('bounce_count') or 0)
        })
    return coaches


def _fetch_coaches_from_apollo(location):
    """
    Stub for Apollo API: returns 9 sample coaches with random data.
    Replace with real API integration.
    """
    sample = []
    for i in range(1, 10):
        sample.append({
            'id':          i,
            'name':        f'Coach {i}',
            'email':       f'coach{i}@example.com',
            'experience':  random.randint(1, 15),
            'rating':      round(random.uniform(3, 5), 1),
            'lat':         random.uniform(-60, 80),
            'lng':         random.uniform(-180, 180),
            'open_count':  random.randint(0, 5),
            'bounce_count':random.randint(0, 2)
        })
    return sample


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
