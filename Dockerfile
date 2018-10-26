FROM alpine
WORKDIR /srv/
ENV DEBUG False
RUN echo '@testing http://nl.alpinelinux.org/alpine/edge/testing'  >> /etc/apk/repositories; \
    apk add --no-cache py3-psycopg2 gdal@testing geos@testing
RUN rm -rf /root/.cache; ln -s /dev/null /root/.cache
RUN pip3 install -U pip poetry --no-cache-dir
#RUN poetry config settings.virtualenvs.in-project true
RUN poetry config settings.virtualenvs.create false
COPY ./pyproject.toml /srv/
COPY ./poetry.lock /srv/
RUN poetry install -n ; \
    find / -type f -name "*.py[co]" -delete; \
    find / -type d -name "__pycache__" -delete
COPY . /srv/
CMD gunicorn --chdir ./src project.wsgi:application -w 4 -b 0.0.0.0:8000


