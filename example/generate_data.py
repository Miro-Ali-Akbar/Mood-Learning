import io
import zipfile

import numpy as np
import pandas as pd

rng = np.random.default_rng()
dates = pd.date_range("2022-01-01", "2025-12-31")
n = len(dates)


def uniform(low, high):
    return rng.integers(low, high + 1, n)


entries = pd.DataFrame({
    "ID": np.arange(n, 0, -1),
    "DATE (YYYY-MM-DD)": dates.strftime("%Y-%m-%d"),
    "PRODUCTIVITY": uniform(1, 4),
    "MOTIVATION": uniform(1, 4),
    "LONELY": uniform(1, 4),
    "DEPRESSED": uniform(1, 4),
    "ANXIOUS": uniform(1, 4),
    "SLEEP": uniform(2, 24) / 2,
    "FAMILY": uniform(1, 2),
    "NOTE": "",
    "NUTRITION": uniform(1, 2),
    "OUTDOORS": uniform(1, 2),
    "EXERCISE": 0,
    "HYGEINE": uniform(1, 2),
    "CHORES": 0,
    "MENSTRUAL CYCLE": 0,
    "WEIGHT": "",
    "RESTFUL SLEEP": uniform(1, 2),
    "OVERALL OUTLOOK": uniform(1, 3),
    "CAFFEINE": uniform(0, 4),
    "ALCOHOL": uniform(0, 4),
    "MINDFULNESS": 0,
    "THERAPY": 0,
    "NEWS": 0,
    "SOCIAL MEDIA": 0,
})

medication = "ID,NAME,DOSE,UNITS,AMPM,VISIBLE,FREQUENCY,SORTORDER,EDITABLEUNTIL\n"
doses = "ID,ENTRY,MEDICATION,TOOK,DOSETOOK\n"

with zipfile.ZipFile("export.emoodsw", "w") as archive:
    buffer = io.StringIO()
    entries.to_csv(buffer, index=False)
    archive.writestr("entry.csv", buffer.getvalue())
    archive.writestr("medication.csv", medication)
    archive.writestr("entry_medication.csv", doses)
