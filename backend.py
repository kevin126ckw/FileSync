from flask import Flask, render_template, request
from flask import send_from_directory

import os


app = Flask(__name__)


serverips = ['host']

basepath = os.path.dirname(__file__)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = '{0}/static/uploads/{1}'.format(basepath, f.filename)
        f.save(upload_path)
        return "done" + upload_path


    return render_template('upload.html')


@app.route('/download')
def download():
    dir_path = '{0}/static/uploads/'.format(basepath)
    filename = request.args.get('file')
    print('downloading ...')
    return send_from_directory(dir_path, filename, as_attachment=True)
@app.route('/files')
def files():
    filelist = []
    for path in os.listdir('{0}/static/uploads/'.format(basepath)):
        # check if current path is a file
        if os.path.isfile(os.path.join('{0}/static/uploads/'.format(basepath), path)):
            filelist.append(path)
    return render_template('files.html', filelist=filelist)


if __name__ == '__main__':
    app.run(port=6500,debug=True)
