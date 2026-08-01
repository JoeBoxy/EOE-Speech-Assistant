#!/usr/bin/env python3
"""
初始化数据库种子数据 - EOE 中文演讲俱乐部
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app import create_app, db
from flask_app.models.club import Club, Membership
from flask_app.models.user import User
from flask_app.models.meeting import Meeting

app = create_app()

with app.app_context():
    # 清空并重建
    db.drop_all()
    db.create_all()
    print("✅ 数据库表已创建")
    
    # 创建 EOE 俱乐部
    club = Club(
        id='club_eoe_cn',
        name='EOE 中文演讲俱乐部',
        slogan='聚焦中文全品类演讲能力',
        description='EOE 中文演讲俱乐部是 Toastmasters International 旗下的中文演讲俱乐部，每周四晚定期举办例会，致力于提升会员的沟通力和领导力。',
        city='深圳',
        district='南山',
        location='宝马体验中心',
        meeting_time='每周四 19:30-21:30'
    )
    db.session.add(club)
    
    # 创建演示会员
    users_data = [
        {'id': 1, 'openid': 'tim_openid', 'name': 'Tim', 'english': 'Tim'},
        {'id': 2, 'openid': 'becky_openid', 'name': 'Becky', 'english': 'Becky'},
        {'id': 3, 'openid': 'leo_openid', 'name': 'Leo', 'english': 'Leo'},
        {'id': 4, 'openid': 'xixi_openid', 'name': '希希', 'english': 'Xixi'},
        {'id': 5, 'openid': 'yanzhi_openid', 'name': '小燕子', 'english': ''},
        {'id': 6, 'openid': 'jiahui_openid', 'name': '嘉惠', 'english': ''},
        {'id': 7, 'openid': 'tiaotiao_openid', 'name': '跳跳', 'english': ''},
        {'id': 8, 'openid': 'xuanxuan_openid', 'name': '萱萱', 'english': ''},
    ]
    
    users = {}
    for u in users_data:
        user = User(
            id=u['id'],
            wx_openid=u['openid'],
            nick_name=u['name'],
            english_name=u['english']
        )
        db.session.add(user)
        users[u['name']] = user
    
    db.session.flush()
    
    # 创建成员关系
    officer_roles = {
        '希希': '主席',
        'Becky': '教育副主席',
        '嘉惠': '会员副主席',
        'Tim': '公关副主席',
        '跳跳': '秘书长',
        '小燕子': '财务官',
        '萱萱': '接待官'
    }
    
    for name, user in users.items():
        officer = officer_roles.get(name)
        m = Membership(
            club_id='club_eoe_cn',
            user_id=user.id,
            type='member',
            officer_role=officer
        )
        db.session.add(m)
    
    # 创建示例例会
    from datetime import date
    meetings = [
        Meeting(
            id='m_eoe_048', club_id='club_eoe_cn', theme='情绪价值算不算爱',
            form='常规例会', date=date(2026, 3, 19), time='19:30-21:30',
            location='南山宝马体验中心', manager_id=users['希希'].id, status='preparing'
        ),
        Meeting(
            id='m_eoe_047', club_id='club_eoe_cn', theme='2026的4个猜想',
            form='常规例会', date=date(2026, 3, 12), time='19:30-21:30',
            location='南山宝马体验中心', manager_id=users['小燕子'].id, status='finished'
        ),
        Meeting(
            id='m_eoe_046', club_id='club_eoe_cn', theme='春节后遗症门诊',
            form='常规例会', date=date(2026, 2, 26), time='19:30-21:30',
            location='南山宝马体验中心', manager_id=users['Tim'].id, status='finished'
        ),
    ]
    for m in meetings:
        db.session.add(m)
    
    db.session.commit()
    print("✅ 种子数据已插入")
    print(f"   俱乐部: {club.name}")
    print(f"   会员: {len(users_data)} 人")
    print(f"   例会: {len(meetings)} 期")
