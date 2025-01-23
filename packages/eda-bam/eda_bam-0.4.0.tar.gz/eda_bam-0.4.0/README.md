# eda-bam
![LGTM](https://i.lgtm.fun/2vtm.png)

### Use
```bash
$ eda-bam
Usage: eda-bam [OPTIONS] KEYWORD
Try 'eda-bam --help' for help.
╭─ Error ───────────────────────────────────────────────────────────╮
│ Missing argument 'KEYWORD'.                                       │
╰───────────────────────────────────────────────────────────────────╯
$ eda-bam --help

 Usage: eda-bam [OPTIONS] KEYWORD

╭─ Arguments ────────────────────────────────────────────────────────╮
│ *    keyword      TEXT  [default: None] [required]                 │
╰────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────╮
│ --asc            --no-asc                     [default: no-asc]    │
│ --rcnt                               INTEGER  [default: 12]        │
│ --keyword-sum    --no-keyword-sum             [default:            │
│                                               no-keyword-sum]      │
│ --help                                        Show this message    │
│                                               and exit.            │
╰────────────────────────────────────────────────────────────────────╯

$ eda-bam 자유
president  count
      박정희    513
      이승만    438
      노태우    399
      김대중    305
      문재인    275
      김영삼    274
      이명박    262
      전두환    242
      노무현    230
      박근혜    111
      최규하     14
      윤보선      1

$ eda-bam 자유 --asc --rcnt 3 --keyword-sum
president  count  keyword_sum
      윤보선      1            6
      최규하     14           28
      박근혜    111          250
```


### DEV
```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyterlab
```
### EDA
- run jupyterlab
```
$ jupyter lab
```
### Ref
- [install jupyterlab](https://jupyter.org/install)
- https://pypi.org/project/president-speech/
