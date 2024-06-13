# rank-predictor

A tool to predict expected final rank in Japanese mahjong

## Installation

We need Python (we require at least 3.12).

```sh
rank-predictor$ pip install .
```

## Usage

### Converting the mjlog format game records into the annotated data

```sh
rank-predictor-convert 4 h game_record xml annotated-data.csv
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The length of game|Accepts only `t` (Tonpu) or `h` (Hanchan)|
|3|Path to the directory where game records are stored|Only files directly under the directory are targeted|
|4|Extension of game records|Case-sensitive|
|5|Path to the file to save the annotated data|Containing round state, score, and final rank class|
|6|(Optional) Outputs final score|Enabled by specifying `-f` or `--final-score`|
|7|(Optional) Outputs game record file name|Enabled by specifying `-n` or `--filename`|

### Splitting the annotated data into train and test subsets

```sh
rank-predictor-split annotated-data.csv training-data.csv test-data.csv
```

This command serves as a streamlined interface to the `sklearn.model_selection.train_test_split`.  
Refer to the [scikit-learn documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) for optional arguments.

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|Path to the file containing the annotated data||
|2|Path to the file to save a train subset of the annotated data||
|3|Path to the file to save a test subset of the annotated data||
|4|(Optional) test_size|Specify with `--test_size`|
|5|(Optional) train_size|Specify with `--train_size`|
|6|(Optional) random_state|Specify with `-r` or `--random_state`|
|7|(Optional) shuffle|Disabled by specifying `-f` or `--shuffle-false`|

### Training and saving a model

```sh
rank-predictor-train 4 h training-data.csv config.toml model.pickle
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The length of game|Accepts only `t` (Tonpu) or `h` (Hanchan)|
|3|Path to the file containing the annotated data||
|4|Path to the file containing configurations for training||
|5|Path to the file to save the trained model||

### Predicting expected final rank

```sh
rank-predictor 4 h model.pickle 0 0 0 25000 25000 25000 25000
```

Output:

```text
Rank Probability
player_0: [0.30085029 0.26454441 0.20796936 0.22663595]
player_1: [0.2407986  0.26629562 0.20320842 0.28969736]
player_2: [0.21027113 0.27973354 0.32559989 0.18439545]
player_3: [0.24807999 0.18942643 0.26322234 0.29927124]

Expected Rank
player_0: 2.3603909686402478
player_1: 2.541804539120996
player_2: 2.4841196522021267
player_3: 2.61368484003663
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The length of game|Accepts only `t` (Tonpu) or `h` (Hanchan)|
|3|Path to the file where the trained model is saved||
|4|The number of round|East 1 (東1局) is `0`, South 1 (南1局) is `4`, West 1 (西1局) is `8`. Accepts only from `0` to `11`|
|5|The number of counter sticks (本場)||
|6|The number of riichi deposits (供託本数)|\*1|
|7|The score of the qijia (dealer at the start of a game) (起家の点数)|\*1\*2|
|8|The score of the player right next to the qijia (起家の下家の点数)|\*1\*2|
|9|The score of the player across from the qijia (起家の対面の点数)|\*1\*2|
|10|The score of the player left next to the qijia (起家の上家の点数)|Applies only if number of players is `4` \*1\*2|

*1: Accepts only integers greater than or equal to **0**. The total score must be **100,000** for 4-player mahjong and **105,000** for 3-player mahjong. The total score is calculated as follows:  
**(Total Score) = (The Number of Riichi Deposits) * 1,000 + (Sum of All Players' Scores)**

*2: The last two digits of the score must be 0.

## License

Copyright (c) Apricot S. All rights reserved.

This repository is licensed under the [MIT license](LICENSE).
