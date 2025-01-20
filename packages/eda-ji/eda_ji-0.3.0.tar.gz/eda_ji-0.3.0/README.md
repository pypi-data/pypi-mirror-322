# eda-ji

presidents ranked by mentions of the Olympics in their speeches!

### USE
```
groupby( )
sort_value( )
```

### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyterlab
$ pdm add president-speech

$ vi pyproject.toml
$ pdm install

$ vi src/eda_ji/cli.py
$ eda-ji - test

$ git add
$ git commit
$ git push
$ pdm publish
```

### EDA
- run jupyterlab
```
$ jupyter lab
```

### Ref
- [install jupyterlab](https://jupyter.org/install)
- [install president](https://pypi.org/project/president-speech/)
