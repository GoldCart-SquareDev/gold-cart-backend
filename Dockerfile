FROM ubuntu

WORKDIR /goldcart

RUN apt-get update
RUN yes Y | apt-get install gdal-bin libgdal-dev
RUN apt install python3-gdal
RUN apt install binutils libproj-dev
RUN apt install python3
RUN yes Y | apt install python3-pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
