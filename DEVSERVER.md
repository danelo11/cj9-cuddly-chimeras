# Bug Hunt 🐛

## Requirements

### Python

First of all, Python 3.10 needs to be installed on your machine. Preferably Python 3.10.5 which was the Python version used during the qualifier.

### Poetry

The project uses [`poetry`](https://python-poetry.org/) to create an isolated virtual environment and managed the entire packaging process at the same time.

#### Installation

>⚠️The installation process for Windows is different [`Windows`](https://python-poetry.org/docs/#windows-powershell-install-instructions)

```console
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

The installer installs the `poetry` tool to Poetry’s bin directory located at `$HOME/.poetry/bin`.

This directory will be automatically added to your `$PATH` environment variable, by appending a statement to your `*$HOME/.profile*` configuration (or equivalent files). If you do not feel comfortable with this, please pass the `--no-modify-path` flag to the installer and manually add the Poetry’s bin directory to your path.

Each time you open a new terminal, the poetry command is now available.

```console
$ poetry --version
Poetry version 1.1.14
```

If you want to update `poetry` to a concrete version:

```console
$ poetry self update 1.1.14
```

## Clone Repository

```console
$ cd ~

// ssh
$ git clone git@github.com:user/cj9-cuddly-chimeras.git

// https
$ git clone https://github.com/danelo11/cj9-cuddly-chimeras.git

---> 100%
Successfully cloned ✅
```

## Create the environment

Tell `Poetry` to create a virtual environment inside the root of the cloned directory `cj9-cuddly-chimeras`.

```console
$ poetry config virtualenvs.in-project true
```

Pick the Python version that you wanna use within your project:

```console
$ poetry env use <path to python executable>

// or you could directly use the following command if you have python exeutable in your Path

$ poetry env use python3.10
```

That will create a directory `./venv/` with the Python binaries and then you will be able to install packages for that isolated environment.


Install all the **Bug Hunt Game** dependencies in the isolated environment:

```console
$ poetry install
```

#### Activate the environment

```console
$ poetry shell
```

To check it worked, use:

```console
$ which python
home/user/cj9-cuddly-chimeras/.venv/bin/python
```

```console
$ python --version
Python 3.10.5
```

## Configure pre-commit

```console
$ poetry run pre-commit install
```

From now on, every time you try to commit, it checks proper linting and formatting first, before commiting

🎉You successfully complete the installation process🎉
