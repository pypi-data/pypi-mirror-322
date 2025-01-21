# eda-nijin
 ![LGTM](https://i.lgtm.fun/2vtu.png)

### USE
```bash
$ pip install eda-nijin
$ eda-nijin
Usage: eda-nijin [OPTIONS] KEYWORD
Try 'eda-nijin --help' for help.
╭─ Error ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ Missing argument 'KEYWORD'.                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
$ eda-nijin --help
 Usage: eda-nijin [OPTIONS] KEYWORD

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────╮
│ *    keyword      TEXT  [default: None] [required]                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --asc     --no-asc             [default: asc]                                                       │
│ --rcnt                INTEGER  [default: 12]                                                        │
│ --help                         Show this message and exit.                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
$ eda-nijin 자유
president  count
      윤보선      1
      최규하     14
      박근혜    111
      노무현    230
      전두환    242
      이명박    262
      김영삼    274
      문재인    275
      김대중    305
      노태우    399
      이승만    438
      박정희    513
총 합계:12

```
### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyter
```
### EDA
- run jupyterlab
```
$ jupyter lab
```
### REF
- [install jupyterlab](https://jupyter.org/install)
- https://pypi.org/project/president-speech/
