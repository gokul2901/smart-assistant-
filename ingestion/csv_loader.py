import pandas as pd

def load_csv():
    df = pd.read_csv('data/raw data/products.csv')
    return df

df = load_csv()

if __name__ == "__main__":
    print(df.head())