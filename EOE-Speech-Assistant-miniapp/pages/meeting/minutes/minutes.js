const api = require('../../utils/request');

Page({
  data: {
    meeting: {
      id: 'm_eoe_048',
      clubName: 'EOE 中文演讲俱乐部',
      theme: '情绪价值算不算爱',
      date: '2026-03-19',
      number: '第48期',
      winners: {
        bestSpeaker: { name: 'Tim', title: '《IP创投会》' },
        bestEvaluator: { name: '萱萱' },
        bestTableTopics: { name: '嘉宾A' }
      }
    },
    posterUrl: ''
  },

  onLoad(options) {
    const meetingId = options.meetingId || 'm_eoe_048';
    this.loadMeeting(meetingId);
  },

  async loadMeeting(meetingId) {
    try {
      const meeting = await api.get(`/api/meetings/${meetingId}`);
      this.setData({ meeting });
    } catch (err) {
      console.error('加载例会失败:', err);
    }
  },

  async onSavePoster() {
    wx.showLoading({ title: '生成海报中...' });
    try {
      const posterUrl = await this.drawPoster();
      await wx.saveImageToPhotosAlbum({ filePath: posterUrl });
      wx.hideLoading();
      wx.showToast({ title: '已保存到相册', icon: 'success' });
    } catch (err) {
      wx.hideLoading();
      console.error('保存海报失败:', err);
      if (err.errMsg && err.errMsg.includes('auth')) {
        wx.showModal({
          title: '需要授权',
          content: '请允许保存图片到相册',
          success: (res) => {
            if (res.confirm) wx.openSetting();
          }
        });
      } else {
        wx.showToast({ title: '保存失败', icon: 'none' });
      }
    }
  },

  drawPoster() {
    return new Promise((resolve, reject) => {
      const query = wx.createSelectorQuery();
      query.select('#posterCanvas')
        .fields({ node: true, size: true })
        .exec((res) => {
          const canvas = res[0].node;
          const ctx = canvas.getContext('2d');
          const dpr = wx.getSystemInfoSync().pixelRatio;
          
          // Canvas 尺寸: 750 x 1200 (2x for retina)
          const W = 750;
          const H = 1200;
          canvas.width = W * dpr;
          canvas.height = H * dpr;
          ctx.scale(dpr, dpr);
          
          const { meeting } = this.data;
          
          // 背景
          ctx.fillStyle = '#141413';
          ctx.fillRect(0, 0, W, H);
          
          // 装饰圆
          ctx.beginPath();
          ctx.arc(W + 50, -50, 250, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(201, 100, 66, 0.08)';
          ctx.fill();
          
          // 俱乐部名
          ctx.fillStyle = '#b0aea5';
          ctx.font = '24px sans-serif';
          ctx.textAlign = 'left';
          ctx.fillText(meeting.clubName, 60, 80);
          
          // 期数标签
          ctx.fillStyle = 'rgba(255,255,255,0.1)';
          ctx.fillRect(W - 200, 55, 140, 40);
          ctx.fillStyle = '#b0aea5';
          ctx.font = '22px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(meeting.number, W - 130, 82);
          
          // 主题标签
          ctx.textAlign = 'left';
          ctx.fillStyle = '#b0aea5';
          ctx.font = '22px sans-serif';
          ctx.fillText('本期主题', 60, 180);
          
          // 主题文字
          ctx.fillStyle = '#faf9f5';
          ctx.font = '500 48px Georgia, serif';
          ctx.fillText(meeting.theme, 60, 240);
          
          // 日期
          ctx.fillStyle = '#b0aea5';
          ctx.font = '24px sans-serif';
          ctx.fillText(meeting.date, 60, 300);
          
          // 分割线
          ctx.strokeStyle = 'rgba(255,255,255,0.1)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(60, 340);
          ctx.lineTo(W - 60, 340);
          ctx.stroke();
          
          // 获奖名单
          const winners = [
            { icon: '🏆', label: '最佳演讲', name: meeting.winners.bestSpeaker.name, title: meeting.winners.bestSpeaker.title },
            { icon: '🏆', label: '最佳点评', name: meeting.winners.bestEvaluator.name, title: '' },
            { icon: '🏆', label: '最佳即兴', name: meeting.winners.bestTableTopics.name, title: '' }
          ];
          
          let y = 400;
          winners.forEach((w) => {
            // 卡片背景
            ctx.fillStyle = 'rgba(255,255,255,0.05)';
            ctx.beginPath();
            ctx.roundRect(60, y, W - 120, 100, 16);
            ctx.fill();
            
            // 图标
            ctx.font = '36px sans-serif';
            ctx.fillText(w.icon, 90, y + 60);
            
            // 标签
            ctx.fillStyle = '#b0aea5';
            ctx.font = '22px sans-serif';
            ctx.fillText(w.label, 150, y + 45);
            
            // 名字
            ctx.fillStyle = '#faf9f5';
            ctx.font = '32px sans-serif';
            ctx.fillText(w.name, 150, y + 80);
            
            // 标题
            if (w.title) {
              ctx.fillStyle = '#87867f';
              ctx.font = '22px sans-serif';
              ctx.fillText(w.title, 280, y + 80);
            }
            
            y += 130;
          });
          
          // 底部二维码提示区
          ctx.fillStyle = 'rgba(255,255,255,0.03)';
          ctx.fillRect(60, H - 160, W - 120, 100);
          ctx.fillStyle = '#b0aea5';
          ctx.font = '22px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('扫码报名下期例会 →', W / 2, H - 105);
          
          // 导出
          wx.canvasToTempFilePath({
            canvas,
            width: W,
            height: H,
            destWidth: W * dpr,
            destHeight: H * dpr,
            success: (res) => resolve(res.tempFilePath),
            fail: reject
          });
        });
    });
  },

  onShareToMoments() {
    this.onSavePoster();
  }
});
