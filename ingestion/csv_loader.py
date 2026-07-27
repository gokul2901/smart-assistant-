import os
import glob
import pandas as pd

def load_csv():
    raw_files = glob.glob('data/raw/*.csv') + glob.glob('data/raw data/*.csv')
    if raw_files:
        return pd.read_csv(raw_files[0])
    raise FileNotFoundError("No CSV data files found in data/raw/")

df = load_csv()

if __name__ == "__main__":
    print(df.head())