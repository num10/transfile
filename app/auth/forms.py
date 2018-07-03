#!/usr/bin/ python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能有字母，数字，点或下划线')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致.')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被其他用户使用')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码',
                              validators=[DataRequired()])
    submit = SubmitField('修改密码')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重设密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重设密码')


from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, IMAGES

PDF = tuple('pdf'.split())
WORD = tuple('doc docx'.split())

pdfs = UploadSet('pdfs',PDF)
photos = UploadSet('photos', IMAGES)
words = UploadSet('words',WORD)

class PdfForm(FlaskForm):

    pdf = FileField(u'上传PDF文件', validators=[
        FileAllowed(['pdf'], u'只能上传PDF！')])
    submit = SubmitField('PDF转换为WORD')

class PhotoForm(FlaskForm):
    photo = FileField(u'上传图片', validators=[
        FileAllowed(photos, u'只能上传图片！')])
    submit = SubmitField('图片转换为WORD')

class TranslateForm(FlaskForm):
    word = FileField(u'上传WORD文件', validators=[
        FileAllowed(['doc','docx'], u'只能上传WORD(doc或docx)！')])
    submit = SubmitField('翻译（英译中）')