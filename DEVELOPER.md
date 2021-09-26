# Developer Notes for msdss-base-api

Richard Wen  
rrwen.dev@gmail.com

## Install

Setup and install a development environment:

1. Install [git](https://git-scm.com/)
2. Install [Anaconda Python 3](https://www.anaconda.com/distribution/)
3. Install [GraphViz](https://www.graphviz.org/)
4. Clone this repository `git clone`
5. Move to the cloned folder `cd msdss-base-api`
6. Install python dependencies with `bin\install.bat` or `bin/install.sh`

In Mac OS (with [Homebrew](https://brew.sh/) installed):

```
brew install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-api
cd msdss-base-api
chmod +x bin/install.sh
source bin/install.sh
```

In Linux (Ubuntu):

```
apt install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-api
cd msdss-base-api
chmod +x bin/install.sh
source bin/install.sh
```

In Windows (with [Chocolatey](https://chocolatey.org/) installed):

```
choco install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-api
cd msdss-base-api
bin\install
```

## Virtual Python Environment

A [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) will also be created with `bin/install`, which installs the environment defined by `env.yml`.

If you are opening a new terminal, you will need to use `bin/activate` to activate the environment.

In Linux/Mac OS:

```
source bin/activate.sh
```

In Windows:

```
bin\activate
```

**Note**: The environment exists inside the `tmp/` folder.

## Documentation

The documentation is automatically built with [sphinx](http://www.sphinx-doc.org/en/master/).

### Building the documentation

You can build the documentation files into the `docs` folder by running `bin/build_docs`.

In Linux/Mac OS:

```
source bin/build_docs.sh
```

In Windows:

```
bin\build_docs
```

### Rebuilding the documentation

You can also completely rebuild the docs (reinstalling the package, and removing existing documentation) with `bin/rebuild_docs`.

In Linux/Mac OS:

```
source bin/rebuild_docs.sh
```

In Windows:

```
bin\rebuild_docs
```