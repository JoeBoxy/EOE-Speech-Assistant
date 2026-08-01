/**
 * 认证相关工具函数
 * 处理微信登录、token 管理、用户信息获取
 */
const request = require('./request');
const config = require('./config');

// 存储键名
const USER_INFO_KEY = 'user_info';

/**
 * 检查是否已登录
 */
function isLoggedIn() {
  const token = request.getToken();
  return !!token;
}

/**
 * 获取本地存储的用户信息
 */
function getStoredUserInfo() {
  return wx.getStorageSync(USER_INFO_KEY) || null;
}

/**
 * 保存用户信息到本地
 */
function saveUserInfo(userInfo) {
  wx.setStorageSync(USER_INFO_KEY, userInfo);
}

/**
 * 清除登录状态
 */
function clearLoginState() {
  request.clearToken();
  wx.removeStorageSync(USER_INFO_KEY);
}

/**
 * 微信小程序登录
 * 1. 获取微信登录 code
 * 2. 获取用户信息（可选）
 * 3. 调用后端登录接口
 * @param {boolean} withUserInfo - 是否获取用户信息（头像、昵称）
 */
function login(withUserInfo = true) {
  return new Promise((resolve, reject) => {
    // 1. 获取微信登录 code
    wx.login({
      success: (loginRes) => {
        if (!loginRes.code) {
          reject(new Error('获取登录凭证失败'));
          return;
        }
        
        const loginData = {
          code: loginRes.code
        };
        
        // 2. 如果需要，获取用户信息
        if (withUserInfo) {
          getWxUserProfile().then((userProfile) => {
            loginData.nickname = userProfile.nickName;
            loginData.avatar_url = userProfile.avatarUrl;
            // 执行后端登录
            doBackendLogin(loginData, resolve, reject);
          }).catch((err) => {
            // 用户拒绝授权，仍然可以登录，只是没有用户信息
            console.log('获取用户信息失败:', err);
            doBackendLogin(loginData, resolve, reject);
          });
        } else {
          // 直接登录，不获取用户信息
          doBackendLogin(loginData, resolve, reject);
        }
      },
      fail: (err) => {
        console.error('wx.login 失败:', err);
        reject(new Error('微信登录失败'));
      }
    });
  });
}

/**
 * 获取微信用户信息
 * 使用 wx.getUserProfile（需要用户点击触发）
 */
function getWxUserProfile() {
  return new Promise((resolve, reject) => {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        resolve(res.userInfo);
      },
      fail: (err) => {
        reject(err);
      }
    });
  });
}

/**
 * 调用后端登录接口
 */
function doBackendLogin(loginData, resolve, reject) {
  request.post(config.API.LOGIN, loginData)
    .then((data) => {
      // 保存 token
      request.setToken(data.token);
      
      // 保存用户信息
      if (data.user_info) {
        saveUserInfo(data.user_info);
      }
      
      resolve({
        token: data.token,
        expireDays: data.expire_days,
        userInfo: data.user_info
      });
    })
    .catch((err) => {
      reject(err);
    });
}

/**
 * 从后端获取最新用户信息
 */
function fetchUserInfo() {
  return new Promise((resolve, reject) => {
    if (!isLoggedIn()) {
      reject(new Error('未登录'));
      return;
    }
    
    request.get(config.API.GET_USER_INFO, true)
      .then((data) => {
        saveUserInfo(data);
        resolve(data);
      })
      .catch((err) => {
        reject(err);
      });
  });
}

/**
 * 更新用户信息
 * @param {object} userInfo - { nickname, avatar_url }
 */
function updateUserInfo(userInfo) {
  return new Promise((resolve, reject) => {
    if (!isLoggedIn()) {
      reject(new Error('未登录'));
      return;
    }
    
    request.put(config.API.UPDATE_USER_INFO, userInfo, true)
      .then((data) => {
        saveUserInfo(data);
        resolve(data);
      })
      .catch((err) => {
        reject(err);
      });
  });
}

/**
 * 退出登录
 */
function logout() {
  clearLoginState();
  return Promise.resolve();
}

module.exports = {
  isLoggedIn,
  getStoredUserInfo,
  saveUserInfo,
  clearLoginState,
  login,
  getWxUserProfile,
  fetchUserInfo,
  updateUserInfo,
  logout
};
