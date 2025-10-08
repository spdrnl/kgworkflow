## If you do not want to use uv
If you do not want to run uv, you can install the required Python as follows:
```sh
pip install -r requirements.txt

It is in the long run recommended to use uv. In the next section we will see how to use uv.

## Install uv
For macOS and Linux you can install uv with the following commands:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick overview of uv
A quick overview of uv commands is available at: https://docs.astral.sh/uv/getting-started/features/

## Install uv
To install uv on macOS and Linux you can run the following command:
```sh
wget -qO- https://astral.sh/uv/install.sh | sh
```
To install uv on Windows you can download the installer from https://astral.sh/uv/install.exe, or use PowerShell:
```sh
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

## Install Python packages
```sh
uv sync
```

## Run test
With uv tests can be run as follows:
```sh
uv run pytest
```

## Install command line tools
With uv it is easy to install command line tools. See the project.scripts section in the pyproject.toml file. If you run the command below, the command line tools will be installed in the project directory.
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
## Easily distribute your project as a package
uv can distribute your project as a package via for example PyPI. The command to upload your project as package to PyPI is about as complex as:
```sh
uv publish
```
