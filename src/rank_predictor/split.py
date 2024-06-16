from pathlib import Path

import polars as pl
from sklearn.model_selection import train_test_split

from rank_predictor.types import DataName


def split(
    input_data_path: Path,
    train_data_path: Path,
    test_data_path: Path,
    test_size: float | None = None,
    train_size: float | None = None,
    random_state: int | None = None,
    *,
    shuffle: bool = True,
    stratify: bool = False,
) -> None:
    input_data = pl.read_csv(input_data_path)

    label = None
    if stratify:
        label = input_data.select(DataName.RANK_CLASS).to_series()

    train_data, test_data = train_test_split(
        input_data,
        test_size=test_size,
        train_size=train_size,
        random_state=random_state,
        shuffle=shuffle,
        stratify=label,
    )

    assert isinstance(train_data, pl.DataFrame)  # noqa: S101
    assert isinstance(test_data, pl.DataFrame)  # noqa: S101

    train_data.write_csv(train_data_path)
    test_data.write_csv(test_data_path)
