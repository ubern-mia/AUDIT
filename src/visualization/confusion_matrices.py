import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np


def plt_confusion_matrix(matrix, classes, normalized=True):

    # create a personalized Blues cmap
    blue_colors = plt.cm.Blues(np.linspace(0.0, .5, 100))
    custom_cmap = LinearSegmentedColormap.from_list('CustomBlues', blue_colors)

    classes_to_remove = []
    x = matrix.copy()
    if len(classes_to_remove) > 0:
        for c in classes_to_remove:
            classes.pop(c)
            x = np.delete(x, c, axis=0)
            x = np.delete(x, c, axis=1)

    # Plotting the normalized matrix as a heatmap with single color background and lines between rows
    fig, ax = plt.subplots(facecolor='w', edgecolor='k')  # Set the background color here
    ax.imshow(x, cmap=custom_cmap, vmin=0, vmax=np.max(x))

    # Adding annotations
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if i != j:
                if normalized:
                    plt.text(j, i, f'{x[i, j]:.1f}%', ha='center', va='center', color='black', fontsize=12)
                else:
                    plt.text(j, i, f'{x[i, j]:,}', ha='center', va='center', color='black', fontsize=12)

    # Adding gridlines between rows
    ax.set_xticks(np.arange(-0.5, x.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, x.shape[0], 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

    # Adjusting ticks and gridlines
    plt.xticks(np.arange(x.shape[1]), labels=classes)
    plt.yticks(np.arange(x.shape[0]), labels=classes)
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    plt.ylabel("True \nlabel", rotation=0, fontsize=12, labelpad=60)
    plt.suptitle("Predicted label", fontsize=12)

    # remove ticks
    plt.tick_params(axis='x', length=0)
    plt.tick_params(axis='y', length=0)
    plt.grid(False)

    # plt.title('Normalized Confusion Matrix')
    return fig
