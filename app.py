import os, csv, random
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    # ... your existing Coach Hub logic (filters, CSV, etc.) ...
    return render_template('index.html', coaches=filtered)

@app.route('/activity')
def activity():
    # ... your existing Email Hub logic ...
    return render_template('activity.html', analytics=analytics)

@app.route('/dashboard')
def dashboard():
    """
    Dashboard: show globe points for each coach with open/bounce stats,
    and a list of coaches who opened.
    """
    # Stub: generate 20 coaches at random world coords with random open/bounce
    coaches = []
    for i in range(20):
        coaches.append({
            'name':    f'Coach {i+1}',
            'lat':     random.uniform(-60,80),
            'lng':     random.uniform(-180,180),
            'open_count':   random.randint(0,10),
            'bounce_count': random.randint(0,3)
        })
    return render_template('dashboard.html', coaches=coaches)

def _parse_csv(csv_file):
    # ... your existing parser ...
    pass

def _fetch_coaches_from_apollo(filters=None):
    # ... your existing Apollo stub ...
    pass

if __name__=='__main__':
    port = int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)
