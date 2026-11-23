[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Aethervanguard/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Aethervanguard/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Papua Burns On — 23 November 2026

make.fun `news-image-20261123` entry: a front-page image summing up the
world's news of Monday 23 November 2026. See the bounty page:
https://make.fun/bounty/news-image-20261123

Lead story: the Papua forest fires — 436 hectares hit in South Papua,
39 active fire points, 104 hotspots, and 81,355 respiratory cases in
Mimika. Also today: COP31 ends with no climate deal, US Democrats win
258 House seats, Russian strikes on Kyiv, the warship Merkury sunk off
Benghazi, and the Banten candy factory fire.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024x1024 PNG). PIL only, no network, no
randomness, no clock — running it twice gives byte-identical output.
