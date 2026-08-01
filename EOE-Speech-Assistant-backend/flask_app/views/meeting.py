from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_app import db
from flask_app.models.meeting import Meeting, Registration, TimerRecord
from flask_app.models.club import Membership, Club
import json

bp = Blueprint('meeting', __name__)

@bp.route('/clubs/<club_id>/meetings', methods=['GET'])
def list_meetings(club_id):
    """获取俱乐部例会列表"""
    meetings = Meeting.query.filter_by(club_id=club_id).order_by(Meeting.date.desc()).all()
    return jsonify([m.to_dict() for m in meetings])

@bp.route('/meetings/public', methods=['GET'])
def list_public_meetings():
    """获取所有公开活动（发现页用）"""
    status = request.args.get('status', 'preparing')
    meetings = Meeting.query.filter_by(visibility='public').order_by(Meeting.date.desc()).all()
    
    result = []
    for m in meetings:
        club = Club.query.get(m.club_id)
        data = m.to_dict()
        data['clubName'] = club.name if club else ''
        data['clubCity'] = club.city if club else ''
        data['clubDistrict'] = club.district if club else ''
        result.append(data)
    
    return jsonify(result)

@bp.route('/meetings/<meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    """获取例会详情"""
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': '例会不存在'}), 404
    
    club = Club.query.get(meeting.club_id)
    data = meeting.to_dict(include_registrations=True)
    if club:
        data['clubName'] = club.name
    return jsonify(data)

@bp.route('/clubs/<club_id>/meetings', methods=['POST'])
def create_meeting(club_id):
    """创建例会"""
    data = request.get_json() or {}
    
    meeting = Meeting(
        id=data.get('id'),
        club_id=club_id,
        theme=data.get('theme'),
        theme_direction=data.get('themeDirection'),
        sub_theme=data.get('subTheme'),
        form=data.get('form', '常规例会'),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else None,
        time=data.get('time'),
        location=data.get('location'),
        manager_id=data.get('managerId'),
        status=data.get('status', 'preparing')
    )
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 201

@bp.route('/meetings/<meeting_id>/register', methods=['POST'])
def register_role(meeting_id):
    """报名角色"""
    from flask_app.utils.jwt_helper import get_current_user_id
    user_id = get_current_user_id()
    
    data = request.get_json() or {}
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': '例会不存在'}), 404
    
    # 检查是否已报名该角色
    existing = Registration.query.filter_by(
        meeting_id=meeting_id, 
        role=data.get('role')
    ).first()
    if existing:
        return jsonify({'error': '该角色已被占用'}), 400
    
    reg = Registration(
        meeting_id=meeting_id,
        user_id=user_id,
        club_id=meeting.club_id,
        role=data.get('role'),
        guest_name=data.get('guestName'),
        source=data.get('source'),
        speech_title=data.get('speechTitle'),
        project_level=data.get('projectLevel'),
        goal=data.get('goal'),
        estimated_duration=data.get('estimatedDuration')
    )
    db.session.add(reg)
    db.session.commit()
    
    return jsonify(reg.to_dict()), 201

@bp.route('/meetings/<meeting_id>/registrations', methods=['GET'])
def get_registrations(meeting_id):
    """获取例会报名列表"""
    regs = Registration.query.filter_by(meeting_id=meeting_id).all()
    return jsonify([r.to_dict() for r in regs])

@bp.route('/meetings/<meeting_id>/timer', methods=['POST'])
def record_timer(meeting_id):
    """记录时间"""
    data = request.get_json() or {}
    
    record = TimerRecord(
        meeting_id=meeting_id,
        user_id=data.get('userId'),
        speaker_name=data.get('speakerName'),
        speech_title=data.get('speechTitle'),
        duration=data.get('duration'),
        target_min=data.get('targetMin'),
        target_max=data.get('targetMax'),
        is_overtime=data.get('isOvertime', False)
    )
    db.session.add(record)
    db.session.commit()
    
    return jsonify(record.to_dict()), 201

@bp.route('/meetings/<meeting_id>/timer', methods=['GET'])
def list_timer_records(meeting_id):
    """获取时间记录"""
    records = TimerRecord.query.filter_by(meeting_id=meeting_id).all()
    return jsonify([r.to_dict() for r in records])
