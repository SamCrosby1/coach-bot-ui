import os
import itertools
import requests
import openai
import smtplib

from flask import Flask, render_template, request, redirect, url_for
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key    = os.getenv("OPENAI_API_KEY")
APOLLO_KEY        = os.getenv("APOLLO_API_KEY")
SMTP_HOST         = os.getenv("SMTP_HOST")
ACCOUNTS          = [
    (os.getenv("SMTP_USER_1"), os.getenv("SMTP_PASS_1")),
    (os.getenv("SMTP_USER_2"), os.getenv("SMTP_PASS_2")),
]
account_cycle     = itertools.cycle(ACCOUNTS)

GENERIC_SUBJECT   = os.getenv("GENERIC_EMAIL_SUBJECT")
body_path         = os.getenv("GENERIC_EMAIL_BODY_PATH", "templates/generic_body.html")
with open(body_path, 'r') as f:
    GENERIC_BODY = f.read()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/coaches', methods=['GET'])
def coaches_page():
    coaches = []
    return render_template('coaches.html', coaches=coaches)


@app.route('/activity', methods=['GET'])
def activity_page():
    activity = []
    return render_template('activity.html', activity=activity)


@app.route('/import', methods=['POST'])
def import_csv():
    csv_file = request.files.get('csv_file')
    if csv_file:
        pass
    return redirect(url_for('coaches_page'))


@app.route('/search', methods=['POST'])
def search_apollo():
    specialties = request.form.get('specialties', '')
    location    = request.form.get('location', '')
    experience  = request.form.get('experience', '')
    return redirect(url_for('coaches_page'))


def send_email(to_email, first_line):
    from_email, pwd = next(account_cycle)
    msg = MIMEText(f"<p>{first_line}</p>\n{GENERIC_BODY}", 'html')
    msg['Subject'], msg['From'], msg['To'] = GENERIC_SUBJECT, from_email, to_email
    with smtplib.SMTP(SMTP_HOST, 587) as server:
        server.starttls()
        server.login(from_email, pwd)
        server.send_message(msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
