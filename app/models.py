from datetime import datetime, date
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

    def as_dict(self):
        return { 'uid': self.uid,
                'name': self.name,
                'content': self.content,
                'status': self.status,
                'created_at': self.created_at if self.created_at is None else self.created_at.isoformat(),
                'updated_at': self.updated_at if self.updated_at is None else self.updated_at.isoformat(),
                'started_at': self.started_at if self.started_at is None else self.started_at.isoformat(),
                'ended_at': self.ended_at if self.ended_at is None else self.ended_at.isoformat()
        }
