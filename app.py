import os, itertools, requests, openai, smtplib
from flask import Flask, render_template, request, redirect, url_for
from email.mime.text import MIMEText

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
APOLLO_KEY     = os.getenv("APOLLO_API_KEY")
SMTP_HOST      = os.getenv("SMTP_HOST")
ACCOUNTS       = [
    (os.getenv("SMTP_USER_1"), os.getenv("SMTP_PASS_1")),
    (os.getenv("SMTP_USER_2"), os.getenv("SMTP_PASS_2")),
]
account_cycle = itertools.cycle(ACCOUNTS)
GENERIC_SUBJECT = os.getenv("GENERIC_EMAIL_SUBJECT")
with open(os.getenv("GENERIC_EMAIL_BODY_PATH"), 'r') as f:
    GENERIC_BODY = f.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titles = request.form.getlist('title')
        run_batch(titles)
        return redirect(url_for('running'))
    sample_titles = ["Leadership Coach", "Career Coach", "Life Coach"]
    return render_template('index.html', titles=sample_titles)

@app.route('/running')
def running():
    return "Batch started! Check your logs on Railway/Render."

def fetch_coaches(titles):
    resp = requests.get(
      "https://api.apollo.io/v1/coaches",
      headers={"Authorization": f"Bearer {APOLLO_KEY}"},
      params={"specialties": ",".join(titles)}
    )
    return resp.json().get("coaches", [])

def personalize_first_line(coach):
    prompt = (f"You’re emailing {coach['first_name']} "
              f"{coach['last_name']} who specializes in "
              f"{', '.join(coach.get('specialties', []))}. "
              "Write one warm, concise opening sentence.")
    return openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt, max_tokens=40, temperature=0.7
    ).choices[0].text.strip()

def send_email(to_email, first_line):
    from_email, pwd = next(account_cycle)
    msg = MIMEText(f"<p>{first_line}</p>\n{GENERIC_BODY}", 'html')
    msg['Subject'], msg['From'], msg['To'] = GENERIC_SUBJECT, from_email, to_email
    s = smtplib.SMTP(SMTP_HOST, 587)
    s.starttls(); s.login(from_email, pwd)
    s.send_message(msg); s.quit()

def run_batch(titles):
    for coach in fetch_coaches(titles):
        line = personalize_first_line(coach)
        send_email(coach['email'], line)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
