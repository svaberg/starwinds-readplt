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

        def readstr32(content):
            null_int = struct.pack("I", 0)
            null_loc = content.find(null_int)
            null_loc = math.ceil(null_loc / 4) * 4

            return content[0:null_loc:4].decode("ascii")

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
        if content[ptr : ptr + 4] == struct.pack("I", 3):
            log.debug("Found FEQUADRILATERAL zone type.")
            num_corners_per_elem = 4
        elif content[ptr : ptr + 4] == struct.pack("I", 5):
            log.debug("Found FEBRICK zone type.")
            num_corners_per_elem = 8
        else:
            raise ValueError(f"Unrecognized zone type.")
        ptr += 4
        log.debug(f"Using {num_corners_per_elem} corners per element.")

        assert content[ptr : ptr + 4] == struct.pack("I", 0)  # Var location
        ptr += 4

        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Are raw local 1-to-1 face neighbors
        ptr += 4
        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Number of miscellaneous user-defined face neighbor connections
        ptr += 4

        (num_points,) = struct.unpack("I", content[ptr : ptr + 4])
        ptr += 4
        log.debug(f"Number of points: {num_points}.")

        (num_elem,) = struct.unpack("I", content[ptr : ptr + 4])
        ptr += 4
        log.debug(f"Number of elements: {num_elem}.")

        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Are raw local 1-to-1 face neighbors
        ptr += 4
        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Are raw local 1-to-1 face neighbors
        ptr += 4
        assert content[ptr : ptr + 4] == struct.pack(
            "I", 0
        )  # Are raw local 1-to-1 face neighbors
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

        log.debug(f"Start of point data at {hex(ptr)}.")
        num_bytes = num_points * num_vars * 4
        points = struct.unpack(f"{num_bytes // 4}f", content[ptr : ptr + num_bytes])
        ptr += num_bytes

        log.debug(f"Start of connectivity at {hex(ptr)}.")

        num_bytes = num_corners_per_elem * num_elem * 4
        corners = struct.unpack(f"{num_bytes // 4}I", content[ptr : ptr + num_bytes])
        ptr += num_bytes

        points = np.array(points).reshape(len(variables), -1).transpose()
        corners = np.array(corners, dtype=int).reshape(-1, num_corners_per_elem)
        return points, corners, aux, title, variables, zone_name
