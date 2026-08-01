Page({
  data: {
    member: {
      id: 'user_tim',
      name: 'Tim',
      englishName: 'Tim',
      avatar: '',
      region: '南山',
      profession: '产品经理',
      memberSince: '2024-11',
      officerRole: 'VPPR',
      stats: {
        totalSpeeches: 12,
        bestSpeakerCount: 3,
        bestEvaluatorCount: 1,
        bestTableTopicsCount: 2,
        avgDuration: 6.5,
        roleCounts: { host: 5, timer: 3, tableTopicsMaster: 2, preparedSpeaker: 12, evaluator: 8 }
      }
    },
    speeches: [
      { meetingTheme: '《IP创投会》', role: '备稿演讲', date: '2025-07-03', duration: '7:32' },
      { meetingTheme: '拒绝年龄焦虑', role: '主席/即兴主持', date: '2025-07-10', duration: '-' },
      { meetingTheme: '精神稀缺', role: '主席/时间官', date: '2025-07-24', duration: '-' }
    ]
  },

  onLoad(options) {
    const memberId = options.id || 'user_tim';
    // TODO: 从后端加载成员详情
    console.log('查看成员:', memberId);
  }
});
