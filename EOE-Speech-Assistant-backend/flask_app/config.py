import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eoe-toastmasters-dev-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///eoe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 微信小程序配置
    WECHAT_APPID = os.environ.get('WECHAT_APPID') or ''
    WECHAT_SECRET = os.environ.get('WECHAT_SECRET') or ''
    
    # JWT
    JWT_SECRET = os.environ.get('JWT_SECRET') or 'eoe-jwt-secret'
    JWT_EXPIRE_DAYS = 30
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
