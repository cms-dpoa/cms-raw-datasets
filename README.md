# cms-raw-datasets

## Usage:


Generate the `.txt` and `.json` files with the eos links:
```
python3 make_eos_file_information.py --f <input file with dataset names>
```
which outputs the files into the `output` dir.


Generate the information from DAS regarding the datasets:
```
python3 make_das_json_information.py --f <input file with dataset names>
```


You may need to generate a GRID proxy before running the above command:
```
voms-prozy-init --voms cms
```


Generate the RAW dataset records:
```
python make_raw_dataset_record.py --if EphemeralHLTPhysics-datasets.txt  --s record-v1.0.0.json --tf EphemeralHLTPhysics_template.json
python make_raw_dataset_record.py --if ZeroBias-datasets.txt  --s record-v1.0.0.json --tf ZeroBias_template.json
```
which are generated, validated with the schema, and written to `output`.


```
Usage: make_raw_dataset_record.py [OPTIONS]

Options:
  --if PATH  input file with dataset names  [required]
  --of TEXT  output record json file name
  --s PATH   json schema file  [required]
  --tf PATH  template record file  [required]
  --help     Show this message and exit.
```


## Links:

*  Record schema information: https://github.com/cernopendata/cernopendata-portal/tree/main/cernopendata/jsonschemas/records

*  Example RAW record: https://opendata.cern.ch/record/67

*  JSON schema: https://json-schema.org/

