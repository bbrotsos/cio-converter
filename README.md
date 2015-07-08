first install schema dependencies
```
pip install jsonschema
```
Convert csv to json:

```
python3 src/convertCio.py data/cio-example.csv data/output.json
```
Convert json to csv:

```
python3 src/convertCio.py data/cio-example.json data/output.csv
```