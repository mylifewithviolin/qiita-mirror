# はじめに
今年の1月にMind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、[前回の記事](https://qiita.com/mylifewithviolin/items/6ff94130804c5ab42612)では、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに接続してみました。今回はその少し改良でエラー処理を追加しました。

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

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード

今回は「評価した値」ではなく、エラー結果を返す「評価した値０」を使用します。また、エラー情報の取得はTcl_GetValueを使った単語を使用します。

## ライブラリ
```mind:odebctcl.src
コマンドトークン設定は　コマンドラインにトークンを設定と　等価。
コマンドトークン追加は　コマンドラインにトークンを追加と　等価。
値を取得は             c_getvarと  等価。

接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　定数　2000バイト。

改行コマンドトークン設定とは　（トークン　→　・）
    コマンドトークン設定し
    「＆ＬＦ＆」を　コマンドトークン追加すること。

改行コマンドトークン追加とは　（トークン　→　・）
    コマンドトークン追加し
    「＆ＬＦ＆」を　コマンドトークン追加すること。

ODBCライブラリをロードとは　（・　→　・）
    "package require tdbc::odbc"を　評価すること。

SQL実行とは 	　（接続文字列 SQL文字列　→　結果文字列）
        connectStrは　文字列実体　長さ　接続文字列最大長
        commandStrは　文字列実体　長さ　SQL文字列最大長
        成否は　変数
    commandStrに　入れ
    connectStrに　入れ
    「set stdout [open "CONOUT$" "w"]」を　改行コマンドトークン設定し
    「fconfigure $stdout -buffering line」を　改行コマンドトークン追加し
    「set connectionString {」を　コマンドトークン追加し
    connectStrを　コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「set db [tdbc::odbc::connection create db $connectionString]」を　改行コマンドトークン追加し
    「set stmt [$db prepare {」を　コマンドトークン追加し
    commandStrを　コマンドトークンを追加し
    「}]」を　改行コマンドトークン追加し
    「set result [$stmt execute]」を　改行コマンドトークン追加し
    「$result foreach row {」を　改行コマンドトークン追加し
    「puts $stdout [dict get $row ]」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    「$db close」を　改行コマンドトークン追加し
    「close $stdout」を　コマンドトークン追加し
     コマンドラインを　評価した値０を　成否に　入れ
     成否が　０に　等しい
        ならば　「実行に失敗しました。」を　表示し　
                「errorInfo」と　10で　値を取得して　表示し　改行し
        つぎに
     返すこと。 

結果をモニタするとは　（結果文字列　→　・）
    表示し　改行すること。

コマンドラインをモニタするとは　（・　→　・）
    改行し
    コマンドラインを　表示し　改行し　改行すること。

```

## テスト用コード
[前回の記事](https://qiita.com/mylifewithviolin/items/6ff94130804c5ab42612)と同じです。

SQLServerとMysqlのSELECT文はいまのところ共通ですが、PostgreSQLは日本語列名をダブルクォーテーションで囲わないと「言語id」になってしまうため囲っています。
TclスクリプトのモニタはＳＱＬを実行した結果の後に出力しています。


# お題のソースコードのMind9βでのビルド

```cmd:
C:\developments\vscode\mind9>mind testodbctcl guilib 

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\mind9-beta\bin\mindexw.exe --> testodbctcl.exe
```
ビルド成功です！:tada:

# お題のMind9βでの実行の様子
コンソールウィンドウを展開していますので、CUI出力を以下に示します。
前半は実行した結果、後半はMindのTcl評価へ与えたTclスクリプトの確認用出力です。これを３つのデータベースに対して実行しました。

前記掲載状態のコードは正常スクリプトのため、正常実行されます。その結果は[前回の記事](https://qiita.com/mylifewithviolin/items/6ff94130804c5ab42612)をご参照ください。

次にTclスクリプトでエラーを起こすため、下記のコードの「$row」の後に存在しない列名「xxx」を追記して実行します。

```mind:odebctcl.src
    「puts $stdout [dict get $row xxx]」を　改行コマンドトークン追加し
```
スクリプト部分はリテラル書きなのでいったんビルドしなおして実行します。

```cmd:
実行に失敗しました。key "xxx" not known in dictionary
    while executing
"dict get $row xxx"
    ("uplevel" body line 2)
    invoked from within
"uplevel 1 [lindex $args 1]"
    (class "::tdbc::resultset" method "foreach" line 40)
    invoked from within
"$result foreach row {
puts $stdout [dict get $row xxx]
}"


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row xxx]
}
$result close
$stmt close
$db close
close $stdout

実行に失敗しました。can't create object "db": command already exists with that name
    while executing
"tdbc::odbc::connection create db $connectionString"
    invoked from within
"set db [tdbc::odbc::connection create db $connectionString]"


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言 語;UID=root;PWD=mind;charset=cp932}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row xxx]
}
$result close
$stmt close
$db close
close $stdout

実行に失敗しました。can't create object "db": command already exists with that name
    while executing
"tdbc::odbc::connection create db $connectionString"
    invoked from within
"set db [tdbc::odbc::connection create db $connectionString]"


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 言語名 WHERE "言語ID" IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row xxx]
}
$result close
$stmt close
$db close
close $stdout
```
エラー内容無事に取得できました:tada:
2回目以降のエラー内容が異なっているのは、1回目の処理が失敗したタイミングがDB接続開通した後なので、クローズ処理が実行されず、同じ接続識別子のdbでオープンしようとしたのでここでエラーとなっていることがわかります。このあたりはまだ試作状態でスクリプトを一本書きしていますので、次回から分割実行に進行します。


エラー判定ができるようになったので、次回は結合クエリより先にトランザクションの記述方法などを検討してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。まだほんのさわりの部分ですが、今年で生誕４０周年を迎える日本語プログラミング言語Mind、ついに新バージョンがベールをぬぎはじめます！
