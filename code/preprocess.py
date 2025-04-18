import numpy as np
import pandas as pd

# Columns to remove
bad_columns = {
    "NOTE", "MENSTRUAL CYCLE", "WEIGHT", "MINDFULNESS", "THERAPY", "NEWS", "SOCIAL MEDIA", "CHORES", "ID", "EXERCISE"
}

frame = pd.read_csv("data/entry.csv")

def discard_unwanted_columns(df, bad_columns):
    kept_cols = [col for col in df.columns if col not in bad_columns]
    cleaned_df = df[kept_cols]
    cleaned_df = cleaned_df.replace(0, np.nan)
    # Be in root when running python
    cleaned_df.to_csv("data/data.csv", index=False)

discard_unwanted_columns(frame, bad_columns)
