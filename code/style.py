import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ink, muted, grid, surface = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
blue, red = "#2a78d6", "#e34948"

diverging = LinearSegmentedColormap.from_list("diverging", [blue, "#f0efec", red])
diverging.set_bad(surface)


def style(ax, title):
    ax.set_facecolor(surface)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(muted)
    ax.tick_params(colors=muted, labelsize=9)
    ax.set_title(title, loc="left", color=ink, fontsize=11)


def heatmap(ax, matrix, title, xlabel="", ylabel=""):
    ax.imshow(np.ma.masked_invalid(matrix.to_numpy()), cmap=diverging, vmin=-0.5, vmax=0.5, aspect="auto")
    ax.set_xticks(range(matrix.shape[1]), matrix.columns, rotation=45, ha="right", fontsize=9, color=muted)
    ax.set_yticks(range(matrix.shape[0]), matrix.index, fontsize=9, color=muted)
    for (i, j), value in np.ndenumerate(matrix.to_numpy()):
        if not np.isnan(value):
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=7, color=ink)
    ax.set_title(title, loc="left", color=ink, fontsize=11)
    ax.set_xlabel(xlabel, color=muted, fontsize=9)
    ax.set_ylabel(ylabel, color=muted, fontsize=9)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
