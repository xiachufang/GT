FROM python:3.7

RUN pip3 install pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN set -ex && pipenv install --deploy --system

COPY . /app

CMD ./run
