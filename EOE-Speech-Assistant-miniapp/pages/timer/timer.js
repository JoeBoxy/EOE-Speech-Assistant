const COLOR_OPTIONS = [
  { id: 'green', label: '绿牌' },
  { id: 'yellow', label: '黄牌' },
  { id: 'red', label: '红牌' }
];

const SHARE_TITLE = 'EOE演讲线上助手｜演讲时间牌';
const SHARE_PATH = '/pages/timer/timer';

Page({
  data: {
    colorOptions: COLOR_OPTIONS,
    selectedColor: '',
    selectedLabel: '',
    elapsed: 0,
    displayTime: '00:00',
    isRunning: false,
    hasStarted: false
  },

  onLoad() {
    this.timerId = null;
    this.timerStartedAt = 0;
    this.timerBaseElapsed = 0;
    wx.setKeepScreenOn({ keepScreenOn: true });
    this.enableShareMenu();
  },

  enableShareMenu() {
    if (typeof wx.showShareMenu !== 'function') return;

    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  onShareAppMessage() {
    return {
      title: SHARE_TITLE,
      path: SHARE_PATH
    };
  },

  onShareTimeline() {
    return {
      title: SHARE_TITLE,
      query: ''
    };
  },

  onSelectColor(event) {
    const color = event.currentTarget.dataset.color;
    const selected = COLOR_OPTIONS.find((item) => item.id === color);

    if (!selected) return;

    this.setData({
      selectedColor: selected.id,
      selectedLabel: selected.label
    });

    if (!this.data.hasStarted) {
      this.startTimer();
    }
  },

  onExitDisplay() {
    this.setData({
      selectedColor: '',
      selectedLabel: ''
    });
  },

  startTimer() {
    if (this.data.isRunning) return;

    this.timerBaseElapsed = this.data.elapsed;
    this.timerStartedAt = Date.now();
    this.setData({
      isRunning: true,
      hasStarted: true
    });

    this.timerId = setInterval(() => {
      const elapsed = this.getCurrentElapsed();
      this.setData({
        elapsed,
        displayTime: this.formatTime(elapsed)
      });
    }, 250);
  },

  onPauseTimer() {
    if (!this.data.isRunning) return;

    const elapsed = this.getCurrentElapsed();
    clearInterval(this.timerId);
    this.timerId = null;
    this.setData({
      elapsed,
      displayTime: this.formatTime(elapsed),
      isRunning: false
    });
  },

  onResumeTimer() {
    this.startTimer();
  },

  onResetTimer() {
    clearInterval(this.timerId);
    this.timerId = null;
    this.timerStartedAt = 0;
    this.timerBaseElapsed = 0;
    this.setData({
      elapsed: 0,
      displayTime: '00:00',
      isRunning: false,
      hasStarted: false
    });
  },

  getCurrentElapsed() {
    if (!this.data.isRunning) return this.data.elapsed;

    return this.timerBaseElapsed + Math.floor((Date.now() - this.timerStartedAt) / 1000);
  },

  formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
  },

  onUnload() {
    clearInterval(this.timerId);
    wx.setKeepScreenOn({ keepScreenOn: false });
  }
});
