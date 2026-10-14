# はじめに
日本語プログラミング言語Mindの小技「再帰呼び出し」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# 対応バージョン
本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。

■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# この小技に関連するMind言語マニュアル
現時点で言及されている箇所を発見できていません。

# 小技の解説
「再帰呼び出し」は関数がその処理の中で自分自身を呼び出すことを指し、Mindでも実装できます。通常のループ反復の実装に対する注意点は他のプログラミング言語と同様と推定されます。

**・終了条件:** 終了条件がないと無限ループになる。（スタックオーバーフローが発生。）
**・メモリ使用量:** 深い再帰はメモリ不足（スタックオーバーフロー）を引き起こす。
**・計算量増加:** 通常のループ反復よりも計算コストが高くなる場合がある。
ただし、Mindの通常の処理単語呼び出しの場合、単語の呼び出しもスタックを介して行われるので、実行コストは単純反復とあまり変わらない可能性があります。

本記事では、基本的な再帰の例として「階乗」の計算を実装してみます。

本記事の主題ではありませんが、「階乗」の計算のような大きな整数を扱う場合の注意点として、Mindの整数型は符号付３２ビット整数型となるため、その最大値を超えた大きな計算値には非対応となります。

# Mindプログラムソース

```mind:factorial.src
階乗を求めるとは  （値　→　階乗）
        値は　変数
    値に　入れ
    値が １　以下
    ならば １をつむ
    さもなければ 値から　１を　引いて　階乗を求め　値を　掛ける
    つぎに。

メインとは  （・　→　・）
    「10の階乗：」を　表示し　１０の　階乗を求めて　数値表示し　改行し
    「11の階乗：」を　表示し　１１の　階乗を求めて　数値表示し　改行し
    「12の階乗：」を　表示し　１２の　階乗を求めて　数値表示し　改行し
    「13の階乗：」を　表示し　１３の　階乗を求めて　数値表示し　改行すること。
```
# コンパイル結果

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind factorial file   

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta-7\bin\mindex.exe --> factorial.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind factorial file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> factorial.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind factorial file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> factorial.exe
```
# 実行結果
つづいて実行してみます。Mind9βの結果です。記述は割愛していますがMind7/8も同じです。

```cmd:
C:\developments\vscode\mind9\algorithm>factorial                         
10の階乗：3628800
11の階乗：39916800
12の階乗：479001600
13の階乗：1932053504
```
符号付３２ビット整数型で扱えるのは12の階乗までです。13の階乗の本来の値は6227020800となります。Mind8の場合はCランタイムを少し修正すると６４ビット整数型も扱えるようになります。[^1]　また下記の参考情報の３つ目の記事がMindユーザーの@ITvisionさんによる多倍長整数での階乗を計算した記事となります。[^2]



# 参考情報
この小技を使った記述例の記事です。

https://qiita.com/ITvision/items/c0bf3789a59df83d2d70

https://qiita.com/mylifewithviolin/items/f13c96aba7e9f80679c5

https://qiita.com/ITvision/items/51d3a1d82c5b83e0a5cd

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。

[^1]: ほぼ自分用の備忘録ですが、Mind8のCランタイム改修で倍精度整数の四則演算を対応した記事です。
[Mindで倍精度整数を使ってみる -Qiita](
https://qiita.com/mylifewithviolin/items/711a21e09990058c76bb)
 [Mind8で倍精度整数同士の四則演算＋αを実装してみる（64bit整数四則演算）-Qiita](
https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)
[^2]: Mindユーザーの@ITvisionさんによる構造体を使って多倍長整数を実現した記事
 [日本語プログラミング言語Mind８で十進数計算（符号付長整数計算）-Qiita](
https://qiita.com/ITvision/items/84e3d5b2065a323ec275)
