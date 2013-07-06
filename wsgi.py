import os
from bottle import Bottle, mako_view
application = Bottle()


def linecount(filename):
    lines = -1
    with open(filename, 'rb') as fp:
        for lines, _ in enumerate(fp):
            pass
    return lines


@application.route('/')
@mako_view('index.mako')
def index():
    filenames = ['dates/' + filename for filename in os.listdir('dates')]
    files = [dict(name=filename, lines=linecount(filename)) for filename in filenames]
    return dict(files=files)
