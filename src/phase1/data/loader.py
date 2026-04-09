from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from datasets import load_dataset


@dataclass(frozen=True)
class DatasetRef:
    dataset_id: str
    split: str = "train"


class DatasetLoader:
    def __init__(self, dataset_ref: DatasetRef) -> None:
        self.dataset_ref = dataset_ref

    def load(self) -> pd.DataFrame:
        ds = load_dataset(self.dataset_ref.dataset_id, split=self.dataset_ref.split)
        return ds.to_pandas()
