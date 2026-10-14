# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind９βのTclとのインターフェース単語を使い、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しております。（SQLコマンドテキストの内容としては各RDBによって異なっていきますが、処理単語としては同じとなります。）[前々回](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)まででSQLServerでトランザクションを、前回はMysqlを検証しましたので今回はPostgreSQLを検証します。

# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6

SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32
postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86

# ９βの言語拡張機能「評価」とは
ご関心があるようでしならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはPostgreSQLです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード

## ライブラリ
たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)をご参照ください。

今回は文字列パラメータセットの単語にエンコードを指定していません。SQLServerと同じ状態で動作しました。

## PostgreSQL版テスト用コード
たいへんお手数ですが、全体は[前回の記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)をご参照ください。
接続文字列をdatasourcePgsqlに変更して、日本語テーブル名、列名をすべてダブルクォーテーションで囲いました。これはめんどうなのでポスグレで日本語テーブル名列名は使わないという遠因になりそうです。

```mind:testodebctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。

TCLのODBCでトランザクションするとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (:id1,:id2)」
　　INSERT1は　　　文字列定数　「INSERT INTO "開発言語名" ("開発言語ID","開発言語名") VALUES (:dgid,:dgnm)」
　　INSERT2は　　　文字列定数　「INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (:gid,:dgid)」
　　UPDATEは　　　文字列定数　「UPDATE "言語名" SET "よみがな" = :yomi WHERE "言語ID" = :id」
　　DELETEは　　　文字列定数　「DELETE "開発言語" WHERE "言語ID" = :gid AND "開発言語ID" = :id」
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
※～略～

```

# お題のMind9βでの実行の様子
それでは実行してみます。

```cmd:
set stmt [$db prepare  {SELECT LN."言語ID",LN."言語名",LN."よみがな",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言 語ID" WHERE LN."言語ID" IN (:id1,:id2)}]
set id1 1
set id2 7


言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 7 言語名 {Mind for Android} よみがな あたらしいよみがな 開発言語ID 3 開発言語名 Java


set stmt [$db prepare  {UPDATE "言語名" SET "よみがな" = :yomi WHERE "言語ID" = :id}]
set yomi {あたらしいよみがな}
set id 7
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO "開発言語名" ("開発言語ID","開発言語名") VALUES (:dgid,:dgnm)}]
set dgid 10
set dgnm {Tcl/Tk}
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (:gid,:dgid)}]
set dgid 10
set gid 1
$stmt execute
$stmt close

言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 10 開発言語名 Tcl/Tk
言語ID 7 言語名 {Mind for Android} よみがな あたらしいよみがな 開発言語ID 3 開発言語名 Java
```
無事に動作しました。SQLテキストでテーブル名、列名をダブルクォーテーションで囲う手間を気にしなければ、SQLServerと同じように使えそうです。ロールバックも正常動作しています。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。MysqlはC言語インターフェースのODBCのときの由来で接続情報にコードページを指定していましたが、逆にない方がTclの場合は動きそうな気もしてきましたので、次回接続文字列からcp938の指定とってみて検証してみます。ただしSELECT系はそれで正常動作していたので、とってはダメかもしれません。
