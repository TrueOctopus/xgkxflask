# -*- coding: utf-8 -*-
from flask import jsonify, request
from ..models import User, db
from . import api
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/static/imgs/'


@api.route('/posts/uploadProfile', methods=['POST', 'GET'])
def uploadProfile():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        # email = data['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'code': 0, 'message': '用户不存在'})

        username = data.get('username')
        name = data.get('name')
        sex = data.get('sex')
        college = data.get('college')
        major = data.get('major')
        grade = data.get('grade')
        student_num = data.get('student_num')
        phone_num = data.get('phone_num')
        about_me = data.get('about_me')
        profile_photo = data.get('profile_photo')

        # username = data['username']
        # name = data['name']
        # sex = data['sex']
        # college = data['college']
        # major = data['major']
        # grade = data['grade']
        # student_num = data['student_num']
        # phone_num = data['phone_num']
        # about_me = data['about_me']

        # try:
        #     f = request.files['profile_photo']
        #     if f is not None:
        #         file_dir = UPLOAD_FOLDER
        #         filename = secure_filename(f.filename)
        #         ext = filename.split('.', 1)[-1]
        #         new_name = email.split('.', 1)[0] + '.' + ext
        #         f.save(os.path.join(file_dir, new_name))
        #         user.profile_photo = new_name
        # except Exception as e:
        #     pass
            # return jsonify({'code': -2, 'message': str(e)})

        user.username = username
        user.name = name
        user.sex = sex
        user.college = college
        user.major = major
        user.grade = grade
        user.student_num = student_num
        user.phone_num = phone_num
        user.about_me = about_me

        if profile_photo is not None:
            user.profile_photo = profile_photo

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 1, 'message': '更新成功'})
        except Exception as e:
            # print(e)
            db.session.rollback()
            return jsonify({'code': -1, 'message': '添加失败'})


@api.route('/posts/addUser', methods=['POST', 'GET'])
def addUser():
    if request.method == 'POST':
        user_data = request.json
        email = user_data.get('email')
        username = user_data.get('username')
        password = user_data.get('password')

        user = User(email=email, username=username,
                    password=password, confirmed=True)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify({'code': 0, 'message': str(e)})
        json_data = user.to_json()
        json_data['code'] = 1
        json_data['message'] = '添加成功'
        return jsonify(json_data)
