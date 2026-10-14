# はじめに
今年の1月にMind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、[前回の記事](https://qiita.com/mylifewithviolin/items/69f51b477dc02f46daef)からMind関係者の中では以前から話題となっていた[Tclのデータベースアクセス機能](https://qiita.com/ITvision/items/19b3749e015aabd0c331)について検討してみました。TclのODBCデータベース操作ライブラリやTcl自体についてほぼ知識がないので手探り状態からのスタートです。

昨年2024年のいまごろは
[MindでデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/47edb441d94d2aa7f0a5)というような記事を投稿していました。

これはマイクロソフトのODBC規格のインターフェースをC/C++で実装された公開サンプルをCで調整実装してMind用のインターフェースとしてDLL化した事案でした。

他に下記のようなデータベースについても接続検証しておりましたので、今回これらの環境も引き続き利用いたします。
[MindでデータベースMySQL8.3 クエリーしてみる（ステップ1.5）結果セット受け取り](
https://qiita.com/mylifewithviolin/items/61db83b43d18e5d0a9fa)
[MindでデータベースPostgreSQL16.1 クエリーしてみる（ステップ1.6）結果セット文字列返し書式解除](
https://qiita.com/mylifewithviolin/items/987a8e6edfbea394e42d)

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

https://www.tcl.tk/man/tcl9.0/TdbcodbcCmd/index.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成していました。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード

今回は各データベースへの接続情報はSQL文はテストプログラムソース側に移して、ライブラリ側はよりライブラリっぽくしました。

## ライブラリ
```mind:odebctcl.src
コマンドトークン設定は　コマンドラインにトークンを設定と　等価。
コマンドトークン追加は　コマンドラインにトークンを追加と　等価。

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
    「puts $stdout [dict get $row]」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    「$db close」を　改行コマンドトークン追加し
    「close $stdout」を　コマンドトークン追加し
     コマンドラインを　評価した値を　返すこと。 

結果をモニタするとは　（結果文字列　→　・）
    表示し　改行すること。

コマンドラインをモニタするとは　（・　→　・）
    改行し
    コマンドラインを　表示し　改行し　改行すること。

```

## テスト用コード
```mind:testodbctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=mind;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;」。
SELECT1は　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」。
SELECT2は　　　文字列定数　「SELECT * FROM 言語名 言語名 WHERE "言語ID" IN (1,7)」。

TCLのODBCでクエリするとは　（・　→　・）

    ODBCライブラリをロードし
    datasourceSqlsvrと　SELECT1で　SQL実行し　結果をモニタし
    コマンドラインをモニタし
    datasourceMySqlと　SELECT1で　SQL実行し　結果をモニタし
    コマンドラインをモニタし
    datasourcePgsqlと　SELECT2で　SQL実行し　結果をモニタし
    コマンドラインをモニタすること。

※ テスト用
メインとは
    コンソールを開く
    
    TCLのODBCでクエリすること。
```

SQLServerとMysqlのSELECT文はいまのところ共通ですが、PostgreSQLは日本語列名をダブルクォーテーションで囲わないと「言語id」になってしまうため囲っています。


# お題のソースコードのMind9βでのビルド

```cmd:
C:\developments\vscode\mind9>mind testodbctcl guilib 

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\mind9-beta\bin\mindexw.exe --> testodbctcl.exe
```
ビルド成功しました！:tada:

# お題のMind9βでの実行の様子
コンソールウィンドウを展開していますので、CUI出力を以下に示します。
前半は実行した結果、後半はMindのTcl評価へ与えたTclスクリプトの確認用出力です。これを３つのデータベースに対して実行しました。

```cmd:
言語ID 1 言語名 Ｍｉｎｄ 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいｄ


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close
$db close
close $stdout

言語ID 1 言語名 Mind 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいど


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close
$db close
close $stdout

言語ID 1 言語名 Mind 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいど


set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM 言語名 言語名 WHERE "言語ID" IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close
$db close
close $stdout
```
動きました:tada:


次回はもう少し複雑な結合クエリーやパラメータ化、結果の項目切り出し方法などを検討してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。まだほんのさわりの部分ですが、今年で生誕４０周年を迎える日本語プログラミング言語Mind、ついに新バージョンがベールをぬぎはじめます！
