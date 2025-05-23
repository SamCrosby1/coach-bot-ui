import os, csv, random, math
from flask import Flask, render_template, request, url_for
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Sample coaches
SAMPLE_COACHES = [
  {'name':'Alice Smith','email':'alice@example.com','role':'Fitness','experience':5,'rating':4.2,'lat':40.71,'lng':-74.0,'open_count':1},
  {'name':'Bob Johnson','email':'bob.j@example.org','role':'Leadership','experience':8,'rating':4.8,'lat':51.50,'lng':-0.12,'open_count':0},
  {'name':'Carla Davis','email':'carla@coaching.io','role':'Business','experience':3,'rating':3.9,'lat':34.05,'lng':-118.24,'open_count':1},
  {'name':'David Lee','email':'davidl@fitcoach.io','role':'Fitness','experience':10,'rating':4.5,'lat':35.68,'lng':139.69,'open_count':1},
  {'name':'Eva Martínez','email':'eva.m@example.net','role':'Wellness','experience':6,'rating':4.1,'lat':48.85,'lng':2.35,'open_count':0},
  {'name':'Frank Wu','email':'frank.wu@example.com','role':'Leadership','experience':7,'rating':4.7,'lat':-33.86,'lng':151.21,'open_count':1},
  {'name':'Grace Kim','email':'grace.kim@coachhub.com','role':'Business','experience':4,'rating':4.0,'lat':52.52,'lng':13.40,'open_count':0},
  {'name':'Henry Patel','email':'henry.p@example.org','role':'Wellness','experience':2,'rating':3.7,'lat':19.07,'lng':72.88,'open_count':1},
  {'name':'Isabella Rossi','email':'isabella.rossi@italy.coach','role':'Fitness','experience':9,'rating':4.9,'lat':41.90,'lng':12.50,'open_count':1},
]

# Email activity sample
def make_activity():
    acts=[]
    for c in SAMPLE_COACHES:
        acts.append({
          'email': c['email'],
          'status': 'sent',
          'opened': c['open_count'],
          'bounced': 1 if random.random()<0.1 else 0,
          'visited': 1 if random.random()<0.3 else 0
        })
    return acts

@app.route('/', methods=['GET','POST'])
def index():
    # Gather coaches
    coaches = SAMPLE_COACHES.copy()
    if request.method=='POST' and 'csv_file' in request.files:
        coaches = _parse_csv(request.files['csv_file'])
    elif request.method=='GET' and request.args.get('location'):
        coaches = _search_stub(request.args)

    # Apply filters
    args = request.args
    def keep(c):
        if args.get('location') and args['location'].lower() not in c['role'].lower(): return False
        if args.get('role') and args['role'].lower() not in c['role'].lower(): return False
        if args.get('min_rating') and float(args['min_rating'])>c['rating']: return False
        if args.get('min_exp') and float(args['min_exp'])>c['experience']: return False
        return True
    filtered = [c for c in coaches if keep(c)]

    # Pagination
    page = int(request.args.get('page',1))
    per  = 5
    total = math.ceil(len(filtered)/per)
    start = (page-1)*per
    end   = start+per
    coaches_page = filtered[start:end]

    # Build next/prev querystrings
    def qs(p): 
        q = dict(request.args); q['page']=p; return urlencode(q)
    qs_prev = qs(page-1) if page>1 else ''
    qs_next = qs(page+1) if page<total else ''

    return render_template('index.html',
                           coaches=coaches_page, page=page, total_pages=total,
                           qs_prev=qs_prev, qs_next=qs_next)

@app.route('/activity')
def activity():
    activities = make_activity()
    return render_template('activity.html', activities=activities)

@app.route('/dashboard')
def dashboard():
    # Metrics
    acts = make_activity()
    total = len(acts)
    opens  = sum(a['opened'] for a in acts)
    bounces= sum(a['bounced'] for a in acts)
    replies= 0  # stub
    clicks = sum(a['visited'] for a in acts)
    metrics = [
      {'title':'Total Sent','value':total},
      {'title':'Open Rate','value':f"{opens}/{total}"},
      {'title':'Bounce Rate','value':f"{bounces}/{total}"},
      {'title':'Click Rate','value':f"{clicks}/{total}"},
      {'title':'Replies','value':replies},
    ]
    return render_template('dashboard.html',
                           coaches=SAMPLE_COACHES, analytics={'trend':[
                              {'date':d,'open':random.randint(0,total),
                               'bounce':random.randint(0,total//2),
                               'reply':random.randint(0,total//4),
                               'click':random.randint(0,total//3)}
                              for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
                            ]},
                           metrics=metrics)

def _parse_csv(f):
    text=f.stream.read().decode().splitlines()
    reader=csv.DictReader(text)
    out=[]
    for r in reader:
        out.append({k: (float(v) if k in ('experience','rating','lat','lng','open_count') else v)
           for k,v in r.items()})
    return out

def _search_stub(args):
    # ignores location stub for demo
    return SAMPLE_COACHES

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=True)
