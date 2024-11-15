from flask import Flask, render_template, request, redirect, url_for, make_response, stream_with_context, Response
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import requests
import urllib
from urllib import parse
from flask_basicauth import BasicAuth

# --------- CONFIG START ---------
debug = True
Authorization = '1677034306556'
app_port = 5000
bind_ip = '0.0.0.0'
header = {
    'Authorization': Authorization,
    #'Connection': 'keep-alive',
    # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFXTT4S1LKA1LUDBd',
    #'Cookie': 'SHIROJSESSIONID=75ace860-0f00-4db0-9440-6c6d53cdf101',
    #'Host': 'host:8088',
    #'Origin': 'http://host:8088',
    #'Referer': 'http://host:8088/njfxq/search/clue/clueFeedBackDetailAll?id=1574192996457648130&Paramspage=clue'
    #           '&caseId=1567439544410976257',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
    #              'Safari/537.36'

}
username = 'admin'
password = '111111'
force_auth = True
server_list = ['127.0.0.1']

# --------- CONFIG END -----------

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password
app.config['BASIC_AUTH_FORCE'] = force_auth
basepath = os.path.dirname(__file__)
basic_auth = BasicAuth(app)


@app.route('/', methods=['POST', 'GET'])
@basic_auth.required
def index():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basepath, 'static', secure_filename(f.filename))
        f.save(upload_path)
        print('uploading ...')
        fileObject = {
            'type': (None, '6', None),
            'orgType': (None, 'B', None),
            'file': (f.filename, open(upload_path, 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        for serverip in server_list:
            req = requests.post("http://" + serverip + ':6500/upload?file='+request.args.get('file'), headers=header,
                                files=fileObject)
            print("post server ", serverip, " back:", req.text)
        print("upload complete")

    return render_template('upload.html', server_list=server_list)


@app.route("/files")
@basic_auth.required
def files():
    #response = make_response(redirect("http://"+request.args.get('serverip') + ':6500/files'))
    response = requests.get("http://" + request.args.get('serverip') + ':6500/files', headers=header).text
    #response.headers['Authorization'] = Authorization
    #print(response.headers)
    if debug:
        type(response)
        print(response)
    return response


@app.route("/download")
@basic_auth.required
def download():
    #response = redirect("http://" + request.args.get('serverip') + ':6500/download')
    #response = redirect("/test")
    response = requests.get("http://"+request.args.get('serverip') + ':6500/download?file='+urllib.parse.quote(request.args.get('file')), headers=header, stream=True)
    response.headers['Authorization'] = Authorization
    #with app.test_request_context('/download'):
    #    requests.get(response.location, headers=header)
    if debug:
        print(response.headers)
    #return response
    back_header = {
        'Content-Disposition': 'attachment; filename='+urllib.parse.quote(request.args.get('file')),
        'Content-Type': response.headers['Content-Type'],
        'Content-Length': response.headers['Content-Length']
    }
    return Response(stream_with_context(response.iter_content(chunk_size=1024)), content_type = response.headers['content-type'], headers=back_header)
@app.route("/test")
def test():
    return str(request.headers)

if __name__ == '__main__':
    app.run(debug=debug, port=5000, host=bind_ip)
