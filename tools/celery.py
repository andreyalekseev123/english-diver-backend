from invoke import task

from . import is_local_python
from .docker import run_containers


@task
def run(context):
    """Start celery worker"""
    if is_local_python:
        context.run(
            "celery --app config.celery:app worker --beat --scheduler=django "
            "--loglevel=info"
        )
    else:
        run_containers(context, "celery")
