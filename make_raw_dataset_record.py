import click
import json

@click.command()
@click.option(
    '--f',
    'input_file_name',
    type=click.Path(exists=True),
    help='input file with dataset names'
)
def main(input_file_name):
    if ( input_file_name is None ):
        raise click.UsageError("You must provide a file which contains dataset names")

    if input_file_name:
        print(input_file_name)

    record = {}

    
    

if __name__ == "__main__":
    main()
