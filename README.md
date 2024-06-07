# rank-predictor

A tool for predict expected final rank in Japanese mahjong.

Reference (Broken Link): <http://critter.sakura.ne.jp/jun_keisan_setumei.html>

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
|5|Path to the file containing round state, score, and final rank class||
|6|(Optional) Outputs final score|Enabled by specifying `-f` or `--final-score`|
|7|(Optional) Outputs game record file name|Enabled by specifying `-n` or `--filename`|

### Training and saving a model

```sh
rank-predictor-train 4 h config.toml training-data.csv model.pickle
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The length of game|Accepts only `t` (Tonpu) or `h` (Hanchan)|
|3|Path to the file containing configurations for training||
|4|Path to the file containing round state, score, and final rank class||
|5|Path to the file where the trained model is saved||

### Predicting expected final rank

```sh
rank-predictor 4 h 0 0 0 25000 25000 25000 25000 --model model.pickle
```

The meaning of each argument is as follows:

|Index|Explanation|Note|
|-|-|-|
|1|The number of players|Accepts only `4` or `3`|
|2|The length of game|Accepts only `t` (Tonpu) or `h` (Hanchan)|
|3|The number of round|East 1 (東1局) is `0`, South 1 (南1局) is `4`. Accepts only from `0` to `7`|
|4|The number of counter sticks (本場)|Accepts only from `0` to `99`|
|5|The number of riichi deposits (供託本数)|\*1|
|6|The score of the qijia (dealer at the start of a game) (起家の点数)|\*1\*2|
|7|The score of the player right next to the qijia (起家の下家の点数)|\*1\*2|
|8|The score of the player across from the qijia (起家の対面の点数)|\*1\*2|
|9|The score of the player left next to the qijia (起家の上家の点数)|Applies only if number of players is `4` \*1\*2|
|10|(Optional) Path to the file where the trained model is saved|If not specified, the application will use the default model that is included with the project.|

*1: Accepts only integers greater than or equal to **0**. The total score must be **100,000** for 4-player mahjong and **105,000** for 3-player mahjong. The total score is calculated as follows:  
**(Total Score) = (The Number of Riichi Deposits) * 1,000 + (Sum of All Players' Scores)**

*2: Only the part of the score that is 100 or greater is considered. For example, an input of `25199` is interpreted as `25100`.

## License

Copyright (c) Apricot S. All rights reserved.

This repository is licensed under the [MIT license](LICENSE).
