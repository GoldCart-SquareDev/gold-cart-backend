!# /bin/bash
python manage.py migrate
python manage.py collectstatic
gunicorn gold_cart.wsgi