from invoke import UnexpectedExit, task

from .common import print_green

DATABASE_CONTAINERS = (
    "postgres",
    "redis",
)


@task
def startdb(context):
    """Start postgres and redis

    By default, they start as daemons
    """
    run_containers(context, *DATABASE_CONTAINERS, d=True)


@task
def build(context, clean=False):
    """Build a docker image with the necessary parameters.
    """
    context.run(
        "DOCKER_BUILDKIT=1 "
        "docker build . "
        "--file ci/docker/Dockerfile "
        "--tag english-diver-backend "
        "--build-arg REQUIREMENTS_FILE=development "
        f"--no-cache={clean}"
    )


def docker_compose_up(context, command):
    """Up ``command`` using docker-compose

    docker-compose up <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    return context.run(" ".join(["docker-compose", "up", command]))


def docker_compose_run(context, command):
    """Run ``command`` using docker-compose

    docker-compose run <command>

    Used function so lately it can be extended to use different docker-compose
    files
    """
    return context.run(" ".join(["docker-compose", "run", "--rm", command]))


def run_containers(context, *containers, **kwargs):
    """Run containers

    If redis can't start, we decide that it's already running and don't showing
    errors.
    """
    print_green("Start {} containers ".format(containers))
    for container in containers:
        run_string = " ".join([
            "docker-compose",
            "up",
            "-d" if kwargs.get("d") else "",
            container
        ])
        if container != "redis":
            context.run(run_string)
        else:
            try:
                context.run(run_string)
            except UnexpectedExit:
                pass


def stop_containers(context, *containers):
    """Stop containers
    """
    print_green("Stopping {} containers ".format(containers))
    context.run(
        " ".join(["docker-compose", "stop"] + list(containers))
    )
