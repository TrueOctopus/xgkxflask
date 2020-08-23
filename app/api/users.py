# -*- coding: utf-8 -*-
from flask import jsonify, request, flash, render_template, current_app, \
    make_response
from flask_cors import *

from . import api
from ..models import User, db, Permission, Role
from mail import send_email
from .forms import ForgetPwdForm
import jwt
from datetime import datetime, timedelta


@api.route('/users/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        accout = request.get_json()
        email = accout.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': 0, 'message': '用户不存在'})
        else:
            password = accout.get('password')
            if user.verify_password(password):
                payload = {
                    'user_id': user.id,
                    'email': user.email,
                    'permission': user.role.name,
                    'exp': datetime.utcnow() + timedelta(days=1)
                }
                token = jwt.encode(payload,
                                   key=current_app.config['SECRET_KEY'],
                                   algorithm='HS256')
                json_data = user.to_json()
                json_data['token'] = bytes.decode(token)
                json_data['code'] = 1
                json_data['message'] = '登陆成功'
                return jsonify(json_data)
            else:
                return jsonify({'code': -1, 'message': '密码错误'})


@api.route('/users/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        accout = request.get_json()
        email = accout.get('email')
        password = accout.get('password')
        username = accout.get('username')

        try:
            user = User(email=email, password=password, username=username)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, '确认账户',
                       'auth/email/confirm',
                       user=user, token=token, email=user.email)
            return jsonify({'code': 1, 'message': '验证邮件已发送'})
        except Exception as e:
            print(e)
            return jsonify({'code': 0, 'message': '用户已存在'})


@api.route('/users/confirm/<email>/<token>', methods=['GET'])
def confirm(email, token):
    user = User.query.filter_by(email=email).first()
    if user is None:
        # flash('用户不存在')
        return jsonify({'code': -1, 'message': '用户不存在'})
    if user.confirmed:
        # flash('已验证')
        return jsonify({'code': 2, 'message': '已验证'})
    if user.confirm(token):
        db.session.commit()
        # flash('完成验证')
        return jsonify({'code': 1, 'message': '完成验证'})
    else:
        # flash('链接是无效的或已经超时')
        return jsonify({'code': 0, 'message': '链接是无效的或已经超时'})


@api.route('/users/confirm', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'POST':
        token = request.headers['Authorization']
        try:
            data = jwt.decode(token,
                              key=current_app.config['SECRET_KEY'],
                              algorithm='HS256')
            email = data.get('email')
        except Exception as e:
            return jsonify({'code': -1, 'message': 'token超时'})

        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': 0, 'message': '用户不存在'})
        if user.confirmed is False:
            token = user.generate_confirmation_token()
            send_email(user.email, '确认账户',
                       'auth/email/confirm',
                       user=user, email=user.email, token=token)
            return jsonify({'code': 1, 'message': '验证邮件已发送'})
        else:
            return jsonify({'code': 2, 'message': '用户已完成验证'})


@api.route('/users/changePassword', methods=['POST', 'GET'])
def changePassword():
    if request.method == 'POST':
        data = request.get_json()
        # token = request.headers['Authorization']
        # try:
        #     payload = jwt.decode(token,
        #                          key=current_app.config['SECRET_KEY'],
        #                          algorithm='HS256')
        #     email = payload.get('email')
        # except Exception as e:
        #     return jsonify({'code': -3, 'message': 'token超时'})
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': 0, 'message': '用户不存在'})
        else:
            oldPassword = data.get('oldPassword')
            if user.verify_password(oldPassword):
                newPassword = data.get('newPassword')
                user.password = newPassword
                try:
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'code': 1, 'message': '密码已修改'})
                except Exception as e:
                    return jsonify({'code': -1,
                                    'message': '修改失败：' + str(e)})
            else:
                return jsonify({'code': -2, 'message': '原密码错误'})


@api.route('/users/forgetPassword', methods=['POST', 'GET'])
def forgetPassword():
    if request.method == 'POST':
        # token = request.headers['Authorization']
        # try:
        #     payload = jwt.decode(token,
        #                          key=current_app.config['SECRET_KEY'],
        #                          algorithm='HS256')
        #     email = payload.get('email')
        # except Exception as e:
        #     # print(e)
        #     return jsonify({'code': -1, 'message': 'token失效请重新登录'})
        email = request.get_json().get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': 0, 'message': '用户不存在'})
        else:
            token = user.generate_changePwd_token()
            send_email(user.email, '忘记密码',
                       'auth/email/forgetPwd',
                       user=user, email=user.email, token=token)
            return jsonify({'code': 1, 'message': '修改邮件已发送'})


@api.route('/users/forgetPwd/<email>/<token>', methods=['GET', 'POST'])
def forgetPwd(email, token):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'code': 0, 'message': '用户不存在'})
    if user.forgetPwdConfirm(token):
        form = ForgetPwdForm()
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash("修改成功，请返回登录")
        return render_template('auth/forgetPwd.html', form=form)
        # return jsonify({'code': 1, 'message': '修改完成'})
    else:
        return jsonify({'code': -1, 'message': '链接是无效的或已经超时'})


def delete(user):
    # noinspection PyBroadException
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception:
        return False


@api.route('/users/deleteUserById/<int:id>', methods=['GET'])
def deleteUserById(id):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        permission = payload.get('permission')
        id_jwt = payload.get('user_id')
    except Exception as e:
        # print(e)
        return jsonify({'code': -3, 'message': 'token失效请重新登录'})
    if id == id_jwt:
        return jsonify({'code': -4, 'message': '你不能删除你自己'})
    if permission == 'Administrator':
        user = User.query.filter_by(id=id).first()
        if user is None:
            return jsonify({'code': -1, 'message': '用户不存在'})
        if delete(user):
            return jsonify({'code': 1, 'message': '删除成功'})
        else:
            return jsonify({'code': 0, 'message': '删除失败'})
    else:
        return jsonify({'code': -2, 'message': '权限不足'})


@api.route('/users/deleteUserByEmail/<email>', methods=['GET'])
def deleteUserByEmail(email):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        permission = payload.get('permission')
        email_jwt = payload.get('email')
    except Exception as e:
        # print(e)
        return jsonify({'code': -3, 'message': 'token失效请重新登录'})

    if email_jwt == email:
        return jsonify({'code': -4, 'message': '你不能删除你自己'})
    if permission == 'Administrator':
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': -1, 'message': '用户不存在'})
        if delete(user):
            return jsonify({'code': 1, 'message': '删除成功'})
        else:
            return jsonify({'code': 0, 'message': '删除失败'})
    else:
        return jsonify({'code': -2, 'message': '权限不足'})


@api.route('/users/changePermission', methods=['POST', 'GET'])
def changePermission():
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token,
                                 key=current_app.config['SECRET_KEY'],
                                 algorithm='HS256')
            permission = payload.get('permission')
            email_base = payload.get('email')
        except Exception as e:
            # print(e)
            return jsonify({'code': -4, 'message': 'token失效请重新登录'})

        if permission == 'Administrator':
            email = request.get_json().get('email')
            perm = request.get_json().get('perm')
            user = User.query.filter_by(email=email).first()

            if email_base == email or user.role.name == 'Administrator':
                return jsonify({'code': -3, 'message': '你不能修改管理员的权限'})
            if not user:
                return jsonify({'code': -1, 'message': '用户不存在'})
            else:
                user.role = Role.query.filter_by(name=perm).first()
                try:
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'code': 1, 'message': '修改成功'})
                except Exception as e:
                    # print(e)
                    return jsonify({'code': -2, 'message': '添加至数据库失败'})

        else:
            return jsonify({'code': 0, 'message': '权限不足'})
