# -*- coding: utf-8 -*-
import jwt
from flask import jsonify, request, current_app
from ..models import User, db
from . import api
import os
import base64
# from werkzeug.utils import secure_filename

UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/static/imgs/'
UPLOAD_ART_FOLDER = r'/home/zzy/xgkxflask/app/static/imgs/artimgs/'
# UPLOAD_FOLDER = r'app/static/imgs/'


def D_BASE64(origStr):
    # base64 decode should meet the padding rules
    if len(origStr) % 3 == 1:
        origStr += "=="
    elif len(origStr) % 3 == 2:
        origStr += "="

    dStr = base64.b64decode(origStr)
    return dStr


@api.route('/posts/uploadProfile', methods=['POST', 'GET'])
def uploadProfile():
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token,
                                 key=current_app.config['SECRET_KEY'],
                                 algorithm='HS256')
            email = payload.get('email')
        except Exception as e:
            # print(e)
            return jsonify({'code': -2, 'message': 'token失效请重新登录'})

        data = request.json
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
        # print(profile_photo)

        if profile_photo:
            if profile_photo != user.profile_photo:
                file_name = email.split('.')[0]
                # print(file_name)
                etc = profile_photo.split(';')[0].split('/')[1]
                # print(etc)
                file_name = file_name + '.' + etc
                profile_photo = profile_photo.split(',')[1]
                image_data = D_BASE64(profile_photo)

                f = open(UPLOAD_FOLDER + file_name, 'wb')
                f.write(image_data)
                f.close()
                profile_photo = file_name

        user.username = username
        user.name = name
        user.sex = sex
        user.college = college
        user.major = major
        user.grade = grade
        user.student_num = student_num
        user.phone_num = phone_num
        user.about_me = about_me

        if profile_photo:
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
        if all([email, username, password]):
            user = User(email=email, username=username,
                        password=password, confirmed=True)
        else:
            return jsonify({'code': -1, 'message': '添加失败， 信息不全'})
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify({'code': 0, 'message': str(e)})
        json_data = user.to_json()
        json_data['code'] = 1
        json_data['message'] = '添加成功'
        return jsonify(json_data)


@api.route('/posts/uploadImg', methods=['POST', 'GET'])
def uploadImg():
    if request.method == 'POST':
        f = request.files['image']
        if f is not None:
            file_dir = UPLOAD_ART_FOLDER
            filename = f.filename
            etc = filename.split('.')[1]
            mdict = ['jpg', 'jpeg', 'gif', 'png', 'raw', 'tiff', 'svg']
            for i in mdict:
                if i == etc:
                    path = os.path.join(file_dir, filename)
                    if os.path.isfile(path):
                        return jsonify({'code': 0, 'message': '图片已存在'})
                    f.save(path)
                    return jsonify({'code': 1, 'message': '上传成功'})
            return jsonify({'code': -1, 'message': '类型错误'})
