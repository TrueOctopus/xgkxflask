# -*- coding: utf-8 -*-
import jwt
from flask import jsonify, request, current_app

from mail import send_email
from . import api
from ..models import Applicant, db


@api.route('/uploadApplicant', methods=['POST', 'GET'])
def uploadApplicant():
    if request.method == 'POST':
        data = request.get_json()

        name = data.get('name')
        sex = data.get('sex')
        birthday = data.get('birthday')
        class_name = data.get('class_name')
        intention = data.get('intention')
        qq = data.get('qq')
        major = data.get('major')
        phone_num = data.get('phone_num')
        email = data.get('email')
        specialty = data.get('specialty')
        office = data.get('office')
        software = data.get('software')
        about_me = data.get('about_me')
        cognition = data.get('cognition')

        stu = Applicant(name=name, sex=sex, birthday=birthday,
                        class_name=class_name, intention=intention, qq=qq,
                        major=major, phone_num=phone_num, email=email,
                        specialty=specialty, office=office, software=software,
                        about_me=about_me, cognition=cognition)
        try:
            db.session.add(stu)
            db.session.commit()
            return jsonify({'code': 1, 'message': '上传成功'})
        except Exception as e:
            # print(e)
            return jsonify({'code': -1, 'message': '数据库添加错误'})


@api.route('/getApplicantById/<int:id>', methods=['GET'])
def getApplicantById(id):
    stu = Applicant.query.filter_by(id=id).first()
    if stu is None:
        return jsonify({'code': 0, 'message': '用户不存在'})
    else:
        json_data = stu.to_json()
        json_data['code'] = 1
        json_data['message'] = '查询成功'
        return jsonify(json_data)


@api.route('/getApplicantByName/<name>', methods=['GET'])
def getApplicantByName(name):
    stu = Applicant.query.filter_by(name=name).first()
    if stu is None:
        return jsonify({'code': 0, 'message': '用户不存在'})
    else:
        json_data = stu.to_json()
        json_data['code'] = 1
        json_data['message'] = '查询成功'
        return jsonify(json_data)


@api.route('/getApplicantList', methods=['GET'])
def getApplicantList():
    json_data = []
    for stu in Applicant.query:
        json_data.append(stu.to_json())
    return jsonify(json_data)


@api.route('/deleteApplicantById/<int:id>', methods=['GET'])
def deleteApplicantById(id):
    stu = Applicant.query.filter_by(id=id).first()
    if stu is None:
        return jsonify({'code': 0, 'message': '用户不存在'})
    else:
        db.session.delete(stu)
        db.session.commit()
        return jsonify({'code': 1, 'message': '删除成功'})


@api.route('/deleteApplicantByName/<name>', methods=['GET'])
def deleteApplicantByName(name):
    stu = Applicant.query.filter_by(name=name).first()
    if stu is None:
        return jsonify({'code': 0, 'message': '用户不存在'})
    else:
        db.session.delete(stu)
        db.session.commit()
        return jsonify({'code': 1, 'message': '删除成功'})


@api.route('/confirmApplication', methods=['GET', 'POST'])
def confirmApplication():
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token,
                                 key=current_app.config['SECRET_KEY'],
                                 algorithm='HS256')
            permission = payload.get('permission')
        except Exception as e:
            # print(e)
            return jsonify({'code': 0, 'message': 'token失效请重新登录'})

        if permission == 'Administrator':
            email = request.get_json().get('email')
            user = Applicant.query.filter_by(email=email).first()
            if not user.passed:
                if not user:
                    return jsonify({'code': -2, 'message': '用户不存在'})
                else:
                    send_email(user.email, '申请通过',
                               'auth/email/application',
                               user=user, email=user.email)
                    user.passed = 1
                    try:
                        db.session.add(user)
                        db.session.commit()
                    except Exception as e:
                        # print(e)
                        return jsonify({'code': -4, 'message': '添加至数据库失败'})
                    return jsonify({'code': 1, 'message': '发送成功'})
            else:
                return jsonify({'code': -3, 'message': '已通过'})
        else:
            return jsonify({'code': -1, 'message': '权限不足'})
