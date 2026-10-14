# はじめに
日本語プログラミング言語Mindのバージョン９の言語拡張機能「評価」でTclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQL、SQLiteに対する共通処理単語を実装しております。今回はPostgreSQLでの動作を検証します。[Mind9ベータ版で実装](https://qiita.com/mylifewithviolin/items/ce0f273d595b48f93de1)のリリース版での追検証となります。本記事はマニュアル未記載な内容でMind９の本来のサポートレベルを超えた内容です。

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 9.03

postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86　odebcドライバは32bit版です。

# Mind９の言語拡張機能「評価」とは
ご関心があるようでしたならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQL、SQLiteでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはPostgreSQLです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
前記ODBC接続用パッケージを使ったMind記述のodbctclライブラリを使用します。ODBC接続用TclランタイムはMind9パッケージに含まれていますが、当ライブラリはユーザー作成ライブラリです。また、TclはMind9の場合Tcl/Tkを利用するために導入されているため、GUIライブラリに依存する関係となります。

## TCL用ODBCライブラリ
たいへんお手数ですが、ソースコード全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/12bd2c6ee6aea2d39ee8)をご参照ください。この範囲のコードはMind9依存です。Mind9非依存のC言語拡張のODBCライブラリと概ねMind単語の仕様を揃えています。

DB接続とDB接続の単語です。
>構文　＝　＜接続文字列＞を　DB接続する　→　＜真／偽＞
構文　＝　DB切断する　→　＜真／偽＞

SQL文とプレースホルダをセットする単語です。
>構文　＝　＜SQL文字列＞SQL文をセットし
構文　＝　＜プレースホルダ文字列＞と　＜数値＞で　整数のSQLパラメータをセット　→　・
構文　＝　＜プレースホルダ文字列＞と　＜文字列＞で　文字列のSQLパラメータをセット　→　・

SQL文を実行する単語で前者は結果セットが返るもの、後者は結果セットが返らないものです。
>構文　＝　結果セット取得　→　＜結果文字列＞　＜真／偽＞
構文　＝　SQLコマンド実行　→　＜真／偽＞

## 結果セットを構造体に格納するコード
こちらのコードは型のキャストは行っていない簡易コードなので、各DB共通コードとなっています。[こちらの記事](https://qiita.com/mylifewithviolin/items/ce0f273d595b48f93de1)をご参照ください。

この範囲のコードはMind7/8/9で動作します。

## PostgreSQL版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。PostgreSQLの場合は、日本語テーブル名、列名をすべてダブルクォーテーションで囲いました。プレースホルダはSQLServerと共通でした。

```mind:pgsqlodbctcl.src
"odbctcl3.src"を　コンパイル。
"wordsSeparate.src"を　コンパイル。
"viewmodel2.src"を　コンパイル。

datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=*******;」。

TCLのODBCで照会するとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1,:id2)」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourcePgsqlで　DB接続し　成否に　入れ
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
C:\developments\vscode\mind9\odbc>mind pgsqlodbctcl guilib

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\Mind9\bin\mindexw.exe --> pgsqlodbctcl.exe
```

# お題のMind9での実行の様子
それでは実行してみます。実際にはMindがコンソールウィンドウを開いています。

```cmd:
set stmt [$db prepare  {SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1,:id2)}]
set id1 1
set id2 7


結果をVIEW開発言語に格納する開始
1       Mind    まいんど        1985    8       Mind
1       Mind    まいんど        1985    1       C
1       Mind    まいんど        1985    10      Tcl/Tk
7       MindforAndroid  まいんどふぉーあんどろいど      2012    3       Java

結果の行数：4
1|Mind|まいんど|1985|8|Mind
1|Mind|まいんど|1985|1|C
1|Mind|まいんど|1985|10|Tcl/Tk
7|MindforAndroid|まいんどふぉーあんどろいど|2012|3|Java
```
無事に動作しました:tada:
「結果をVIEW開発言語に格納する開始」という行出力の後の４行が、Tclが返している結果セットの文字列をそのまま出力したものです。

「結果の行数：4」の後が、結果セットの文字列を構造体配列に格納してから、それをパイプ区切りでコンソール出力したものです。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。普段はJavaの場合はSpringBootといっしょにmybatisを、C#の場合はEntityFrameworkをよく使います。
