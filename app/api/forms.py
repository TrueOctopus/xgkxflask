# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, length


class ForgetPwdForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired(),
                                               EqualTo(
                                                   'password2',
                                                   message='两次密码必须相同'),
                                               length(min=6, max=30,
                                                      message='长度必须为6位以上')])
    password2 = PasswordField('确认密码', validators=[DataRequired(),
                                                  length(min=6, max=30,
                                                         message='长度必须为6位以上')])
    submit = SubmitField('更改密码')
