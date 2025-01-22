import click
from .lib.datasets.factory import dataset_factory
from .lib.utils import get_files, build_output_path, establish_output_dir



@click.command(
    name="dmsp-to-aacgm",
    help="Converts geomagnetic coordinates in DMSP data files to AACGM coordinates.\n\n"
         "input_path: Path of a dmsp file or directory containing dmsp files for conversion.\n\n"
         "output_dir: Optional directory to save converted files. Defaults to 'aacgm'."
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

    if output_dir is None:
        output_dir = "aacgm"

    establish_output_dir(output_dir)

    for file_path in get_files(input_path):
        print(f"Converting {file_path}...")
        try:
            data_set = dataset_factory(file_path)
            data_set.convert()
            data_set.save(
                output_path=build_output_path(file_path, output_dir)
            )
        except Exception as e:
            print(f"Could not process {file_path} due to: {str(e)}")
        print("Conversion complete!")