import os
import sys

from flask import *
from interface_flask.server import app
from jinja2 import TemplateNotFound

from settings import current, exec_dir

api = Blueprint(
    'api',
    __name__,
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['api']['template-dir'],
    # static_folder=settings['interface']['api']['static-dir']
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['api']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['api']['static-dir'])
)

@api.route('/')
def index():
    return {
        "Hello": "Alex"
    }


@api.route('/show_image')
def show_image():
    # if request.method == "POST":
    path = request.args['path']

    resp = make_response(open(path, 'rb').read())
    if path.endswith('.jpg'):
        resp.content_type = "image/jpeg"
    elif path.endswith('.png'):
        resp.content_type = "image/png"

    return resp






