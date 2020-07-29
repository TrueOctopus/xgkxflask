# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from ..models import User, db
from .form import EditProfileForm


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.college = form.college.data
        current_user.location = form.location.data
        current_user.class_name = form.class_name.data
        current_user.student_num = form.student_num.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('你的个人资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.college.data = current_user.college
    form.location.data = current_user.location
    form.class_name.data = current_user.class_name
    form.student_num.data = current_user.student_num
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
