## Q_00
- シーケンスの一部分を切り取ってコピーを返してくれる仕組みを、スライスと呼びます。
- なお、シーケンスの先頭要素のインデックスは0からです。ステップも大事

## Q_01
- ステップで一個飛ばし

## Q_2
- Pythonの組み込み関数zip()は複数のオブジェクトの要素をまとめる関数。
- forループで複数のリストの要素を取得する際に使う
#### 要素数が異なる場合の処理　
- zip関数では多い要素が無視される
- itertools.zip_longest()関数では足りない分の要素が埋められる
- forループで複数のリストの要素を取得
- forループの中で複数のイテラブルオブジェクト（リストやタプルなど）の要素を同時に取得して使いたい場合は、zip()関数の引数にそれらを指定する。

names = ['Alice', 'Bob', 'Charlie']
ages = [24, 50, 18]

for name, age in zip(names, ages):
    print(name, age)
 出力結果
 Alice 24
 Bob 50 
 Charlie 18

#### reduce関数とは
- reduceの主な目的は、複数の値を一つの値に縮約することにある。map関数やfilter関数に似ていて、関数を引数に取ることができる。
- reduce関数では、第一引数に引数を2つ取る関数を指定し、第二引数にはイテラブルなオブジェクトを指定します。

具体的には、以下のとおりです。

まず、引数を２つとるfuncと、リストsample_listを用意します
reduce(func, sample_list) を呼び出すと、sample_listの最初の2つの要素に関数funcが適用されます(つまり、func(sample_list[0], sample_list[1])の用な感じ)
最初の2つの要素を使って計算された値をresult1とすると、今度はこの値とsample_list[2]をfuncは引数にとって、計算をします(つまり、func(result1, sample_list[[2]) の用な感じです)
あとは、これが要素がなくなるまで繰り返します。
簡単ですね。

◯reduce関数の使い方
以下みたいな感じで使います。

from functools import reduce

def add(x, y):
    return x + y

a = [1, 2, 3, 4, 5,]
print(reduce(add, a))

出力結果
15

#### lambdaとは？
- lambdaは lambda 引数: 返り値　という形で書きます。
- 短く書いているだけですので、無名ではなくする(関数を定義する)と

def func(引数):
    return 返り値
となります。上記のlambda式と、関数funcは同じ実行をします。　つまり

def return_twice(n):
    return n * 2
は

lambda n: n * 2
となります。
