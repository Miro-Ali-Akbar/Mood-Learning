import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from style import blue, grid, ink, muted, red, style, surface

targets = ["DEPRESSED", "ANXIOUS", "MOTIVATION"]
methods = {"Guess the mean": "#c3c2b7", "Guess yesterday": "#8a8984", "Model": blue}

df = pd.read_csv("data/data.csv", parse_dates=["DATE"], index_col="DATE")


def make_features(df):
    features = {}
    for col in df.columns:
        name = col.title()
        features[f"{name} yesterday"] = df[col].shift(1)
        features[f"{name} 2 days ago"] = df[col].shift(2)
        features[f"{name} 3 days ago"] = df[col].shift(3)
        features[f"{name} week avg"] = df[col].shift(1).rolling(7, min_periods=1).mean()
    features["Weekday"] = df.index.dayofweek
    return pd.DataFrame(features, index=df.index)


def evaluate(X_all, target):
    yesterday = f"{target.title()} yesterday"
    rows = df[target].notna() & X_all[yesterday].notna()
    X, y = X_all[rows], df.loc[rows, target]
    low, high = y.min(), y.max()

    errors = {name: [] for name in methods}
    for train, test in TimeSeriesSplit(n_splits=5).split(X):
        model = make_pipeline(SimpleImputer(), StandardScaler(), RidgeCV(alphas=np.logspace(-1, 3, 20)))
        model.fit(X.iloc[train], y.iloc[train])
        prediction = model.predict(X.iloc[test]).round().clip(low, high)
        errors["Guess the mean"].append(mean_absolute_error(y.iloc[test], [round(y.iloc[train].mean())] * len(test)))
        errors["Guess yesterday"].append(mean_absolute_error(y.iloc[test], X[yesterday].iloc[test]))
        errors["Model"].append(mean_absolute_error(y.iloc[test], prediction))

    return {
        "errors": {name: np.mean(values) for name, values in errors.items()},
        "weights": pd.Series(model[-1].coef_, index=X.columns),
        "actual": y.iloc[test],
        "predicted": pd.Series(prediction, index=y.index[test]),
    }


def plot_errors(ax, results):
    height = 0.26
    for i, (name, color) in enumerate(methods.items()):
        values = [results[t]["errors"][name] for t in targets]
        positions = np.arange(len(targets)) + (i - 1) * height
        ax.barh(positions, values, height=height - 0.03, color=color, label=name)
        for position, value in zip(positions, values):
            ax.text(value + 0.005, position, f"{value:.2f}", va="center", fontsize=9, color=ink)
    ax.set_yticks(range(len(targets)), [t.title() for t in targets])
    ax.invert_yaxis()
    ax.set_xlabel("Average error in points on the 1-4 scale (lower is better)", color=muted, fontsize=9)
    style(ax, "How well can tomorrow be predicted?")
    ax.legend(frameon=False, loc="lower right", fontsize=9)


def plot_weights(ax, result, target):
    top = result["weights"].reindex(result["weights"].abs().sort_values().index).tail(8)
    ax.barh(top.index, top.values, color=[red if v > 0 else blue for v in top.values], height=0.7)
    ax.axvline(0, color=muted, linewidth=0.8)
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_xlabel("<- lowers tomorrow    raises tomorrow ->", color=muted, fontsize=9)
    style(ax, f"What moves {target.title()}")


def plot_timeline(ax, result, target):
    actual = result["actual"].rolling(7).mean().tail(180)
    predicted = result["predicted"].rolling(7).mean().tail(180)
    ax.plot(actual.index, actual, color=methods["Guess yesterday"], linewidth=2, label="Actual")
    ax.plot(predicted.index, predicted, color=methods["Model"], linewidth=2, label="Predicted")
    ax.set_ylim(1, 4)
    ax.grid(axis="y", color=grid, linewidth=0.8)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    style(ax, f"{target.title()}, 7-day average, last 6 months")


X_all = make_features(df)
results = {target: evaluate(X_all, target) for target in targets}

for target, result in results.items():
    print(f"\n{target} (MAE, lower is better)")
    for name, value in result["errors"].items():
        print(f"  {name:16} {value:.3f}")

fig = plt.figure(figsize=(16, 14), facecolor=surface)
layout = fig.add_gridspec(3, 3, height_ratios=[1, 1.2, 1], hspace=0.45, wspace=0.55)
plot_errors(fig.add_subplot(layout[0, :]), results)
for i, target in enumerate(targets):
    plot_weights(fig.add_subplot(layout[1, i]), results[target], target)
    plot_timeline(fig.add_subplot(layout[2, i]), results[target], target)
fig.savefig("finished/forecast.png", dpi=150, bbox_inches="tight", facecolor=surface)
