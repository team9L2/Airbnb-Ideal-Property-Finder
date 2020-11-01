from DataLoader.DataLoader import DataLoader
import pandas as pd

class BostonDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def load(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
