from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app import db

class Analysis(db.Model):
    __tablename__ = 'analysis'
    __table_args__ = (
        db.UniqueConstraint('uid'),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    uid = db.Column(db.String())
    name = db.Column(db.String())
    content = db.Column(JSON)
    status = db.Column(db.String())

    def __init__(self, uid, name, content, status):
        self.uid = uid
        self.name = name
        self.content = content
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)