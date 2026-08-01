const api = require('../../../utils/request');

Page({
  data: {
    meetingId: '',
    agenda: [
      { id: 'open', label: '主席开场', duration: 5, completed: false },
      { id: 'prepared1', label: '备稿演讲 1', duration: 7, completed: false, speaker: 'Tim' },
      { id: 'prepared2', label: '备稿演讲 2', duration: 7, completed: false, speaker: '' },
      { id: 'tableTopics', label: '即兴环节', duration: 15, completed: false },
      { id: 'evaluation', label: '点评环节', duration: 10, completed: false },
      { id: 'vote', label: '投票颁奖', duration: 5, completed: false }
    ],
    currentIndex: -1,
    elapsed: 0,
    isRunning: false,
    timerId: null,
    totalPlanned: 49,
    totalElapsed: 0,
    completedCount: 0
  },

  onLoad(options) {
    const meetingId = options.meetingId || 'm_eoe_048';
    this.setData({ meetingId });
  },

  onAgendaTap(e) {
    const index = e.currentTarget.dataset.index;
    const { agenda, currentIndex, isRunning } = this.data;
    
    if (currentIndex >= 0 && currentIndex !== index && isRunning) {
      this.completeCurrentAndStart(index);
    } else if (currentIndex === index) {
      if (isRunning) {
        this.pauseTimer();
      } else {
        this.startTimer();
      }
    } else {
      this.startItem(index);
    }
  },

  startItem(index) {
    this.pauseTimer();
    const { agenda } = this.data;
    agenda.forEach((item, i) => {
      if (i > index) item.completed = false;
    });
    
    this.setData({
      currentIndex: index,
      elapsed: 0,
      isRunning: true,
      agenda: [...agenda],
      completedCount: agenda.filter(a => a.completed).length
    });
    
    this.data.timerId = setInterval(() => {
      this.setData({
        elapsed: this.data.elapsed + 1,
        totalElapsed: this.data.totalElapsed + 1
      });
    }, 1000);
  },

  completeCurrentAndStart(nextIndex) {
    const { agenda, currentIndex, elapsed } = this.data;
    agenda[currentIndex].completed = true;
    agenda[currentIndex].actualDuration = Math.floor(elapsed / 60 * 10) / 10;
    
    this.pauseTimer();
    this.startItem(nextIndex);
  },

  startTimer() {
    if (this.data.isRunning) return;
    this.setData({ isRunning: true });
    this.data.timerId = setInterval(() => {
      this.setData({
        elapsed: this.data.elapsed + 1,
        totalElapsed: this.data.totalElapsed + 1
      });
    }, 1000);
  },

  pauseTimer() {
    if (!this.data.isRunning) return;
    clearInterval(this.data.timerId);
    this.setData({ isRunning: false });
  },

  onCompleteTap() {
    const { agenda, currentIndex } = this.data;
    if (currentIndex < 0) return;
    
    agenda[currentIndex].completed = true;
    agenda[currentIndex].actualDuration = Math.floor(this.data.elapsed / 60 * 10) / 10;
    
    this.pauseTimer();
    
    const nextIndex = currentIndex + 1;
    if (nextIndex < agenda.length) {
      this.setData({ agenda: [...agenda], completedCount: agenda.filter(a => a.completed).length });
      setTimeout(() => this.startItem(nextIndex), 300);
    } else {
      this.setData({ currentIndex: -1, elapsed: 0, agenda: [...agenda], completedCount: agenda.filter(a => a.completed).length });
      wx.showToast({ title: '会议结束 🎉', icon: 'none' });
    }
  },

  onResetTap() {
    wx.showModal({
      title: '重置议程',
      content: '确定重置所有环节进度？',
      success: (res) => {
        if (res.confirm) {
          this.pauseTimer();
          const agenda = this.data.agenda.map(item => ({
            ...item,
            completed: false,
            actualDuration: undefined
          }));
          this.setData({ agenda, currentIndex: -1, elapsed: 0, totalElapsed: 0, completedCount: 0 });
        }
      }
    });
  },

  formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  },

  getProgressColor(elapsed, plannedMinutes) {
    const plannedSeconds = plannedMinutes * 60;
    const ratio = elapsed / plannedSeconds;
    if (ratio < 0.7) return '#5a7c5a';
    if (ratio < 1) return '#c96442';
    return '#b53333';
  },

  onUnload() {
    clearInterval(this.data.timerId);
  }
});
