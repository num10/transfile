#!/usr/bin/ python
# -*- coding: UTF-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:root@localhost/shihaodata'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '992346986@qq.com'

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xmktrsdiyxgnbcbd'
    FLASKY_MAIL_SUBJECT_PREFIX = '[文件转换中心]'
    FLASKY_MAIL_SENDER = 'pdf2word <992346986@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    UPLOADED_PDFS_DEST = '/home/shihao/project/transfile/app/uploads'
    UPLOADED_PHOTOS_DEST = '/home/shihao/project/transfile/app/uploads'
    UPLOADED_WORDS_DEST = '/home/shihao/project/transfile/app/uploads'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/shihaodata'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql:/'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/shihaodata'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}