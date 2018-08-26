FROM alpine
WORKDIR /srv/
ENV DEBUG False
COPY ./requirements.txt /srv/
RUN  echo '@testing http://nl.alpinelinux.org/alpine/edge/testing'  >> /etc/apk/repositories
RUN apk add --no-cache py3-psycopg2 gdal@testing geos@testing; \
    pip3 install -U pip; \
    pip3 install -r /srv/requirements.txt --no-cache-dir; \
    find / -type f -name "*.py[co]" -delete; \
    find / -type d -name "__pycache__" -delete
COPY . /srv/
CMD gunicorn --chdir ./src project.wsgi:application -w 4 -b 0.0.0.0:8000


