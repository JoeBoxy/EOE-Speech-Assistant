App({
  onLaunch() {
    console.log('EOE演讲线上助手 · 时间牌启动');
    this.setupUpdateManager();
  },

  setupUpdateManager() {
    if (typeof wx.getUpdateManager !== 'function') {
      console.warn('当前微信版本不支持小程序更新管理');
      return;
    }

    const updateManager = wx.getUpdateManager();

    updateManager.onCheckForUpdate((result) => {
      console.log(result.hasUpdate ? '检测到小程序新版本' : '当前已是最新版本');
    });

    updateManager.onUpdateReady(() => {
      wx.showModal({
        title: '发现新版本',
        content: '新版本已准备完成，需要重启小程序后使用。',
        showCancel: false,
        confirmText: '立即重启',
        success: (result) => {
          if (result.confirm) {
            updateManager.applyUpdate();
          }
        }
      });
    });

    updateManager.onUpdateFailed(() => {
      wx.showModal({
        title: '更新失败',
        content: '新版本下载失败，请检查网络后重新打开小程序。',
        showCancel: false,
        confirmText: '我知道了'
      });
    });
  }
});
