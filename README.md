_work in progress_

first install schema dependencies
```
pip install jsonschema
```

Populate example [csv](data/cio-example.csv)

Convert csv to json:

```
python3 src/convertCio.py data/cio-example.csv data/output.json
```

If you want to convert JSON file back to csv
Convert json to csv:
```
python3 src/convertCio.py data/cio-example.json data/output.csv
```