from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app import db

class Analysis(db.Model):
    __tablename__ = 'analysis'

    uid = db.Column(db.String(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    name = db.Column(db.String())
    content = db.Column(JSON)
    status = db.Column(db.String())

    def __repr__(self):
        return '<uid {}>'.format(self.uid)