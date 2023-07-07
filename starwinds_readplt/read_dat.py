import numpy as np


def read_dat(filename):
    # Read file header and close file
    # Only one zone supported.
    with open(filename) as file:
        # Assume title, variables and zone are fixed.
        dataset_title = file.readline()
        dataset_title = dataset_title.removeprefix("TITLE=").rstrip().strip('"')

        # REad variables
        variables = file.readline()
        variables = variables.removeprefix("VARIABLES =")
        variables = variables.split(",")
        variables = [v.strip().strip('"') for v in variables]

        # Read zone title and other things from the zone title line
        zone_title_line = file.readline()
        # print(f"Number of variables {len(variables)}.")
        zone_title, zone_n, *_tokens = zone_title_line.split(", ")
        zone_title = zone_title.removeprefix("ZONE T=").strip('"').rstrip()

        zone_n = int(zone_n.split("=")[1])
        # print(f"Number of points {zone_n}.")

        # Read aux data into array
        auxdata = []
        while line := file.readline():
            if line.startswith("AUXDATA"):
                auxdata.append(line.rstrip())
            else:
                break
        # print(f"Number of auxdata rows {len(auxdata)}.")

    keys = [a.split("=", 1)[0] for a in auxdata]
    vals = [a.split("=", 1)[1] for a in auxdata]

    keys = [k.removeprefix("AUXDATA ") for k in keys]
    vals = [v.strip('"').strip() for v in vals]

    aux = {k: v for k, v in zip(keys, vals)}

    # Read points into array
    points = np.loadtxt(filename, skiprows=3 + len(auxdata), max_rows=zone_n)

    # Read corners
    corners = np.loadtxt(filename, dtype=int, skiprows=3 + len(auxdata) + zone_n)
    corners = corners - 1  # Index from zero (like in the binary format)

    return points, corners, aux, dataset_title, variables, zone_title
