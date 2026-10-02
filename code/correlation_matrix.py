import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from style import heatmap, surface

df = pd.read_csv("data/data.csv", index_col="DATE")
df.columns = [col.title() for col in df.columns]

fig, ax = plt.subplots(figsize=(12, 10), facecolor=surface)
corr = df.corr()
np.fill_diagonal(corr.values, np.nan)
heatmap(ax, corr, "Same-day correlation")
fig.colorbar(ax.images[0], ax=ax, shrink=0.5, label="Correlation (red = rise together)")
fig.savefig("finished/correlation_matrix.png", dpi=150, bbox_inches="tight", facecolor=surface)
