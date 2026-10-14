# はじめに
日本語プログラミング言語Mindの小技「文字列の定数配列」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載があります。
５ 配列
└定数配列
　└文字列の定数配列

>先の「定数配列」は数値定数専用であったが、文字列定数を配列にしたい場合にはこちらを用いる。
>
>構文＝
＜配列名＞は　文字列定数配列
　　　　＜文字列定数＞　＜文字列定数＞　・・・・・
　　　　＜文字列定数＞　＜文字列定数＞　・・・・・
　　　　・・・・・・・・・・・・・・・。
　定数のソースコード上の縦横並びは自由だが、結果的には１次元配列として生成される。



本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。


# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
Mindの小技「文字列の定数配列」は、Mindの定数による配列機能の中で、文字列定数の配列です。数値系の変数型の定数配列も別にありますが、それは本記事では扱いません。

配列は、同じ型のデータを連続して格納するデータ構造です。各データは「要素」と呼ばれ、インデックス（添字）を使って識別されます。この点は他のプログラミング言語と同じですが、インデックスの初期値は１から開始となる点は注意事項です。


# Mindプログラムソース
```mind:conststrarray.src
文字列定数配列１０桁は　文字列定数配列
「１あ３４５６７８９０」
「１２い４５６７８９２」
「１あ３う５６７８９３」
「１２３４え６７８９４」
「１２３４５お７８９５」。

メインとは　（・　→　・）
    「文字列定数配列１０桁」を　一行表示し
    文字列定数配列１０桁の　要素数で　回数指定し
        文字列定数配列１０桁（回数）を　一行表示し
    繰り返す。
```
文字列定数配列を宣言して、メインではそれらの要素数を使って回数指定ループを構成し、各要素のインデックスをMindの回数指定構文の「回数」（１から開始）で指定して表示しています。


# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind conststrarray file   

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> conststrarray.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind conststrarray file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> conststrarray.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind constantarray file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> conststrarray.exe
```

# 実行結果
つづいて実行してみます。

## Mind7/8/9β
Mind8の結果です。記述は割愛していますがMind7/9βも同じです。

```cmd:
C:\developments\vscode\mind9>conststrarray 
文字列定数配列１０桁
１あ３４５６７８９０
１２い４５６７８９２
１あ３う５６７８９３
１２３４え６７８９４
１２３４５お７８９５

C:\developments\vscode\mind9>
```



# 参考情報
この小技「文字列の定数配列」を使った記述例の記事は下記が該当します。

https://qiita.com/ITvision/items/a51170946b0ab8b0cfad

https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできます。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
