import os, csv, random
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# A small sample of fake coaches, with lat/lng & open stats
SAMPLE_COACHES = [
    {'name':'Alice Smith','email':'alice.smith@example.com','experience':5,'rating':4.2,
     'lat':40.71,'lng':-74.00,'open_count':3,'bounce_count':0},
    {'name':'Bob Johnson','email':'bob.j@example.org','experience':8,'rating':4.8,
     'lat':51.50,'lng':-0.12,'open_count':5,'bounce_count':1},
    {'name':'Carla Davis','email':'carla.davis@coaching.io','experience':3,'rating':3.9,
     'lat':34.05,'lng':-118.24,'open_count':1,'bounce_count':0},
    {'name':'David Lee','email':'davidl@fitcoach.io','experience':10,'rating':4.5,
     'lat':35.68,'lng':139.69,'open_count':4,'bounce_count':2},
    {'name':'Eva Martínez','email':'eva.m@example.net','experience':6,'rating':4.1,
     'lat':48.85,'lng':2.35,'open_count':2,'bounce_count':0},
    {'name':'Frank Wu','email':'frank.wu@example.com','experience':7,'rating':4.7,
     'lat':-33.86,'lng':151.21,'open_count':6,'bounce_count':1},
    {'name':'Grace Kim','email':'grace.kim@coachhub.com','experience':4,'rating':4.0,
     'lat':52.52,'lng':13.40,'open_count':0,'bounce_count':0},
    {'name':'Henry Patel','email':'henry.p@example.org','experience':2,'rating':3.7,
     'lat':19.07,'lng':72.88,'open_count':3,'bounce_count':0},
    {'name':'Isabella Rossi','email':'isabella.rossi@italy.coach','experience':9,'rating':4.9,
     'lat':41.90,'lng':12.50,'open_count':7,'bounce_count':2},
]

@app.route('/', methods=['GET','POST'])
def index():
    # Always start from our sample for preview
    coaches_list = SAMPLE_COACHES.copy()

    # (You can still override via CSV or location if you want)
    if request.method=='POST' and 'csv_file' in request.files:
        coaches_list = _parse_csv(request.files['csv_file'])
    elif request.method=='GET' and request.args.get('location'):
        loc = request.args.get('location','').strip()
        coaches_list = _fetch_coaches_from_apollo(loc)

    # Show only first 5 coaches
    displayed = coaches_list[:5]
    return render_template('index.html', coaches=displayed)


@app.route('/dashboard')
def dashboard():
    # Use the same SAMPLE_COACHES for globe, but you can generate fresh too
    return render_template('dashboard.html', coaches=SAMPLE_COACHES)


@app.route('/activity')
def activity():
    # Stub analytics (unchanged from before)
    trend = [{'date':f'Day-{i}', 'open_rate':random.uniform(20,80),
              'click_rate':random.uniform(5,30),'bounce_count':random.randint(0,5)}
             for i in range(7)]
    subjects = [{'subject':s,'count':random.randint(20,100)} for s in
                ['Quick Question','Opportunity for You','Let’s Connect']]
    analytics = {'trend':trend,'subjects':subjects,'geo':[]}
    return render_template('activity.html', analytics=analytics)


def _parse_csv(csv_file):
    text = csv_file.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    out=[]
    for i,row in enumerate(reader):
        out.append({
            'name':        row.get('name','').strip(),
            'email':       row.get('email','').strip(),
            'experience':  float(row.get('experience') or 0),
            'rating':      float(row.get('rating') or 0),
            'lat':         float(row.get('lat') or 0),
            'lng':         float(row.get('lng') or 0),
            'open_count':  int(row.get('open_count') or 0),
            'bounce_count':int(row.get('bounce_count') or 0)
        })
    return out

def _fetch_coaches_from_apollo(location):
    # Just return our sample for now
    return SAMPLE_COACHES

if __name__=='__main__':
    port = int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)
