from ..api import app
from ..error_handlers import *

@app.route('/index')
def index():
    return "Welcome to Glory Recipes!"