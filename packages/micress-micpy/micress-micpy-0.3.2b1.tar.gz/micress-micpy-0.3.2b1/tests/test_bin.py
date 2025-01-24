# pylint: disable=missing-docstring
# pylint: disable=protected-access
# spell: disable=unknown-word

import gzip

import numpy as np
import pytest

from micpy import bin


class TestChunk:
    @pytest.mark.parametrize(
        "chunk_size, expected_data",
        [
            (1, [b"1", b"2", b"3", b"4", b"5", b"6"]),
            (2, [b"12", b"34", b"56"]),
            (3, [b"123", b"456"]),
            (4, [b"1234", b"56"]),
            (5, [b"12345", b"6"]),
            (6, [b"123456"]),
            (7, [b"123456"]),
            (-1, [b"123456"]),
        ],
    )
    def test_iterate(self, tmp_path, chunk_size: int, expected_data: list[bytes]):
        filename = tmp_path / "file.txt"

        with open(filename, "wb+") as f:
            f.write(b"123456")
            chunks = list(bin.Chunk.iterate(f, chunk_size=chunk_size, compressed=False))

        assert len(chunks) == len(expected_data)
        assert [chunk.data for chunk in chunks] == expected_data

    @pytest.mark.parametrize("chunk_size", [1, 2, 3, 4, 5, 6, 7, -1])
    def test_join(self, tmp_path, chunk_size: int):
        filename = tmp_path / "file.txt"
        expected_data = b"123456"

        with open(filename, "wb+") as f:
            f.write(expected_data)
            chunks = list(bin.Chunk.iterate(f, chunk_size=chunk_size, compressed=False))

        assert b"".join(chunk.data for chunk in chunks) == expected_data

    @pytest.mark.parametrize("chunk_size", [1, 2, 3, 4, 5, 6, 7, -1])
    def test_join_compressed(self, tmp_path, chunk_size: int):
        filename = tmp_path / "file.txt"
        expected_data = b"123456"

        with open(filename, "wb+") as f:
            f.write(gzip.compress(expected_data))
            chunks = list(bin.Chunk.iterate(f, chunk_size=chunk_size, compressed=True))

        assert b"".join(chunk.data for chunk in chunks) == expected_data


VALID_HEADER = bin.Header(48, 0.1, 10)
VALID_HEADER_BYTES = b"0\x00\x00\x00\xcd\xcc\xcc=\n\x00\x00\x00"


class TestHeader:
    def test_to_bytes(self):
        assert VALID_HEADER.to_bytes() == VALID_HEADER_BYTES

    def test_from_bytes(self):
        header = bin.Header.from_bytes(VALID_HEADER_BYTES)

        assert header.size == VALID_HEADER.size
        assert header.time == VALID_HEADER.time
        assert header.body_length == VALID_HEADER.body_length

    def test_to_bytes_from_bytes(self):
        header = bin.Header.from_bytes(VALID_HEADER.to_bytes())

        assert header.size == VALID_HEADER.size
        assert header.time == VALID_HEADER.time
        assert header.body_length == VALID_HEADER.body_length

    def test_read(self, tmp_path):
        filename = tmp_path / "file.txt"

        with open(filename, "wb") as f:
            f.write(VALID_HEADER_BYTES)

        header = bin.Header.read(filename, compressed=False)

        assert header.size == VALID_HEADER.size
        assert header.time == VALID_HEADER.time
        assert header.body_length == VALID_HEADER.body_length

    def test_read_compressed(self, tmp_path):
        filename = tmp_path / "file.txt"

        with open(filename, "wb") as f:
            f.write(gzip.compress(VALID_HEADER_BYTES))

        header = bin.Header.read(filename, compressed=True)

        assert header.size == VALID_HEADER.size
        assert header.time == VALID_HEADER.time
        assert header.body_length == VALID_HEADER.body_length

    def test_invalid_header(self):
        with pytest.raises(ValueError):
            bin.Header(0, 0, 0)


class TestPosition:
    @pytest.mark.parametrize("chunk_size", [1, 2, 3, 4, 5, -1])
    def test_iterate(self, tmp_path, chunk_size: int):
        filename = tmp_path / "file.txt"

        times = [0.1, 0.2, 0.3, 0.4, 0.5]

        with open(filename, "wb") as f:
            for time in times:
                f.write(bin.Header(48, time, 10).to_bytes())
                f.write(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float32))
                f.write(bin.Footer(10).to_bytes())

        with open(filename, "rb") as f:
            positions = list(
                bin.Position.iterate(f, chunk_size=chunk_size, compressed=False)
            )

        assert len(positions) == len(times)
        assert [position.time for position in positions] == times

    @pytest.mark.parametrize("chunk_size", [1, 2, 3, 4, 5, -1])
    def test_iterate_compressed(self, tmp_path, chunk_size: int):
        filename = tmp_path / "file.txt"

        times = [0.1, 0.2, 0.3, 0.4, 0.5]

        with gzip.open(filename, "wb") as f:
            for time in times:
                f.write(bin.Header(48, time, 10).to_bytes())
                f.write(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float32))
                f.write(bin.Footer(10).to_bytes())

        with open(filename, "rb") as f:
            positions = list(
                bin.Position.iterate(f, chunk_size=chunk_size, compressed=True)
            )

        assert len(positions) == len(times)
        assert [position.time for position in positions] == times


class TestIndex:
    def from_filename(self, tmp_path):
        filename = tmp_path / "file.txt"

        times = [0.1, 0.2, 0.3, 0.4, 0.5]

        with open(filename, "wb") as f:
            for time in times:
                f.write(bin.Header(48, time, 10).to_bytes())
                f.write(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float32))
                f.write(bin.Footer(10).to_bytes())

        index = bin.Index.from_filename(filename, compressed=False)

        assert len(index) == len(times)
        assert [position.time for position in index] == times


class TestFile:
    @pytest.mark.parametrize(
        "condition, length",
        [
            (lambda field: field.time > 0.1, 4),
            (lambda field: field.time > 0.1 and field.time <= 0.4, 3),
            (lambda field: field.time == 0.1 or field.time == 0.5, 2),
            (lambda field: field.time in [0.1, 0.3, 0.5], 3),
            # (lambda field: field.time < 0.1, 0),
            (None, 5),
        ],
    )
    def test_read_condition(self, tmp_path, condition, length: int):
        filename = tmp_path / "file.txt"

        times = [np.float32(i) for i in [0.1, 0.2, 0.3, 0.4, 0.5]]

        with open(filename, "wb") as f:
            for time in times:
                f.write(bin.Header(48, time, 10).to_bytes())
                f.write(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float32))
                f.write(bin.Footer(10).to_bytes())

        with bin.File(filename) as f:
            f._compressed = False
            fields = f.read(condition)

        assert len(fields) == length
