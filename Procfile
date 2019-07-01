web: gunicorn run:app
release: python manage.py db downgrade
release: python manage.py db migrate
release: python manage.py db upgrade
