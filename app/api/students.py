# -*- coding: utf-8 -*-
from flask import jsonify, request, current_app, make_response, send_file
from sqlalchemy import text

from . import api
from ..models import User, db, Student, Dormitory
import jwt
import xlwt

UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/'
# UPLOAD_FOLDER = r''


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
            all_results = User.query \
                .join(Student, User.student_id == Student.id) \
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


@api.route('/stu/getStudentExcel', methods=['GET'])
def getStudentExcel():
    dormitory_list = [['暂无', '1', '8'],
                      ['3号楼101', '1', '8'],
                      ['3号楼102', '1', '8'],
                      ['6号楼101', '1', '6'],
                      ['6号楼102', '1', '6'],
                      ['6号楼103', '1', '6'],
                      ['6号楼104', '1', '6'],
                      ['6号楼106', '1', '6'],
                      ['6号楼107', '1', '6'],
                      ['6号楼108', '1', '6'],
                      ['6号楼111', '1', '6'],
                      ['6号楼112', '1', '6'],
                      ['6号楼113', '1', '6'],
                      ['6号楼114', '1', '6'],
                      ['6号楼115', '1', '6'],
                      ['6号楼116', '1', '6'],
                      ['6号楼201', '1', '6'],
                      ['6号楼202', '1', '6'],
                      ['6号楼203', '1', '6'],
                      ['6号楼204', '1', '6'],
                      ['6号楼205', '1', '6'],
                      ['6号楼206', '1', '6'],
                      ['6号楼207', '1', '6'],
                      ['6号楼208', '1', '6'],
                      ['6号楼209', '1', '6'],
                      ['6号楼212', '1', '6'],
                      ['6号楼213', '1', '6'],
                      ['6号楼214', '1', '6'],
                      ['6号楼215', '1', '6'],
                      ['6号楼216', '1', '6'],
                      ['6号楼217', '1', '6'],
                      ['6号楼301', '1', '6'],
                      ['6号楼302', '1', '6'],
                      ['6号楼303', '1', '6'],
                      ['6号楼304', '1', '6'],
                      ['6号楼305', '1', '6'],
                      ['6号楼306', '1', '6'],
                      ['6号楼307', '1', '6'],
                      ['6号楼308', '1', '6'],
                      ['6号楼309', '1', '6'],
                      ['6号楼312', '1', '6'],
                      ['6号楼313', '1', '6'],
                      ['6号楼314', '1', '6'],
                      ['6号楼315', '1', '6'],
                      ['6号楼316', '1', '6'],
                      ['6号楼317', '1', '6'],

                      ['10号楼421', '0', '8'],
                      ['10号楼422', '0', '8'],
                      ['10号楼423', '0', '8'],
                      ['10号楼403', '0', '2'],
                      ['7号楼301', '0', '5'],
                      ['7号楼302', '0', '5'],
                      ['7号楼303', '0', '5'],
                      ['7号楼304', '0', '5'],
                      ['7号楼306', '0', '5'],
                      ['7号楼307', '0', '5'],
                      ['7号楼308', '0', '5'],
                      ['7号楼309', '0', '5'],
                      ['7号楼310', '0', '5'],
                      ['7号楼311', '0', '5'],
                      ['7号楼312', '0', '5'],
                      ['7号楼313', '0', '5'],
                      ['7号楼314', '0', '5'],
                      ['7号楼315', '0', '5'],
                      ['7号楼316', '0', '5'],
                      ['7号楼317', '0', '5']]
    stu_list = Student.query.all()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Students')
    header = ['id', '考生号', '学制', '学年', '专业', '学院', '姓名', '性别',
              '身份证号', '民族', '政治面貌', '职务', '荣誉', '报到情况', '宿舍',
              '贫困认证', '科类', '出生日期', '考生类别', '毕业类别', '中学名称',
              '外语语种', '报到校区', '是否报到', '报到时间', '交通工具', '是否延迟报到',
              '延迟报道原因', '是否有宗教信仰', '联系方式', '家长姓名', '家长联系方式',
              '省份', '市', '县', '详细地址', '籍贯', '户籍地址', 'QQ']
    for i in range(len(header)):
        worksheet.write(0, i, label=header[i])
    # workbook.save('students.xls')

    count = 1
    for stu in stu_list:
        info = []
        info.append(stu.id)
        info.append(stu.candidate_number)
        info.append(stu.eductional_systme)
        info.append(stu.academic_year)
        info.append(stu.professional)
        info.append(stu.college)
        info.append(stu.name)
        info.append(stu.sex)
        info.append(stu.idcard)
        info.append(stu.ethnic)
        info.append(stu.political_landscape)
        info.append(stu.position)
        info.append(stu.honor)
        info.append('是' if stu.check_in else '否')
        info.append(dormitory_list[0 if not stu.dormitory_id
                    else stu.dormitory_id][0])  # 宿舍
        info.append(stu.poor_certification)
        info.append(stu.subject_category)
        info.append(stu.birthday)
        info.append(stu.candidate_category)
        info.append(stu.graduation_category)
        info.append(stu.middle_school_name)
        info.append(stu.foreign_language)
        info.append(stu.report_campus)
        info.append('是' if stu.whether_report else '否')
        info.append(stu.estimated_arrival_time)
        info.append(stu.transportation)
        info.append('是' if stu.whether_delay_report else '否')
        info.append(stu.delay_report_reason)
        info.append('有' if stu.the_religion else '无')
        info.append(stu.phone_number)
        info.append(stu.parents_name)
        info.append(stu.parents_phone_number)
        info.append(stu.province)
        info.append(stu.city)
        info.append(stu.county)
        info.append(stu.detailed_address)
        info.append(stu.native_place)
        info.append(stu.household_address)
        info.append(stu.qq)

        for i in range(len(info)):
            worksheet.write(count, i, label=info[i])
        count += 1
    workbook.save(UPLOAD_FOLDER + 'students.xls')
    try:
        response = make_response(
            send_file(UPLOAD_FOLDER + 'students.xls',
                      as_attachment=True))
        return response
    except Exception as e:
        return jsonify({'code': 0, 'message': str(e)})
