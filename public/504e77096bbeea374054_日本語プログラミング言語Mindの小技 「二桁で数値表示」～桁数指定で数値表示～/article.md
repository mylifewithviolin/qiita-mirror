# はじめに
日本語プログラミング言語Mindの小技「二桁で数値表示」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載があります。
８ 入出力を行う単語
└コンソールへの出力
　└数値を表示


>　数値を表示するためには次の単語が利用できる。
>（整数向け）
>
>構文＝
＜数値＞を　　　　　　　数値表示　　　　→　・
＜数値＞を　　　　　　　二桁で数値表示　→　・
＜数値＞を　　　　　　　三桁で数値表示　→　・
＜数値＞を　　　　　　　四桁で数値表示　→　・
＜数値＞を　　　　　　　五桁で数値表示　→　・
＜数値＞を　＜桁数＞で　桁数指定で数値表示　→　・
 
本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。


# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
Mindの小技「二桁で数値表示」は、Mindの桁数指定で数値表示機能の一つです。単語内で指定された桁数で空白を前半に埋めて数値（整数）を表示します。５桁までが予約されています。それ以外はスタックに桁数を置いて「桁数指定で数値表示」を実行します。

# Mindプログラムソース
```mind:2digitnumber.src
整数配列は　１５の　変数。

整数配列の値を二桁表示するとは  （・　→　・）
    「要素番号　」を　表示し
    整数配列の　要素数で　回数指定し
        回数を　二桁で数値表示し　「　」を　表示し
    繰り返す
    改行する
    「配列の値　」を　表示し
    整数配列の　要素数で　回数指定し
        整数配列の　要素数から　回数を　引いて　５を　加えて　整数配列（回数）に　入れる
        整数配列（回数）を　二桁で数値表示し　「　」を　表示し
    繰り返す
    改行する。


メインとは  （・　→　・）
    整数配列の値を二桁表示する。
```

# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind 2digitnumber file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> 2digitnumber.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind 2digitnumber file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> 2digitnumber.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind 2digitnumber file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> 2digitnumber.exe
```

# 実行結果
つづいて実行してみます。

## Mind7/8/9β
Mind8の結果です。記述は割愛していますがMind7/9βも同じです。

```cmd:
C:\developments\vscode\mind9>2digitnumber
要素番号　 1　 2　 3　 4　 5　 6　 7　 8　 9　10　11　12　13　14　15　
配列の値　19　18　17　16　15　14　13　12　11　10　 9　 8　 7　 6　 5　

C:\developments\vscode\mind9>
```
いかがでしょうか？イメージがつかめれば幸いです。

# 参考情報
この小技「二桁で数値表示」を使った記述例は下記の記事が該当しています。

https://qiita.com/mylifewithviolin/items/52d7324860f845f628e3

https://qiita.com/mylifewithviolin/items/d8099ff94c05bb4ef3cf

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできます。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
