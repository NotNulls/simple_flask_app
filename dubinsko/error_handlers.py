from distutils.log import error
from flask import render_template, Blueprint
from dubinsko.routes import bp

bp = Blueprint('errors', __name__)

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500