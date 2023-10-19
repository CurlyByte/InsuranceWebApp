from flask import render_template, Blueprint

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.route
def page_not_found():
    return render_template("404.html"),404



