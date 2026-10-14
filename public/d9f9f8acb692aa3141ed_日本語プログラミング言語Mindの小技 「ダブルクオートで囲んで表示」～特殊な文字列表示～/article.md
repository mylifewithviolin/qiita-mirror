# はじめに
日本語プログラミング言語Mindの小技「ダブルクオートで囲んで表示」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載があります。
８ 入出力を行う単語
└コンソールへの出力
　└文字列を表示


>　構文＝＜文字列＞を　　ダブルクオートで囲んで表示　→　・
>
>上記最後の「ダブルクオートで囲んで表示」は「表示」の代わりに使うもので、"あいう" のように、指定した文字列をダブルクオートで囲んで表示するものである。文字列両端にタブや空白などが含まれている場合に、これを使うとはっきり視認できるので、プログラムの動作確認に使うことも多い。
 
本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。


# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
Mindの小技「ダブルクオートで囲んで表示」は、Mindの特殊な文字列表示機能の一つです。指定した文字列をダブルクオートで囲んで表示します。

# Mindプログラムソース
```mind:lineread2.src
サンプル物理ファイルパスは　文字列定数　"c:\developments\vscode\mind9\sample.txt"。
サンプルファイルは　        ファイル。

メインとは　（・　→　・）
        行は　文字列
    サンプルファイルを　サンプル物理ファイルパスで　オープンし
    エラー？
    ならば　「サンプルファイルのオープンに失敗しました。（」を　表示し
    　　　　エラー文字列を　表示し　「）」を　一行表示し
            実行終わり
    つぎに
    
    「サンプルファイルをオープンしました。」を　一行表示し
    ここから
        サンプルファイルから　一行読み出し　行に　入れ
        データ終り？
        ならば　打ち切り
        つぎに
　　　　行を　ダブルクオートで囲んで表示し　改行し
    繰り返し

    サンプルファイルを　クローズし
    「サンプルファイルをクローズしました。」を　一行表示する。
```

# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind lineread2 file   

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> lineread2.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind lineread2 file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> lineread2.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind lineread2 file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> lineread2.exe
```

# 実行結果
つづいて実行してみます。
sample.txtは下記の内容です。

```cmd:
C:\developments\vscode\mind9>type sample.txt 
サンプルテキストファイルの１行目です。
C:\developments\vscode\mind9>
```

## Mind7/8/9β
Mind8の結果です。記述は割愛していますがMind7/9βも同じです。

```cmd:
C:\developments\vscode\mind9>lineread2
サンプルファイルをオープンしました。
"サンプルテキストファイルの１行目です。"
サンプルファイルをクローズしました。

C:\developments\vscode\mind9>
```
いかがでしょうか？イメージがつかめれば幸いです。

# 参考情報
この小技「ダブルクオートで囲んで表示」を使った記述例は下記の記事が該当しています。

https://qiita.com/mylifewithviolin/items/4ce004fa4db8c683d0f2

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできます。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
