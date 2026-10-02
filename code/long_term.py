import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from style import grid, ink, muted, style, surface

colors = {
    "Depressed": "#2a78d6",
    "Anxious": "#eb6834",
    "Motivation": "#1baf7a",
    "Lonely": "#eda100",
    "Caffeine": "#e87ba4",
    "Alcohol": "#008300",
    "Sleep": "#4a3aa7",
}
groups = {
    "Mood (1-4)": ["Depressed", "Anxious", "Motivation", "Lonely"],
    "Caffeine and alcohol (0-4)": ["Caffeine", "Alcohol"],
    "Sleep (hours)": ["Sleep"],
}
pairs = [("Lonely", "Depressed"), ("Caffeine", "Anxious"), ("Alcohol", "Anxious"), ("Sleep", "Anxious")]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df = pd.read_csv("data/data.csv", parse_dates=["DATE"], index_col="DATE")
df.columns = [col.title() for col in df.columns]
taken = pd.read_csv("data/antidepressant.csv", parse_dates=["DATE"])["DATE"]
periods = taken.groupby((taken.diff() > pd.Timedelta(days=14)).cumsum()).agg(["min", "max", "size"])
periods = periods[periods["size"] >= 7]
starts = periods["min"]
stops = periods["max"][periods["max"] < df.index.max() - pd.Timedelta(days=14)]

monthly = df.resample("MS")
trend = monthly.mean()[monthly.size() >= 20].rolling(3, min_periods=1).mean()
season = df.groupby(df.index.month).mean()
ranked = df.rank()
yearly = pd.DataFrame({
    f"{a} and {b}": ranked.groupby(ranked.index.year).apply(lambda year: year[a].corr(year[b]))
    for a, b in pairs
})


def lines(ax, frame, columns, line_colors):
    ax.grid(axis="y", color=grid, linewidth=0.8)
    ends = []
    for column, color in zip(columns, line_colors):
        ax.plot(frame.index, frame[column], color=color, linewidth=2)
        ends.append((frame[column].dropna().iloc[-1], frame[column].dropna().index[-1], column))
    low, high = ax.get_ylim()
    gap = (high - low) * 0.05
    previous = -float("inf")
    for y, x, column in sorted(ends):
        y = max(y, previous + gap)
        previous = y
        ax.annotate(column, (x, y), xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color=ink)


fig, axes = plt.subplots(3, 3, figsize=(20, 14), facecolor=surface, gridspec_kw={"hspace": 0.45, "wspace": 0.3})

for ax, (title, columns) in zip(axes[0], groups.items()):
    lines(ax, trend, columns, [colors[c] for c in columns])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    style(ax, f"{title}, 3-month average over the years")

mood = axes[0, 0]
mood.set_title("Mood (1-4), 3-month average, dashed = antidepressant", loc="left", color=ink, fontsize=11)
for dates, label in ((starts, "start"), (stops, "stop")):
    for date in dates:
        mood.axvline(date, color=muted, linewidth=1, linestyle="--")
        mood.annotate(label, (date, 1), xycoords=("data", "axes fraction"), xytext=(4, -4),
                      textcoords="offset points", va="top", fontsize=8, color=muted)

for ax, (title, columns) in zip(axes[1], groups.items()):
    lines(ax, season, columns, [colors[c] for c in columns])
    ax.set_xticks(range(1, 13), months)
    ax.set_xlim(0.5, 13.5)
    style(ax, f"{title}, average by month of year")

for ax in axes[2, 1:]:
    ax.remove()
ax = fig.add_subplot(axes[2, 0].get_gridspec()[2, :])
axes[2, 0].remove()
lines(ax, yearly, yearly.columns, [colors[a] for a, _ in pairs])
for column in yearly.columns:
    ax.scatter(yearly.index, yearly[column], color=colors[column.split(" and ")[0]], s=40, zorder=3,
               edgecolor=surface, linewidth=2)
ax.axhline(0, color=muted, linewidth=0.8)
ax.set_xticks(yearly.index)
ax.set_xlim(yearly.index.min() - 0.2, yearly.index.max() + 0.6)
ax.set_ylabel("Rank correlation, same day", color=muted, fontsize=9)
style(ax, "Do the relationships hold every year?")

fig.savefig("finished/long_term.png", dpi=150, bbox_inches="tight", facecolor=surface)
