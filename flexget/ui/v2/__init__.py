import logging
import os

from flask import Flask, send_from_directory, render_template
from flask_compress import Compress

from flexget.webserver import register_app

log = logging.getLogger('webui')

config = None
exists = True

ui_base = os.path.dirname(os.path.realpath(__file__))
ui_dist = os.path.join(ui_base, 'dist')
ui_assets = os.path.join(ui_dist, 'assets')

webui_app = Flask(__name__, template_folder=ui_dist)
Compress(webui_app)
webui_app.url_path = '/v2/'


@webui_app.route('/assets/<path:path>')
def serve_app(path):
    return send_from_directory(ui_assets, path)


@webui_app.route('/')
@webui_app.route('/<path:path>')
def root(path='index.html'):
    if not exists:
        return send_from_directory(ui_base, 'index.html')
    return render_template('index.html', base_url=config['base_url'])


def register_web_ui(cfg):
    global config, exists
    config = cfg

    if not os.path.exists(ui_dist):
        exists = False
        log.fatal(
            'Failed to start web ui,'
            ' this can happen if you are running from GitHub version and forgot to run the web ui build, '
            'see http://flexget.com/wiki/Web-UI/v2 for instructions'
        )

    register_app(webui_app.url_path, webui_app)
