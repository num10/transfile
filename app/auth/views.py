#!/usr/bin/ python
# -*- coding: UTF-8 -*-

import os
from config import basedir
from flask import render_template, redirect, request, url_for, flash,send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,\
    PasswordResetForm,PasswordResetRequestForm,\
    PdfForm,PhotoForm,TranslateForm,pdfs,photos,words
from ..transform.pic2word import pic2word
from ..transform.pdf2word import pdf2word
from ..transform.translate import translatefile


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('auth.trans'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '认证您的账户',
                   'auth/email/confirm', user=user, token=token)
        flash('认证信息已发送至您的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已修改')
            return redirect(url_for('main.index'))
        else:
            flash('非法密码')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重设密码',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('邮箱已发送，请查收')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('重设密码成功')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('认证成功')
    else:
        flash('认证失败')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '认证您的账户',
               'auth/email/confirm', user=current_user, token=token)
    flash('认证信息已发送至您的邮箱，请查收！')
    return redirect(url_for('main.index'))


@auth.route('/transform')
def trans():
    return render_template('auth/dealfile.html')

@auth.route('/transpdf', methods=['GET', 'POST'])
def transpdf():
    form=PdfForm()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if form.pdf.data and form.validate_on_submit():
        form.pdf.data.filename = 'changefilename.pdf'# 更改上传的文件名，因为flask-uploads会忽略中文名，导致报错
        filename = pdfs.save(form.pdf.data)
        if filename:
            path=basedir+'/app/uploads/'
            wordfilename=pdf2word(path+filename)
            return send_from_directory(basedir+'/app/downloads',
                                       wordfilename, as_attachment=True)
    return render_template('auth/transpdf.html',form=form)

@auth.route('/transpic',methods=['GET', 'POST'])
def transpic():
    form=PhotoForm()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if form.photo.data and form.validate_on_submit():
        file_extension=os.path.splitext(form.photo.data.filename)
        form.photo.data.filename = 'changefilename.'+str(file_extension)
        filename = photos.save(form.photo.data)
        if filename:
            path=basedir+'/app/uploads/'
            wordfilename=pic2word(path+filename)
            return send_from_directory(basedir+'/app/downloads',
                                       wordfilename, as_attachment=True)
    return render_template('auth/transpic.html', form=form)

@auth.route('/translate',methods=['GET', 'POST'])
def translate():
    form=TranslateForm()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if form.word.data and form.validate_on_submit():
        file_extension = os.path.splitext(form.word.data.filename)
        form.word.data.filename = 'changefilename.' + str(file_extension)
        filename = words.save(form.word.data)
        if filename:
            path=basedir+'/app/uploads/'
            wordfilename=translatefile(path+filename)
            return send_from_directory(basedir+'/app/downloads',
                                       wordfilename, as_attachment=True)
    return render_template('auth/translate.html',form=form)