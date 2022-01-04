FROM python:3.8-slim as base

RUN apt-get update && apt-get install --no-install-recommends -y iputils-ping

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local

COPY . /app_dir

WORKDIR /app_dir

EXPOSE 5000

CMD "./gunicorn_starter.sh"
