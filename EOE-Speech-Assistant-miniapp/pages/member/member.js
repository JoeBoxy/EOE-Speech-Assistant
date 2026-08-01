const api = require('../../utils/request');

Page({
  data: {
    members: [],
    loading: true
  },

  onLoad() {
    this.loadMembers();
  },

  async loadMembers() {
    try {
      const memberships = await api.get('/api/clubs/club_eoe_cn/members');
      const members = memberships.map(m => ({
        id: m.user?.id,
        name: m.user?.nickName,
        englishName: m.user?.englishName,
        role: m.type === 'officer' ? '官员' : '会员',
        officerRole: m.officerRole,
        avatar: m.user?.avatar,
        speeches: 0,
        best: 0
      }));
      this.setData({ members, loading: false });
    } catch (err) {
      console.error('加载成员失败:', err);
      this.setData({ loading: false });
    }
  },

  onMemberTap(e) {
    const memberId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/member/profile/profile?id=${memberId}`
    });
  }
});
