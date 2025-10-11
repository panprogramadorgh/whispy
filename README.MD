# WhisperPy

## Easy Installation

```sh
pip install whisperpy
```

## Manual Installation from Source

Pull the respository:

```sh
git pull --rebase origin main
```

Or clone if it wasn't already:

```sh
git clone git@github.com:panprogramadorgh/whisperpy.git
```

Initialize and update the submodules if needed:

```bash
git submodule update --init --recursive
```

After creating a virtual environment, install the package from the src directory of this project:

```sh
pip install ./src
```

## Installation for C++ Users

### Classic Pipeline

Run from the root of the project:

```sh
./configure.sh && ./make.sh
```

### Using Docker ?

There is a docker compose file in the project, so you can just run the following to compile the backend:

```sh
# This will raise a container that compiles the C++ backend for you.
docker compose up whisperpy_deploy_builder
```

> Note: Be carefull with docker builds because it uses a modern version of GCC that may require the latest versions of both libc and libstdc++.


## Runnint Tests

It is not necessary for most users, but is worth noting to know that you can run or write your own tests within the `./tests` directory.

All tests are written using the `unittest` python built-in package.

So in order to run the tests, you can do:

```sh
python3 -m unittest discover -s ./tests
```

> Note: Before running any tests, you have to be careful since one test may try to install the packages since it could be considered as part of the test.