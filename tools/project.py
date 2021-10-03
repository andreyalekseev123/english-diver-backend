import os

from invoke import task

from . import (
    INTERPRETER_LOCAL,
    INVOKE_CONFIG_PATH,
    common,
    data,
    django,
    docker,
    is_local_python,
    tests,
)


@task
def init(context, interpreter=INTERPRETER_LOCAL):
    """Init project from scratch. Set up dev tools, Django app, services"""
    common.print_green("Preparing project for local development")
    create_invoke_config(interpreter)
    init_local(context)
    prepare_python_env(context)
    docker.startdb(context)
    django.migrate(context)
    django.createsuperuser(context)
    django.set_default_site(context)
    data.fill_sample_data(context)
    tests.run(context)


def init_local(context):
    """Create settings for local environment"""
    template_path = "config/settings/local.py.template"
    destination_path = "config/settings/local.py"
    context.run(f"cp {template_path} {destination_path}")


@task
def prepare_python_env(context):
    """Build python environ"""
    if is_local_python:
        sync_requirements(context)
    else:
        docker.build(context)


def create_invoke_config(interpreter, force=False):
    """Create `.invoke` file."""
    if force or not os.path.isfile(INVOKE_CONFIG_PATH):
        conf_data = (
            "[Project]\n"
            f"interpreter = {interpreter}"
        )
        with open(INVOKE_CONFIG_PATH, "w", encoding="locale") as config_file:
            config_file.write(conf_data)
        common.print_green(f"File `{INVOKE_CONFIG_PATH}` is created")
    else:
        common.print_yellow(f"File `{INVOKE_CONFIG_PATH}` already exists")


def sync_requirements(context, env="development"):
    """Install requirements."""
    common.print_green("Install requirements")
    context.run(f"pip-sync requirements/{env}.txt")
    context.run("pip install -r requirements/local_build.txt")


@task
def compile_requirements(context, upgrade=False):
    """Compile dependencies."""
    common.print_green("Compile requirements with pip-compile")
    upgrade = "--upgrade" if upgrade else ""
    in_files = [
        "development.in",
        "production.in",
    ]
    for in_file in in_files:
        with context.cd("requirements"):
            context.run(
                "pip-compile {in_file} {upgrade}".format(
                    in_file=in_file,
                    upgrade=upgrade)
            )
