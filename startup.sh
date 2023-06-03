! /bin/bash
python3 manage.py migrate
gunicorn gold_cart.wsgi