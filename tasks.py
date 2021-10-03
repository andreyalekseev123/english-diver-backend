from invoke import Collection

from tools import (
    celery,
    data,
    django,
    docker,
    project,
    system,
    tests,
)

ns = Collection(
    celery,
    data,
    django,
    docker,
    project,
    system,
    tests,
)

# Configurations for run command
ns.configure({"run": {"pty": True, "echo": True}})
