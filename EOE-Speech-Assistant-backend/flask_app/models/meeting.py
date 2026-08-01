from datetime import datetime
from flask_app import db
import json

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.String(32), primary_key=True)
    club_id = db.Column(db.String(32), db.ForeignKey('clubs.id'), nullable=False)
    
    theme = db.Column(db.String(256), nullable=False)
    theme_direction = db.Column(db.String(64), nullable=True)
    sub_theme = db.Column(db.String(128), nullable=True)
    form = db.Column(db.String(32), default='常规例会')  # 常规例会/工作坊/辩论赛/读书会/特殊例会
    
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(32), nullable=True)
    location = db.Column(db.String(256), nullable=True)
    
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # preparing, signing, ongoing, finished
    status = db.Column(db.String(16), default='preparing')
    visibility = db.Column(db.String(16), default='public')
    
    # Vote results stored as JSON
    vote_results = db.Column(db.Text, nullable=True)
    minutes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    club = db.relationship('Club', back_populates='meetings')
    registrations = db.relationship('Registration', back_populates='meeting', lazy='dynamic')
    timer_records = db.relationship('TimerRecord', back_populates='meeting', lazy='dynamic')
    evaluations = db.relationship('Evaluation', back_populates='meeting', lazy='dynamic')
    
    def to_dict(self, include_registrations=False):
        data = {
            'id': self.id,
            'clubId': self.club_id,
            'theme': self.theme,
            'themeDirection': self.theme_direction,
            'subTheme': self.sub_theme,
            'form': self.form,
            'date': self.date.isoformat() if self.date else None,
            'time': self.time,
            'location': self.location,
            'managerId': self.manager_id,
            'status': self.status,
            'visibility': self.visibility,
            'voteResults': json.loads(self.vote_results) if self.vote_results else {},
            'minutes': json.loads(self.minutes) if self.minutes else {},
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
        if include_registrations:
            data['registrations'] = [r.to_dict() for r in self.registrations]
        return data


class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.String(32), db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    club_id = db.Column(db.String(32), db.ForeignKey('clubs.id'), nullable=False)
    
    # 角色类型
    role = db.Column(db.String(32), nullable=False)
    # 嘉宾报名时填写的名字
    guest_name = db.Column(db.String(64), nullable=True)
    source = db.Column(db.String(64), nullable=True)
    
    # 备稿演讲信息
    speech_title = db.Column(db.String(256), nullable=True)
    project_level = db.Column(db.String(32), nullable=True)
    goal = db.Column(db.String(512), nullable=True)
    estimated_duration = db.Column(db.Integer, nullable=True)
    actual_duration = db.Column(db.Float, nullable=True)
    
    attended = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    meeting = db.relationship('Meeting', back_populates='registrations')
    user = db.relationship('User', back_populates='registrations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meetingId': self.meeting_id,
            'userId': self.user_id,
            'clubId': self.club_id,
            'role': self.role,
            'guestName': self.guest_name,
            'source': self.source,
            'speechTitle': self.speech_title,
            'projectLevel': self.project_level,
            'goal': self.goal,
            'estimatedDuration': self.estimated_duration,
            'actualDuration': self.actual_duration,
            'attended': self.attended,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class TimerRecord(db.Model):
    __tablename__ = 'timer_records'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.String(32), db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    speaker_name = db.Column(db.String(64), nullable=False)
    speech_title = db.Column(db.String(256), nullable=True)
    duration = db.Column(db.Float, nullable=False)  # seconds
    target_min = db.Column(db.Integer, nullable=True)
    target_max = db.Column(db.Integer, nullable=True)
    is_overtime = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    meeting = db.relationship('Meeting', back_populates='timer_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meetingId': self.meeting_id,
            'speakerName': self.speaker_name,
            'speechTitle': self.speech_title,
            'duration': self.duration,
            'targetMin': self.target_min,
            'targetMax': self.target_max,
            'isOvertime': self.is_overtime
        }


class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.String(32), db.ForeignKey('meetings.id'), nullable=False)
    club_id = db.Column(db.String(32), db.ForeignKey('clubs.id'), nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    strengths = db.Column(db.Text, nullable=True)
    suggestions = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    meeting = db.relationship('Meeting', back_populates='evaluations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meetingId': self.meeting_id,
            'speakerId': self.speaker_id,
            'evaluatorId': self.evaluator_id,
            'strengths': self.strengths,
            'suggestions': self.suggestions,
            'isPublic': self.is_public
        }
