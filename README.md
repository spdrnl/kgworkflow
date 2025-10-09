# kgworkflow

## Introduction

The goal of this project is to provide a simple and easy to use workflow for working with knowledge graphs. The idea is that you can mix and match:
- External command line tools
- Python in source code files
- Commandline tools developed by yourself
- Notebooks
- Automated workflow setups

The project shows:
- How to execute OWL related tasks using Python.
- How to create your own command line tools for these tasks.
- How to execute a workflow of command line tools.
- How to run Jupyter notebooks using developed Python modules.
- How to automate Jupyter notebooks.
- How to potentially distribute your project as a package.

The project is structured in such a way that it can be used in a simple and more advanced way. 

The tools that are used in the examples are:

- python
- uv
- just
- jupyter
- git

All these tools are available for Windows, macOS and Linux.

uv is a tool that makes it easy to manage Python projects. It is a wrapper around pip and virtualenv. It is a newer version of a tool called Poetry. 

just is a command runner. just resembles make, it is more light-weight though. It is designed to run recipes. just can also be used anywhere on the command prompt. uv scripts, notebooks, anything can be made executable with it. It is even possible to embed Python code in justfiles.

Python, git and Jupyter are assumed to be known and installed.

Contributions to this project are welcome. Do you have an interesting OWL or SPARQL task, create a pull request.

## If you do not want to use uv
If you do not want to run uv and just, you can install the required Python as follows:

```sh
pip install -r requirements.txt
```

Now you can use the project to develop Python programs.

It is in the long run recommended to use uv and just. These tools can save you a lot of time in the long run. On top of that, these tools are currently popular in main stream development teams.

## Install uv

To install uv on macOS and Linux you can run the following command:

```sh
wget -qO- https://astral.sh/uv/install.sh | sh
```

To install uv on Windows you can download the installer from https://astral.sh/uv/install.exe, or use PowerShell:

```sh
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

### Install project using uv
Open the env-RENAME-ME file and follow the instructions. Next execute the following commands:

```sh
uv venv
uv sync
```
or:
```sh
just install-project
```
### Run tests

With uv tests can be run as follows:

```sh
uv run pytest
```

You can also run the tests with pytest directly, but then you need to make sure that you use the correct Python
interpreter:

```sh
pytest
```

Having uv select the correct Python interpreter makes running a more advanced workflow easier later on.

### Quick overview of uv

A quick overview of uv commands is available at: https://docs.astral.sh/uv/getting-started/features/

For a crash course see: https://www.youtube.com/watch?v=zgSQr0d5EVg

## Install just

To install just see: https://just.systems/man/en/

For a crash course see: https://www.youtube.com/watch?v=W3pSSVwx--k

Here is a real enthousiast: https://www.youtube.com/watch?v=R6gBWDlQowM&t=60s

Just is more a command runner than a workflow engine. It shines in two ways:
- Use it as repository for command you are likely to forget otheriwse
- Create simple recipes to automate task sequences you would otherwise do by hand.

make is more advanced that just; for example it avoids running compilations if nothing changed. Just on the other hand is versatile, and can also easily be used outside development projects to create all kinds tools.
## Install your own command line tools

With uv it is easy to install command line tools. See the project.scripts section in the pyproject.toml file. If you run
the command below, the command line tools will be installed in the project directory so that you can execute them from
the project directory.

```sh
uv pip install --editable .
```

The --editable flag installs the project in editable mode; meaning you can make changes to the project and the changes
will be reflected in the installed package.

Or, if you have installed just:

```sh
just pip-install
```

If you changed the scripts in pyproject.toml, you have to reinstall the project.

You can now execute:

```sh
sparql-select -h
```

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

## Getting your feet wet

To show how these tools all tie together, let's execute a SPARQL query. If you installed all the tools as described
above, you can execute a command to do this in four different ways.

Execute a SPARQL query using the Python interpreter:

```sh
python -m kgworkflow.sparql_select  -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

Execute a SPARQL query using a uv script, see pyproject.toml for more information:

```sh
uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

Execute a SPARQL query as a command line tool if you installed the project as a package using pip:

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

Execute a SPARQL query as part of a workflow using just:

```sh
 just sparql-select
```

See the justfile for more information. On Windows the example command 'echo' might not work. In that case you can maybe
use 'echo.exe'.

In just, you can add options to the commands, and execute them in a specific order. This saves a lot of time and
memorizing the order of the commands.

## Developing your own command line tools

If you want to develop your own project using this project, issue this command to remove the remote origin from the
project:

```sh
git remote rm origin
```

or

```sh
just remove-origin
```

## Running notebooks

If you want to run Jupyter notebooks, check the notebooks directory. There you will find an example notebook that loads
a SPARQL query using the package developed in this project.

Note the extra magic at the top of the notebook. This magic tells Jupyter to reload the modules when the notebook is
executed. You need to re-import the modules when you change the code.

Also, you can run notebooks from the command line:
```sh
just run-notebook ./notebooks/example.ipynb
```

## Logging configuration
Special attention has been paid to the logging configuration. The logging configuration can be found in the logging.yaml file.

Note that for the module kgworkflow.util.helper the log level has been set to DEBUG. Fine grained logging configuration can help debugging and error reporting.
## Easily distribute your project as a package

uv can distribute your project as a package via for example PyPI. The command to upload your project as package to PyPI
is about as complex as:

```sh
uv publish
```

For example, a single project could have a set of SPARQL tools, ASK, SELECT, CONSTRUCT, validate and format for example. If you upload such a project to PyPI, then you can readily install it and use it in a different project.

Software quality requires reuse. Tools are designed to do just that. If you want quality software, consider thinking in tools.
