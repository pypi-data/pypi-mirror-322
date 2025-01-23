import os
import click
from .lib.filetypes.factory import dataset_factory
from .lib.utils import get_files, build_output_path



@click.command(
    name="dmsp-to-aacgm",
    help="Converts geomagnetic coordinates in DMSP data files to AACGM coordinates.\n\n"
         "input_path: Path of a dmsp file or directory containing dmsp files for conversion.\n\n"
         "output_dir: Optional directory to save converted files. If not supplied, the input files will be modified."
)
@click.argument(
    "input_path",
    type=click.Path(exists=True),
    metavar="<input path>"
)
@click.argument(
    "output_dir",
    type=click.Path(file_okay=False),
    required=False,
    metavar="<output dir>"
)
def cli(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file_path in get_files(input_path):
        print(f"Converting {file_path}...")
        try:
            output_path = build_output_path(file_path, output_dir)
            data_set = dataset_factory(file_path, output_path)
            data_set.convert()
            data_set.close()
        except Exception as e:
            print(f"Could not process {file_path} due to: {str(e)}")
        print("Conversion complete!")