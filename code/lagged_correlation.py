import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from style import heatmap, surface

targets = ["DEPRESSED", "ANXIOUS", "MOTIVATION"]

df = pd.read_csv("data/data.csv", parse_dates=["DATE"], index_col="DATE").rank()
df.columns = [col.title() for col in df.columns]
yesterday = df.shift(1)


def partial_corr(x, y, control):
    rows = pd.concat([x, y, control], axis=1).dropna().to_numpy()
    x, y, control = rows.T
    design = np.column_stack([np.ones_like(control), control])
    x_rest = x - design @ np.linalg.lstsq(design, x, rcond=None)[0]
    y_rest = y - design @ np.linalg.lstsq(design, y, rcond=None)[0]
    return np.corrcoef(x_rest, y_rest)[0, 1]


next_day = pd.DataFrame({today: {col: yesterday[col].corr(df[today]) for col in df.columns} for today in df.columns})

profile = {}
for target in (t.title() for t in targets):
    inputs = [col for col in df.columns if col != target]
    profile[(target, "same day")] = {col: df[col].corr(df[target]) for col in inputs}
    profile[(target, "next day")] = {col: yesterday[col].corr(df[target]) for col in inputs}
    profile[(target, "next day, beyond\ntoday's mood")] = {
        col: partial_corr(yesterday[col], df[target], yesterday[target]) for col in inputs
    }
profile = pd.DataFrame(profile)
profile.columns = [f"{target}: {when}" for target, when in profile.columns]

fig, (left, right) = plt.subplots(1, 2, figsize=(22, 10), facecolor=surface, gridspec_kw={"width_ratios": [1, 1.1], "wspace": 0.3})
heatmap(left, next_day, "Today vs tomorrow", "Tomorrow", "Today")
heatmap(right, profile, "Does a habit matter more the next day?", ylabel="Habit or mood today")
for edge in (2.5, 5.5):
    right.axvline(edge, color=surface, linewidth=6)
fig.colorbar(right.images[0], ax=[left, right], shrink=0.5, label="Rank correlation (red = rise together)")
fig.savefig("finished/lagged_correlation.png", dpi=150, bbox_inches="tight", facecolor=surface)
