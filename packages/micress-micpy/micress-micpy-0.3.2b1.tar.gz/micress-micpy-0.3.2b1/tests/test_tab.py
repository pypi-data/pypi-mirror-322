# pylint: disable=missing-docstring
# spell: disable=unknown-word

import pandas as pd
import pytest

from micpy import tab


class TestParse:
    def test_empty_input(self):
        with pytest.raises(pd.errors.EmptyDataError):
            tab.parse(string="")

    def test_header_without_body(self):
        string = """
# A1  B1  C1
# A2  B2  C2
"""
        with pytest.raises(pd.errors.EmptyDataError):
            tab.parse(string=string)

    def test_body_without_header(self):
        string = """
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame([[11, 12, 13], [21, 22, 23], [31, 32, 33]])
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_singleline_header(self):
        string = """
# H1  H2  H3
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]], columns=["H1", "H2", "H3"]
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_multiline_header(self):
        string = """
# A1  B1  C1
# A2  B2  C2
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["A1 A2", "B1 B2", "C1 C2"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_multiline_header_with_trailing_spaces(self):
        string = """
# A1  B1  C1
 # A2  B2  C2
  # A3  B3  C3
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["A1 A2 A3", "B1 B2 B3", "C1 C2 C3"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_header_comments(self):
        string = """
## This is a header comment
### This is a header comment
#### This is a header comment
# A1  B1  C1
 ## This is a header comment
 ### This is a header comment
 #### This is a header comment
# A2  B2  C2
  ## This is a header comment
# A3  B3  C3
   ## This is a header comment
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["A1 A2 A3", "B1 B2 B3", "C1 C2 C3"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_body_comments(self):
        string = """
# H1  H2  H3
11 12 13
# This is a body comment
21 22 23
## This is a body comment
31 32 33
### This is a body comment
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["H1", "H2", "H3"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_blank_lines(self):
        string = """
# A1  B1  C1

# A2  B2  C2

11 12 13

21 22 23

31 32 33

"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["A1 A2", "B1 B2", "C1 C2"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_various_delimiter_lengths(self):
        string = """
#    A1  B1  C1
#   A2    B2  C2
#  A3      B3  C3
# A4        B4  C4
11       12 13
 21     22 23
  31   32 33
   41 42 43
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33], [41, 42, 43]],
            columns=["A1 A2 A3 A4", "B1 B2 B3 B4", "C1 C2 C3 C4"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_spaces_in_header(self):
        string = """
# This is  This  This is
# col 1  is col 2  col 3
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["This is col 1", "This is col 2", "This is col 3"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_placeholders_in_header(self):
        string = """
# -  A1  -   -   D1  E1  -   G1
# -  -   B2  -   D2  -   F2  G2
# -  -   -   C3  -   E3  F3  G3
11 12 13 14 15 16 17 18
21 22 23 24 25 26 27 28
31 32 33 34 35 36 37 38
"""
        expected_df = pd.DataFrame(
            [
                [11, 12, 13, 14, 15, 16, 17, 18],
                [21, 22, 23, 24, 25, 26, 27, 28],
                [31, 32, 33, 34, 35, 36, 37, 38],
            ],
            columns=["", "A1", "B2", "C3", "D1 D2", "E1 E3", "F2 F3", "G1 G2 G3"],
        )
        df = tab.parse(string=string)
        assert df.equals(expected_df)

    def test_header_body_mismatch(self):
        string = """
# A1  B1
11 12 13
21 22 23
31 32 33
"""
        with pytest.raises(tab.FormatError):
            tab.parse(string=string, ignore_invalid_header=False)

    def test_parse_header_off(self):
        string = """
# A1  B1  C1
# A2  B2  C2
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]], columns=[0, 1, 2]
        )
        df = tab.parse(string=string, parse_header=False)
        assert df.equals(expected_df)

    def test_ignore_invalid_header_off(self):
        string = """
# A1  B1
11 12 13
21 22 23
31 32 33
"""
        with pytest.raises(tab.FormatError):
            tab.parse(string=string, ignore_invalid_header=False)


class TestRead:
    def test_valid_file(self, tmp_path):
        string = """
# A1  B1  C1
# A2  B2  C2
11 12 13
21 22 23
31 32 33
"""
        expected_df = pd.DataFrame(
            [[11, 12, 13], [21, 22, 23], [31, 32, 33]],
            columns=["A1 A2", "B1 B2", "C1 C2"],
        )

        path = tmp_path / "valid_file.txt"
        path.write_text(string)

        df = tab.read(filename=path)
        assert df.equals(expected_df)

    def test_invalid_file(self, tmp_path):
        string = """
# A1  B1
11 12 13
21 22 23
31 32 33
"""
        path = tmp_path / "invalid_file.txt"
        path.write_text(string)

        with pytest.raises(tab.FormatError):
            tab.read(filename=path, ignore_invalid_header=False)
