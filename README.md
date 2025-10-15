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

A workflow going from notebook, to Python code, to commmand line tool is fully supported. The first two steps of this workflow are often mentioned, creating your command line tools though is less popular. Creating your tools does not only save you time in the log run, it also helps you to structure your project. Lastly. If you think in tools, then you making the step to the cloud is often small. All cloud environments support workflows that execute tools; whether it is Github, Azure, AWS or GCP.

The project is structured in such a way that it can be used in a simple and more advanced way. 

The tools that are used in the examples are:

- python
- uv
- just
- taskfile
- turtlefmt
- jupyter
- git

All these tools are available for Windows, macOS and Linux. Note that for VS Code and Intellij all these tools have IDE plugins too.

uv is a tool that makes it easy to manage Python projects. It is a wrapper around pip and virtualenv. It is a newer version of a tool called Poetry. 

just is a command runner. just resembles make, it is more light-weight though. It is designed to run single commands or recipes. just can also be used anywhere on the command prompt. uv scripts, notebooks, anything can be made executable with it. It is even possible to embed Python code in justfiles.

Once you workflow gets a bit bigger, and you want to avoid running longer running tasks unnecessary, then taskfile can help you out. taskfile allows you to plan your whole workflow, and rerun necessary steps after you made changes to your project.

In general just is handy to notate technical commands that you want to run and don't want to be bothered remembering. Or if you would like to use different sparql reasoners strategies for example. taskfile is handy to plan your workflow for creating ontologies. It is possible then to refer to just for different strategies. See for example the section 'task primer'.

turtlefmt formats and validates your turtle files. This adds extra assurance to a publication process.

Python, git and Jupyter are assumed to be known and installed.

Additionally, you can install these ontology tools in your project:
- Jena ARQ
- ROBOT

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

The first command creates a virtual environment. The second command installs the project in the virtual environment. just, taskfile and turtlefmt are installed as well through PyPI.

If you are working in an IDE like VS Code or Intellij, then if you open a terminal, then the virtual environment will be activated automatically and tools like taskfile and just will be available. .

Alternatively, you can activate the virtual environment manually:
```sh
source .venv/bin/activate
```

This will 
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

To add a package to your project use:
```sh
uv add pandas
```

## just primer

just is installed for your project through uv. If you ran 'uv sync' then you are good to go.

For a crash course see: https://www.youtube.com/watch?v=W3pSSVwx--k

Here is a real enthousiast: https://www.youtube.com/watch?v=R6gBWDlQowM&t=60s

Just is more a command runner than a workflow engine. It shines in two ways:
- Use it as repository for commands you are likely to forget otherwise.
- Create simple recipes to automate task sequences you would otherwise do by hand.

To see how just can be used to automate workflows, see the justfile in the project. For example, you can run:
```sh
just run-test
```

This will run pytest.

## task primer
task is installed for your project through uv. If you ran 'uv sync' then you are good to go. For more information see: https://taskfile.dev/

###
See the taskfile.yaml for how to execute commands in such a way that task remembers if a task does not need to be rerun. By specifying sources and generates settings, task can track if a source changed since the last run. Also see the status directive to programmatically decide if a task is up to date.

Try running the following task twice:
```sh
task infer-toy
```
The infer task will run the hermit reasoner over the a small toy ontology and output the result to a file in the output directory. task refers to just to execute the right hermit settings. This way you can keep several hermit settings in just and refer to them in task.

You will see that the second time around task will notify you that the task is up to date. This is because the ontology did not change since the last run. This way you can easily create a workflow that only runs tasks that are necessary once you made changes to your project.

## Install your own command line tools

With uv it is easy to install your own Python command line tools. See the project.scripts section in the pyproject.toml file. If you run
the command below, the command line tools configured in project.scripts will be installed in the project directory so that you can execute them from
the project directory.

```sh
uv pip install --editable .
```

The --editable flag installs the project and the project.scripts in editable mode; meaning you can make changes to the project and the changes
will be reflected in the installed package.

If you changed the scripts in pyproject.toml, you have to reinstall the project.

If you have installed just:

```sh
just install-tools
```

You can now execute:

```sh
sparql-select -h
```

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv
```

This command line tool is created using the Python source code files. Command line tools can handily integrate with taskfile. If you upload your package to PyPI, then after installation these tools become automatically available to other developers.

## Getting your feet wet

To show how these tools all tie together, let's execute a SPARQL query. If you installed all the tools as described
above, you can execute a command to do this in four different ways.

Execute a SPARQL query using the Python interpreter, use the right venv:

```sh
python -m kgworkflow.tools.sparql_select  -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv
```

or 

```sh
uv run python -m kgworkflow.tools.sparql_select  -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv
```
Execute a SPARQL query using a uv script, see pyproject.toml for more information:

```sh
uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv
```

Execute a SPARQL query as a command line tool if you installed the project as a package using pip:

```sh
sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv
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

Also, as you are going to make changes to your repo, install the git pre-commit hooks. These hooks format your Python and Jupyter notebook files so that if someone else clones the repo, all the files look neat:

```sh
pre-commit install
```

Here is a controversial opinion: pre-commit hooks are over used. The number of hours spent by developers committing changes twice because a formatter or linter was complaining is staggering. Better to manually trigger a format, and have a check on the server side.

## Format your turtle files
Also installed through uv is turtlefmt, a formatter for turtle files. To format your turtle files, run:
```sh
turtlefmt test/resources/ttl/ input/ttl output
```
or:
```sh
just format-turtle
```
turtlefmt is also written in Rust, so it is very fast.

## Running notebooks

If you want to run Jupyter notebooks, check the notebooks directory. There you will find an example notebook that loads
a SPARQL query using the package developed in this project.

Note the extra magic (this is an official term for commands that start with %) at the top of the notebook. This magic tells Jupyter to reload the modules when the notebook is
executed. You need to re-import the modules when you change the code.

Also, you can run notebooks from the command line:
```sh
just run-notebook ./notebooks/example.ipynb
```

## Logging configuration
Special attention has been paid to the logging configuration. The logging configuration can be found in the logging.yaml file.

Note that for the module kgworkflow.util.helper the log level has been set to DEBUG. Fine grained logging configuration can help debugging and error reporting.

## Install ontology tools
To install ontology tools, run:
```sh
just install-ext
```

## Easily distribute your project as a package

uv can distribute your project as a package via for example PyPI. The command to upload your project as package to PyPI
is about as complex as:

```sh
uv publish
```

For example, a single project could have a set of SPARQL tools, ASK, SELECT, CONSTRUCT, validate and format for example. If you upload such a project to PyPI, then you can readily install it and use it in a different project.

Software quality requires reuse. Tools are designed to do just that. If you want quality software, consider thinking in tools.
