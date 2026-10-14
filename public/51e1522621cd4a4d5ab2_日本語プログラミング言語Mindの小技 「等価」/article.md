# はじめに
日本語プログラミング言語Mindの小技「等価」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語マニュアルの記述はありません。または発見できませんでした。つまり裏技？

失礼しました。Mind8プログラミングマニュアルに記載がありました。
２ プログラム表記の基本
└等価定義

>ある単語に別の名前を付ける機能である。
>
>構文＝
>＜新名称＞は ＜旧名称＞と 等価。

本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。

# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
「等価」はMindの定義済単語を別名に置き換える機能です。サンプルを使って
説明します。

# Mindプログラムソース

```mind:touka.src
文字列コンソール出力して改行は　　一行表示と　　等価。

メインは　　
「小技の等価とは単語名を変えること」を　一行表示
「小技の等価とは単語名を変えること」を　文字列コンソール出力して改行。

```

# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind touka file   

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> touka.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind touka file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> touka.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind touka file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:XXXXXXX
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> touka.exe
```
# 実行結果
つづいて実行してみます。Mind９βの結果です。記述は割愛していますがMind7/8も同じです。

```cmd:
C:\developments\vscode\mind9>touka
小技の等価とは単語名を変えること
小技の等価とは単語名を変えること
```

# 参考情報
この小技を使った記述例の記事です。

https://qiita.com/mylifewithviolin/items/3288336a9c346a429fee

https://qiita.com/mylifewithviolin/items/903a0a7c8aeea6ec3148

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は日本語プログラミング言語Mind生誕４０周年プロジェクトの一環です。興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスして、Mindコンパイラをダウンロードできますよ。[Mindプログラミングマニュアル（基本文法）](https://www.scripts-lab.co.jp/mind/ver8/doc/index.html)ページから気になるお題の構文を選んで、この記事のようにサンプル実装実行してQiitaにアウトプットしてみましょう！筆者はMind7/8/9βで検証しておりますが、もちろんMind8だけでもじゅうぶんです。またお題が既存記事とかぶるのはまったく問題ありません。同じお題でみなさまの多様斬新なサンプルをお待ちしております:grinning:
