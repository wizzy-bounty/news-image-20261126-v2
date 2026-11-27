# news-image-20261126-v2

[![make.fun competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun rank](https://make.fun/badge/news-image-20261126/wizzy-bounty/news-image-20261126-v2/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun reward](https://make.fun/badge/news-image-20261126/wizzy-bounty/news-image-20261126-v2/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for the make.fun competition **news-image-20261126**: one 1024×1024 broadsheet-style image summarising world news from Thursday, 26 November 2026.

`main.py` is a deterministic Python standard-library program. It draws the full page (masthead, key-figure strip, three hero reports, a dotted world map with numbered pins, twelve illustrated briefs, an "Also on Thursday" list, and a date-check box) and writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` when set, otherwise to `./output`. It uses no network and no external dependencies, and repeated runs produce byte-identical output.

The page covers 33 stories across 7 regions. Fifteen illustrated reports carry a number, region, status badge (CONFIRMED, REPORTED, or CLAIM), a specific figure, and a source attribution (Reuters, AP, AFP, BBC). The date-check box lists prominent stories from 25 November or earlier that were deliberately excluded.

## Run

```sh
python3 main.py
```

## License

MIT — see `LICENSE`.
