# -*- coding: utf-8 -*-
from flask import jsonify, request, flash
from . import api
from ..models import User, db
from mail import send_email


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
                json_data = user.to_json()
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
        flash('用户不存在')
        return jsonify({'code': -1, 'message': '用户不存在'})
    if user.confirmed:
        flash('已验证')
        return jsonify({'code': 2, 'message': '已验证'})
    if user.confirm(token):
        db.session.commit()
        flash('已验证完成')
        return jsonify({'code': 1, 'message': '已验证完成'})
    else:
        flash('链接是无效的或已经超时')
        return jsonify({'code': 0, 'message': '链接是无效的或已经超时'})


@api.route('/users/confirm', methods=['GET', 'POST'])
def resend_confirmation():
    if request.method == 'POST':
        email = request.get_json().get('email')
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
