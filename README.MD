# WhisperPy

## Compilation Steps

Pull the respository:

```bash
git pull --rebase origin main
```

Initialize and update the submodules if needed:

```bash
git submodule init
git submodule update
```

Build a docker image:

```bash
docker build -t whisperpy
```

And run the container:

```bash
docker container run -n your_container_name whisperpy
```

Doing this whole process, it will compile library backend and run a high level interface [test](./tests/basic-test.py).