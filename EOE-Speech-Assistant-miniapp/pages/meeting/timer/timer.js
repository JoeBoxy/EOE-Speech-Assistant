const api = require('../../utils/request');

Page({
  data: {
    meetingId: '',
    speakers: [],
    currentSpeaker: null,
    elapsed: 0,
    isRunning: false,
    timerId: null,
    records: []
  },

  onLoad(options) {
    const meetingId = options.meetingId || 'm_eoe_048';
    this.setData({ meetingId });
    this.loadTimerRecords(meetingId);
  },

  async loadTimerRecords(meetingId) {
    try {
      const records = await api.get(`/api/meetings/${meetingId}/timer`);
      this.setData({ records: records || [] });
    } catch (err) {
      console.error('加载时间记录失败:', err);
    }
  },

  onSelectSpeaker(e) {
    const speaker = e.currentTarget.dataset.speaker;
    this.setData({ currentSpeaker: speaker, elapsed: 0, isRunning: false });
  },

  onStart() {
    if (this.data.isRunning) return;
    this.setData({ isRunning: true });
    this.data.timerId = setInterval(() => {
      this.setData({ elapsed: this.data.elapsed + 1 });
    }, 1000);
  },

  onPause() {
    if (!this.data.isRunning) return;
    clearInterval(this.data.timerId);
    this.setData({ isRunning: false });
  },

  async onEnd() {
    clearInterval(this.data.timerId);
    const { currentSpeaker, elapsed, records, meetingId } = this.data;
    
    const record = {
      speakerName: currentSpeaker.name,
      speechTitle: currentSpeaker.title,
      duration: elapsed,
      targetMin: currentSpeaker.targetMin,
      targetMax: currentSpeaker.targetMax,
      isOvertime: elapsed > currentSpeaker.targetMax * 60
    };
    
    try {
      await api.post(`/api/meetings/${meetingId}/timer`, record);
      records.push(record);
      this.setData({ isRunning: false, elapsed: 0, records, currentSpeaker: null });
      wx.showToast({ title: '记录已保存', icon: 'success' });
    } catch (err) {
      wx.showToast({ title: '保存失败', icon: 'none' });
    }
  },

  formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  },

  getTimeStatus() {
    const { elapsed, currentSpeaker } = this.data;
    if (!currentSpeaker) return 'normal';
    const greenEnd = currentSpeaker.targetMin * 60;
    const yellowEnd = currentSpeaker.targetMax * 60;
    const redEnd = (currentSpeaker.targetMax + 0.5) * 60;
    if (elapsed < greenEnd) return 'green';
    if (elapsed < yellowEnd) return 'yellow';
    if (elapsed < redEnd) return 'red';
    return 'overtime';
  },

  onUnload() {
    clearInterval(this.data.timerId);
  }
});
