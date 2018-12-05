FROM python:3.7.1-stretch

RUN pip install pipenv

COPY . /src
WORKDIR /src

RUN pipenv install --system
RUN mkdir /src/data

CMD errbot
