import matplotlib.pyplot as plt
def plot(data, triangles):    
    fig, ax = plt.subplots()
    img = ax.tricontourf(triangles, data, levels=100)
    plt.colorbar(img)
    ax.triplot(triangles, color='k', linewidth=.1)
    return fig, ax

