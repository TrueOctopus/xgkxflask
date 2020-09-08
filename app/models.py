# -*- coding: utf-8 -*-
# import json
from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
# import xlrd


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, index=True)
    users = db.relationship('User', backref='student', uselist=False,
                            cascade='all')
    candidate_number = db.Column(db.String(14), index=True, unique=True)  # 考生号
    eductional_systme = db.Column(db.Integer, default=4)  # 学制
    academic_year = db.Column(db.String(32), default='20级')  # 学年
    professional = db.Column(db.String(64))  # 专业
    college = db.Column(db.String(64))  # 学院
    name = db.Column(db.String(64))  # 姓名
    sex = db.Column(db.String(8))  # 性别
    idcard = db.Column(db.String(18), index=True)  # 身份证号
    ethnic = db.Column(db.String(64))  # 民族
    political_landscape = db.Column(db.String(64))  # 政治面貌
    position = db.Column(db.String(64))  # 职务
    honor = db.Column(db.String(256))  # 荣誉
    counselor_id = db.Column(db.Integer, default=0)  # 辅导员ID
    check_in = db.Column(db.Boolean, default=False, index=True)  # 报到情况
    note = db.Column(db.String(256))  # 奇怪的信息
    dormitory_id = db.Column(db.Integer)  # 宿舍ID
    poor_certification = db.Column(db.String(8))  # 贫困认证

    # 新增
    # student_number = db.Column(db.String(12), index=True)  # 学号
    # student_class = db.Column(db.String(10), index=True)  # 班级
    subject_category = db.Column(db.String(32))  # 科类
    birthday = db.Column(db.String(32))  # 出生日期
    candidate_category = db.Column(db.String(32))  # 考生类别
    graduation_category = db.Column(db.String(32))  # 毕业类别
    middle_school_name = db.Column(db.String(64))  # 中学名称
    foreign_language = db.Column(db.String(32))  # 外语种类
    report_campus = db.Column(db.String(32))  # 报道校区
    # 需填写
    phone_number = db.Column(db.String(11))  # 联系电话
    province = db.Column(db.String(32))  # 省
    city = db.Column(db.String(32))  # 市
    county = db.Column(db.String(64))  # 县
    detailed_address = db.Column(db.String(256))  # 详细地址
    native_place = db.Column(db.String(256))  # 籍贯
    household_address = db.Column(db.String(256))  # 户籍地址
    father_name = db.Column(db.String(64))  # 父亲姓名
    father_phone_number = db.Column(db.String(11))  # 父亲联系电话
    mother_name = db.Column(db.String(64))  # 母亲姓名
    mother_phone_number = db.Column(db.String(11))  # 母亲联系电话
    qq = db.Column(db.String(32))  # QQ号码

    # @staticmethod
    # def importInformation():
    #     data = xlrd.open_workbook('app/1.xlsx', 'r')
    #     table = data.sheets()[0]
    #     nrows = table.nrows  # 行
    #     for i in range(1, nrows):
    #         # print(table.row_values(i))
    #         stu = Student(candidate_number=table.row_values(i)[5],
    #                       eductional_systme=table.row_values(i)[2],
    #                       academic_year=table.row_values(i)[3],
    #                       student_number=table.row_values(i)[4],
    #                       student_class=table.row_values(i)[8],
    #                       professional=table.row_values(i)[6],
    #                       college=table.row_values(i)[7],
    #                       name=table.row_values(i)[0],
    #                       sex=table.row_values(i)[1],
    #                       idcard=table.row_values(i)[8],
    #                       province=table.row_values(i)[9],
    #                       city=table.row_values(i)[10],
    #                       county=table.row_values(i)[11],
    #                       detailed_address=table.row_values(i)[12],
    #                       native_place=table.row_values(i)[13],
    #                       household_address=table.row_values(i)[14],
    #                       phone_number=table.row_values(i)[15],
    #                       ethnic=table.row_values(i)[16],
    #                       political_landscape=table.row_values(i)[17],
    #                       poor_certification=table.row_values(i)[21],
    #                       father_name=table.row_values(i)[22],
    #                       father_phone_number=table.row_values(i)[23],
    #                       mother_name=table.row_values(i)[24],
    #                       mother_phone_number=table.row_values(i)[25],
    #                       )
    #         db.session.add(stu)
    #     db.session.commit()

    def to_json(self):
        json_data = {
            'id': self.id,  # id
            'name': self.name,  # 姓名
            'idcard': self.idcard,  # 身份证号
            'address':
                str(self.province) + str(self.city) + str(self.county),  # 地址
            'province': self.province,
            'city': self.city,
            'county': self.county,
            'detailed_address': self.detailed_address,  # 详细地址
            'candidate_number': self.candidate_number,  # 考生号
            'eductional_systme': self.eductional_systme,  # 学制
            'academic_year': self.academic_year,  # 学年
            # 'student_number': self.student_number,  # 学号
            # 'student_class': self.student_class,  # 班级
            'professional': self.professional,  # 专业
            'college': self.college,  # 学院
            'sex': self.sex,  # 性别
            'native_place': self.native_place,  # 籍贯
            'household_address': self.household_address,  # 户籍地址
            'subject_category': self.subject_category,  # 科类
            'birthday': self.birthday,  # 出生日期
            'candidate_category': self.candidate_category,  # 考生类别
            'graduation_category': self.graduation_category,  # 毕业类别
            'middle_school_name': self.middle_school_name,  # 中学名称
            'foreign_language': self.foreign_language, # 外语种类
            'report_campus': self.report_campus,  # 报道校区
            'phone_number': self.phone_number,  # 联系电话
            'ethnic': self.ethnic,  # 民族
            'political_landscape': self.political_landscape,  # 政治面貌
            'position': self.position,  # 职务
            'dormitory_id': self.dormitory_id,  # 宿舍ID
            'poor_certification': self.poor_certification,  # 贫困认证
            'father_name': self.father_name,  # 父亲姓名
            'father_phone_number': self.father_phone_number,  # 父亲联系电话
            'mother_name': self.mother_name,  # 母亲姓名
            'mother_phone_number': self.mother_phone_number,  # 母亲联系电话
            'counselor_id': self.counselor_id,  # 辅导员ID
            'check_in': self.check_in,  # 报到情况
            'qq': self.qq,  # QQ
            'honor': self.honor,  # 荣誉

            # 'time1': d['time1'],
            # 'time2': d['time2'],
            # 'smoke': d['smoke'],
            # 'habit': d['habit'],
            # 'specialty': d['specialty']
        }
        return json_data

    def __repr__(self):
        return '<Student %r>' % self.name
# 分班
# 宿舍情况：每个宿舍的人数 每个人的姓名 床铺号 已报道与未报道 未报到的人名


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)  # id
    username = db.Column(db.String(64), unique=True)  # 昵称
    name = db.Column(db.String(64))  # 姓名 important
    profile_photo = db.Column(db.Text(), default='default.jpg')  # 头像
    sex = db.Column(db.Integer)  # 性别 important
    grade = db.Column(db.String(64))  # 年级 important
    college = db.Column(db.String(64))  # 学院 important
    major = db.Column(db.String(64))  # 专业 important
    student_num = db.Column(db.String(12),
                            unique=True, index=True)  # 学号 important
    phone_num = db.Column(db.String(11), unique=True)  # 电话 important
    email = db.Column(db.String(64), unique=True, index=True)  # 邮箱地址
    password_hash = db.Column(db.String(128))  # 密码
    about_me = db.Column(db.Text())  # 个人介绍
    confirmed = db.Column(db.Boolean, default=False)  # 邮箱验证
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 用户身份
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'),
                           index=True, unique=True)  # 用户ID

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def add_permission(self, perm):
        if not self.role.has_permission(perm):
            self.role = Role.query.filter_by(
                permissions=self.role.permissions + perm).first()

    def remove_permission(self, perm):
        if self.role.has_permission(perm):
            self.role = Role.query.filter_by(
                permissions=self.role.permissions - perm).first()

    @property
    def password(self):
        raise AttributeError('密码未设定')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def generate_changePwd_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'pwd': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.add_permission(Permission.SPEAK)
        db.session.add(self)
        return True

    def forgetPwdConfirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('pwd') != self.id:
            return False
        return True

    # def generate_auth_token(self, expiration):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #     return User.query.get(data['id'])
    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'profile_photo': self.profile_photo,
            'sex': self.sex,
            'college': self.college,
            'major': self.major,
            'grade': self.grade,
            'student_num': self.student_num,
            'phone_num': self.phone_num,
            'email': self.email,
            'about_me': self.about_me,
            'confirmed': self.confirmed,
            'role_id': self.role_id,
            'student_id': self.student_id
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.name


class Dormitory(db.Model):
    __tablename__ = 'dormitories'
    id = db.Column(db.Integer, primary_key=True, index=True)
    dormitory_name = db.Column(db.String(32), index=True)  # 名称
    type_id = db.Column(db.Integer)  # 男女宿舍
    can = db.Column(db.Boolean, default=True)  # 是否可用
    live_number = db.Column(db.Integer)  # 宿舍最大人数
    now_number = db.Column(db.Integer, default=0)  # 宿舍目前人数

    def to_json(self):
        students = Student.query.filter_by(dormitory_id=self.id).all()
        json_post = {
            'name': self.dormitory_name,
            'now_number': self.now_number,
            'live_number': self.live_number,
            'students': [student.to_json() for student in students]
        }
        return json_post

    @staticmethod
    def generate_dormitory():
        dormitory_list = [['3号楼105', '1', '8'],
                          ['3号楼106', '1', '8'],
                          ['3号楼107', '1', '8'],
                          ['3号楼108', '1', '8'],
                          ['3号楼109', '1', '8'],
                          ['3号楼110', '1', '8'],
                          ['3号楼201', '1', '8'],
                          ['3号楼202', '1', '8'],
                          ['3号楼203', '1', '8'],
                          ['3号楼204', '1', '8'],
                          ['3号楼205', '1', '8'],
                          ['1号楼221', '0', '6'],
                          ['1号楼222', '0', '6'],
                          ['1号楼223', '0', '6'],
                          ['1号楼224', '0', '6'],
                          ['1号楼301', '0', '6'],
                          ['1号楼302', '0', '6'],
                          ['1号楼303', '0', '6'],
                          ['1号楼304', '0', '6'],
                          ['1号楼305', '0', '6'],
                          ['1号楼306', '0', '4']]
        for dormitory in dormitory_list:
            dd = Dormitory(dormitory_name=dormitory[0],
                           type_id=dormitory[1],
                           live_number=dormitory[2])
            db.session.add(dd)
        db.session.commit()

    def __repr__(self):
        return '<Dormitory %r>' % self.name


class Permission:
    ACCESS = 1
    SPEAK = 2
    PUBLISH = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)  # 默认用户
    permissions = db.Column(db.Integer)  # 用户权限
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Tourist': [],
            'UnauthenticatedUser': [Permission.ACCESS],
            'NormalUser': [Permission.ACCESS, Permission.SPEAK],
            'KXMember': [Permission.ACCESS, Permission.SPEAK,
                         Permission.PUBLISH],
            'Administrator': [Permission.ACCESS, Permission.SPEAK,
                              Permission.PUBLISH, Permission.ADMIN]
        }
        default_role = 'UnauthenticatedUser'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, index=True)  # id
    art_type = db.Column(db.String(64), index=True)  # 文章类型（activity或notice）
    title = db.Column(db.String(64), unique=True, index=True)  # 标题
    body = db.Column(db.Text)  # 正文
    image = db.Column(db.String(64))  # 图片
    filename = db.Column(db.String(64), index=True)  # 文件名
    timestamp = db.Column(db.String(64),
                          default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # 时间戳 格式%Y-%m-%d %H:%M:%S

    def to_json(self):
        json_user = {
            'id': self.id,
            'art_type': self.art_type,
            'title': self.title,
            'body': self.body,
            'image': self.image,
            'filename': self.filename,
            'timestamp': self.timestamp
        }
        return json_user

    def to_json_nobody(self):
        json_user = {
            'id': self.id,
            'art_type': self.art_type,
            'title': self.title,
            'image': self.image,
            'filename': self.filename,
            'timestamp': self.timestamp
        }
        return json_user

    def __repr__(self):
        return '<Article %r>' % self.name


class Applicant(db.Model):
    __tablename__ = 'applicant'
    id = db.Column(db.Integer, primary_key=True, index=True)  # id
    name = db.Column(db.String(24), index=True)  # 姓名
    sex = db.Column(db.Integer)  # 性别
    birthday = db.Column(db.String(12))  # 生日
    class_name = db.Column(db.String(12))  # 班级
    intention = db.Column(db.String(12), index=True)  # 意向
    qq = db.Column(db.String(24), unique=True)  # qq
    major = db.Column(db.String(24))  # 专业
    phone_num = db.Column(db.String(11), unique=True)  # 电话
    email = db.Column(db.String(64), unique=True)  # 邮箱地址
    specialty = db.Column(db.String(64))  # 爱好与特长
    office = db.Column(db.String(64))  # 曾担任的职务
    software = db.Column(db.String(64))  # 会用的软件
    about_me = db.Column(db.Text())  # 个人介绍
    cognition = db.Column(db.Text())  # 认知
    passed = db.Column(db.Integer, default=0)  # 是否通过申请

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'sex': self.sex,
            'birthday': self.birthday,
            'class_name': self.class_name,
            'intention': self.intention,
            'qq': self.qq,
            'major': self.major,
            'phone_num': self.phone_num,
            'email': self.email,
            'specialty': self.specialty,
            'office': self.office,
            'software': self.software,
            'about_me': self.about_me,
            'cognition': self.cognition,
            'passed': self.passed
        }
        return json_data

    def __repr__(self):
        return '<Applicant %r>' % self.name
