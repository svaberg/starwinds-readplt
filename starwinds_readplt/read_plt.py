# This SWMF/BATSRUS .plt format reader is based on the .plt format specification at
# https://tecplot.azureedge.net/products/360/current/360_data_format_guide.pdf
# but it is not a generic .plt reader and should only be used for SWMF/BATSRUS output.

import numpy as np
import struct
import math
import logging

log = logging.getLogger(__name__)


def read_plt(filename):
    with open(filename, mode="rb") as file:  # b is important -> binary
        content = file.read()

        ptr = 0

        assert content[ptr : ptr + 8].decode("ascii") == "#!TDV112"
        ptr += 8

        assert content[ptr : ptr + 4] == struct.pack("I", 1)  # Integer value of 1
        ptr += 4

        assert content[ptr : ptr + 4] == struct.pack("I", 0)  # Filetype full
        ptr += 4

        title = readstr32(content[ptr:])
        ptr += len(title) * 4 + 4

        # Read number of variables
        (num_vars,) = struct.unpack("I", content[ptr : ptr + 4])
        log.debug(f"Number of variables {num_vars}.")
        ptr += 4

        variables = []
        for _ in range(num_vars):
            vname = readstr32(content[ptr:])
            ptr += len(vname) * 4 + 4

            variables.append(vname)

        zone_marker = struct.pack("f", 299.0)
        ptr = content.find(zone_marker)
        ptr += 4
        assert ptr % 4 == 0

        # Read zone name
        zone_name = readstr32(content[ptr:])
        ptr += len(zone_name) * 4 + 4

        log.debug(f"Zone name: {zone_name}.")

        assert content[ptr : ptr + 4] == struct.pack("i", -1)  # Parentzone
        ptr += 4

        assert content[ptr : ptr + 4] == struct.pack("i", -1)  # StrandID
        ptr += 4

        (_solutiontime,) = struct.unpack("d", content[ptr : ptr + 8])
        ptr += 8

        ptr += 4  # Default zone color

        # Support FEQUADRILATERAL (2D) and FEBRICK (3D) only
        # experimental support for ORDERED
        if content[ptr : ptr + 4] == struct.pack("I", 0):
            log.debug("Found ORDERED zone type.")
            num_corners_per_elem = 0
        elif content[ptr : ptr + 4] == struct.pack("I", 3):
            log.debug("Found FEQUADRILATERAL zone type.")
            num_corners_per_elem = 4
        elif content[ptr : ptr + 4] == struct.pack("I", 5):
            log.debug("Found FEBRICK zone type.")
            num_corners_per_elem = 8
        else:
            raise ValueError(f"Unrecognized zone type {content[ptr : ptr + 4]}.")
        ptr += 4
        log.debug(f"Using {num_corners_per_elem} corners per element.")

        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Variable location must be NODE=0
        ptr += 4

        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # No raw local one-to-one face neighbours should be supplied
        ptr += 4
        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # There should be zero miscellaneous user-defined face neighbor connections
        ptr += 4

        if num_corners_per_elem == 0:
            # We are in an ordered zone (experimental)
            # Read IMax, JMax, KMax
            (max_i,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4
            log.debug(f"Max I: {max_i}.")
            (max_j,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4
            log.debug(f"Max J: {max_j}.")
            (max_k,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4
            log.debug(f"Max K: {max_k}.")

            num_points = max_i * max_j * max_k
        else:
            # We are in an FE zone.
            # Read number of points and number of elements
            (num_points,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4
            log.debug(f"Number of points: {num_points}.")

            (num_elem,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4
            log.debug(f"Number of elements: {num_elem}.")

            # These are the I, J, and K cell dimension which
            # are always zero (for now).
            assert content[ptr : ptr + 4] == struct.pack("I", 0)
            ptr += 4
            assert content[ptr : ptr + 4] == struct.pack("I", 0)
            ptr += 4
            assert content[ptr : ptr + 4] == struct.pack("I", 0)
            ptr += 4

        aux = dict()
        while True:
            (aux_data,) = struct.unpack("I", content[ptr : ptr + 4])
            ptr += 4

            if aux_data == 0:
                break

            key = readstr32(content[ptr:])
            ptr += len(key) * 4 + 4
            ptr += 4  # Format

            val = readstr32(content[ptr:])
            ptr += len(val) * 4 + 4

            val = val.strip()

            aux[key] = val
            log.debug(f'"{key}"="{val}"')

        # Now look for the end of header
        eoh_marker = struct.pack("f", 357.0)
        eoh_loc = content.find(eoh_marker)
        if eoh_loc == ptr:
            # No gaps
            pass
        ptr += 4

        assert content[ptr : ptr + 4] == zone_marker
        ptr += 4

        # Skip reading 24 variable types (float)
        ptr += num_vars * 4

        # No 'passive variables'
        assert content[ptr : ptr + 4] == struct.pack("I", 0)
        ptr += 4

        # No 'sharing'
        assert content[ptr : ptr + 4] == struct.pack("I", 0)
        ptr += 4

        assert content[ptr : ptr + 4] == struct.pack("i", -1)
        ptr += 4

        # Read min and max for each variable
        num_bytes = 2 * num_vars * 8
        struct.unpack(f"{2*num_vars}d", content[ptr : ptr + num_bytes])
        ptr += num_bytes

        #
        # Read point data
        #
        log.debug(f"Start of point data at {hex(ptr)}.")
        num_bytes = num_points * num_vars * 4
        points = np.frombuffer(
            content, dtype=np.float32, count=num_bytes // 4, offset=ptr
        )
        ptr += num_bytes

        points = np.array(points).reshape(len(variables), -1).transpose()

        #
        # Read corner data
        #
        if num_corners_per_elem > 0:
            log.debug(f"Start of connectivity at {hex(ptr)}.")
            num_bytes = num_corners_per_elem * num_elem * 4
            corners = np.frombuffer(
                content, dtype=np.int32, count=num_bytes // 4, offset=ptr
            )
            ptr += num_bytes

            corners = np.array(corners, dtype=int).reshape(-1, num_corners_per_elem)
        else:
            corners = None

        return points, corners, aux, title, variables, zone_name


def readstr32(content):
    null_int = struct.pack("I", 0)
    null_loc = content.find(null_int)
    null_loc = math.ceil(null_loc / 4) * 4

    return content[0:null_loc:4].decode("ascii")
