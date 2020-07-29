# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    name = StringField('你的姓名', validators=[Length(0, 64)])
    college = StringField('学院', validators=[Length(0, 64)])
    class_name = StringField('班级', validators=[Length(0, 64)])
    student_num = IntegerField('学号', validators=[Length(0, 12)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = TextAreaField('个人介绍')
    submit = SubmitField('提交')
