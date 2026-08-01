from flask import Blueprint, request, jsonify
from flask_app import db
from flask_app.models.club import Club, Membership
from flask_app.models.user import User

bp = Blueprint('club', __name__)

@bp.route('/clubs', methods=['GET'])
def list_clubs():
    """获取俱乐部列表"""
    clubs = Club.query.filter_by(status='active').all()
    return jsonify([c.to_dict() for c in clubs])

@bp.route('/clubs/<club_id>', methods=['GET'])
def get_club(club_id):
    """获取俱乐部详情"""
    club = Club.query.get(club_id)
    if not club:
        return jsonify({'error': '俱乐部不存在'}), 404
    return jsonify(club.to_dict(include_members=True))

@bp.route('/clubs', methods=['POST'])
def create_club():
    """创建俱乐部（管理员权限）"""
    data = request.get_json() or {}
    
    club = Club(
        id=data.get('id'),
        name=data.get('name'),
        slogan=data.get('slogan'),
        description=data.get('description'),
        city=data.get('city'),
        district=data.get('district'),
        location=data.get('location'),
        meeting_time=data.get('meetingTime')
    )
    db.session.add(club)
    db.session.commit()
    
    return jsonify(club.to_dict()), 201

@bp.route('/clubs/<club_id>/members', methods=['GET'])
def list_members(club_id):
    """获取俱乐部成员列表"""
    memberships = Membership.query.filter_by(club_id=club_id).all()
    return jsonify([m.to_dict() for m in memberships])

@bp.route('/clubs/<club_id>/join', methods=['POST'])
def join_club(club_id):
    """加入俱乐部"""
    from flask_app.utils.jwt_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未登录'}), 401
    
    club = Club.query.get(club_id)
    if not club:
        return jsonify({'error': '俱乐部不存在'}), 404
    
    # 检查是否已加入
    existing = Membership.query.filter_by(club_id=club_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': '已经是成员'}), 400
    
    data = request.get_json() or {}
    membership = Membership(
        club_id=club_id,
        user_id=user_id,
        type=data.get('type', 'guest'),
        source=data.get('source')
    )
    db.session.add(membership)
    db.session.commit()
    
    return jsonify(membership.to_dict()), 201
