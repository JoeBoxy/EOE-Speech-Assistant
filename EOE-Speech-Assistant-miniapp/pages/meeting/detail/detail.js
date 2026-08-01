const api = require('../../utils/request');

Page({
  data: {
    type: 'club',
    club: null,
    meeting: null,
    meetings: []
  },

  onLoad(options) {
    const type = options.type || 'club';
    this.setData({ type });
    
    if (type === 'meeting') {
      const meetingId = options.id;
      this.loadMeetingDetail(meetingId);
    } else {
      const clubId = options.clubId || options.id || 'club_eoe_cn';
      this.loadClubDetail(clubId);
    }
  },

  async loadClubDetail(clubId) {
    try {
      const club = await api.get(`/api/clubs/${clubId}`);
      const meetings = await api.get(`/api/clubs/${clubId}/meetings`);
      this.setData({ club, meetings });
    } catch (err) {
      console.error('加载俱乐部详情失败:', err);
    }
  },

  async loadMeetingDetail(meetingId) {
    try {
      const meeting = await api.get(`/api/meetings/${meetingId}`);
      // 同时加载俱乐部信息
      const club = await api.get(`/api/clubs/${meeting.clubId}`);
      this.setData({ meeting, club });
    } catch (err) {
      console.error('加载活动详情失败:', err);
    }
  },

  onRegisterTap() {
    wx.switchTab({ url: '/pages/meeting/meeting' });
  },

  onMeetingTap(e) {
    const meetingId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/meeting/detail/detail?id=${meetingId}&type=meeting`
    });
  },

  onJoinTap() {
    wx.showModal({
      title: '加入俱乐部',
      content: '申请加入 EOE 中文演讲俱乐部？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '申请已提交', icon: 'success' });
        }
      }
    });
  }
});
