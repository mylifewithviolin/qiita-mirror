# はじめに
日本語プログラミング言語Mindのバージョン９の言語拡張機能「評価」でTclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しております。今回はSQLite3での動作を検証します。本記事はマニュアル未記載な内容でMind９の本来のサポートレベルを超えた内容です。

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 9.03

SQLite version 3.43.2 2023-10-10 12:14:04


# Mind９の言語拡張機能「評価」とは
ご関心があるようでしたならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。これによりSQLServer、Mysql、PostgreSQL、SQLite3などをある程度共通のライブラリで操作することができます。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLite3です。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

SQLite3のデータベース作成の手順は[こちらの記事](https://qiita.com/mylifewithviolin/items/55933ef08fb62d292204)をご参照ください。

# SQLite

SQLiteはODBCドライバーに付属のものを使用しています。上記の記事では64bit版ドライバーをダウンロードしていましたが、今回は32bit版です。

```
C:\Program Files (x86)\SQLite ODBC Driver>sqlite3
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite>
```

http://www.ch-werner.de/sqliteodbc/

Current version
sqliteodbc.exe　←こちらをダウンロード
sqliteodbc_w64.exe

# お題のソースコード

## ライブラリ
tclDatabaseのtdbc:odbcというODBC接続用パッケージを使ったMind記述のodbctclライブラリの一部です。

```mind:odbctcl3.src

結果を取得とは 	　（・　→　結果文字列 1:成功/0:失敗）
    「set result [$stmt execute]」を　改行コマンドトークン設定し
    「set outputList {}」を　改行コマンドトークン追加し
    「$result foreach row {」を　改行コマンドトークン追加し
    「set fields [dict values $row]」を　改行コマンドトークン追加し
    「set line [join $fields "\t"]」を　改行コマンドトークン追加し
    「lappend outputList $line」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    「return [join $outputList "\t\n"]」を　改行コマンドトークン追加し
    ※コマンドラインをモニタ
    コマンドラインを　評価した値０すること。 
```

たいへんお手数ですが、「結果を取得」の定義部以外のソースコード全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/12bd2c6ee6aea2d39ee8)をご参照ください。この範囲のコードはMind9依存です。

## 結果セットを構造体に格納するコード
たいへんお手数ですが、ソースコード全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/1dd3a8091a6524adfe3c)をご参照ください。
この範囲のコードはMind7/8/9で動作します。

## SQLite3版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。tclDatabaseのtdbc:odbcのプレースホルダはODBCネィティブの「？,？・・・」ではくSQLServerなどと同様「:id1,:id2・・・」となります。
また、日本語名のテーブル名、列名はダブルクォーテーションで囲ます。この点はODBCネィティブと同じです。

```mind:sqliteodbctcl.src
"odbctcl3.src"を　コンパイル。
"wordsSeparate.src"を　コンパイル。
"viewmodel2.src"を　コンパイル。

datasourceSqliteは 文字列定数 「DRIVER={SQLite3 ODBC Driver};Database=c:\sqlite3\日本語プログラミング言語.db;」。

TCLのODBCで照会するとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1, :id2)」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourceSqliteで　DB接続し　成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし　終わり
    つぎに

    SELECTで　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
 
    結果をVIEW開発言語に格納し
    VIEW開発言語を出力し

    DB切断し　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに。

※ テスト用
メインとは
    コンソールを開く

    TCLのODBCで照会すること。
```


# お題のソースコードのMind9でのビルド
TclはMind9の場合Tcl/Tkを利用するために導入されているため、ＧＵＩアプリケーション用のライブラリからのコンパイルが必要となります。
```cmd:
C:\developments\vscode\mind9\odbc>mind sqliteodbctcl guilib

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\Mind9\bin\mindexw.exe --> sqliteodbctcl.exe
```

# お題のMind9での実行の様子
それでは実行してみます。
```cmd:
set stmt [$db prepare  {SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1, :id2)}]
set id1 1
set id2 7


結果をVIEW開発言語に格納する開始
1       Ｍｉｎｄ        まいんど        1985    1       C
1       Ｍｉｎｄ        まいんど        1985    8       Mind
1       Ｍｉｎｄ        まいんど        1985    10      Tcl/Tk
7       Mind for Android        まいんど        2012    3       Java

結果の行数：4
1|Ｍｉｎｄ|まいんど|1985|1|C
1|Ｍｉｎｄ|まいんど|1985|8|Mind
1|Ｍｉｎｄ|まいんど|1985|10|Tcl/Tk
7|Mind for Android|まいんど|2012|3|Java

```
無事に動作しました。
「結果をVIEW開発言語に格納する開始」という出力の後、「結果の行数：4」までの間がTclが返している結果セットの文字列をそのまま出力したものです。
「結果の行数：4」の後が、結果セットの文字列を構造体配列に格納してから、それをパイプ区切りでコンソール出力したものです。

実際には下記のコードでMindがコンソールウィンドウを開いています。
```mind:sqliteodbctcl.src
メインとは
    コンソールを開く
```
![tclodbcsqlite.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/1e04c004-3533-4c96-aca1-33db1034f09f.jpeg)


上記のテキスト出力は上図のCUI出力を示したものとなります。

今回はSELECTの結果でしたが、INSERTやUPDATE、DELETEも、漸次リリース版で追検証して参ります。

# 参考情報
日本語プログラミング言語MindのC言語DLL拡張単語odbcライブラリでSQLite３の接続を検証した記事です。こちらは以前のバージョンのMindでも動作し、コンソールアプリとして実装できますのでWebアプリのバックエンドとして利用可能です。

https://qiita.com/mylifewithviolin/items/e701fda39574ed0778ae

C言語DLL拡張単語odbcライブラリの場合では戻ってくる文字列の文字コード変換が必要でした。SQLiteはUTF-8で文字コード固定です。

https://qiita.com/mylifewithviolin/items/97b8ca5b68373e300405

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。普段はJavaの場合はSpringBootといっしょにmybatisを、C#の場合はEntityFrameworkをよく使います。
