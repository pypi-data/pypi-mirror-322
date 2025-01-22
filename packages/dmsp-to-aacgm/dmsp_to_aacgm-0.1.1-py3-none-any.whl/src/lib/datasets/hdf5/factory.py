from typing import List
import h5py
from ..model import DataSet
from ..hdf5.mag import MagHdf5
from ..hdf5.flux import FluxHdf5



def hdf5_dataset_factory(file_path: str) -> DataSet:
    data_sets: List[DataSet] = [MagHdf5, FluxHdf5]
    contents = h5py.File(file_path, "r+")
    for data_set in data_sets:
        if data_set.match(contents):
            return data_set(contents)
    raise Exception("Unknown hdf5 dataset")