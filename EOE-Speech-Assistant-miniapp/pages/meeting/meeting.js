const app = getApp();
const api = require('../../utils/request');

Page({
  data: {
    currentClub: null,
    currentMeeting: null,
    registrations: [],
    roleGrid: [],
    userRole: 'guest',
    loading: true
  },

  onLoad() {
    const currentClub = app.globalData.currentClub;
    this.setData({ currentClub });
    this.loadCurrentMeeting();
  },

  onShow() {
    this.loadCurrentMeeting();
  },

  async loadCurrentMeeting() {
    try {
      const meetings = await api.get(`/api/clubs/club_eoe_cn/meetings`);
      const currentMeeting = meetings.find(m => m.status === 'preparing') || meetings[0];
      if (!currentMeeting) {
        this.setData({ loading: false });
        return;
      }
      
      // 获取报名详情
      const detail = await api.get(`/api/meetings/${currentMeeting.id}`);
      const registrations = detail.registrations || [];
      
      const roles = this.buildRolesFromRegistrations(registrations);
      const roleGrid = this.buildRoleGrid(roles);
      
      this.setData({ 
        currentMeeting: detail,
        registrations,
        roleGrid,
        loading: false 
      });
    } catch (err) {
      console.error('加载例会失败:', err);
      this.setData({ loading: false });
    }
  },

  buildRolesFromRegistrations(regs) {
    const roles = {
      host: null,
      tableTopicsMaster: null,
      timer: null,
      grammarian: null,
      generalEvaluator: null,
      preparedSpeaker1: null,
      preparedSpeaker2: null,
      evaluator1: null,
      evaluator2: null,
      tableTopics: []
    };
    
    const roleMap = {
      'host': 'host',
      'tableTopicsMaster': 'tableTopicsMaster',
      'timer': 'timer',
      'grammarian': 'grammarian',
      'generalEvaluator': 'generalEvaluator',
      'preparedSpeaker1': 'preparedSpeaker1',
      'preparedSpeaker2': 'preparedSpeaker2',
      'evaluator1': 'evaluator1',
      'evaluator2': 'evaluator2',
      'tableTopicsSpeaker': 'tableTopics'
    };
    
    regs.forEach(r => {
      const key = roleMap[r.role];
      if (key === 'tableTopics') {
        roles.tableTopics.push({
          name: r.guestName || '会员',
          userId: r.userId,
          isGuest: !r.userId
        });
      } else if (key && roles[key] !== undefined) {
        roles[key] = {
          name: r.guestName || '会员',
          userId: r.userId,
          title: r.speechTitle
        };
      }
    });
    
    return roles;
  },

  buildRoleGrid(roles) {
    return [
      [
        { key: 'host', label: '主持人', data: roles.host },
        { key: 'tableTopicsMaster', label: '即兴主理', data: roles.tableTopicsMaster },
        { key: 'timer', label: '时间官', data: roles.timer }
      ],
      [
        { key: 'preparedSpeaker1', label: '备稿1', data: roles.preparedSpeaker1 },
        { key: 'preparedSpeaker2', label: '备稿2', data: roles.preparedSpeaker2 },
        { key: 'generalEvaluator', label: '总点评', data: roles.generalEvaluator }
      ],
      [
        { key: 'grammarian', label: '语法官', data: roles.grammarian },
        { key: 'evaluator1', label: '备稿点评1', data: roles.evaluator1 },
        { key: 'evaluator2', label: '备稿点评2', data: roles.evaluator2 }
      ]
    ];
  },

  onRoleTap(e) {
    const { key, label } = e.currentTarget.dataset;
    const { userRole, currentMeeting } = this.data;
    
    if (userRole === 'guest' && key !== 'tableTopics') {
      wx.showModal({
        title: '会员专享',
        content: '成为会员后可报名核心角色',
        showCancel: false
      });
      return;
    }

    if (currentMeeting.roles[key]) {
      wx.showModal({
        title: '角色已被占用',
        content: `${label} 已由 ${currentMeeting.roles[key].name} 担任`,
        showCancel: false
      });
      return;
    }

    wx.showModal({
      title: `报名 ${label}`,
      content: '确认报名该角色？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '报名成功', icon: 'success' });
          // TODO: 调用后端 API
        }
      }
    });
  },

  onTableTopicsTap() {
    wx.showModal({
      title: '报名即兴演讲',
      content: '确认报名即兴演讲环节？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '报名成功', icon: 'success' });
        }
      }
    });
  },

  onVoteTap() {
    wx.navigateTo({ url: '/pages/meeting/vote/vote' });
  },

  onTimerTap() {
    wx.navigateTo({ url: '/pages/meeting/timer/timer' });
  },

  onMinutesTap() {
    wx.navigateTo({ url: '/pages/meeting/minutes/minutes' });
  },

  onHostConsoleTap() {
    const meetingId = this.data.currentMeeting?.id || 'm_eoe_048';
    wx.navigateTo({ url: `/pages/meeting/host-console/host-console?meetingId=${meetingId}` });
  },

  onHistoryTap() {
    wx.showToast({ title: '历史例会开发中', icon: 'none' });
  }
});
