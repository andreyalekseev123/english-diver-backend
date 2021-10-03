from . import docker, is_local_python

WAIT_FOR_IT_SCRIPT = "./tools/wait-for-it.sh postgres:5432 -- "


def run_web(context, command):
    """Run command in``web`` container.

    docker-compose run --rm web <command>
    """
    return docker.docker_compose_run(
        context,
        " ".join(["--service-ports", "web", command])
    )


def run_web_python(context, command):
    """Run command using web python interpreter"""
    return run_web(context, " ".join([WAIT_FOR_IT_SCRIPT, "python3", command]))


def run_local_python(context, command):
    """Run command using local python interpreter"""
    docker.startdb(context)
    return context.run(" ".join([
        WAIT_FOR_IT_SCRIPT,
        "python3",
        command
    ]))


if is_local_python:
    run_python = run_local_python
else:
    run_python = run_web_python
