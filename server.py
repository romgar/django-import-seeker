#-*- coding: utf-8 -*-

import os

from flask import Flask
from flask import render_template
app = Flask(__name__)

from introspection import DjangoImportSeeker


@app.route('/')
def server():
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy_settings'

    djangoIS = DjangoImportSeeker('render', 'django')

    result = djangoIS.process_seek()
    return render_template('home.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
