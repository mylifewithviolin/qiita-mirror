# はじめに
日本語プログラミング言語Mindの小技「論理演算」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載があります。
６ 数値演算
├１つの値を受け取り、１つの値を返すもの
└２つの値を受け取り、１つの値を返すもの


「NOT(否定)」は「１つの値を受け取り、１つの値を返すもの」の中に記載があります。

>構文＝＜数値＞の　ＮＯＴ　　　　　→　＜数値＞　　　A → Aの全ビット反転

「AND(論理積)」「OR(論理和)」「XOR(排他的論理和)」は「２つの値を受け取り、１つの値を返すもの」の中に記載があります。

>　　　＜数値１＞と　　＜数値２＞を　ＡＮＤ　　→　＜数値＞　　→ A & B
構文＝＜数値１＞と　　＜数値２＞を　ＯＲ　　　→　＜数値＞　　→ A | B
　　　＜数値１＞と　　＜数値２＞を　ＸＯＲ　　→　＜数値＞　　→ A xor B


本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。

# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
「論理演算」は日本語プログラミング言語Mindの基本的な論理演算機能です。他のプログラミング言語との違いは、演算子と演算対象の変数（や式）の置き方（書き方）にあります。

**一般的なプログラミング言語の記法**

**AND(論理積)**

C = A && B
C = A And B

**OR(論理和)**

C = A || B
C = A Or B

**XOR(排他的論理和)**

C = A ^ B
C = A Xor B

**NOT(否定)**

C = !A
C = ~A　（ビット反転）
C = Not A


**Mindの記法(日本語表現記述）**

**AND(論理積)**

Aと Bの　ANDを　Cに　入れる

**OR(論理和)**

Aと Bの　ORを　Cに　入れる

**XOR(排他的論理和)**

Aと Bの　XORを　Cに　入れる

**NOT(否定)**

Aの　NOTを　Cに　入れる

※MindのNOTはビット反転です。


日本語表現の場合は上記のように後置法（逆ポーランド記法）となります。
以下、さっそくサンプルソースコードで実際の演算結果を出力してみます。


# Mindプログラムソース

```mind:logicaloperation.src
ダブル表示改行とは  （変数　→　・）
    ダブル表示し　改行すること。

メインとは  （・　→　・） 
        Aは　変数
        Bは　変数
        Cは　変数

Aに　１を　入れる
Bに　０を　入れる
「A：」を　表示し　Aを　ダブル表示改行し
「B：」を　表示し　Bを　ダブル表示改行し　改行し

※Mindの記法(日本語表現記述）
※**AND(論理積)**
「AND(論理積)」を　一行表示し

Aと Bの　ANDを　Cに　入れる
「C：」を　表示し　Cを　ダブル表示改行し　改行し

※**OR(論理和)**
「OR(論理和)」を　一行表示し

Aと Bの　ORを　Cに　入れる
「C：」を　表示し　Cを　ダブル表示改行し　改行し


※**XOR(排他的論理和)**
「XOR(排他的論理和)」を　一行表示し

Aと Bの　XORを　Cに　入れる
「C：」を　表示し　Cを　ダブル表示改行し　改行し


※**NOT(否定)**
※MindのNOTはビット反転です。
「NOT(否定)」を　一行表示し

Aの　NOTを　Cに　入れる
「C：」を　表示し　Cを　ダブル表示改行。
```


# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind logicaloperation file   

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> logicaloperation.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind logicaloperation file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> logicaloperation.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind logicaloperation file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> logicaloperation.exe
```
# 実行結果
つづいて実行してみます。
Mind8の結果です。記述は割愛していますがMind7/9βも同じです。

```cmd:
C:\developments\vscode\mind9>logicaloperation
A：00000001
B：00000000

AND(論理積)
C：00000000

OR(論理和)
C：00000001

XOR(排他的論理和)
C：00000001

NOT(否定)
C：FFFFFFFE

C:\developments\vscode\mind9>
```
いかがでしょうか？イメージつかめていただければ幸いです。0と1が８つ並んでいると８ビットを表示しているように見えますが、これは４ビットづつ３２ビット変数を表示しています。


# 参考情報
この小技「論理演算」を使った記述例の記事は下記が該当します。

https://qiita.com/mylifewithviolin/items/0672c3fa0352ec87be69


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできますよ。


面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
