# This SWMF/BATSRUS .plt format reader is based on the .plt format specification at
# https://tecplot.azureedge.net/products/360/current/360_data_format_guide.pdf
# but it is not a generic .plt reader and should only be used for SWMF/BATSRUS output.
"""Reader for SWMF/BATSRUS binary Tecplot .plt files."""

import numpy as np
import struct
import math
import logging

log = logging.getLogger(__name__)

TECPLOT_MAGIC = "#!TDV112"
INTEGER_VALUE_ONE = 1
FILE_TYPE_FULL = 0
ZONE_MARKER = 299.0
END_OF_HEADER_MARKER = 357.0
ZONE_TYPE_ORDERED = 0
ZONE_TYPE_FEQUADRILATERAL = 3
ZONE_TYPE_FEBRICK = 5
NO_PARENT_ZONE = -1
NO_STRAND_ID = -1
VARIABLE_LOCATION_NODE = 0
NO_SHARING_ZONE = -1


class Cursor:
    """Sequential byte cursor for binary parsing."""

    def __init__(self, content):
        self.content = content
        self.ptr = 0

    def advance(self, n):
        """Advance by n bytes and return the consumed slice."""
        start = self.ptr
        self.ptr += n
        return self.content[start : self.ptr]

    def read_array(self, dtype, count):
        """Read a NumPy array view and advance by its size in bytes."""
        array = np.frombuffer(self.content, dtype=dtype, count=count, offset=self.ptr)
        self.ptr += array.nbytes
        return array

    def find(self, marker):
        """Move the cursor to the next occurrence of marker."""
        loc = self.content.find(marker, self.ptr)
        if loc < 0:
            raise ValueError(f"Marker {marker!r} not found.")
        self.ptr = loc


def read_plt(filename):
    """Read a BATSRUS .plt file into arrays and metadata."""
    with open(filename, mode="rb") as file:  # b is important -> binary
        content = file.read()
        cursor = Cursor(content)

        if cursor.advance(8).decode("ascii") != TECPLOT_MAGIC:
            raise ValueError(f"Expected Tecplot magic {TECPLOT_MAGIC!r}.")
        if cursor.advance(4) != struct.pack("I", INTEGER_VALUE_ONE):
            raise ValueError(
                f"Expected integer value {INTEGER_VALUE_ONE} after Tecplot magic."
            )
        if cursor.advance(4) != struct.pack("I", FILE_TYPE_FULL):
            raise ValueError(f"Expected full file type marker {FILE_TYPE_FULL}.")

        title = readstr32(cursor)

        # Read number of variables
        (num_vars,) = struct.unpack("I", cursor.advance(4))
        log.debug(f"Number of variables {num_vars}.")

        variables = []
        for _ in range(num_vars):
            vname = readstr32(cursor)
            variables.append(vname)

        zone_marker = struct.pack("f", ZONE_MARKER)
        cursor.find(zone_marker)
        if cursor.advance(4) != zone_marker:
            raise ValueError(f"Expected zone marker {ZONE_MARKER}.")
        if cursor.ptr % 4 != 0:
            raise ValueError("Zone marker is not aligned to a 4-byte boundary.")

        # Read zone name
        zone_name = readstr32(cursor)

        log.debug(f"Zone name: {zone_name}.")

        if cursor.advance(4) != struct.pack("i", NO_PARENT_ZONE):
            raise ValueError(f"Expected parent zone marker {NO_PARENT_ZONE}.")

        if cursor.advance(4) != struct.pack("i", NO_STRAND_ID):
            raise ValueError(f"Expected strand ID marker {NO_STRAND_ID}.")

        (_solutiontime,) = struct.unpack("d", cursor.advance(8))

        cursor.advance(4)  # Default zone color

        # Support FEQUADRILATERAL (2D) and FEBRICK (3D) only
        # experimental support for ORDERED
        zone_type = cursor.advance(4)
        if zone_type == struct.pack("I", ZONE_TYPE_ORDERED):
            log.debug("Found ORDERED zone type.")
            num_corners_per_elem = 0
        elif zone_type == struct.pack("I", ZONE_TYPE_FEQUADRILATERAL):
            log.debug("Found FEQUADRILATERAL zone type.")
            num_corners_per_elem = 4
        elif zone_type == struct.pack("I", ZONE_TYPE_FEBRICK):
            log.debug("Found FEBRICK zone type.")
            num_corners_per_elem = 8
        else:
            raise ValueError(f"Unrecognized zone type {zone_type}.")
        log.debug(f"Using {num_corners_per_elem} corners per element.")

        if cursor.advance(4) != struct.pack("I", VARIABLE_LOCATION_NODE):
            raise ValueError(
                f"Expected variable location NODE={VARIABLE_LOCATION_NODE}."
            )

        if cursor.advance(4) != struct.pack("I", 0):
            raise ValueError("Expected 0 raw local face neighbours.")
        if cursor.advance(4) != struct.pack("I", 0):
            raise ValueError("Expected 0 miscellaneous face neighbour connections.")

        if num_corners_per_elem == 0:
            # We are in an ordered zone (experimental)
            # Read IMax, JMax, KMax
            (max_i,) = struct.unpack("I", cursor.advance(4))
            log.debug(f"Max I: {max_i}.")
            (max_j,) = struct.unpack("I", cursor.advance(4))
            log.debug(f"Max J: {max_j}.")
            (max_k,) = struct.unpack("I", cursor.advance(4))
            log.debug(f"Max K: {max_k}.")

            num_points = max_i * max_j * max_k
        else:
            # We are in an FE zone.
            # Read number of points and number of elements
            (num_points,) = struct.unpack("I", cursor.advance(4))
            log.debug(f"Number of points: {num_points}.")

            (num_elem,) = struct.unpack("I", cursor.advance(4))
            log.debug(f"Number of elements: {num_elem}.")

            # These are the I, J, and K cell dimension which
            # are always zero (for now).
            if cursor.advance(4) != struct.pack("I", 0):
                raise ValueError("Expected I cell dimension 0.")
            if cursor.advance(4) != struct.pack("I", 0):
                raise ValueError("Expected J cell dimension 0.")
            if cursor.advance(4) != struct.pack("I", 0):
                raise ValueError("Expected K cell dimension 0.")

        aux = dict()
        while True:
            (aux_data,) = struct.unpack("I", cursor.advance(4))

            if aux_data == 0:
                break

            key = readstr32(cursor)
            cursor.advance(4)  # Format

            val = readstr32(cursor)

            val = val.strip()

            aux[key] = val
            log.debug(f'"{key}"="{val}"')

        # Now look for the end of header
        eoh_marker = struct.pack("f", END_OF_HEADER_MARKER)
        cursor.find(eoh_marker)
        cursor.advance(4)

        if cursor.advance(4) != zone_marker:
            raise ValueError(f"Expected zone marker {ZONE_MARKER} after end of header.")

        # Skip reading 24 variable types (float)
        cursor.advance(num_vars * 4)

        # No 'passive variables'
        if cursor.advance(4) != struct.pack("I", 0):
            raise ValueError("Expected passive variables flag 0.")

        # No 'sharing'
        if cursor.advance(4) != struct.pack("I", 0):
            raise ValueError("Expected variable sharing flag 0.")

        if cursor.advance(4) != struct.pack("i", NO_SHARING_ZONE):
            raise ValueError(f"Expected sharing zone marker {NO_SHARING_ZONE}.")

        # Read min and max for each variable
        num_bytes = 2 * num_vars * 8
        struct.unpack(f"{2*num_vars}d", cursor.advance(num_bytes))

        #
        # Read point data
        #
        log.debug(f"Start of point data at {hex(cursor.ptr)}.")
        points = cursor.read_array(np.float32, num_points * num_vars)
        points = np.array(points).reshape(len(variables), -1).transpose()

        #
        # Read corner data if they exist (not in ORDERED zones).
        #
        if num_corners_per_elem > 0:
            log.debug(f"Start of connectivity at {hex(cursor.ptr)}.")
            corners = cursor.read_array(np.int32, num_corners_per_elem * num_elem)
            corners = np.array(corners, dtype=int).reshape(-1, num_corners_per_elem)
        else:
            corners = None

        return points, corners, aux, title, variables, zone_name


def readstr32(cursor):
    """
    Read a null-terminated 32-bit character string from the cursor.
    """
    null_int = struct.pack("I", 0)
    null_loc = cursor.content.find(null_int, cursor.ptr)

    null_loc = math.ceil(null_loc / 4) * 4

    string = cursor.content[cursor.ptr : null_loc : 4].decode("ascii")
    cursor.advance(null_loc + 4 - cursor.ptr)
    return string
