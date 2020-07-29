# -*- coding: utf-8 -*-
from flask import jsonify
from . import api
from ..models import User


@api.route('/getById/<int:id>', methods=['GET'])
def getById(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 200
    return jsonify(user.to_json()), 201
