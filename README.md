# The World in One Day — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

`main.py` draws a single 1024x1024 PNG that sums up the world news of
Monday 23 November 2026. Two heroes lead the page: Nvidia's Jensen
Huang returns and the stock jumps 31 percent, and the COP31 climate
talks collapse in Antalya with no deal. Below them, a four-number
stat strip (Nasdaq +6.5%, 450 German schools, 258 House seats,
Bitcoin $55,130) and a seven-section region grid carry 36 dated
stories in all across 7 regions, with an "also on Monday" closer.
Every headline is set large enough that the page's structure, heroes
and big numbers read when the image is shown about 300 pixels across.

## How it works

- Pure Python 3 standard library — no third-party packages, no
  network, no randomness, no clock reads. Two runs are byte-identical.
- A hand-built RGB canvas, a 5x7 bitmap lettering set, a Bresenham
  line for the markets chart, and a small `zlib`/`struct` PNG writer
  render the poster; headlines are wrapped to measured widths so
  nothing overflows its frame.
- Every story was researched on 24 Nov 2026 from wire copy and front
  pages; the reporting behind each item is listed in `SOURCES.md`.

## Run it

```sh
python3 main.py
```

Writes `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ck3acpkm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
