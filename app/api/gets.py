# -*- coding: utf-8 -*-
import math

from flask import Response, jsonify, request, current_app
import jwt
from sqlalchemy import text

from . import api
from ..models import User, Article
# from flask_pagination import Pagination

UPLOAD_ART_FOLDER = r'/home/zzy/xgkxflask/app/static/imgs/artimgs/'
UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/static/imgs/'
# UPLOAD_FOLDER = r'app/static/imgs/'


@api.route('/gets/getById/<int:id>', methods=['GET'])
def getById(id):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        id_jwt = payload.get('user_id')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if id_jwt == id:
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'msg': '用户不存在'}), 200
        return jsonify(user.to_json()), 201


@api.route('/gets/getByEmail/<email>', methods=['GET'])
def getByEmail(email):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        email_jwt = payload.get('email')
    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    if email_jwt == email:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'msg': '用户不存在'}), 200
        return jsonify(user.to_json()), 201


@api.route('/gets/getList', methods=['GET', 'POSt'])
def getList():
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token,
                             key=current_app.config['SECRET_KEY'],
                             algorithm='HS256')
        permission = payload.get('permission')

    except Exception as e:
        # print(e)
        return jsonify({'code': 0, 'message': 'token失效请重新登录'})

    pageNum = request.get_json().get('pageNum')
    pageSize = request.get_json().get('pageSize')
    name = request.get_json().get('name')
    sex = request.get_json().get('sex')
    email = request.get_json().get('email')
    phone_num = request.get_json().get('phone_num')

    if permission == 'Authorization' or 'KXMember':

        all_results = User.query.filter(
            User.name.like(
                "%" + name + "%") if name is not None else text(''),
            User.sex.like(
                "%" + sex + "%") if sex is not None else text(''),
            User.email.like(
                "%" + email + "%") if email is not None else text(''),
            User.phone_num.like(
                "%" + phone_num + "%") if phone_num is not None else text('')
        )
        count = len(all_results.all())
        json_data = []
        page = all_results.paginate(page=pageNum,
                                    per_page=pageSize)
        for i in page.items:
            json_data.append(i.to_json())
        # for i in User.query:
        #     json_data.append(i.to_json())
        # start = (pageNum - 1) * pageSize
        # end = pageNum * pageSize \
        #     if len(json_data) > pageNum * pageSize else len(json_data)
        # paginate = Pagination(page=pageNum, total=len(json_data))
        data = {'data': json_data, 'count': count}
        return jsonify(data), 201


@api.route('/gets/getImgs/<imgName>', methods=['GET'])
def getImgs(imgName):
    imgPath = UPLOAD_FOLDER + imgName
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'svg': 'image/svg+xml'
    }
    mime = mdict[(imgName.split('.')[1])]
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@api.route('/gets/getArtImgs/<imgName>', methods=['GET'])
def getArtImgs(imgName):
    imgPath = UPLOAD_ART_FOLDER + imgName
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'svg': 'image/svg+xml'
    }
    mime = mdict[(imgName.split('.')[1])]
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@api.route('/gets/getAllArtList', methods=['GET'])
def getAllArtList():
    json_data = []
    for i in Article.query.order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getNoticeArtList', methods=['GET'])
def getNoticeArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='notice')\
            .order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getActivityArtList', methods=['GET'])
def getActivityArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='activity')\
            .order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getArtById/<int:id>', methods=['GET'])
def getArtById(id):
    art = Article.query.filter_by(id=id).first()
    if not art:
        return jsonify({'code': 0, 'msg': '文章不存在'})
    return jsonify(art.to_json())


# 无正文返回
@api.route('/gets/getNoBodyArtList', methods=['GET'])
def getNoBodyArtList():
    json_data = []
    for i in Article.query.order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json_nobody())
    return jsonify(json_data)


@api.route('/gets/getNoBodyNoticeArtList', methods=['GET'])
def getNoBodyNoticeArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='notice')\
            .order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json_nobody())
    return jsonify(json_data)


@api.route('/gets/getNoBodyActivityArtList', methods=['GET'])
def getNoBodyActivityArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='activity')\
            .order_by(Article.timestamp.desc()).all():
        json_data.append(i.to_json_nobody())
    return jsonify(json_data)


@api.route('/gets/getNoBodyArtById/<int:id>', methods=['GET'])
def getNoBodyArtById(id):
    art = Article.query.filter_by(id=id).first()
    if not art:
        return jsonify({'code': 0, 'msg': '文章不存在'})
    return jsonify(art.to_json_nobody())
