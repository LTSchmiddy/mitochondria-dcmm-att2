import os
import sys

from flask import *
from interface_flask.server import app
from jinja2 import TemplateNotFound

from settings import current, exec_dir

print(os.path.join(exec_dir, current['interface']['pages']['template-dir']))
print(os.path.join(exec_dir, current['interface']['pages']['static-dir']))

pages = Blueprint(
    'pages',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['pages']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['pages']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['pages']['template-dir'],
    # static_folder=settings['interface']['pages']['static-dir']
)


# Page endpoints:
@pages.route('/blank')
def blank():
    return ""

@pages.route('/launch_settings')
def launch_settings():
    return render_template("launch_settings.html")

@pages.route('/startup')
def startup():
    return render_template("startup.html")

@pages.route('/')
def index():
    return render_template("index.html")


@pages.route('/lorem_ipsum')
def lorem_ipsum():
    return render_template("old/lorem_ipsum.html")



