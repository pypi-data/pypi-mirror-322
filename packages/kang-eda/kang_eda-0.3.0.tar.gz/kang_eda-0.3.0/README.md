# kang-eda
![LGTM](https://i.lgtm.fun/2vrl.png)

### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyterlab
$ pdm add <...>

$ git add .
$ git commit -m
$ git push
$ pdm publish
```

### EDA
- run jupyterlab

```
$ jupyter lab
```

### How To Use
```bash
$ pip install kang-eda or pdm add kang-eda
$ python
>>> from kang_eda.cli import group_by_count
>>> group_by_count()
```


### Ref
- [install jupyterlab](https://jupyter.org/install)
- [President](https://pypi.org/project/president-speech/)
