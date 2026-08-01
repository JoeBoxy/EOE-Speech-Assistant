const auth = require('./utils/auth');

App({
  onLaunch: function () {
    console.log('EOE演讲线上助手小程序启动');
    this.checkLoginStatus();
  },

  checkLoginStatus: function() {
    if (auth.isLoggedIn()) {
      auth.fetchUserInfo()
        .then((userInfo) => {
          this.globalData.userInfo = userInfo;
          this.globalData.isLoggedIn = true;
          if (this.userInfoReadyCallback) {
            this.userInfoReadyCallback(userInfo);
          }
        })
        .catch((err) => {
          console.error('获取用户信息失败:', err);
          if (err.message && err.message.includes('过期')) {
            auth.clearLoginState();
            this.globalData.isLoggedIn = false;
            this.globalData.userInfo = null;
          }
        });
    } else {
      this.globalData.isLoggedIn = false;
    }
  },

  setLoginState: function(isLoggedIn, userInfo = null) {
    this.globalData.isLoggedIn = isLoggedIn;
    this.globalData.userInfo = userInfo;
  },

  globalData: {
    userInfo: null,
    isLoggedIn: false,
    currentClub: {
      id: 'club_eoe_cn',
      name: 'EOE 中文演讲俱乐部',
      slogan: '聚焦中文全品类演讲能力',
      memberCount: 32
    }
  }
});
