web: gunicorn main:app
web: gunicorn store.wsgi --log-file -
web: python manage.py migrate && gunicorn store.wsgi --log-file -
