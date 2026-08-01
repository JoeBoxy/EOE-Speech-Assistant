const app = getApp();

Page({
  data: {
    userInfo: null,
    isLoggedIn: false,
    myClubs: [
      { id: 'club_eoe_cn', name: 'EOE 中文演讲俱乐部', role: '会员', officerRole: '' }
    ],
    isOfficer: false
  },

  onLoad() {
    this.setData({
      userInfo: app.globalData.userInfo,
      isLoggedIn: app.globalData.isLoggedIn
    });
    
    app.userInfoReadyCallback = (userInfo) => {
      this.setData({ userInfo, isLoggedIn: true });
    };
  },

  onShow() {
    this.setData({
      userInfo: app.globalData.userInfo,
      isLoggedIn: app.globalData.isLoggedIn
    });
  },

  onLogin() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        const userInfo = res.userInfo;
        app.setLoginState(true, userInfo);
        this.setData({ userInfo, isLoggedIn: true });
      }
    });
  },

  onClubTap(e) {
    const clubId = e.currentTarget.dataset.id;
    wx.showToast({ title: `切换到 ${clubId}`, icon: 'none' });
  },

  onAdminTap() {
    wx.navigateTo({ url: '/pages/admin/admin' });
  },

  onSettingsTap() {
    wx.showToast({ title: '设置开发中', icon: 'none' });
  },

  onAboutTap() {
    wx.showModal({
      title: '关于 EOE',
      content: 'EOE演讲线上助手\n免费的 Toastmasters 工具平台',
      showCancel: false
    });
  }
});
