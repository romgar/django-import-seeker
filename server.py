#-*- coding: utf-8 -*-

import os

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

from introspection import DjangoImportSeeker


@app.route('/')
def server():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():

    result = []
    if request.method == 'POST':
        string_to_find = request.form['string_to_find']

        os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy_settings'

        djangoIS = DjangoImportSeeker(string_to_find, 'django')

        result = djangoIS.process_seek()

    return render_template('home.html', result=" ".join(result))


if __name__ == '__main__':
    app.debug = True
    app.run()
