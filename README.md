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



## Links:

*  Record schema information: https://github.com/cernopendata/cernopendata-portal/tree/main/cernopendata/jsonschemas/records

*  Example RAW record: https://opendata.cern.ch/record/67

*  JSON schema: https://json-schema.org/

