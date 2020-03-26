##################
# Python Builder #
##################

FROM python:3.7.5-slim-buster as python-builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

#########
# Final #
#########

FROM python:3.7.5-slim-buster

RUN adduser --group --system exporter

ENV HOME=/home/exporter
ENV APP_HOME=/home/exporter/nextcloud-exporter
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/venv
WORKDIR $APP_HOME

RUN apt update && apt upgrade -y \
    && apt autoclean \
    && apt autoremove -y
COPY --from=python-builder /usr/src/app/venv /usr/src/app/venv

ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY . $APP_HOME

RUN chown -R exporter:exporter $APP_HOME

user exporter

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "main:app_dispatch"]
