import numpy as np
import logging
log = logging.getLogger(__name__)


class LineReader:
    def __init__(self, filename):
        self.file = open(filename)
        self.line_no = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        return False
    
    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        if not line:
            raise StopIteration
        self.line_no += 1
        return line
    
    def peek(self):
        pos = self.file.tell()
        line = self.file.readline()
        self.file.seek(pos)
        return line
    
    def loadtxt(self, max_rows, *args, **kwargs):
        line_no = self.line_no
        interval_str = f"lines {line_no + 1} to {line_no + max_rows}"
        log.debug(f"Try reading {max_rows} data rows from {interval_str}.")
        try:
            array = np.loadtxt(self.file, max_rows=max_rows, *args, **kwargs)
        except ValueError as e:
            if not "the number of columns changed from" in e.args[0]:
                raise
            msg_tokens = e.args[0].split(";")[0].split()
            row_id = int(msg_tokens[-1])
            row_id += line_no
            msg = " ".join(msg_tokens[:-1]) + f" {row_id}"
            raise ValueError(msg) from e

        read_lines = array.shape[0]
        self.line_no += read_lines
        if read_lines == max_rows:
            log.debug(f"Successfully read {read_lines} data rows.")
        else:
            log.warning(f"Only read {read_lines} data rows out of expected {max_rows}.")
        return array


def read_dat(filename):
    # Read file header and close file
    # Only one zone supported.
    with LineReader(filename) as reader:

        # Assume title, variables and zone are fixed.
        title = next(reader)
        if not title.startswith("TITLE="):
            raise ValueError(f"Expected dataset title line starting with 'TITLE=', got '{title}'")
        title = title.removeprefix("TITLE=").rstrip().strip('"')

        # Read variables
        variables = next(reader)
        if not variables.startswith("VARIABLES"):
            raise ValueError(f"Expected variables line starting with 'VARIABLES', got '{variables}'")
        variables = variables.removeprefix("VARIABLES =")
        variables = variables.split(",")
        variables = [v.strip().strip('"') for v in variables]
        log.debug(f"Number of variables {len(variables)}.")

        # Read zone title and other things from the zone line
        zone_line = next(reader)
        if not zone_line.startswith("ZONE"):
            raise ValueError(f"Expected zone title line starting with 'ZONE', got '{zone_line}'")
        zone_line = zone_line.removeprefix("ZONE").split(",")
        zone = {}
        for item in zone_line:
            key, value = item.split("=", 1)
            zone[key.strip()] = value.strip().strip('"').strip() # Strip whitespace and quotes
        zone_title = zone.get("T", None)
        zone_n = int(zone.get("N"))
        zone_e = int(zone.get("E"))


        # Read aux data into array
        auxdata = []
        while True:
            line = reader.peek()
            if not line or not line.startswith("AUXDATA"):
                break
            auxdata.append(next(reader).rstrip())
        log.debug(f"Number of auxdata rows {len(auxdata)}.")
        # Build aux data dict
        keys = [a.split("=", 1)[0] for a in auxdata]
        vals = [a.split("=", 1)[1] for a in auxdata]
        keys = [k.removeprefix("AUXDATA ") for k in keys]
        vals = [v.strip('"').strip() for v in vals]
        aux = {k: v for k, v in zip(keys, vals)}

        # End of header processing.

        # Read points into array
        log.debug(f"Reading {zone_n} points from file lines {reader.line_no + 1} to {reader.line_no + zone_n}.")
        points = reader.loadtxt(max_rows=zone_n)
        log.debug(f"Finished reading points. Shape is {points.shape}.")
        if points.shape[1] != len(variables):
            raise ValueError(f"Expected {len(variables)} columns of point data, got {points.shape[1]}.")
        if points.shape[0] != zone_n:
            raise ValueError(f"Expected {zone_n} rows of point data, got {points.shape[0]}.")

        # Read corners
        log.debug(f"Reading {zone_e} corners from file lines {reader.line_no + 1} to {reader.line_no + zone_e}.")
        corners = reader.loadtxt(max_rows=zone_e, dtype=int)
        log.debug(f"Finished reading corners. Shape is {corners.shape}.")
        if corners.shape[0] != zone_e:
            raise ValueError(f"Expected {zone_e} rows of corner data, got {corners.shape[0]}.")

        corners = corners - 1  # Index from zero (like in the binary format)

        tail = reader.file.read().strip()
        if tail:
            log.warning(f"File has {len(tail)} extra characters after expected data. Ignoring.")
            raise ValueError(f"File has {len(tail)} extra characters after expected data. Ignoring.")

        return points, corners, aux, title, variables, zone_title
