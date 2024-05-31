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

### Converting the mjlog format game records into the training data

```sh
rank-predictor-convert 4 game_record training-data.csv
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|Path to the directory where game records are stored||
|3|Path to the file containing round, score, and final score||

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
rank-predictor 4 1 0 0 25000 25000 25000 25000 --model model.pickle
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The number of round|East 1 (東1局) is `1`, South 1 (南1局) is `5`. Accepts only from `1` to `8`|
|3|The number of counter sticks (本場)|Accepts only from `0` to `99`|
|4|The number of riichi deposits (供託本数)|\*1|
|5|The score of the qijia (dealer at the start of a game) (起家の点数)|\*1\*2|
|6|The score of the player right next to the qijia (起家の下家の点数)|\*1\*2|
|7|The score of the player across from the qijia (起家の対面の点数)|\*1\*2|
|8|The score of the player left next to the qijia (起家の上家の点数)|Applies only if number of players is `4` \*1\*2|
|9|(Optional) Path to the file where the trained model is saved|If not specified, the application will use the default model that is included with the project.|

*1: Accepts only integers greater than or equal to **0**. The total score must be **100,000** for 4-player mahjong and **105,000** for 3-player mahjong. The total score is calculated as follows:  
**(Total Score) = (The Number of Riichi Deposits) * 1,000 + (Sum of All Players' Scores)**

*2: Only the part of the score that is 100 or greater is considered. For example, an input of `25123` is interpreted as `25100`.

## License

Copyright (c) Apricot S. All rights reserved.

This repository is licensed under the [MIT license](LICENSE).
