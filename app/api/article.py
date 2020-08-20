# -*- coding: utf-8 -*-
import codecs
import os
import markdown
import re
from flask import jsonify, request, render_template, make_response, send_file
# from werkzeug.utils import secure_filename
from . import api
from ..models import db, Article
from datetime import datetime

UPLOAD_FOLDER = r'/home/zzy/xgkxflask/app/static/articles/'
# UPLOAD_FOLDER = r'app/static/articles/'  # 测试用


def createPath(file):
    file_dir = UPLOAD_FOLDER
    # filename = secure_filename(f.filename)
    filename = file.filename

    etc = filename.split('.', 1)[-1]
    if etc != 'md':
        return jsonify({'code': -1, 'message': '类型错误，应为md文档'})
    path = os.path.join(file_dir, filename)
    return path, filename.split('.')[0]


@api.route('/article/uploadArt', methods=['POST', 'GET'])
def uploadArt():
    if request.method == 'POST':
        f = request.files['article']
        if f is not None:
            path, file_name = createPath(f)
            if os.path.isfile(path):
                return jsonify({'code': -4, 'message': '上传失败，文章已存在'})
            f.save(path)

            file = codecs.open(path, 'r', 'utf-8')
            text = file.read()
            info = text.split('---', 2)[1]
            body = text.split('---', 2)[2]

            html = markdown.markdown(body,
                                     extensions=['markdown.extensions.tables'])

            images = re.compile(r'gets/getImgs/(.*)"').findall(html)
            img_str = '|'
            for img in images:
                img_str += str(img) + '|'
            # print(image_str)
            # print(info)
            art_type = re.compile(r'art_type:\s(.*)\r').findall(info)[0]
            # print(art_type)
            title = re.compile(r'title:\s(.*)\r').findall(info)[0]
            # print(title)
            timestamp = re.compile(r'timestamp:\s(.*)').findall(info)[0]
            # print("|"+timestamp+"|")
            # timestamp = None
            # print(art_type, title, timestamp)
            # print(info)

            if all([body, art_type, title, file_name]):
                art = Article(body=html, art_type=art_type,
                              title=title, image=img_str, filename=file_name)
                if len(timestamp) > 8:
                    # print(len(timestamp))
                    art.timestamp = timestamp
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
            path, file_name = createPath(f)
            # if not os.path.isfile(path):
            #     return jsonify({'code': -4, 'message': '文档不存在'})
            f.save(path)

            file = codecs.open(path, 'r', 'utf-8')
            text = file.read()
            info = text.split('---', 2)[1]
            body = text.split('---', 2)[2]

            title = re.compile(r'title:\s(.*)\r').findall(info)[0]
            art = Article.query.filter_by(title=title).first()
            if art is None:
                return jsonify({'code': -4, 'message': '文档不存在'})

            art_type = re.compile(r'art_type:\s(.*)\r').findall(info)[0]
            html = markdown.markdown(body,
                                     extensions=['markdown.extensions.tables'])

            images = re.compile(r'gets/getImgs/(.*)"').findall(html)
            img_str = '|'
            for img in images:
                img_str += str(img) + '|'
            # print(img_str)

            if all([body, art_type, title, file_name]):
                art.body = html
                art.image = img_str
                art.art_type = art_type
                art.filename = file_name
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


@api.route('/article/downloadArt', methods=['POST', 'GET'])
def downloadArt():
    name = request.form.get('name')
    if os.path.isfile(UPLOAD_FOLDER + name + '.md'):
        # ROOT_FOLDER = os.path.join(os.getcwd(), UPLOAD_FOLDER + name + '.md')
        ROOT_FOLDER = UPLOAD_FOLDER + name + '.md'
        response = make_response(send_file(ROOT_FOLDER, name + '.md',
                                           as_attachment=True))
        return response
    else:
        return jsonify({'code': 0, 'message': '文件不存在'})


@api.route('/article', methods=['GET', 'POST'])
def article():
    return render_template('file.html')
