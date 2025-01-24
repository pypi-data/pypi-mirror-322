# pylint: disable=missing-docstring
# pylint: disable=protected-access
# spell: disable=unknown-word

from pathlib import Path

import numpy as np
import pytest

from micpy import geo


class TestFind:
    @pytest.mark.parametrize("filename", ["file", "file.conc1", "file_conc1.mcr"])
    def test_valid_filenames(self, filename: str):
        expected_basename = "file"
        assert geo._get_basename(Path(filename)) == Path(expected_basename)

    @pytest.mark.parametrize(
        "dirname", ["/dir/", "/dir1/dir2/" "dir/", "dir1/dir2/", "/", "./", "../"]
    )
    def test_valid_dirnames(self, dirname: str):
        filename = dirname + "file.conc1"
        expected_basename = dirname + "file"
        assert geo._get_basename(Path(filename)) == Path(expected_basename)

    @pytest.mark.parametrize("extension", [".geof", ".geof.mcr", "_geof", "_geof.mcr"])
    def test_valid_extensions(self, tmp_path, extension):
        bin_path = tmp_path / "file.conc1"
        geo_path = tmp_path / f"file{extension}"
        geo_path.touch()

        assert geo.find(bin_path) == geo_path

    def test_empty_filename(self):
        with pytest.raises(ValueError):
            geo.find("")

    def test_non_existent_file(self, tmp_path):
        bin_path = tmp_path / "file.conc1"

        with pytest.raises(geo.GeometryFileNotFoundError):
            geo.find(bin_path)

    def test_multiple_files(self, tmp_path):
        bin_path = tmp_path / "file.conc1"
        geo_path1 = tmp_path / "file.geof"
        geo_path2 = tmp_path / "file_geof.mcr"
        geo_path1.touch()
        geo_path2.touch()

        with pytest.raises(geo.MultipleGeometryFilesError):
            geo.find(bin_path)

    def test_directory(self, tmp_path):
        bin_path = tmp_path / "file.conc1"
        bin_path.mkdir()

        with pytest.raises(geo.GeometryFileNotFoundError):
            geo.find(bin_path)


BASIC_DATA = np.array(
    [(24, (10, 20, 30), (1.0, 2.0, 3.0), 24)], dtype=geo.Type.BASIC.value
)
EXTENDED_DATA = np.array(
    [
        (
            24,
            (10, 20, 30),
            (1.0, 2.0, 3.0),
            24,
            50,
            b"1.234",
            b"31/12/1999",
            b"01/01/2000",
            b"Linux",
            b"double",
            50,
        )
    ],
    dtype=geo.Type.EXTENDED.value,
)


class TestWrite:
    def test_basic_data(self, tmp_path):
        data = BASIC_DATA
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, data)
        assert path.exists()

    def test_extended_data(self, tmp_path):
        data = EXTENDED_DATA
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, data)
        assert path.exists()

    def test_invalid_type(self, tmp_path):
        data = [(24, (10, 20, 30), (1.0, 2.0, 3.0), 24)]
        path = tmp_path / "file.geof"
        pytest.raises(ValueError, geo.write_ndarray, path, data)

    def test_invalid_dtype(self, tmp_path):
        data = np.array([24, 10, 20, 30, 1.0, 2.0, 3.0, 24])
        path = tmp_path / "file.geof"
        pytest.raises(ValueError, geo.write_ndarray, path, data)

    @pytest.mark.parametrize("header, footer", [(0, 24), (24, 0), (0, 0)])
    def test_invalid_header_or_footer(self, tmp_path, header, footer):
        data = np.array(
            [(header, (10, 20, 30), (1.0, 2.0, 3.0), footer)],
            dtype=geo.Type.BASIC.value,
        )
        path = tmp_path / "file.geof"
        pytest.raises(ValueError, geo.write_ndarray, path, data)


class TestRead:
    @pytest.mark.parametrize("compress", [True, False])
    def test_basic_data(self, tmp_path, compress):
        data = BASIC_DATA
        datatype = geo.Type.BASIC
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, data, compressed=compress)
        read_data = geo.read_ndarray(path, type=datatype, compressed=compress)
        np.testing.assert_array_equal(data, read_data)

    @pytest.mark.parametrize("compress", [True, False])
    def test_extended_data(self, tmp_path, compress):
        data = EXTENDED_DATA
        datatype = geo.Type.EXTENDED
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, data, compressed=compress)
        read_data = geo.read_ndarray(path, type=datatype, compressed=compress)
        np.testing.assert_array_equal(data, read_data)

    def test_write_extended_read_basic(self, tmp_path):
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, EXTENDED_DATA)
        read_data = geo.read_ndarray(path, type=geo.Type.BASIC)
        np.testing.assert_array_equal(BASIC_DATA, read_data)

    def test_write_basic_read_extended(self, tmp_path):
        path = tmp_path / "file.geof"
        geo.write_ndarray(path, BASIC_DATA)
        pytest.raises(ValueError, geo.read_ndarray, path)

    def test_non_existent_file(self):
        with pytest.raises(FileNotFoundError):
            geo.read_ndarray("non_existing_file")
