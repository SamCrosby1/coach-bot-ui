import os, csv, random
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    # Parse filters & sorting
    args = request.values
    filters = {
        'location':    args.get('location','').strip(),
        'specialty':   args.get('specialty','').strip(),
        'min_exp':     float(args.get('min_exp') or 0),
        'max_exp':     float(args.get('max_exp') or 999),
        'min_rating':  float(args.get('min_rating') or 0),
        'radius':      float(args.get('radius') or 9999),
        'sort_by':     args.get('sort_by','')
    }
    # Load from CSV or Apollo stub
    if request.method=='POST' and 'csv_file' in request.files:
        coaches = _parse_csv(request.files['csv_file'])
    else:
        coaches = _fetch_coaches_from_apollo(filters)

    # Apply simple in-memory filters & sorting (stub logic)
    filtered = []
    for c in coaches:
        if filters['min_exp'] <= c.get('experience',0) <= filters['max_exp'] \
        and c.get('rating',0) >= filters['min_rating']:
            filtered.append(c)
    if filters['sort_by'] in ('name','rating','experience','distance'):
        filtered.sort(key=lambda x: x.get(filters['sort_by'],''))

    return render_template('index.html', coaches=filtered)

@app.route('/activity')
def activity():
    # Stub analytics data
    # Trend: last 7 days
    trend = []
    for i in range(7):
        trend.append({
            'date': f'Day-{7-i}',
            'open_rate': round(random.uniform(20,80),1),
            'click_rate': round(random.uniform(5,30),1),
            'bounce_count': random.randint(0,5)
        })
    # Top subjects
    subjects = [
        {'subject': 'Quick Question','count': random.randint(20,100)},
        {'subject': 'Opportunity for you','count': random.randint(20,100)},
        {'subject': 'Let’s connect','count': random.randint(20,100)},
    ]
    # Geo data
    geo = [
        {'name':'New York, USA','lat':40.7,'lng':-74,'clicks':random.randint(0,50)},
        {'name':'London, UK','lat':51.5,'lng':-0.1,'clicks':random.randint(0,50)},
        {'name':'Sydney, AUS','lat':-33.9,'lng':151.2,'clicks':random.randint(0,50)},
    ]
    analytics = {'trend':trend,'subjects':subjects,'geo':geo}
    return render_template('activity.html', analytics=analytics)

def _parse_csv(csv_file):
    text = csv_file.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    out=[]
    for idx,row in enumerate(reader):
        out.append({
            'id': idx,
            'name': row.get('name','').strip(),
            'email': row.get('email','').strip(),
            'experience': float(row.get('experience') or 0),
            'rating': float(row.get('rating') or 0),
            'distance': float(row.get('distance') or 0),
        })
    return out

def _fetch_coaches_from_apollo(filters):
    """
    Replace with real Apollo call, using filters dict.
    Here we stub 9 random coaches.
    """
    sample = []
    for i in range(1,10):
        sample.append({
            'id': i,
            'name': f'Coach {i}',
            'email': f'coach{i}@example.com',
            'experience': random.randint(1,15),
            'rating': round(random.uniform(3,5),1),
            'distance': random.randint(1,100)
        })
    return sample

if __name__=='__main__':
    port = int(os.getenv('PORT',5000))
    app.run(host='0.0.0.0', port=port, debug=True)
