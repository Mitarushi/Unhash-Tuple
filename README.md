# はじめに
このライブラリはPythonでhashが衝突するtupleを生成することを目的としています。\
例えば、tupleを要素とするdictを使ったコードをTLEに出来るかもしれません。

# 使い方
## ライブラリとして
Python3.8以降のコードを目標とする場合、このファイルから次のtuple_unhashをimportして使ってください。\

```python:
def tuple_unhash(length: int,
                 h: int = -1,
                 rand_min: int = 0,
                 rand_max: int = INT_HASH_MOD) -> typing.Tuple[int]:
```

引数は次のようになっています。

- __length__ 出力するtupleの長さを指定します。
- __h__ 出力するtupleのhashの値を指定します。h=-1の時はランダムに選ばれます。
- __rand_min__ 出力するtupleの要素の最小値を指定します。
- __rand_max__ 出力するtupleの要素の最大値を指定します。

この関数は全ての要素がrand_min以上rand_max以下を満たし、hash(tuple)がhと等しくなるようなtupleを出力します。\
内部で (rand_max - rand_min) / 2^64 の確率で成功するアルゴリズムが動いているため、 rand_max - rand_min が小さいと結果が返ってこないことがあります。

Python3.7以前のコードを目標とする場合、tuple_unhash_oldを使う必要があります。

```python:
def tuple_unhash_old(length: int,
                 h: int = -1,
                 rand_min: int = 0,
                 rand_max: int = INT_HASH_MOD) -> typing.Tuple[int]:
```


### 使用例

```python
>>> from tuple_unhash import tuple_unhash
>>> t = tuple_unhash(length=3, h=114514, rand_min=1, rand_max=10**18)
>>> t
(397059355314417439, 883021301061962745, 900389205006229751)
>>> hash(t)
114514
```

## コマンドラインから
このファイルを以下のように実行してください。

```
python3 tuple_unhash.py N length [-hash] [-rand_min] [-rand_max] [--old] [--format]
```
引数は以下のようになっています。
- __N__ 出力するtupleの数を指定します。
- __length__ 出力するtupleの長さを指定します。
- __-hash__ 出力するtupleのhashの値を指定します。h=-1の時はランダムに選ばれます。デフォルトでは-1です。
- __-rand_min__ 出力するtupleの要素の最小値を指定します。デフォルトでは1です。
- __-rand_max__ 出力するtupleの要素の最大値を指定します。デフォルトでは10^18です。
- __--old__ Python3.7以前のhashアルゴリズムを使うか指定します。
- __--format__ 出力を整形するか指定します。

その他の説明はライブラリとして使う場合と同じです。

### 使用例

```
$ python3 tuple_unhash.py 5 2 -hash=114514 --format
tuple: (795991427670691295, 402722339456043928) hash: 114514
tuple: (63424750791895889, 953523278258007066)  hash: 114514
tuple: (98205639403261696, 19554033715234907)   hash: 114514
tuple: (638522960139015932, 878751555382584078) hash: 114514
tuple: (182324011327499293, 721983218446794)    hash: 114514

$ python3 tuple_unhash.py 5 2 -hash=114514 --old
344314772390522996 106400238917669799
529630170844197337 142135937562574752
926898369229964861 986091976560480908
185138772593179541 619924701839294852
467206824899899803 897423250900150506
```

# 参考
[CPythonでのtupleのhashの実装](https://github.com/python/cpython/blob/80017752ba938852d53f9d83a404b4ecd9ff2baa/Objects/tupleobject.c#L405)\
[過去バージョンでのhashの実装](https://github.com/python/cpython/blob/caba55b3b735405b280273f7d99866a046c18281/Objects/tupleobject.c#L348)\
[CPythonでhashが変更された差分](https://github.com/python/cpython/commit/aeb1be5868623c9cd9cf6d7de3015a43fb005815)

# 問題例
[mojaocder](https://mojacoder.app/users/Mitarushi/problems/crime-counting2)



> 問題文
> ===
>
> Mitarushi国では、国民の情報は二つの整数である**生年月日**と**競技プログラミングのレート**によって管理されています。\
>つまり、人$x$と人$y$の**生年月日**と**レート**がともに等しく、かつその時に限り、人$x$と人$y$は同一人物です。\
>ところで、Mitarushi国では順番に$N$個の事件が順に起こり、$i$番目の事件の犯人の生年月日とレートが$A_i$と$B_i$であることを警察は突き止めました。\
>あなたの目的は、$i$番目の事件は$N$事件の中で$i$番目の犯人が何回目に起こした物かを知ることです。
>
>制約
>-----
>- 入力はすべて整数である。
>- $1 \leq N \leq 2\times10^5$
>- $1 \leq A_i \leq 10^{18}\ (1 \leq i \leq N)$
>- $1 \leq B_i \leq 10^{18}\ (1 \leq i \leq N)$
>

## 提出コード
[Python3での提出 (TLE)](https://mojacoder.app/users/Mitarushi/problems/crime-counting2/submissions/d2860fe4-cd2c-4094-ae93-1c7ebde3f760)\
[PyPy3での提出 (TLE)](https://mojacoder.app/users/Mitarushi/problems/crime-counting2/submissions/26675a9f-cf91-4484-b58f-74023f6d1db3)

```python3
from collections import defaultdict
import sys
input = sys.stdin.readline

n = int(input())
d = defaultdict(lambda: 0)

for _ in range(n):
    a, b = map(int, input().split())
    d[(a, b)] += 1
    print(d[(a, b)])
```