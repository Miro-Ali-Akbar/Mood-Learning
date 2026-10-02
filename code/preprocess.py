import numpy as np
import pandas as pd

bad_columns = {
    "NOTE", "MENSTRUAL CYCLE", "WEIGHT", "MINDFULNESS", "THERAPY", "NEWS", "SOCIAL MEDIA", "CHORES", "ID", "EXERCISE"
}
zero_is_value = ["CAFFEINE", "ALCOHOL"]
antidepressant = "antidepp"

frame = pd.read_csv("data/raw/entry.csv")


def clean(df):
    df = df.drop(columns=[col for col in df.columns if col in bad_columns])
    df = df.rename(columns={"DATE (YYYY-MM-DD)": "DATE"})
    df["DATE"] = pd.to_datetime(df["DATE"])
    df = df.sort_values("DATE").set_index("DATE")

    other = df.columns.difference(zero_is_value)
    df[other] = df[other].replace(0, np.nan)
    for col in zero_is_value:
        tracked_from = df.index[df[col] != 0].min()
        df.loc[df.index < tracked_from, col] = np.nan
    return df


def antidepressant_days(entries):
    medication = pd.read_csv("data/raw/medication.csv")
    doses = pd.read_csv("data/raw/entry_medication.csv")
    medication_id = medication.loc[medication["NAME"] == antidepressant, "ID"].iloc[0]
    taken = doses[(doses["MEDICATION"] == medication_id) & (doses["TOOK"] == 2)]
    dates = entries.set_index("ID").loc[taken["ENTRY"], "DATE (YYYY-MM-DD)"]
    return pd.DataFrame({"DATE": sorted(dates)})


clean(frame).to_csv("data/data.csv")
antidepressant_days(frame).to_csv("data/antidepressant.csv", index=False)
