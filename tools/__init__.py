import configparser

INTERPRETER_WEB = "web"
INTERPRETER_LOCAL = "local"
INVOKE_CONFIG_PATH = ".invoke"

# read config
# config should be saved in file with name ".invoke"
# Format:
# ## .invoke
# [Project]
# interpreter = local

config = configparser.ConfigParser({"interpreter": INTERPRETER_WEB})
config.read(INVOKE_CONFIG_PATH)

# pylint: disable=invalid-name
project_interpreter = INTERPRETER_WEB

if config.has_section("Project"):
    project_interpreter = config.get("Project", "interpreter")

is_local_python = (project_interpreter == INTERPRETER_LOCAL)
