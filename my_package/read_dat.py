import numpy as np

def read_dat(filename):

    # Read file header and close file
    with open(filename) as file:

        # Assume title, variables and zone are fixed.
        # Only one zone supported.
        title = file.readline()
        variables = file.readline()
        zone = file.readline()

        numvars = len(variables.split(","))
        #print(f"Number of variables {numvars}.")
        zone_n = int(zone.split(",")[1].split("=")[1])
        #print(f"Number of points {zone_n}.")
        
        # Read aux data into array
        auxdata = []
        while (line := file.readline()):
            if line.startswith("AUXDATA"):
                auxdata.append(line.rstrip())
            else:
                break
        #print(f"Number of auxdata rows {len(auxdata)}.")

    keys = [a.split("=", 1)[0] for a in auxdata]
    vals = [a.split("=", 1)[1] for a in auxdata]

    keys = [k.strip("AUXDATA ") for k in keys]
    vals = [v.strip("\"").strip() for v in vals]

    aux = {k:v for k, v in zip(keys,vals)}
    import pdb; pdb.set_trace()


    # Read points into array 
    points = np.loadtxt(filename, skiprows = 3 + len(auxdata), max_rows=zone_n)

    # Read corners
    corners = np.loadtxt(filename, dtype=int, skiprows = 3 + len(auxdata) + zone_n)
    corners = corners - 1  # Index from zero (like in the binary format)

    return points, corners, aux

