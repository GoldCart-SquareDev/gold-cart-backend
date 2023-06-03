!# /bin/bash
python manage.py collectstatic
gunicorn gold_cart.wsgi