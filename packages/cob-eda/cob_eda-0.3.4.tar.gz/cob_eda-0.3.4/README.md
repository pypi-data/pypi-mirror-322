# cob-eda

## 역대 대통령의 "올림픽" 발언 횟수 출력

```bash
$ from cob_eda.cli import group_by_count
$ group_by_count()
```
- 올림픽 발언 횟수 내림 차순으로 출력합니다. 

## 입력한 단어별 역대 대통령  발언 횟수 출력

```bash
$ from cob_eda.cli import psearch_by_count
$ psearch_by_count()
```
- 검색할 키워드를 입력
- 일치하는 단어가 있다면 내림차순으로 출력
- 일치하지 않는다면 다시 입력창으로
- 종료를 원한다면 '종료하겠습니다'를 입력 


## Dev

```bash
$ source .venv/bin/activate
$ pdm add pandas
$ pdm add -dG eda jupyterlab
```

## EDA
- $ jupyter lab


## Ref
- [install jupyterlab](https://jupyter.org/install)
- [president-speech](https://pypi.org/project/president-speech/)

