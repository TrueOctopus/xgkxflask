# -*- coding: utf-8 -*-
from flask import jsonify, request
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
            print(e)
            return jsonify({'code': -1, 'message': str(e)})


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
