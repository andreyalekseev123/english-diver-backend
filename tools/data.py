from invoke import task

from tools import django


@task
def fill_sample_data(
    context,
    script="fill_sample_data",
    script_args="--silent"
):
    """Fill database with sample data."""
    return django.manage(
        context,
        "runscript {} {}".format(script, script_args)
    )
