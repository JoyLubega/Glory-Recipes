from Api.api import app
from Api.views import dummy_view, user_views, category_views

if __name__ == '__main__':
    app.run(debug=True)
