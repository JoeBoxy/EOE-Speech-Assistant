from flask import Blueprint, request, jsonify
from flask_app import db
from flask_app.models.user import User
from flask_app.utils.jwt_helper import generate_token
import httpx

bp = Blueprint('auth', __name__)

@bp.route('/auth/login', methods=['POST'])
def wx_login():
    """微信小程序登录"""
    data = request.get_json() or {}
    code = data.get('code')
    user_info = data.get('userInfo', {})
    
    if not code:
        return jsonify({'error': '缺少 code 参数'}), 400
    
    # 调用微信接口（简化：开发模式直接 mock）
    # 实际应调用 utils/wechat.py 的 code2session
    openid = f'mock_openid_{code[:10]}' if code.startswith('mock') or len(code) < 10 else code
    
    # 查找或创建用户
    user = User.query.filter_by(wx_openid=openid).first()
    if not user:
        user = User(
            wx_openid=openid,
            nick_name=user_info.get('nickName'),
            avatar_url=user_info.get('avatarUrl')
        )
        db.session.add(user)
        db.session.commit()
    else:
        # 更新用户信息
        if user_info.get('nickName'):
            user.nick_name = user_info['nickName']
        if user_info.get('avatarUrl'):
            user.avatar_url = user_info['avatarUrl']
        db.session.commit()
    
    token = generate_token(user.id)
    
    return jsonify({
        'token': token,
        'userInfo': user.to_dict()
    })

@bp.route('/user/info', methods=['GET'])
def get_user_info():
    """获取当前用户信息"""
    from flask_app.utils.jwt_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未登录'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify(user.to_dict())

@bp.route('/user/info', methods=['PUT'])
def update_user_info():
    """更新用户信息"""
    from flask_app.utils.jwt_helper import get_current_user_id
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': '未登录'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.get_json() or {}
    if 'englishName' in data:
        user.english_name = data['englishName']
    if 'region' in data:
        user.region = data['region']
    if 'profession' in data:
        user.profession = data['profession']
    
    db.session.commit()
    return jsonify(user.to_dict())
