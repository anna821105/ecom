web: gunicorn main:app
web: gunicorn ecom.wsgi --log-file -
web: python manage.py migrate && gunicorn ecom.wsgi --log-file -
