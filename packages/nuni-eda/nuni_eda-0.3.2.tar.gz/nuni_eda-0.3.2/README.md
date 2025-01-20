# nuni-eda
 - EDA cli that prints data filtered and sorted by keyword


### EDA Development environment setting
```bash
$ install pdm
$ git clone

# pdm venv create (at different delvelopment environment)
$ source .venv/bin/activate
$ pdm install pandas
$ pdm install jupyter lab
$ jupyter lab
...(coding)

$ git add <file_name>
$ git commit -a
$ git push
$ pdm publish
Username: __token__
# PR - Merge
# Tag - Release
```

### TEST
```bash
$ pdm add -dG test pytest
$ pytest
```


### Use
```bash
$ pip install nuni-eda
$ nuni-eda

```
