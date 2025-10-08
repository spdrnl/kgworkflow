# kg-workflow

## Introduction

The goal of this project is to provide a simple and easy to use workflow for working with knowledge graphs. The project
shows:

- How to execute OWL related tasks using Python.
- How to create your command line tools using for these tasks.
- How to execute a workflow of commands line tools.
- How to potentially distribute your project as a package.

The project is structured in such a way that it can be used in a simple and more advanced way. Below are some examples
of the type of commands that the project will allow you to execute. The tools that are used in the examples are:

- python
- uv
- just

uv is a tool that makes it easy to manage Python projects. It is a wrapper around pip and virtualenv. It is a newer version of a tool called Poetry. just is a tool similar to make. make, although a standard under Linux, is somewhat dated. All these tools are available for Windows, macOS and Linux.

Execute a SPARQL query using the Python interpreter:

```sh
python -m sparql_select  -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv```
```

Execute a SPARQL query using uv:

```sh
uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

Execute a SPARQL query as a command line tool:

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```

Execute a SPARQL query as part of a workflow using just:

```sh
 just sparql-select-test
```

## If you do not want to use uv

If you do not want to run uv and just, you can install the required Python as follows:

```sh
pip install -r requirements.txt
```

Now you can use the project to develop Python programs.

It is in the long run recommended to use uv and just. These tools can save you a lot o time.

## Install uv

To install uv on macOS and Linux you can run the following command:

```sh
wget -qO- https://astral.sh/uv/install.sh | sh
```

To install uv on Windows you can download the installer from https://astral.sh/uv/install.exe, or use PowerShell:

```sh
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

### Install Python packages

```sh
uv sync
```

### Run test
With uv tests can be run as follows:

```sh
uv run pytest
```

You can also run the tests with pytest directly, but then you need to make sure that you use the correct Python interpreter:

```sh
pytest
```
Having uv select the correct Python interpreter makes running a more advanced workflow easier.

### Quick overview of uv

A quick overview of uv commands is available at: https://docs.astral.sh/uv/getting-started/features/

## Install command line tools

With uv it is easy to install command line tools. See the project.scripts section in the pyproject.toml file. If you run
the command below, the command line tools will be installed in the project directory so that you can execute them from the project directory.

```sh
uv pip install --editable
```

The --editable flag installs the project in editable mode; meaning you can make changes to the project and the changes will be reflected in the installed package.

You can now execute:

```sh
sparql-select -h
```

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv
```
## Install just
To install just see: https://just.systems/man/en/

## Execute a workflow
To execute a workflow with just run:
```sh
 just sparql-select-test
```

See the justfile for more information. On Windows the example command 'echo' might not work. In that case you can can maybe use 'echo.exe'.

In just, you can add options to the commands, and execute them in a specific order. This saves a lot of time and memorizing the order of the commands.

## Easily distribute your project as a package

uv can distribute your project as a package via for example PyPI. The command to upload your project as package to PyPI
is about as complex as:

```sh
uv publish
```
