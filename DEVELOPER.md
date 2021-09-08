# Developer Notes for msdss-base-api

Richard Wen  
rrwen.dev@gmail.com

## Install

Setup and install a development environment:

1. Install [Anaconda Python 3](https://www.anaconda.com/)
2. Clone this repository `git clone`
3. Move into the cloned folder `cd`
4. Create a virtual environment for development `conda env create`

```bash
git clone https://github.com/rrwen/msdss-base-api
cd msdss-base-api
conda env create -f environment.yml
```

For Mac OSX/Linux users, `sudo` may be used to create the virtual environment:

```bash
git clone https://github.com/rrwen/msdss-base-api
cd msdss-base-api
sudo conda env create -f environment.yml
```

## Recreating the Virtual Environment

To recreate the virtual environment (when (environment.yml)[environment.yml] is changed):

1. Remove the virtual environment `conda remove`
2. Recreate the virtual environment `conda create`

```
conda remove -y --name msdss-base-api --all
conda env create -f environment.yml
```

## Local Package Install

Install the package locally for testing:
s
1. Activate virtual environment `conda activate`
2. Build distribution files in the *dist/* folder `python -m build`
3. Remove existing installations `pip uninstall`
4. Install locally using distribution files `pip install`

```bash
conda activate msdss-base-api
python -m build
pip uninstall msdss-base-api
pip install dist/msdss-base-api-<VERSION>.tar.gz
```

**Note**: Replace `<VERSION>` with the version seen in the *dist/* folder.