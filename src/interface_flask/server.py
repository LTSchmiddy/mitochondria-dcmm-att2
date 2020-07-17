import os
from flask import Flask, send_from_directory
import settings
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        # 'stream': 'ext://flask.logging.wsgi_errors_stream',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# app = Flask(__name__)

# app = Flask(__name__, root_path=os.getcwd(), template_folder="interface_flask/templates", static_folder="static")
# app = Flask(__name__, root_path=os.getcwd(), template_folder=settings['interface']['template-dir'], static_folder=settings['interface']['static-dir'])
app = Flask(__name__, root_path=os.getcwd())

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

from interface_flask.pages import pages
from interface_flask.panes import panes
from interface_flask.api import api

@pages.context_processor
def jinja2_values():
    def to_int(x):
        return int(x)

    return dict(
        settings=settings #,
        # to_int=to_int
    )




app.register_blueprint(pages, url_prefix='/')
app.register_blueprint(panes, url_prefix='/panes/')
app.register_blueprint(api, url_prefix='/api/')

