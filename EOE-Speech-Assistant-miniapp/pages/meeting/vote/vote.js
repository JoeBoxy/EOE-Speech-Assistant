const api = require('../../utils/request');

Page({
  data: {
    meetingId: '',
    candidates: {
      bestSpeaker: [],
      bestEvaluator: [],
      bestTableTopics: []
    },
    myVotes: {
      bestSpeaker: null,
      bestEvaluator: null,
      bestTableTopics: null
    },
    hasVoted: false,
    isAdmin: true,
    voteOpen: false
  },

  onLoad(options) {
    const meetingId = options.meetingId || 'm_eoe_048';
    this.setData({ meetingId });
    this.loadVoteData(meetingId);
  },

  async loadVoteData(meetingId) {
    try {
      const data = await api.get(`/api/meetings/${meetingId}/vote`);
      this.setData({
        candidates: data.candidates || this.data.candidates,
        voteOpen: data.voteOpen || false
      });
    } catch (err) {
      console.error('加载投票数据失败:', err);
    }
  },

  onCandidateTap(e) {
    const { category, id } = e.currentTarget.dataset;
    if (!this.data.voteOpen) {
      wx.showToast({ title: '投票未开始', icon: 'none' });
      return;
    }
    if (this.data.hasVoted) {
      wx.showToast({ title: '您已投票', icon: 'none' });
      return;
    }
    const myVotes = { ...this.data.myVotes, [category]: id };
    this.setData({ myVotes });
  },

  async onSubmitVote() {
    const { myVotes, meetingId } = this.data;
    if (!myVotes.bestSpeaker || !myVotes.bestEvaluator || !myVotes.bestTableTopics) {
      wx.showToast({ title: '请完成三项投票', icon: 'none' });
      return;
    }

    wx.showModal({
      title: '确认投票',
      content: '投票后不可更改，确认提交？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await api.post(`/api/meetings/${meetingId}/vote`, myVotes);
            this.setData({ hasVoted: true });
            wx.showToast({ title: '投票成功', icon: 'success' });
          } catch (err) {
            wx.showToast({ title: '投票失败', icon: 'none' });
          }
        }
      }
    });
  },

  onToggleVote() {
    const newState = !this.data.voteOpen;
    this.setData({ voteOpen: newState });
    wx.showToast({ title: newState ? '投票已开启' : '投票已关闭', icon: 'none' });
  },

  onShowResults() {
    wx.showToast({ title: '结果展示开发中', icon: 'none' });
  }
});
