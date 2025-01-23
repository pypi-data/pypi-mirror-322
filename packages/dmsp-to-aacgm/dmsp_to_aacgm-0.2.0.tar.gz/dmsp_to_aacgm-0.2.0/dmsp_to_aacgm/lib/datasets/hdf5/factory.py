from typing import List, Optional
import h5py
from ..model import DataSet
from ..hdf5.mag import MagHdf5
from ..hdf5.flux import FluxHdf5


def hdf5_dataset_factory(file_path: str, output_path: Optional[str] = None) -> DataSet:

    if output_path is None:
        output_path = file_path
    
    if file_path != output_path:
        input_file = h5py.File(file_path, "r")
        file_contents = h5py.File(output_path, "w")
        for key in input_file.keys():
            input_file.copy(key, file_contents)
        input_file.close()
    else:
        file_contents = h5py.File(file_path, "r+")

    data_sets: List[DataSet] = [MagHdf5, FluxHdf5]
    for data_set in data_sets:
        if data_set.match(file_contents):
            return data_set(file_contents)
        
    raise Exception("Unknown hdf5 dataset")