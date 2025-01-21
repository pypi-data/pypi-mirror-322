# jerreda

[![LGTM](https://lgtm.lol/p/843)](https://lgtm.lol/i/843)

## USE

### group_by_count(keyword: str)
```bash
$ pip install jerreda
$ python
>>> from jerreda.cli import group_by_count
>>> group_by_count(keyword: str=<KEYWORD>, asc: bool=<IS_ASC>, rcnt: int=<NUMBER>)
```

### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG add jupyterlab
$ pdm add president-speech

$ git add .
$ git commit -a
$ git push
$ pdm publish

View at:
https://pypi.org/project/jerreda/0.3.5/
```

### EDA
- run jupyterlab
```bash
$ jupyter lab

```

### TEST
```
# $ pdm add -dG test pytest
$ pytest
$ pytest -s
$ pytest --cov
```

## REF
- [Install Jupyterlab](https://jupyter.org/install)
- [PyPI President-speech](https://pypi.org/project/president-speech/)
