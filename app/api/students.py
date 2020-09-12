# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app
from sqlalchemy import text

from . import api
from ..models import User, db, Student, Dormitory
import jwt


@api.route('/stu/linkUser', methods=['GET', 'POST'])
def linkUser():
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token,
                                 key=current_app.config['SECRET_KEY'],
                                 algorithm='HS256')
            email = payload.get('email')
        except Exception as e:
            # print(e)
            return jsonify({'code': 0, 'message': 'token失效请重新登录'})

        idcard = request.get_json().get('idcard')
        user = User.query.filter_by(email=email).first()

        if user:
            if user.linked:
                return jsonify({'code': -5, 'message': '用户已关联'})
            stu = Student.query.filter_by(idcard=idcard).first()
            if stu:
                unique_stu_id = User.query.filter_by(student_id=stu.id).first()
                if unique_stu_id:
                    return jsonify({'code': -4, 'message': '新生信息已被关联'})
                user.student = stu
                user.sex = 1 if stu.sex == '男' else 0
                # user.student_num = stu.student_number
                # user.phone_num = stu.phone_number
                user.name = stu.name
                user.grade = stu.academic_year
                user.college = stu.college
                user.major = stu.professional
                user.linked = True
                try:
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return jsonify({'code': -3, 'message': '关联失败'})
                return jsonify({'code': 1, 'message': '关联成功'})
            else:
                return jsonify({'code': -2, 'message': '未查询到新生信息'})
        else:
            return jsonify({'code': -1, 'message': '未查询到用户信息'})


@api.route('/stu/getStudentInfo', methods=['GET'])
def getStudentInfo():
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        email_jwt = payload.get('email')
    except Exception as e:
        # print(e)
        return jsonify({'code': -1, 'message': 'token失效请重新登录'})

    user = User.query.filter_by(email=email_jwt).first()
    if not user:
        return jsonify({'code': 0, 'message': '用户不存在'})
    else:
        json_data = user.student.to_json()
        json_data['email'] = user.email
        json_data['student_id'] = user.student_id
        json_data['code'] = 1
        json_data['message'] = '获取成功'
        return jsonify(json_data)


@api.route('/stu/getCheckInNum', methods=['GET'])
def getCheckInNum():
    stu = Student.query.filter_by(check_in=True).all()
    return jsonify([{'value': len(stu)}])


@api.route('/stu/getCheckOutNum', methods=['GET'])
def getCheckOutNum():
    stu = Student.query.filter_by(check_in=False).all()
    return jsonify([{'value': len(stu)}])


@api.route('/stu/checkByIdcard/<idcard>', methods=['GET'])
def checkByIdcard(idcard):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        email = payload.get('email')
        perm = payload.get('permission')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if perm == 'Administrator':
        stu = Student.query.filter_by(idcard=idcard).first()
        if stu:
            user = User.query.filter_by(email=email).first()
            if user:
                json_data = stu.to_json()
                json_data['email'] = user.email
                json_data['student_id'] = user.student_id
                json_data['code'] = 1
                json_data['message'] = '查询成功'
                return jsonify(stu.to_json())
            else:
                return jsonify({'code': -3, 'message': '用户不存在'})
        else:
            return jsonify({'code': -2, 'message': '新生信息不存在'})
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/checkById/<int:stu_id>', methods=['GET'])
def checkById(stu_id):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        perm = payload.get('permission')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if perm == 'Administrator':
        stu = Student.query.filter_by(id=stu_id).first()
        return jsonify(stu.to_json())
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/getStudentList', methods=['GET', 'POST'])
def getStudentList():
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        perm = payload.get('permission')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if perm == 'Administrator':
        flag = request.get_json().get('flag')
        pageNum = request.get_json().get('pageNum')
        pageSize = request.get_json().get('pageSize')
        name = request.get_json().get('name')
        sex = request.get_json().get('sex')
        phone_num = request.get_json().get('phone_num')

        stu_list = []
        if flag == 0:
            all_results = User.query.filter_by(linked=1).filter(
                User.name.like(
                    "%" + name + "%") if name is not None else text(''),
                User.sex.like(
                    "%" + sex + "%") if sex is not None else text(''),
                User.phone_num.like(
                    "%" + phone_num + "%")
                if phone_num is not None else text('')
            )
            count = len(all_results.all())
            page = all_results.paginate(page=pageNum,
                                        per_page=pageSize)
            for i in page.items:
                json_data = i.student.to_json()
                json_data['email'] = i.email
                json_data['student_id'] = i.student_id
                stu_list.append(json_data)
            data = {'data': stu_list, 'count': count}
            return jsonify(data), 201

        elif flag == 1:
            all_results = User.query\
                .join(Student, User.student_id == Student.id)\
                .filter(
                    User.linked == 1,
                    Student.check_in == True,
                    User.name.like(
                        "%" + name + "%") if name is not None else text(''),
                    User.sex.like(
                        "%" + sex + "%") if sex is not None else text(''),
                    User.phone_num.like(
                        "%" + phone_num + "%")
                    if phone_num is not None else text('')
                )
            count = len(all_results.all())
            page = all_results.paginate(page=pageNum,
                                        per_page=pageSize)
            for i in page.items:
                json_data = i.student.to_json()
                json_data['email'] = i.email
                json_data['student_id'] = i.student_id
                stu_list.append(json_data)
            data = {'data': stu_list, 'count': count}
            return jsonify(data), 201

        elif flag == 2:
            all_results = User.query \
                .join(Student, User.student_id == Student.id) \
                .filter(
                    User.linked == 1,
                    Student.check_in == False,
                    User.name.like(
                        "%" + name + "%") if name is not None else text(''),
                    User.sex.like(
                        "%" + sex + "%") if sex is not None else text(''),
                    User.phone_num.like(
                        "%" + phone_num + "%")
                    if phone_num is not None else text('')
                )
            count = len(all_results.all())
            page = all_results.paginate(page=pageNum,
                                        per_page=pageSize)
            for i in page.items:
                json_data = i.student.to_json()
                json_data['email'] = i.email
                json_data['student_id'] = i.student_id
                stu_list.append(json_data)
            data = {'data': stu_list, 'count': count}
            return jsonify(data), 201
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/getRoomList', methods=['GET', 'POST'])
def getRoomList():
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        perm = payload.get('permission')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if perm == 'Administrator':
        room_list = []
        for i in Dormitory.query:
            json_data = {
                'id': i.id,
                'name': i.dormitory_name
            }
            room_list.append(json_data)
        return jsonify(room_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/getNoLinkStudentList', methods=['GET'])
def getNoLinkStudentList():
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
        stu_list = []
        sql = text('SELECT * FROM students WHERE id NOT IN'
                   '(SELECT id FROM students WHERE id IN '
                   '(SELECT student_id FROM users))')
        data = db.session.execute(sql)

        for i in data:
            print(i)
            stu_list.append({
                'id': i[0],
                'name': i[6],
                'idcard': i[8]
            })
        return jsonify(stu_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/uploadInfo', methods=['GET', 'POST'])
def uploadInfo():
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token,
                                 key=current_app.config['SECRET_KEY'],
                                 algorithm='HS256')
            email = payload.get('email')
        except Exception as e:
            # print(e)
            return jsonify({'code': 0, 'message': 'token失效请重新登录'})

        user = User.query.filter_by(email=email).first()
        if user.student:
            data = request.get_json()
            user.student.qq = data.get('qq')
            user.student.phone_number = data.get('phone_number')
            user.phone_num = data.get('phone_number')
            # user.student.father_name = data.get('father_name')
            # user.student.father_phone_number = data.get('father_phone_number')
            # user.student.mother_name = data.get('mother_name')
            # user.student.mother_phone_number = data.get('mother_phone_number')
            user.student.province = data.get('province')
            user.student.city = data.get('city')
            user.student.county = data.get('county')
            user.student.detailed_address = data.get('detailed_address')
            user.student.household_address = data.get('household_address')
            user.student.native_place = data.get('native_place')
            user.student.estimated_arrival_time = \
                data.get('estimated_arrival_time')
            user.student.transportation = data.get('transportation')

            user.student.whether_report = data.get('whether_report')
            user.student.whether_delay_report = data.get('whether_delay_report')
            user.student.delay_report_reason = data.get('delay_report_reason')
            user.student.the_religion = data.get('the_religion')

            user.student.parents_name = data.get('parents_name')
            user.student.parents_phone_number = data.get('parents_phone_number')

            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify({'code': -1, 'message': '上传失败'})
            return jsonify({'code': 1, 'message': '上传成功'})
        return jsonify({'code': -2, 'message': '用户未关联'})


@api.route('/stu/chooseRoom', methods=['GET', 'POST'])
def chooseRoom():
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

        dormitory_name = request.get_json().get('dormitory_name')
        idcard = request.get_json().get('idcard')

        if permission == 'Administrator':
            if not dormitory_name:
                return jsonify({'code': -1, 'message': '宿舍不存在'})
            room = \
                Dormitory.query.filter_by(dormitory_name=dormitory_name).first()
            if not room:
                return jsonify({'code': -1, 'message': '宿舍不存在'})
            else:
                if room.can:
                    stu = Student.query.filter_by(idcard=idcard).first()
                    if stu:
                        stu.dormitory_id = room.id
                        stu.check_in = 1
                        room.now_number += 1
                        if room.live_number == room.now_number:
                            room.can = False
                        try:
                            db.session.add(stu)
                            db.session.add(room)
                            db.session.commit()
                        except Exception as e:
                            print(e)
                            return jsonify({'code': -5, 'message': '添加失败'})
                        return jsonify({'code': 1, 'message': '添加成功'})
                    else:
                        return jsonify({'code': -4, 'message': '新生不存在'})
                else:
                    return jsonify({'code': -2, 'message': '宿舍已满'})
        else:
            return jsonify({'code': -3, 'message': '权限不足'})


@api.route('/stu/showAllRoom', methods=['GET'])
def showAllRoom():
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
        room_list = []
        for i in Dormitory.query:
            room_list.append(i.to_json())
        return jsonify(room_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/showAllUsefulRoom', methods=['GET'])
def showAllUsefulRoom():
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
        room_list = []
        for i in Dormitory.query.filter_by(can=True):
            room_list.append(i.to_json())
        return jsonify(room_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/showMaleRoom', methods=['GET'])
def showMaleRoom():
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
        room_list = []
        for i in Dormitory.query.filter_by(can=True).filter_by(type_id=1):
            room_list.append(i.to_json())
        return jsonify(room_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})


@api.route('/stu/showFemaleRoom', methods=['GET'])
def showFemaleRoom():
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
        room_list = []
        for i in Dormitory.query.filter_by(can=True).filter_by(type_id=0):
            room_list.append(i.to_json())
        return jsonify(room_list)
    else:
        return jsonify({'code': -1, 'message': '权限不足'})
