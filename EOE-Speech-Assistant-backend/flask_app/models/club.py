from datetime import datetime
from flask_app import db

class Club(db.Model):
    __tablename__ = 'clubs'
    
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    slogan = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    logo = db.Column(db.String(512), nullable=True)
    
    city = db.Column(db.String(64), nullable=True)
    district = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(256), nullable=True)
    meeting_time = db.Column(db.String(64), nullable=True)  # e.g. "每周四 19:30"
    
    status = db.Column(db.String(16), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('Membership', back_populates='club', lazy='dynamic')
    meetings = db.relationship('Meeting', back_populates='club', lazy='dynamic',
                               order_by='Meeting.date.desc()')
    
    def to_dict(self, include_members=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slogan': self.slogan,
            'description': self.description,
            'logo': self.logo,
            'city': self.city,
            'district': self.district,
            'location': self.location,
            'meetingTime': self.meeting_time,
            'memberCount': self.memberships.count(),
            'status': self.status
        }
        if include_members:
            officers = [m.to_dict() for m in self.memberships if m.officer_role]
            data['officerTeam'] = officers
        return data


class Membership(db.Model):
    __tablename__ = 'memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.String(32), db.ForeignKey('clubs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # guest, member, officer
    type = db.Column(db.String(16), default='guest')
    officer_role = db.Column(db.String(32), nullable=True)  # president, vpe, vpm, vppr, secretary, treasurer, saa
    
    member_since = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.String(64), nullable=True)  # 渠道来源
    status = db.Column(db.String(16), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    club = db.relationship('Club', back_populates='memberships')
    user = db.relationship('User', back_populates='memberships')
    
    def to_dict(self):
        return {
            'id': self.id,
            'clubId': self.club_id,
            'userId': self.user_id,
            'user': self.user.to_dict() if self.user else None,
            'type': self.type,
            'officerRole': self.officer_role,
            'memberSince': self.member_since.isoformat() if self.member_since else None,
            'source': self.source,
            'status': self.status
        }
