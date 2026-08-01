/**
 * 小程序配置文件
 */
const ENV = {
  development: {
    API_BASE_URL: 'http://localhost:8080',
    DEBUG: true
  },
  production: {
    API_BASE_URL: 'https://your-domain.com',
    DEBUG: false
  }
};

const CURRENT_ENV = 'development';

module.exports = {
  ...ENV[CURRENT_ENV],
  ENV: CURRENT_ENV,
  API: {
    LOGIN: '/api/auth/login',
    GET_USER_INFO: '/api/user/info',
    UPDATE_USER_INFO: '/api/user/info',
    CLUBS: '/api/clubs',
    MEETINGS: '/api/clubs/{clubId}/meetings',
    REGISTER: '/api/meetings/{meetingId}/register',
    VOTE: '/api/meetings/{meetingId}/vote',
    TIMER: '/api/meetings/{meetingId}/timer',
    MEMBERS: '/api/clubs/{clubId}/members'
  }
};
