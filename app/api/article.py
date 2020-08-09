# -*- coding: utf-8 -*-
import codecs
import os
import markdown
import re
from flask import jsonify, request, render_template
# from werkzeug.utils import secure_filename
from . import api
from ..models import db, Article
from datetime import datetime

UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/static/articles/'


def createPath(file):
    file_dir = UPLOAD_FOLDER
    # filename = secure_filename(f.filename)
    filename = file.filename

    etc = filename.split('.', 1)[-1]
    if etc != 'md':
        return jsonify({'code': -1, 'message': '类型错误，应为md文档'})
    path = os.path.join(file_dir, filename)
    return path


@api.route('/article/uploadArt', methods=['POST', 'GET'])
def uploadArt():
    if request.method == 'POST':
        f = request.files['article']
        if f is not None:
            path = createPath(f)
            # if os.path.isfile(path):
            #     return jsonify({'code': -4, 'message': '上传失败，文章已存在'})
            f.save(path)

            file = codecs.open(path, 'r', 'utf-8')
            text = file.read()
            info = text.split('---')[1]
            body = text.split('---')[2]

            html = markdown.markdown(body)
            art_type = re.compile(r'art_type:\s(.*)\n').findall(info)[0]
            title = re.compile(r'title:\s(.*)\n').findall(info)[0]
            timestamp = re.compile(r'timestamp:\s(.*)\n').findall(info)[0]
            # timestamp = None
            # print(art_type, title, timestamp)
            # print(info)

            if all([body, art_type, title]):
                art = Article(body=html, art_type=art_type,
                              title=title, timestamp=timestamp)
                try:
                    db.session.add(art)
                    db.session.commit()
                except Exception as e:
                    # print(e)
                    return jsonify({'code': -3, 'message': '录入数据库失败'})
            else:
                return jsonify({'code': -2, 'message': '上传失败,信息缺失'})
            # return html
            return jsonify({'code': 1, 'message': '上传成功'})
        else:
            return jsonify({'code': 0, 'message': '上传失败'})


@api.route('/article/upgradeArt', methods=['POST', 'GET'])
def upgradeArt():
    if request.method == 'POST':
        f = request.files['article']
        if f is not None:
            path = createPath(f)
            # if not os.path.isfile(path):
            #     return jsonify({'code': -4, 'message': '文档不存在'})
            f.save(path)

            file = codecs.open(path, 'r', 'utf-8')
            text = file.read()
            info = text.split('---')[1]
            body = text.split('---')[2]

            title = re.compile(r'title:\s(.*)\n').findall(info)[0]
            art = Article.query.filter_by(title=title).first()
            if art is None:
                return jsonify({'code': -4, 'message': '文档不存在'})

            art_type = re.compile(r'art_type:\s(.*)\n').findall(info)[0]
            html = markdown.markdown(body)
            if all([body, art_type, title]):
                art.body = html
                art.art_type = art_type
                art.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    db.session.add(art)
                    db.session.commit()
                except Exception as e:
                    # print(e)
                    return jsonify({'code': -3, 'message': '更新数据库失败'})
            else:
                return jsonify({'code': -2, 'message': '更新失败,信息缺失'})
            # return html
            return jsonify({'code': 1, 'message': '更新成功'})
        else:
            return jsonify({'code': 0, 'message': '更新失败'})


@api.route('/article/deleteArt', methods=['POST', 'GET'])
def deleteArt():
    if request.method == 'POST':
        title = request.get_json().get('title')
        art = Article.query.filter_by(title=title).first()
        if art is None:
            return jsonify({'code': 0, 'message': '文章不存在'})
        try:
            db.session.delete(art)
            db.session.commit()
        except Exception as e:
            return jsonify({'code': -1, 'message': str(e)})

        # file_dir = UPLOAD_FOLDER
        # filename = title + '.md'
        # path = os.path.join(file_dir, filename)
        # if not os.path.isfile(path):
        #     return jsonify({'code': 0, 'message': '文档不存在'})
        # os.remove(path)
        return jsonify({'code': 1, 'message': '删除成功'})


@api.route('/article', methods=['GET', 'POST'])
def article():
    return render_template('file.html')
