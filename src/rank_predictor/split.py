"""Provides functionality to split data."""

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
    """Splits the input data into training and test datasets.

    This function wraps scikit-learn's `train_test_split` and saves the
    resulting datasets to the specified paths.

    Args:
        input_data_path: The path to the input data file.
        train_data_path: The path where the training data will be saved.
        test_data_path: The path where the test data will be saved.
        test_size: The proportion or absolute number of the dataset to
            include in the test split. Refer to the scikit-learn
            documentation for `train_test_split` for more details.
            Defaults to None.
        train_size: The proportion or absolute number of the dataset to
            include in the train split. Refer to the scikit-learn
            documentation for `train_test_split` for more details.
            Defaults to None.
        random_state: The seed used by the random number generator.
            Refer to the scikit-learn documentation for
            `train_test_split` for more details. Defaults to None.
        shuffle: Whether or not to shuffle the data before splitting. If
            shuffle=False then stratify must be False. Defaults to True.
        stratify: If True, data is split in a stratified fashion, using
            `rank_class` as the class labels. Defaults to False.
    """
    input_data = pl.read_csv(input_data_path)

    label = None
    if stratify:
        label = input_data.get_column(DataName.RANK_CLASS)

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
