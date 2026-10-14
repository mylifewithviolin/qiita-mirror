# はじめに
日本語プログラミング言語Mindのバージョン９の言語拡張機能「評価」でTclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQL、SQLiteに対する共通処理単語を実装しております。今回はSQLite3でのトランザクション更新動作のコミットを検証します。本記事はマニュアル未記載な内容でMind９の本来のサポートレベルを超えた内容です。

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 9.03

SQLite version 3.43.2 2023-10-10 12:14:04

# Mind９の言語拡張機能「評価」とは
ご関心があるようでしならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQL、SQLiteでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLite3です。

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

## TCL用ODBCライブラリ
たいへんお手数ですが、ソースコード全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/12bd2c6ee6aea2d39ee8)をご参照ください。この範囲のコードはMind9依存です。Mind9非依存のC言語拡張のODBCライブラリと概ねMind単語の仕様を揃えています。

DB接続とDB接続の単語です。
>構文　＝　＜接続文字列＞を　DB接続する　→　＜真／偽＞
構文　＝　DB切断する　→　＜真／偽＞

SQL文とプレースホルダをセットする単語です。
>構文　＝　＜SQL文字列＞SQL文をセットし
構文　＝　＜プレースホルダ文字列＞と　＜数値＞で　整数のSQLパラメータをセット　→　・
構文　＝　＜プレースホルダ文字列＞と　＜文字列＞で　文字列のSQLパラメータをセット　→　・

SQL文を実行する単語で前者が結果セットが返るもの、後者は結果セットが返らないものです。
>構文　＝　結果セット取得　→　＜結果文字列＞　＜真／偽＞
構文　＝　SQLコマンド実行　→　＜真／偽＞

トランザクションを開始する単語です。
>構文　＝　トランザクションを開始　→　＜真／偽＞

トランザクションのスコープ（範囲）を指定する単語、脱出する単語です。
※「スコープ開始」が回数指定構文の等価定義です。「ここからトランザクション」が１を返します。
>構文　＝　ここからトランザクションの　スコープ開始
　　　　　※SQLコマンド実行の結果を成否に入れ　成否が偽　ならば
　　　　　　　スコープを抜け出す　→　・　
　　　　　※つぎに
　　ここまでスコープ

トランザクションをコミットまたはロールバックする単語です。
トランザクションスコープ内で各SQLの実行成否を変数に格納しておき、その実行成否変数を評価できるようにしておきます。

>構文　＝　コミットする　→　＜真／偽＞
構文　＝　ロールバックする　→　＜真／偽＞

## テスト用コード
UPDATE文を実行しておきます。ロールバック検証では開発言語IDの10が追加された状態でIDが同じINSERT文を実行していましたが、コミット検証では存在するIDに対してDELETE文を実行しておくことで、最後まで完走するようにしています。

日本語テーブル名、列名をすべてダブルクォーテーションで囲いました。これはPostgreSQLと同一となります。(接続文字列以外はすべてPostgreSQLと同一です。)

```mind:sqliteodbctcltrancmit.src
"odbctcl4.src"を　コンパイル。

datasourceSqliteは 文字列定数 「DRIVER={SQLite3 ODBC Driver};Database=c:\sqlite3\日本語プログラミング言語.db;」。

TCLのODBCでトランザクションするとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1,:id2)」
　　SELECT1は　　　文字列定数　「SELECT * FROM "言語名" AS LN  WHERE LN."言語ID" IN (:id1,:id2)」
　　SELECT2は　　　文字列定数　「SELECT * FROM "開発言語" AS DL WHERE DL."言語ID" IN (:id1,:id2)」
    SELECT3は　　　文字列定数　「SELECT * FROM "開発言語名" AS DLN WHERE DLN."開発言語ID" IN (:id1,:id2)」
　　INSERT1は　　　文字列定数　「INSERT INTO "開発言語名" ("開発言語ID","開発言語名") VALUES (:dgid,:dgnm)」
　　INSERT2は　　　文字列定数　「INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (:gid,:dgid)」
　　UPDATEは　　　文字列定数　「UPDATE "言語名" SET "よみがな" = :yomi WHERE "言語ID" = :id」
　　DELETE1は　　　文字列定数　「DELETE FROM "開発言語名" WHERE "開発言語ID" = :dgid」
    DELETE2は　　　文字列定数　「DELETE FROM "開発言語" WHERE "言語ID" = :gid AND "開発言語ID" = :dgid」
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
    結果をモニタし

    SELECT1で　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    SELECT2で　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    SELECT3で　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　10で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    トランザクションを開始し　成否に　入れ
    成否が　失敗に　等しい
    ならば　  エラーをモニタし
        　　　DB切断し　捨て　終わり
    つぎに

    ここからトランザクションの　スコープ開始
    
        UPDATEで　SQL文をセットし
        "yomi"と　"あたらしいよみがな"で　文字列のSQLパラメータをセットし
        "id"と　7で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        コマンドラインをモニタ

        DELETE1で　SQL文をセットし
        "dgid"と　10で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        コマンドラインをモニタ

        INSERT1で　SQL文をセットし
        "dgid"と　10で　整数のSQLパラメータをセットし
        "dgnm"と　"Tcl/Tk"で　文字列のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        コマンドラインをモニタ

        DELETE2で　SQL文をセットし
        "dgid"と　10で　整数のSQLパラメータをセットし
        "gid"と　1で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        コマンドラインをモニタ

        INSERT2で　SQL文をセットし
        "dgid"と　10で　整数のSQLパラメータをセットし
        "gid"と　1で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        コマンドラインをモニタ

　　ここまでスコープ

　　成否が　成功に　等しい
　　ならば
        コミットし　失敗に　等しい
        ならば　エラーをモニタし
                DB切断し　捨て　終わり
        つぎに
　　さもなければ
        コマンドラインをモニタし
        「SQL実行に失敗しました。ロールバックします。」を　表示し　改行し　改行し
        ロールバックし　失敗に　等しい
        ならば　エラーをモニタし
                DB切断し　捨て　終わり
        つぎに
　　つぎに


    SELECTで　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    DB切断し　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに。

※ テスト用
メインとは
    コンソールを開く

    TCLのODBCでトランザクションすること。

```

# お題のソースコードのMind9でのビルド
TclはMind9の場合Tcl/Tkを利用するために導入されているため、GUIアプリケーション用のライブラリguilibからのコンパイルが必須となります。
```cmd:
C:\developments\vscode\mind9\odbc>mind sqliteodbctcltrancmit guilib

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\Mind9\bin\mindexw.exe --> sqliteodbctcltrancmit.exe
```


# お題のMind9での実行の様子
それでは実行してみます。実際にはMindがコンソールウィンドウを開いています。

ロールバック検証時のSELECT結果は３テーブル結合クエリーでしたが。本検証ではトランザクション開始前の３テーブル単独の状態もクエリーしておきます。

```cmd:
set stmt [$db prepare  {SELECT LN."言語ID",LN."言語名",LN."よみがな",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言 語ID" WHERE LN."言語ID" IN (:id1,:id2)}]
set id1 1
set id2 7


1       Ｍｉｎｄ        まいんど        1       C
1       Ｍｉｎｄ        まいんど        8       Mind
1       Ｍｉｎｄ        まいんど        10      Tcl/Tk
7       Mind for Android        まいんど        3       Java

set stmt [$db prepare  {SELECT * FROM "言語名" AS LN  WHERE LN."言語ID" IN (:id1,:id2)}]
set id1 1
set id2 7


1       Ｍｉｎｄ        1985    まいんど
7       Mind for Android        2012    まいんど

set stmt [$db prepare  {SELECT * FROM "開発言語" AS DL WHERE DL."言語ID" IN (:id1,:id2)}]
set id1 1
set id2 7


1       1
1       8
1       10
7       3

set stmt [$db prepare  {SELECT * FROM "開発言語名" AS DLN WHERE DLN."開発言語ID" IN (:id1,:id2)}]
set id1 1
set id2 10


1       C
10      Tcl/Tk

set stmt [$db prepare  {UPDATE "言語名" SET "よみがな" = :yomi WHERE "言語ID" = :id}]
set yomi [encoding convertfrom utf-8 "あたらしいよみがな"]
set id 7
$stmt execute
$stmt close


set stmt [$db prepare  {DELETE FROM "開発言語名" WHERE "開発言語ID" = :dgid}]
set dgid 10
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO "開発言語名" ("開発言語ID","開発言語名") VALUES (:dgid,:dgnm)}]
set dgid 10
set dgnm [encoding convertfrom utf-8 "Tcl/Tk"]
$stmt execute
$stmt close


set stmt [$db prepare  {DELETE FROM "開発言語" WHERE "言語ID" = :gid AND "開発言語ID" = :dgid}]
set dgid 10
set gid 1
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (:gid,:dgid)}]
set dgid 10
set gid 1
$stmt execute
$stmt close

1       Ｍｉｎｄ        まいんど        1       C
1       Ｍｉｎｄ        まいんど        8       Mind
1       Ｍｉｎｄ        まいんど        10      Tcl/Tk
7       Mind for Android        B_?WD?Lj       3       Java
```
無事にコミットが成功しました。ただし、よみがなを変える日本語文字のUPDATE文の結果が文字化けしていることがわかります。これはtdbc::odbcとSQLiteのODBCドライバの組み合わせでプレースホルダのSQLBindParameterをうまくUTF-8として扱えていない可能性があります。tdbc::sqlite3のがこのあたりの対応状況はよさそうです。時間をみて後でそちらのパッケージを使ってみます。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
