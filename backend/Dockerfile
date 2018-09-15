FROM python:3.7

COPY app /opt/app
COPY requirements.txt /opt/python/requirements.txt

RUN pip install -r /opt/python/requirements.txt \
 && rm -rf /opt/python

EXPOSE 8000

WORKDIR /opt/app
CMD python manage.py run -h 0.0.0.0 -p 8000

