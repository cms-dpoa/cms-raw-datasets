import click
import json
import os
import re
import subprocess

from pathlib import Path

EOS_BASE_URI = "root://eospublic.cern.ch/"
os.environ["EOS_MGM_URL"] = EOS_BASE_URI

def get_dataset_dir(dataset_name, eos_base_dir):
    '''
    In eos the dataset directory is formed from 
    dataset name /NAME/RUNPERIOD-VERSION/FORMAT
    such that the data files will be found under
    EOS_BASE_DIR/RUNPERIOD/NAME/FORMAT/VERSION
    '''
    dn = dataset_name.split('/')
    assert len(dn) == 4    
    rpv = dn[2].split('-', 1)

    return(
        f'{eos_base_dir}/{rpv[0]}/{dn[1]}/{dn[3]}/{rpv[1]}'
    )

def get_volumes(dataset_name, eos_base_dir):
    '''
    Return list of volumes for the given dataset
    '''
    volumes = []
    dataset_dir = get_dataset_dir(dataset_name, eos_base_dir)

    print(dataset_dir)

    output = subprocess.check_output(
        f'eos ls -1 {dataset_dir}',
        shell=True
    ).decode('utf-8')

    for line in output.split('\n'):
        if line and line != 'file-indexes':
            volumes.append(line)

    return volumes

def get_files(dataset_name, volume, eos_base_dir):
    '''
    Return file list with information about name, size, location for the given dataset and volume.
    '''
    files = []
    dataset_dir = get_dataset_dir(dataset_name, eos_base_dir)

    output = subprocess.check_output(
        f'eos find --xurl --size --checksum {dataset_dir}/{volume}',
        shell=True
    ).decode('utf-8')

    for line in output.split('\n'):
        if line and line != 'file-indexes':

            match = re.match(r"^(.*) size=(.*) checksum=(.*)$", line)

            if match:
                path, size, checksum = match.groups()

                files.append(
                    {
                        'filename': os.path.basename(path),
                        'size': int(size),
                        'checksum': f'adler32: {checksum}',
                        'uri': path
                    }
                )

    return files

def create_output_files(dataset_name, volume, files):

    directory = Path('output')

    if not directory.is_dir():
        directory.mkdir(exist_ok=True)
    
    dn = dataset_name.split('/')
    assert len(dn) == 4
    rpv = dn[2].split('-', 1)
    
    file_name = f'CMS_{rpv[0]}_{dn[1]}_{dn[3]}_{rpv[1]}_{volume}_file_index'

    json_file = directory/f'{file_name}.json'
    
    with json_file.open('w') as f:

        f.write(
            json.dumps(
                files,
                indent=3,
                sort_keys=True,
                separators=(",", ": ")
            )
        )

        f.close()
        

    txt_file = directory/f'{file_name}.txt'

    with txt_file.open('w') as f:
    
        for file in files:
            f.write(
                f'{file["uri"]}\n'
            )

        f.close()

@click.command()
@click.option(
    '--f',
    'file_name',
    type=click.Path(exists=True),
    help='input file with dataset names'
)
@click.option(
    '--d',
    'dataset_name',
    type=str,
    help='dataset name'
)
@click.option(
    '--bd',
    'eos_base_dir',
    type=str,
    help='EOS base directory',
    default='/eos/opendata/cms'
)
def main(file_name, dataset_name, eos_base_dir):
    '''
    For each dataset get the volumes
    and create the index files
    '''
    if (file_name is None and dataset_name is None) or (file_name is not None and dataset_name is not None):
        raise click.UsageError("You must provide exactly one of --f or --d.")

    if file_name:
        dataset_names = [
            fn for fn in open(file_name, 'r').readlines()
        ]
    else:
        dataset_names = [dataset_name]


    print(dataset_names)
    
    for dataset_name in dataset_names:

        # rm the block information at the end if there
        dataset_name = dataset_name.split("#")[0]

        print(dataset_name)
        
        volumes = get_volumes(dataset_name, eos_base_dir)

        for volume in volumes:
            files = get_files(dataset_name, volume, eos_base_dir)
            create_output_files(dataset_name, volume, files)
            

if __name__ == "__main__":
    main()
