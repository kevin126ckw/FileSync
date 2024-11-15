from flask import Flask, render_template, request
from flask import send_from_directory

import os,socket
# --------- CONFIG START ---------
debug = True
Authorization = '1677034306556'
# --------- CONFIG END -----------
app = Flask(__name__)

basepath = os.path.dirname(__file__)


def auth(Token):
    if Token == Authorization:
        return True
    else:
        return False


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if auth(request.headers['Authorization']):
        if request.method == 'POST':
            f = request.files['file']
            upload_path = '{0}/static/uploads/{1}'.format(basepath, f.filename)
            f.save(upload_path)
            return "done" + upload_path

        return render_template('upload.html')
    else:
        return "403 Illegal access", 403


@app.route('/download')
def download():
    if debug:
        print("headers:", request.headers)
    if auth(request.headers['Authorization']):
        dir_path = '{0}/static/uploads/'.format(basepath)
        filename = request.args.get('file')
        print('downloading ...')
        print(dir_path, filename)
        return send_from_directory(dir_path, filename, as_attachment=True)
    else:
        return "403 Illegal access", 403


@app.route('/files')
def files():
    if debug:
        print("headers:", request.headers)
    if auth(request.headers['Authorization']):
        filelist = []
        for path in os.listdir('{0}/static/uploads/'.format(basepath)):
            # check if current path is a file
            if os.path.isfile(os.path.join('{0}/static/uploads/'.format(basepath), path)):
                filelist.append(path)
        return render_template('files.html', filelist=filelist, serverip = request.remote_addr)

    else:
        return "403 Illegal access", 403



if __name__ == '__main__':
    app.run(port=6500, debug=debug)
