from datetime import datetime
from flask_app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    wx_openid = db.Column(db.String(128), unique=True, nullable=False, index=True)
    wx_unionid = db.Column(db.String(128), nullable=True)
    
    # Profile
    nick_name = db.Column(db.String(64), nullable=True)
    english_name = db.Column(db.String(64), nullable=True)
    avatar_url = db.Column(db.String(512), nullable=True)
    region = db.Column(db.String(64), nullable=True)
    profession = db.Column(db.String(128), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('Membership', back_populates='user', lazy='dynamic')
    registrations = db.relationship('Registration', back_populates='user', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nickName': self.nick_name,
            'englishName': self.english_name,
            'avatar': self.avatar_url,
            'region': self.region,
            'profession': self.profession,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
