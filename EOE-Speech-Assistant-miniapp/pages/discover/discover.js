const api = require('../../utils/request');

Page({
  data: {
    meetings: [],
    loading: true,
    activeTab: 'upcoming' // upcoming, past
  },

  onLoad() {
    this.loadMeetings();
  },

  onPullDownRefresh() {
    this.loadMeetings().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  async loadMeetings() {
    this.setData({ loading: true });
    try {
      const meetings = await api.get('/api/meetings/public');
      // 分类：即将开始 / 历史
      const now = new Date();
      const upcoming = meetings.filter(m => new Date(m.date) >= now || m.status === 'preparing');
      const past = meetings.filter(m => new Date(m.date) < now && m.status === 'finished');
      
      this.setData({ 
        meetings: this.data.activeTab === 'upcoming' ? upcoming : past,
        allMeetings: { upcoming, past },
        loading: false 
      });
    } catch (err) {
      console.error('加载活动失败:', err);
      this.setData({ loading: false });
    }
  },

  onTabTap(e) {
    const tab = e.currentTarget.dataset.tab;
    const { allMeetings } = this.data;
    this.setData({
      activeTab: tab,
      meetings: tab === 'upcoming' ? allMeetings.upcoming : allMeetings.past
    });
  },

  onMeetingTap(e) {
    const meetingId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/meeting/detail/detail?id=${meetingId}&type=meeting`
    });
  },

  onRegisterTap(e) {
    const meetingId = e.currentTarget.dataset.id;
    // 跳转到例会页直接报名
    wx.switchTab({ url: '/pages/meeting/meeting' });
  },

  onSearch() {
    wx.showToast({ title: '搜索功能开发中', icon: 'none' });
  }
});
