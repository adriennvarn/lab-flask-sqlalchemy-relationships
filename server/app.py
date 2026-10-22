#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes


@app.route("/events")
def get_events():
    events = Event.query.all()
    if events:
        body = [
            {
                "id": e.id,
                "name": e.name,
                "location": e.location,
            }
            for e in events
        ]
        status = 200
    else:
        body = {"error": "No events found"}
        status = 404

    return make_response(body, status)


@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    sessions = event.sessions if event else None

    if sessions:
        body = [
            {
                "id": s.id,
                "title": s.title,
                "start_time": s.start_time.isoformat(),
            }
            for s in sessions
        ]
        status = 200
    else:
        body = {"error": "Event not found"}
        status = 404

    return make_response(body, status)


@app.route("/speakers")
def get_speakers():
    speakers = Speaker.query.all()

    if speakers:
        body = [
            {
                "id": sp.id,
                "name": sp.name,
            }
            for sp in speakers
        ]
        status = 200
    else:
        body = {"error": "No speakers found."}
        status = 404

    return make_response(body, status)


@app.route("/speakers/<int:id>")
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()

    if speaker:
        body = {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available",
        }
        status = 200
    else:
        body = {"error": "Speaker not found"}
        status = 404

    return make_response(body, status)


@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    speakers = session.speakers if session else None

    if speakers:
        body = [
            {
                "id": sp.id,
                "name": sp.name,
                "bio_text": sp.bio.bio_text if sp.bio else "No bio available",
            }
            for sp in speakers
        ]
        status = 200
    else:
        body = {"error": "Session not found"}
        status = 404
    
    return make_response(body, status)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
