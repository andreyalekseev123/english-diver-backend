# Installing project for developing on local PC

You have to have following installed:
  * [docker](https://docs.docker.com/install/).
    Ensure you can run `docker` without `sudo`.
  * [docker-compose](https://docs.docker.com/compose/install/)
  * [invoke](https://pypi.org/project/invoke/).
    To install invoke and required packages, run:

    ```
    pip install -r requirements/local_build.txt
    ```
## Backend

Backend implemented using Python 3+ and Django.

For easier running of everyday tasks, like:

* run dev server
* run all tests
* run linters
* run celery workers
* ...

We use [invoke](https://pypi.org/project/invoke/).

It provide shortcuts for most of tasks, so it's like collection of bash scrips
or makefile or `npm scripts`.

Also it abstract "python interpreter", so you can use both `virtual env` and
`dockerized` python interpreter for working with project (see `.invoke` file).

* `virtualenv` is easier for experienced developer and allow faster packages
installation, flexibility and looking into sources.
* `dockerized` is simpler for quick starting project

See list of all available commands using `inv -l`

Run to prepare Django backend using dockerized env:

```
inv project.init --interpreter web
```

To start backend application use

```
inv django.run
```

### Virtual env

Default set up will use python interpreter from docker. This requires less
manual set up, but it is slower, and harder to debug application. You can
use virtualenv instead. But this require additional steps:

- Prepare venv and set up requirements
- Change interpreter in `.invoke` to `local`
- Set up aliases for docker hosts in `/etc/hosts`:
  ```
  127.0.0.1 postgres
  127.0.0.1 redis
  127.0.0.1 rabbitmq
  ```
