# coding: utf-8
import os, sys
from flask import Flask, request, json, Response, jsonify, url_for, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
import filter

UPLOAD_FOLDER = 'public/images/tmp'
ALLOWED_EXTENSIONS = set(['PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'])

app = Flask(__name__, static_folder="public/images/tmp")
CORS(app, resources={r"/*": {"origins": "*"}})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/filter/comic', methods = ['POST'])
def filter_image():
    #app.logger.debug(request.files)
    # パラメータ名のチェック

    img_file = request.files['image']
    if not img_file or not allowed_file(img_file.filename):
        abort(400)

    stream = img_file.stream
    filtered_img = filter.apply_filter(stream, 'comic')
    return Response(response=filtered_img, content_type='image/jpeg')

@app.route('/filter/anime', methods = ['POST'])
def filter_image():
    #app.logger.debug(request.files)
    # パラメータ名のチェック

    img_file = request.files['image']
    if not img_file or not allowed_file(img_file.filename):
        abort(400)

    stream = img_file.stream
    filtered_img = filter.apply_filter(stream, 'anime')
    return Response(response=filtered_img, content_type='image/jpeg')

@app.errorhandler(400)
def error_handler(error):
    response = Response(response=None, status=400)
    return response

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
