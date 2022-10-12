import matplotlib.pyplot as plt


def plot(data, triangles, show_cells=False):
    _fig, ax = plt.subplots()
    img = ax.tricontourf(triangles, data, levels=100)
    _cax = plt.colorbar(img)
    if show_cells:
        ax.triplot(triangles, color='k', linewidth=.1)
    return img, ax
