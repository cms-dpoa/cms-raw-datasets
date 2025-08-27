import click
import os
import subprocess
import sys

def write_output(output, dir, file_name):
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    output_file = open(os.path.join(dir, file_name), 'w')
    output_file.write(output.stdout.decode())
    output_file.close()

@click.command()
@click.option(
    '--f',
    'file_name',
    type=click.Path(exists=True),
    help='input file with dataset names'
)
def main(file_name):
    '''
    Query dasgoclient for each dataset and 
    output the json to a file.
    '''
    if ( file_name is None ):
        raise click.UsageError("You must provide an input file name with the --f")

    dataset_names = [
        fn for fn in open(file_name, 'r').readlines()
    ]
    
    for dataset_name in dataset_names:
        
        # There may be block information in the
        # dataset_name that we don't use now.
        dataset_name = dataset_name.split("#")[0].strip()
        
        output_file_name = dataset_name.replace('/', '@')
        
        # Get the dataset information and write to files
        output = subprocess.run(
            [
                'dasgoclient',
                '-query',
                f'dataset={dataset_name}',
                '-json'
            ],
            capture_output=True
        )

        write_output(
            output,
            'das-json-store',
            f'{output_file_name}.json'
        )

        # Get the config information for the dataset and write to files
        output = subprocess.run(
            [
                'dasgoclient',
                '-query',
                f'config dataset={dataset_name}',
                '-json'
            ],
            capture_output=True
        )

        write_output(
            output,
            'das-json-store-config',
            f'{output_file_name}.json'
        )

if __name__ == '__main__':
    main()
