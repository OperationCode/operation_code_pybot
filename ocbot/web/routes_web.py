from flask import request, redirect, url_for, render_template, send_file, after_this_request

import logging
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from werkzeug.datastructures import FileStorage

from ocbot.pipeline.web_api_handlers.handle_code_school import handle_recaptcha_and_errors
from config.all_config_loader import configs
from ocbot import app

VERIFICATION_TOKEN = configs['SLACK_VERIFICATION_TOKEN']

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@limiter.request_filter
def ip_whitelist():
    """
    Whitelists localhost for limiter for development
    """
    return request.remote_addr in ["127.0.0.1", "localhost"]


@app.route("/add_code_school", methods=['POST'])
@limiter.limit("5/hour;1/minute")
def add_new_school():
    """
    This route receives the post from the /new_school form
    """
    imagefile: FileStorage

    try:
        imagefile = request.files['school_logo']
        if imagefile:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename)
            imagefile.save(filename)

    except Exception as e:
        print(e)

    if not imagefile:
        return ''

    return handle_recaptcha_and_errors(request, imagefile)


@app.route('/images/<filename>')
def get_image(filename):
    """
    Fetches stored image.  Used for codeschool icons.
    """
    filepath = os.path.join('web', 'imageStore', filename)
    file_handle = open(os.path.join('ocbot', filepath), 'r')

    @after_this_request
    def remove_file(response):
        try:
            os.remove(os.path.join('ocbot', filepath))
            file_handle.close()

        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filepath)


@app.route("/new_school", methods=['GET'])
def code_school_form():
    """
    This is the route to render the new codeschool form.
    """
    return render_template("code_school.html")


@app.route('/404')
def HTTP404():
    return render_template('HTTP404.html'), 404


@app.route('/403')
def HTTP403():
    return render_template('HTTP403.html'), 403


@app.route('/410')
def HTTP410():
    return render_template('HTTP410.html'), 410


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('HTTP404'))


@app.errorhandler(403)
def page_forbidden(error):
    return redirect(url_for('HTTP403'))


@app.errorhandler(410)
def page_gone(error):
    return redirect(url_for('HTTP410'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
