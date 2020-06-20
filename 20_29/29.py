46

この記事は最終更新日から3年以上が経過しています。
はじめに
自然言語処理と Python のトレーニングのため，東北大学の乾・岡崎研究室 Web ページにて公開されている言語処理100本ノックに挑戦していきます．その中で実装したコードや，抑えておくべきテクニック等々をメモしていく予定です．コードについてはGitHubでも公開していきます．

第1章
第2章・前編
第2章・後編の続きです．
言い訳
しばらくサボっていたおかげで，以前自分が書いたコードを読み解きながらの記事執筆になってしまいました．「3日前の自分は他人」を地で行くスタイル．
その間に習熟度も結構変わっていて，あうあう言いながら自分のコードを眺めていました．
更新の間が空いてしまいましたが，他山の石としていただければ．

第3章: 正規表現
Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．

1行に1記事の情報がJSON形式で格納される
各行には記事名が"title"キーに，記事本文が"text"キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
ファイル全体はgzipで圧縮される
以下の処理を行うプログラムを作成せよ．

20. JSONデータの読み込み
Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．

回答
20.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 20.py

import json

with open("jawiki-country.json") as f:
    article_json = f.readline()
    while article_json:
        article_dict = json.loads(article_json)
        if article_dict["title"] == u"イギリス":
            print(article_dict["text"])
        article_json = f.readline()

コメント
今回用いる jawiki-country.json.gz は 9.9MB もあって結構重いので，readline() で一行ずつ読んでいって「イギリス」の記事だけ print （他記事はスルー）しています．
readlines() とかするとしばらく動作が停止する気がしますし，より広汎な用途があるならともかく「イギリス」の記事のみを対象として操作していくのでこのように実装しました．

今回のテキストデータでは，ファイルの各行が JSON 形式で記述されています．しかしただ読み込むだけ（json.load()）では操作が上手く行えず JSON のメリットを生かせないので，json.loads() を利用して JSON 形式（今回は実質辞書）に変換しています．

モジュール化
ここからしばらく「イギリス」の記事だけ抽出する作業が続くので，以下のようにモジュール化しました．

extract_from_json.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# extract_from_json.py

import json


def extract_from_json(title):
    with open("jawiki-country.json") as f:
        json_data = f.readline()
        while json_data:
            article_dict = json.loads(json_data)
            if article_dict["title"] == title:
                return article_dict["text"]
            else:
                json_data = f.readline()
    return ""

20.py と異なり，今回の関数はタイトルを引数に渡すとその記事の文字列を返してくれます（存在しなければ空文字列）．

21. カテゴリ名を含む行を抽出
記事中でカテゴリ名を宣言している行を抽出せよ．

回答
21.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 21.py

from mymodule import extract_from_json

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    if "Category" in line:
        print(line)

# python3 ならこれでも表示可能（list だけど）
# print([line for line in lines if "Category" in line])

コメント
正規表現の章なのに正規表現を使わず．まあこちらの方が分かりやすいし…
というわけで "Category" という文字列を含む行だけ print しています．

内包記法で書けばすっきり収まるのですが，Python2 では Unicode 文字列を含むリストをそのまま print するとエスケープ表示されてしまいます．そのため日本語として読める形では表示されません．
今回のコードは Python3 で実行可能ですので， Python3 で実行すると上手く処理してくれます．

22. カテゴリ名の抽出
記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．

回答
22.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 22.py

import re
from mymodule import extract_from_json

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    category_line = re.search("^\[\[Category:(.*?)(|\|.*)\]\]$", line)
    if category_line is not None:
        print(category_line.group(1))

コメント
まず21.と同様にカテゴリ行を抜き出して，そこから名前だけを re.search() を用いて抽出します．
re.search() は第2引数で指定された文字列の中で，第1引数の正規表現パターンにマッチする箇所があれば MatchObject インスタンスを返してくれます．
MatchObject がどういうものかはさておき，.group() を使うとマッチした文字列を取得することができます．
今回でいえば category_line.group(0) ではマッチした文字列全体（e.g. "[[Category:イギリス|*]]"）が，category_line.group(1) では最初にマッチした部分文字列（e.g. イギリス）が得られます．

そして肝心の正規表現なのですが，詳細は公式ドキュメントに丸投げして，このページでは具体的な適応例をフォローしていきたいと思います．
今回処理するカテゴリ行はこちら（21.py の実行結果）

22.pyの実行結果
$ python 22.py
[[Category:イギリス|*]]
[[Category:英連邦王国|*]]
[[Category:G8加盟国]]
[[Category:欧州連合加盟国]]
[[Category:海洋国家]]
[[Category:君主国]]
[[Category:島国|くれいとふりてん]]
[[Category:1801年に設立された州・地域]]
基本的には [[Category:カテゴリ名]] ですが，一部 | で区切って読みを指定しているものがあります．なので方針としては，

まず [[Category: で始まる
何かしらの文字列（カテゴリ名）が来る
場合によっては | で区切られた読み仮名が来る
最後に ]] で締める
といった形になります．
これを正規表現で表すと（最適かは自信がありませんが） "^\[\[Category:(.*?)(\|.*)*\]\]$" となります．

意図	実際の正規表現	解説
まず [[Category: で始まる	^\[\[Category:	^ で先頭指定
何かしらの文字列（カテゴリ名）が来る	(.*?)	任意の文字列と最短一致
場合によっては `	` で区切られた読み仮名が来る	`(\
最後に ]] で締める	\]\]$	終端を示す $ は必要ないかも
23. セクション構造
記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．

回答
23.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 23.py

import re
from mymodule import extract_from_json

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    section_line = re.search("^(=+)\s*(.*?)\s*(=+)$", line)
    if section_line is not None:
        print(section_line.group(2), len(section_line.group(1)) - 1)

コメント
基本構造は 22. と同様ですが，今回はセクション名（e.g. == セクション ==）が対象なのでそれを拾っていきます．
微妙に表記揺れがあったので（==セクション==，== セクション ==）それを吸収できるように空白文字を表す \s を間に挟んであります．
セクションのレベルは == の長さに対応しているので（==1==，===2===，...）その長さを取得して -1 することで算出しています．

24. ファイル参照の抽出
記事から参照されているメディアファイルをすべて抜き出せ．

回答
24.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 24.py

import re
from mymodule import extract_from_json

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    file_line = re.search(u"(File|ファイル):(.*?)\|", line)
    if file_line is not None:
        print(file_line.group(2))

コメント
当初 File: から始まるものだけを抜き出していた...間抜け．

正規表現のパターンに日本語が入ってくる都合上 Unicode になっていますが，Python の正規表現パターンではは許されるらしい．
よく r"hogehoge" として raw 文字列にしている例をよく見ますが，これはエスケープ処理がダブって読みにくくなってしまうのを防ぐものなので，少なくともマストではない感じ？
さらに言えば繰り返し正規表現パターンを使い回すのであれば re.compile() を使ってコンパイルする方が効率的らしいです．が，最後に使用した正規表現パターンはキャッシュされるとのことなので，今回はそこまで気にする必要はなさそう．

25. テンプレートの抽出
記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．

回答
25.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 25.py

import re
from mymodule import extract_from_json

temp_dict = {}
lines = re.split(r"\n[\|}]", extract_from_json(u"イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = temp_line.group(2)

for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)

コメント
テンプレートは |テンプレート名 = テンプレート内容 という形で入っているので，それに合わせた正規表現になっています．
上記の通り ^\|(.*?)\s=\s(.*) と書くと1番目の括弧内がテンプレート名，2番めの括弧内がテンプレート内容となるのでそれを辞書に格納しています．

基本的にはテンプレートは |テンプレート名 = テンプレート内容 という形で 各行に 格納されているのですが，ちょっと公式国名が厄介でした．

公式国名
|公式国名 = {{lang|en|United Kingdom of Great Britain and Northern Ireland}}<ref>英語以外での正式国名:<br/>
*{{lang|gd|An Rìoghachd Aonaichte na Breatainn Mhòr agus Eirinn mu Thuath}}（[[スコットランド・ゲール語]]）<br/>
*{{lang|cy|Teyrnas Gyfunol Prydain Fawr a Gogledd Iwerddon}}（[[ウェールズ語]]）<br/>
*{{lang|ga|Ríocht Aontaithe na Breataine Móire agus Tuaisceart na hÉireann}}（[[アイルランド語]]）<br/>
*{{lang|kw|An Rywvaneth Unys a Vreten Veur hag Iwerdhon Glédh}}（[[コーンウォール語]]）<br/>
*{{lang|sco|Unitit Kinrick o Great Breetain an Northren Ireland}}（[[スコットランド語]]）<br/>
**{{lang|sco|Claught Kängrick o Docht Brätain an Norlin Airlann}}、{{lang|sco|Unitet Kängdom o Great Brittain an Norlin Airlann}}（アルスター・スコットランド語）</ref>

上記のように改行（文字=\n）を含んで複数行にまたがっているので，この辺を上手く処理してあげる必要があります．

結局，

split() する際に，\n ではなく \n| or \n} で（re.split()）
テンプレートの境になるところで split()
} が絡んでくるのは 一番最後で | が出てこないからです
\n も含めて re.search() するために re.S というフラグを立てる
| が split() で吹っ飛んでいるので search() で考慮
と色々試行錯誤してできました．

一応中身を確認するため for loop で print していますが，これまた Python3 推奨．何だかんだいって Python3 便利だ...

26. 強調マークアップの除去
25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ（参考: マークアップ早見表）．

回答
26.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 26.py

import re
from mymodule import extract_from_json

temp_dict = {}
lines = re.split(r"\n[\|}]", extract_from_json(u"イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = re.sub(r"'{2,5}", r"", temp_line.group(2))

# 25.py と同様 Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)

コメント
re.sub は正規表現にマッチする部分を置換してくれる関数です．
今回は2個以上5個以下の ' を消去してくれるように書いています．
{n, m} と書くと直前の文字がn個以上m個以下と正規表現で表すことができます．
まあ今回は純粋に ' を全除去すればよかった気も...

27. 内部リンクの除去
26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ（参考: マークアップ早見表）．

回答
27.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 27.py

import re
from mymodule import extract_from_json


def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    return str

temp_dict = {}
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    category_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if category_line is not None:
        temp_dict[category_line.group(1)] = remove_markup(category_line.group(2))

for k, v in sorted(temp_dict.items(), key=lambda x: x[0]):
    print(k, v)

コメント
マークアップを除去する関数 remove_markup() を作成しました．

行番号	除去対象
1行目	強調（26と同様）
2行目	内部リンク
内部リンクの記述法には

[[記事名]]
[[記事名|表示文字]]
[[記事名#節名|表示文字]]
の3種類がありますが，いずれも「[[ から始まって，何らかの記号（]]，|，#）が来るまでが記事名」という法則があるので，それに準拠した正規表現を書きました．

28. MediaWikiマークアップの除去
27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．

回答
28.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 28.py

import re
from mymodule import extract_from_json


def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str)
    str = re.sub(r"<.*?>", r"", str)
    str = re.sub(r"\[.*?\]", r"", str)
    return str

temp_dict = {}
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    temp_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

for k, v in sorted(temp_dict.items(), key=lambda x: x[0]):
    print(k, v)

コメント
27に加え，

行番号	除去対象
1行目	強調（26と同様）
2行目	内部リンク（27と同様）
3行目	（マークアップ早見表には無いけど）言語を指定した表記
4行目	コメント
5行目	外部リンク
を除去できるように remove_markup() を書き換えました．

29. 国旗画像のURLを取得する
テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）

回答
29.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 29.py

import re
import requests
from mymodule import extract_from_json


def json_search(json_data):
    ret_dict = {}
    for k, v in json_data.items():
        if isinstance(v, list):
            for e in v:
                ret_dict.update(json_search(e))
        elif isinstance(v, dict):
            ret_dict.update(json_search(v))
        else:
            ret_dict[k] = v
    return ret_dict


def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str)
    str = re.sub(r"<.*?>", r"", str)
    str = re.sub(r"\[.*?\]", r"", str)
    return str

temp_dict = {}
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    temp_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

url = "https://en.wikipedia.org/w/api.php"
payload = {"action": "query",
           "titles": "File:{}".format(temp_dict[u"国旗画像"]),
           "prop": "imageinfo",
           "format": "json",
           "iiprop": "url"}

json_data = requests.get(url, params=payload).json()

print(json_search(json_data)["url"])
