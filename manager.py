import json
import html
from hashlib import md5
from os import listdir
from os.path import isfile, join, normpath

from flask import Flask, request, send_file, redirect, render_template, render_template_string
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
from werkzeug.datastructures import FileStorage

FILES_PATH = "files/"

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth(realm="DogeFileManager")

# Load users from file
with open('users.json', 'r') as file:
    users = json.load(file)

@auth.verify_password
def verify_password(username, password):
    return username in users and users[username] == md5(password.encode()).hexdigest()

@app.route('/')
@auth.login_required
def bork():
    msg = request.args.get('message')
    if not msg:
       return render_template('index.html')
    else:
        msg = html.escape(msg)
        return render_template_string('{{% extends "index.html" %}}{{% block msg %}}<div class="alert alert-primary">{}</div>{{% endblock %}}'.format(msg))

class FileListResource(Resource):
    @auth.login_required
    def get(self):
        return [f for f in listdir(FILES_PATH) if isfile(join(FILES_PATH, f))]

    @auth.login_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('uploadedFile', type=FileStorage, location='files')

        args = parse.parse_args()

        filePath = FILES_PATH + args['uploadedFile'].filename
        if normpath(filePath).startswith(".."):
            return redirect("/?msg=Invalid%20filename.", code=301)

        with open(filePath, 'wb') as file:
            file.write(args['uploadedFile'].read())

        return redirect("/?message=Sent!", code=301)

class FileResource(Resource):
    @auth.login_required
    def get(self, filename):
        return send_file(FILES_PATH + filename, as_attachment=True)

api.add_resource(FileListResource, '/files')
api.add_resource(FileResource, '/files/<string:filename>')

if __name__ == '__main__':
    app.run(debug=True)
