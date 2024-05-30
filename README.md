# rank-predictor

A tool for predict expected final rank in Japanese mahjong.

Reference (Broken Link): <http://critter.sakura.ne.jp/jun_keisan_setumei.html>

## Installation

Activate virtual environment. We need Python (we require at least 3.12).

```sh
rank-predictor$ python3 -m venv .venv
rank-predictor$ . .venv/bin/activate
(.venv) rank-predictor$ python3 -m pip install .
```

## Usage

### Converting the [天鳳 (Tenhou)](https://tenhou.net/) game records into the training data

```sh
rank-predictor-convert 4 game_record training-data.csv
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|Path to the directory where game records are stored||
|3|Path to the file containing round, score, and final rank||

### Training and saving a model

```sh
rank-predictor-train 4 training-data.csv model.pickle
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|Path to the file containing round, score, and final rank||
|3|Path to the file where the trained model is saved||

### Predicting expected final rank

```sh
rank-predictor-predict 4 model.pickle 1 0 0 250 250 250 250
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|Path to the file where the trained model is saved||
|3|The number of round|East 1 (東1局) is `1`, South 1 (南1局) is `5`. Accepts only from `1` to `8`|
|4|The number of counter sticks (本場)|Accepts only from `0` to `99`|
|5|The number of riichi deposits (供託本数)|\*1|
|6|The score of the qijia (dealer at the start of a game) (起家の点数)|\*1|
|7|The score of the player right next to the qijia (起家の下家の点数)|\*1|
|8|The score of the player across from the qijia (起家の対面の点数)|\*1|
|9|The score of the player left next to the qijia (起家の上家の点数)|Applies only if number of players is `4` \*1|

*1: Accepts only integers greater than or equal to **0**. The total score must be **1000** for 4-player mahjong and **1050** for 3-player mahjong. The total score is calculated as follows:

(Total Score) = (The Number of Riichi Deposits) * 10 + (Sum of All Players' Scores)

## License

Copyright (c) Apricot S. All rights reserved.

This repository is licensed under the [MIT license](LICENSE).
