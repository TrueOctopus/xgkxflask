# -*- coding: utf-8 -*-
from flask import redirect, render_template
from . import test


@test.route('/justanegg', methods=['GET'])
def justanegg():
    return render_template('egg.html')


@test.route('/justanotheregg', methods=['GET'])
def justanotheregg():
    return render_template('justanotheregg.html')


@test.route('/xgkxnb', methods=['GET'])
def xgkxnb():
    return redirect('http://81.70.11.36/api/v1/gets/getImgs/xgkxnb.jpg')
