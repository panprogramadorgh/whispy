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

Select the kind of build that you want to compile. Regular builds are considered for testing, so for production you will need the deployment one.

```bash
docker compose up whisperpy_deploy_builder
```

By doing this whole process, you should be able to compile whisperpy's backend binaries.