# cob-eda

## 입력한 단어별 역대 대통령  발언 횟수 출력 by Typer


```bash

$ from cob_eda.cli import group_by_count
$ group_by_count()
----------------------------------------
$ cob-eda 1번 2번 3번


```

- **group_by_count("1번",2번,3번)**
- 1번 입력: 검색 할 단어 입력 "str"값으로 입력해야합니다
- 2번 입력: 내림차순:"False", 오름차순:"True" //**둘 중 한가지만 입력해야 합니다.**
- 3번 입력: 상위 혹은 하위 몇 명 조회 할 것인지에 대한 정수입력
- **EX) group_by_count("경제", False, 5) => 경제 발언 최다 상위 5명 출력** 


## 입력한 단어별 역대 대통령  발언 횟수 출력 by input

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

