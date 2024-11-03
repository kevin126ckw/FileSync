from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import requests

debug = False

app = Flask(__name__)

header = {
    'Authorization': '1677034306556',
    'Connection': 'keep-alive',
    # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFXTT4S1LKA1LUDBd',
    'Cookie': 'SHIROJSESSIONID=75ace860-0f00-4db0-9440-6c6d53cdf101',
    'Host': 'host:8088',
    'Origin': 'http://host:8088',
    'Referer': 'http://host:8088/njfxq/search/clue/clueFeedBackDetailAll?id=1574192996457648130&Paramspage=clue&caseId=1567439544410976257',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

serverips = ['127.0.0.1']

basepath = os.path.dirname(__file__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(basepath, 'static', secure_filename(f.filename))
        f.save(upload_path)
        print('uploading ...')
        # 请求体Payload
        fileObject = {
            'type': (None, '6', None),
            'orgType': (None, 'B', None),
            'file': (f.filename, open(upload_path, 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        for serverip in serverips:
            req = requests.post("http://" + serverip + ':6500/upload', headers=header,
                            files=fileObject)
            print("post server ",serverip," back:",req.text)
        print("upload complete")

    return render_template('upload.html',serverips=serverips)


if __name__ == '__main__':
    app.run(debug=debug)
