import os
from tempfile import TemporaryDirectory
from typing import List
import unittest
from click.testing import CliRunner
import h5py
from dmsp_to_aacgm.cli import cli
from math import isnan, isclose



class TestHdf5(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()

    def run_tool(self, args: List[str] = []):
        return self.runner.invoke(cli, args)

    def test_hdf5_mag_conversion(self):
        with TemporaryDirectory() as temp_output_dir:
            file_name = "dms_20150410_16s1.001.hdf5"
            input_file = "tests/data/inputs/" + file_name

            result = self.run_tool([input_file, temp_output_dir])
            assert result.exit_code == 0, f"CLI failed: {result.output}"

            output_file_path = os.path.join(temp_output_dir, file_name)
            assert os.path.exists(output_file_path), "Output file was not created"

            self._compare_hdf5_files(output_file_path, "tests/data/outputs/" + file_name)

    def test_hdf5_flux_conversion(self):
        with TemporaryDirectory() as temp_output_dir:
            file_name = "dms_19970525_12e.001.hdf5"
            input_file = "tests/data/inputs/" + file_name

            result = self.run_tool([input_file, temp_output_dir])
            assert result.exit_code == 0, f"CLI failed: {result.output}"

            output_file_path = os.path.join(temp_output_dir, file_name)
            assert os.path.exists(output_file_path), "Output file was not created"

            self._compare_hdf5_files(output_file_path, "tests/data/outputs/" + file_name)

    def _compare_hdf5_files(self, input_path: str, expected_file_path: str):
        with h5py.File(input_path, "r") as actual, h5py.File(expected_file_path, "r") as expected:
            actual_values = actual["Data"]["Table Layout"][()]
            expected_values = expected["Data"]["Table Layout"][()]
            for a, e, in zip(actual_values, expected_values):
                for a_item, e_item in zip(a, e):
                    if not isnan(a_item) and not isnan(e_item):
                        assert isclose(a_item, e_item, rel_tol=1e-12, abs_tol=1e-12), \
                        f"Values in record do not match. Actual: {a} Expected: {e}"

    