from flask import Blueprint, request, jsonify
from flask_app import db
from flask_app.models.meeting import Meeting
import json

bp = Blueprint('vote', __name__)

@bp.route('/meetings/<meeting_id>/vote', methods=['GET'])
def get_vote_status(meeting_id):
    """获取投票状态和候选人"""
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': '例会不存在'}), 404
    
    # 从 minutes 或单独字段读取投票配置
    minutes = json.loads(meeting.minutes) if meeting.minutes else {}
    vote_config = minutes.get('voteConfig', {})
    vote_results = json.loads(meeting.vote_results) if meeting.vote_results else {}
    
    return jsonify({
        'meetingId': meeting_id,
        'voteOpen': minutes.get('voteOpen', False),
        'candidates': vote_config,
        'results': vote_results
    })

@bp.route('/meetings/<meeting_id>/vote', methods=['POST'])
def cast_vote(meeting_id):
    """提交投票"""
    from flask_app.utils.jwt_helper import get_current_user_id
    voter_id = get_current_user_id()
    if not voter_id:
        return jsonify({'error': '未登录'}), 401
    
    data = request.get_json() or {}
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': '例会不存在'}), 404
    
    # 读取现有结果
    results = json.loads(meeting.vote_results) if meeting.vote_results else {}
    
    # 记录投票
    for category, candidate_id in data.items():
        if category not in results:
            results[category] = {}
        if candidate_id not in results[category]:
            results[category][candidate_id] = 0
        results[category][candidate_id] += 1
    
    meeting.vote_results = json.dumps(results)
    db.session.commit()
    
    return jsonify({'success': True, 'results': results})

@bp.route('/meetings/<meeting_id>/vote/config', methods=['PUT'])
def set_vote_config(meeting_id):
    """设置投票候选人（官员权限）"""
    data = request.get_json() or {}
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({'error': '例会不存在'}), 404
    
    minutes = json.loads(meeting.minutes) if meeting.minutes else {}
    minutes['voteConfig'] = data.get('candidates', {})
    minutes['voteOpen'] = data.get('voteOpen', False)
    meeting.minutes = json.dumps(minutes)
    db.session.commit()
    
    return jsonify({'success': True})
