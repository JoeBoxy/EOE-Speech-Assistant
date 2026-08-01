from flask import Blueprint, request, jsonify
from flask_app import db
from flask_app.models.user import User
from flask_app.models.club import Membership
from sqlalchemy import func

bp = Blueprint('member', __name__)

@bp.route('/members/<int:user_id>/profile', methods=['GET'])
def get_member_profile(user_id):
    """获取成员个人主页"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 统计演讲次数
    from flask_app.models.meeting import Registration
    speech_count = Registration.query.filter_by(user_id=user_id).count()
    
    # 统计最佳次数（简化：从 vote_results 中统计，实际应单独建表）
    # 这里返回基础数据
    profile = user.to_dict()
    profile['stats'] = {
        'totalSpeeches': speech_count,
        'bestSpeakerCount': 0,  # TODO: 从 vote_results 统计
        'bestEvaluatorCount': 0,
        'bestTableTopicsCount': 0
    }
    
    return jsonify(profile)

@bp.route('/members/<int:user_id>/speeches', methods=['GET'])
def get_member_speeches(user_id):
    """获取成员演讲历史"""
    from flask_app.models.meeting import Registration, Meeting
    
    regs = Registration.query.filter_by(user_id=user_id).join(Meeting).order_by(Meeting.date.desc()).all()
    result = []
    for r in regs:
        meeting = Meeting.query.get(r.meeting_id)
        result.append({
            'meetingId': r.meeting_id,
            'meetingTheme': meeting.theme if meeting else '',
            'role': r.role,
            'date': meeting.date.isoformat() if meeting and meeting.date else '',
            'duration': r.actual_duration,
            'title': r.speech_title
        })
    return jsonify(result)

@bp.route('/clubs/<club_id>/members/<int:user_id>/role', methods=['PUT'])
def update_member_role(club_id, user_id):
    """更新成员角色（官员权限）"""
    data = request.get_json() or {}
    
    membership = Membership.query.filter_by(club_id=club_id, user_id=user_id).first()
    if not membership:
        return jsonify({'error': '成员不存在'}), 404
    
    membership.type = data.get('type', membership.type)
    membership.officer_role = data.get('officerRole', membership.officer_role)
    db.session.commit()
    
    return jsonify(membership.to_dict())
