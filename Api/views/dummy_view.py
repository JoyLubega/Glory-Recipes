from ..api import app
from ..error_handlers import * # noqa F401


@app.route('/index')
def index():
    return "Welcome to Glory Recipes!"
