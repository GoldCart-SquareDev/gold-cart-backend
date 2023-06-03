FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /goldcart

RUN apt-get update
RUN yes Y | apt-get install gdal-bin libgdal-dev
RUN yes Y | apt install python3-gdal
RUN apt install binutils libproj-dev
RUN yes Y | apt install python3-pip

COPY requirements.txt requirements.txt
RUN pip3  install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "migrate", "&&", "gunicorn", "gold_cart.wsgi"]