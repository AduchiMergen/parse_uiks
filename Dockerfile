FROM alpine
WORKDIR /srv/
ENV DEBUG False
COPY ./requirements.txt /srv/
RUN apk add --no-cache py3-psycopg2; \
    pip3 install -U pip; \
    pip3 install -r /srv/requirements.txt --no-cache-dir; \
    find / -type f -name "*.py[co]" -delete; \
    find / -type d -name "__pycache__" -delete
COPY . /srv/
CMD gunicorn --chdir ./src project.wsgi:application

