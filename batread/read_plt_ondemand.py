"""Experimental on-demand helpers for BATSRUS .plt files."""

import struct
def find_marker(filename, marker, chunksize=8192):
    """
    Find the marker in the file. Return the file position after the marker.
    """
    # Known limitation (intentional for now): this experimental implementation
    # reads the whole file and ignores `chunksize`.
    pos = 0
    with open(filename, "rb") as f:
        _bytes = f.read()
        return _bytes.find(marker)
    # TODO is it possible to find multiple markers in the file? If so, return a list of positions.




class PltFile():
    """
    Class for reading .plt files on demand. The point data and the quad corner data is only read when requested.
    """

if __name__ == "__main__":
    eoh_marker = struct.pack("f", 357.0)
    zone_marker = struct.pack("f", 299.0)

    print(find_marker("examples/3d__var_1_n00000000.plt", b"#!TDV112"))
    print(find_marker("examples/3d__var_1_n00000000.plt", eoh_marker))
    print(find_marker("examples/3d__var_1_n00000000.plt", zone_marker))
