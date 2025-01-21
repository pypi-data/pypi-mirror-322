import os
from pathlib import Path

import pandas as pd


def save(path: str, filename: str, data: pd.DataFrame) -> None:
    if not os.path.exists(path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)

    data.to_parquet(f"{path}/{filename}")
