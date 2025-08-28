import click
import json

from jsonschema import validate, ValidationError
from pathlib import Path

def populate_files(record, directory, pattern):

    matching_files = list(directory.glob(pattern))

    if matching_files:
        for fp in matching_files:
            record['files'] = json.load(
                fp.open('r')
            )

    return record
    
@click.command()
@click.option(
    '--if',
    'input_file_name',
    type=click.Path(exists=True),
    help='input file with dataset names',
    required=True
)
@click.option(
    '--of',
    'output_file_name',
    type=click.STRING,
    help='output record json file name',
    default="record.json"
)
@click.option(
    '--s',
    'json_schema_file',
    type=click.Path(exists=True),
    help='json schema file',
    required=True
)
@click.option(
    '--tf',
    'template_file',
    type=click.Path(exists=True),
    help='template record file',
    required=True
)
def main(input_file_name,
         output_file_name,
         json_schema_file,
         template_file
         ):

    input_datasets = [
        l.rstrip() for l in open(input_file_name, 'r').readlines()
    ]
    
    schema = json.load(
        open(json_schema_file, 'r')
    )

    record_template = json.load(
        open(template_file, 'r')
    )
    
    for d in input_datasets:

        dn = d.split('#')[0]

        record = record_template
        record['title'] = dn

        file_pattern = dn.split('/')[1]
        
        # The eos file names should be in the directory
        # and match the pattern
        directory = Path('output')
        
        if directory.is_dir():
            record = populate_files(
                record,
                directory,
                f'*{file_pattern}*.json'
            )
        
        try:
            validate(instance=record, schema=schema)
        except ValidationError as e:
            print(e)

        record_json = json.dumps(
            record,
            indent=3,
            sort_keys=True,
            separators=(",", ": ")
        )

        output_file_name = dn.replace('/', '_')
        output_file_name = f'CMS{output_file_name}_record.json'
        record_file = directory/output_file_name

        with record_file.open('w') as f:
            f.write(
                record_json
            )
    
            f.close()
    
if __name__ == "__main__":
    main()
