const momentsCategories = [
  { id: 'daily', name: '日常' },
  { id: 'food', name: '美食' },
  { id: 'travel', name: '旅行' },
  { id: 'mood', name: '心情' }
];

const momentsTemplates = [
  {
    id: 1,
    category: 'daily',
    title: '治愈日常',
    text: '把普通的一天，过成自己喜欢的样子。今日份小确幸已到账，生活虽然不总是闪闪发光，但热爱会。'
  },
  {
    id: 2,
    category: 'daily',
    title: '周末放松',
    text: '暂停匆忙，打开周末。把烦恼调成静音，把喜欢的事情调成最大声。'
  },
  {
    id: 3,
    category: 'food',
    title: '美食打卡',
    text: '吃到喜欢的东西，日子就会变得具体。今日快乐很简单，是这一口热气腾腾的满足。'
  },
  {
    id: 4,
    category: 'food',
    title: '咖啡时刻',
    text: '咖啡到位，状态归位。忙碌生活里，总要给自己留一点微苦后回甘的时间。'
  },
  {
    id: 5,
    category: 'travel',
    title: '旅行记录',
    text: '换个地方看人间烟火，答案有时候不在赶路里，而在路过的风景里。'
  },
  {
    id: 6,
    category: 'travel',
    title: '出发心情',
    text: '短暂逃离日常，去见更大的世界。镜头装不下的，是当下那一刻真的很自由。'
  },
  {
    id: 7,
    category: 'mood',
    title: '温柔表达',
    text: '允许一切如其所是，也允许自己慢一点。心里有光的人，走到哪里都不会太暗。'
  },
  {
    id: 8,
    category: 'mood',
    title: '自我鼓励',
    text: '最近很累，但也在认真生活。不是每一步都要很大，只要一直往前，就是答案。'
  }
];

const quoteCategories = [
  { id: 'healing', name: '治愈' },
  { id: 'love', name: '爱情' },
  { id: 'growth', name: '成长' },
  { id: 'energy', name: '力量' }
];

const quoteTemplates = [
  {
    id: 1,
    category: 'healing',
    author: '匿名',
    text: '日子不是突然变好的，是你一点一点把自己哄好的。'
  },
  {
    id: 2,
    category: 'healing',
    author: '匿名',
    text: '总会有一束光，落在你身上，驱散那些说不出口的疲惫。'
  },
  {
    id: 3,
    category: 'love',
    author: '匿名',
    text: '真正让人安心的，从来不是秒回，而是一直都在。'
  },
  {
    id: 4,
    category: 'love',
    author: '匿名',
    text: '喜欢不是权衡利弊后的选择，而是明知道普通，也还是偏爱。'
  },
  {
    id: 5,
    category: 'growth',
    author: '匿名',
    text: '你现在读过的书、走过的路、熬过的夜，都会在未来某一天回过头来照亮你。'
  },
  {
    id: 6,
    category: 'growth',
    author: '匿名',
    text: '成长不是一下子变厉害，而是学会在脆弱里站稳自己。'
  },
  {
    id: 7,
    category: 'energy',
    author: '匿名',
    text: '别急着否定自己，你只是还在去更好的路上。'
  },
  {
    id: 8,
    category: 'energy',
    author: '匿名',
    text: '把今天过好，就是给明天最稳的底气。'
  }
];

module.exports = {
  momentsCategories,
  momentsTemplates,
  quoteCategories,
  quoteTemplates
};
