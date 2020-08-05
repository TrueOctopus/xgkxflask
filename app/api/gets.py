# -*- coding: utf-8 -*-
from flask import Response, jsonify
from . import api
from ..models import User, Article


@api.route('/gets/getById/<int:id>', methods=['GET'])
def getById(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 200
    return jsonify(user.to_json()), 201


@api.route('/gets/getList', methods=['GET'])
def getList():
    json_data = []
    for i in User.query:
        json_data.append(i.to_json())
    return jsonify(json_data), 201


@api.route('/gets/getImgs/<imgName>', methods=['GET'])
def getImgs(imgName):
    imgPath = '/home/zzy/xgkxflask/app/static/imgs/' + imgName
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = mdict[(imgName.split('.')[1])]
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)


@api.route('/gets/getAllArtList', methods=['GET'])
def getAllArtList():
    json_data = []
    for i in Article.query:
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getNoticeArtList', methods=['GET'])
def getNoticeArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='notice'):
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getActivityArtList', methods=['GET'])
def getActivityArtList():
    json_data = []
    for i in Article.query.filter_by(art_type='activity'):
        json_data.append(i.to_json())
    return jsonify(json_data)


@api.route('/gets/getArtById/<int:id>', methods=['GET'])
def getArtById(id):
    art = Article.query.filter_by(id=id).first()
    if not art:
        return jsonify({'code': 0, 'msg': '文章不存在'})
    return jsonify(art.to_json())
