from app.extensions import celery_app
from celery.schedules import crontab
from app.models import *

from app import create_app
from config import Config

app = create_app()
app.config.from_object(Config)
app.app_context().push()

@celery_app.task
def send_reminder():

    from json import dumps
    from httplib2 import Http
    def main(username):
        url = "https://chat.googleapis.com/v1/spaces/AAAA_rUeCfE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=gEWuXk8vUSwQXG7J2it42X9ykPEsC2dwGDDS2Lt5d_g"
        app_message = {"text": f"@{username} We miss you! Join us & listen to our latest melodies."}
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
    for user in User.query.all():
        if not Visit.did_user_visit_today(user.id):
            main(user.username)
    return "Inactive users have been notified."



from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from sqlalchemy import extract
from datetime import datetime
import os

@celery_app.task
def send_report():

    def send_email(to, subject, content_body):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = 'flukeflute@music.com'
        msg['Subject'] = subject
        msg.attach(MIMEText(content_body, 'html'))
        
        client = SMTP(host='localhost', port=1025)
        client.send_message(msg)
        client.quit()

    creators = User.query.filter(User.stage_name.isnot(None)).all()

    current_dir = os.path.dirname(__file__)
    report_path = os.path.join(current_dir, 'templates', 'report.html')
    with open(report_path, 'r') as report:
        template = Template(report.read())
        for creator in creators:
            albums = Album.query.filter(Album.creator_id == creator.id, extract('month', Album.date_created) == datetime.utcnow().month).all()
            tracks = Track.query.filter(Track.creator_id == creator.id, extract('month', Track.release_date) == datetime.utcnow().month).all()
            send_email(creator.email, 'Monthly Report', template.render(tracks=tracks, albums=albums))
    return "Monthly Report Sent"


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(),
        send_reminder.s(),
        name='daily reminder'
    )

    sender.add_periodic_task(
        crontab(),
        send_report.s(),
        name='monthy report'
    )

