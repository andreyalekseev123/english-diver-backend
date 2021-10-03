FROM python:3.9.1-slim-buster as backend

WORKDIR /app
ENV C_FORCE_ROOT=True \
    DJANGO_SETTINGS_MODULE=config.settings.deploy

RUN apt-get update && \
    apt-get install -y \
      git \
      mime-support \
      openssh-client \
      curl && \
    ### Install tools for python
    pip install -U --no-cache-dir pip setuptools wheel && \
    ### Cleaning up unused files
    apt-get purge -yqq --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*


### Django environment variable. Used for settings and requirements installation
ARG REQUIREMENTS_FILE=development
ENV REQUIREMENTS_FILE=${REQUIREMENTS_FILE}

### Install requirements
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/${REQUIREMENTS_FILE}.txt

### Add config files to container
COPY ci/rootfs /
# CMD is set in ECS task definition as there are different CMDs for celery/uwsgi
# TODO: celery worker and beat started using single cmd for simplicity,
# need to separate beat/worker when few celery workers will be needed

### Add source code to container
COPY . /app
