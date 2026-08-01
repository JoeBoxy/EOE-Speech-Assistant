Page({
  data: {
    meetings: [
      { id: 'm_eoe_048', theme: '情绪价值算不算爱', date: '2026-03-19', status: 'preparing' },
      { id: 'm_eoe_047', theme: '2026的4个猜想', date: '2026-03-12', status: 'finished' }
    ]
  },

  onLoad() {
    // TODO: 验证官员权限
  },

  onCreateMeeting() {
    wx.showModal({
      title: '创建新例会',
      editable: true,
      placeholderText: '输入例会主题',
      success: (res) => {
        if (res.confirm && res.content) {
          wx.showToast({ title: '创建成功', icon: 'success' });
          // TODO: 调用后端 API
        }
      }
    });
  },

  onMeetingTap(e) {
    const meetingId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/meeting/detail/detail?id=${meetingId}`
    });
  },

  onVoteManage() {
    wx.navigateTo({ url: '/pages/meeting/vote/vote' });
  },

  onMemberManage() {
    wx.showToast({ title: '成员管理开发中', icon: 'none' });
  }
});
