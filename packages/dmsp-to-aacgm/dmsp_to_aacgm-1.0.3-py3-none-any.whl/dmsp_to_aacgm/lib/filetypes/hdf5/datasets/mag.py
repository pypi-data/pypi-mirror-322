from ....dataset_model import DataSet
import h5py
import aacgmv2
from datetime import datetime


class MagHdf5(DataSet):

    def __init__(self, hdf5_file: h5py.File):
        self.hdf5_file = hdf5_file
        self.data = hdf5_file["Data"]["Table Layout"][()]

    @staticmethod
    def match(hdf5_file: h5py.File) -> bool:
        if data := hdf5_file.get("Data", {}).get("Table Layout"):
            fields = data.dtype.descr
            expected_fields = ["year", "month", "day", "hour", "min",
                                "sec", "recno", "kindat", "kinst", "ut1_unix",
                                "ut2_unix", "gdlat", "glon", "gdalt", "sat_id",
                                "mlt", "mlat", "mlong", "ne", "hor_ion_v",
                                "vert_ion_v", "bd", "b_forward", "b_perp",
                                "diff_bd", "diff_b_for", "diff_b_perp"]
            for field, expected_field in zip(fields, expected_fields):
                if field[0] != expected_field:
                    return False
            return True
        return False

    def convert(self):
        data = self.hdf5_file["Data"]["Table Layout"][()]

        for idx, record in enumerate(data):
            record = list(record)
            year, month, day, hour, minute, second = record[:6]
            gdlat, glon, gdalt = record[11:14]
            mlat, mlon, mlt = aacgmv2.get_aacgm_coord(gdlat, glon, gdalt,
                                                    datetime(year, month, day, hour, minute, second),
                                                    method='ALLOWTRACE')
            data[idx][15] = mlt
            data[idx][16] = mlat
            data[idx][17] = mlon

        self.hdf5_file["Data"]["Table Layout"][...] = data

    def close(self):
        self.hdf5_file.close()