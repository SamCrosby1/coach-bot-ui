import os, csv, random
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Sample coaches with lat/lng & open_count (0 or 1)
SAMPLE_COACHES = [
  {'name':'Alice Smith','email':'alice@example.com','experience':5,'rating':4.2,'lat':40.71,'lng':-74.00,'open_count':1,'bounce_count':0},
  {'name':'Bob Johnson','email':'bob.j@example.org','experience':8,'rating':4.8,'lat':51.50,'lng':-0.12,'open_count':0,'bounce_count':0},
  {'name':'Carla Davis','email':'carla@coaching.io','experience':3,'rating':3.9,'lat':34.05,'lng':-118.24,'open_count':1,'bounce_count':0},
  {'name':'David Lee','email':'davidl@fitcoach.io','experience':10,'rating':4.5,'lat':35.68,'lng':139.69,'open_count':1,'bounce_count':0},
  {'name':'Eva Martínez','email':'eva.m@example.net','experience':6,'rating':4.1,'lat':48.85,'lng':2.35,'open_count':0,'bounce_count':0},
  {'name':'Frank Wu','email':'frank.wu@example.com','experience':7,'rating':4.7,'lat':-33.86,'lng':151.21,'open_count':1,'bounce_count':0},
]

@app.route('/', methods=['GET','POST'])
def index():
    coaches_list = SAMPLE_COACHES.copy()
    if request.method=='POST' and 'csv_file' in request.files:
        coaches_list = _parse_csv(request.files['csv_file'])
    elif request.method=='GET' and request.args.get('location'):
        coaches_list = _fetch_coaches_from_apollo(request.args['location'])
    # Show only first 5
    return render_template('index.html', coaches=coaches_list[:5])

@app.route('/activity')
def activity():
    # Build sample activities from SAMPLE_COACHES
    activities = []
    for c in SAMPLE_COACHES:
        activities.append({
            'to_email': c['email'],
            'status':   'sent',
            'opened':   c['open_count'],
            'clicked':  0
        })
    return render_template('activity.html', activities=activities)

@app.route('/dashboard')
def dashboard():
    # Pass all SAMPLE_COACHES
    return render_template('dashboard.html', coaches=SAMPLE_COACHES)

def _parse_csv(csv_file):
    text = csv_file.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    out=[]
    for row in reader:
        out.append({
            'name': row.get('name','').strip(),
            'email': row.get('email','').strip(),
            'experience': float(row.get('experience') or 0),
            'rating': float(row.get('rating') or 0),
            'lat': float(row.get('lat') or 0),
            'lng': float(row.get('lng') or 0),
            'open_count': int(row.get('open_count') or 0),
            'bounce_count': int(row.get('bounce_count') or 0)
        })
    return out

def _fetch_coaches_from_apollo(location):
    return SAMPLE_COACHES

if __name__=='__main__':
    port = int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)
