# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind９βのTclとのインターフェース単語を使い、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しております。（SQLコマンドテキストの内容としては各RDBによって異なっていきますが、処理単語としては同じとなります。）[前回](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)まででSQLServerでトランザクションを検証しましたので今回はMysqlを検証します。


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
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはMysqlです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード

## ライブラリ
たいへんお手数ですが、[前回の記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)をご参照ください。

今回は下記の単語にエンコードSHIFT-JIS(MS)を指定しています。後述する結果ではこの状態でもUPDATE文が動作しません。当初は前回状態で行って同様でしたので、エンコード指定追加してみています。

```mind:odebctcl.src
文字列のSQLパラメータをセットとは （プレースホルダ　文字列　→　・）
        プレースホルダは　文字列
        パラメータは　文字列
    パラメータに　入れ
    プレースホルダに　入れ
    「set 」を　コマンドトークン追加し
    プレースホルダを　コマンドトークンを追加し
    「 [encoding convertto cp932 」を　コマンドトークンを追加し
    パラメータを　コマンドラインに空白と囲みトークンを追加
    「 ] 」を　改行コマンドトークン追加すること。
```

## Mysql版テスト用コード
たいへんお手数ですが、全体は[前回の記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d.md)をご参照ください。
接続文字列だけdatasourceMysqlに変更しています。

```mind:testodebctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。

TCLのODBCでトランザクションするとは　（・　→　・）
    SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
    「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
    「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)」
　　INSERT1は　　　文字列定数　「INSERT INTO 開発言語名 (開発言語ID,開発言語名) VALUES (:dgid,:dgnm)」
　　INSERT2は　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (:gid,:dgid)」
　　UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id」
　　DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = :gid AND 開発言語ID = :id」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourceMysqlで　DB接続し　成否に　入れ
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
set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7


言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 7 言語名 {Mind for Android} よみがな まいんどふぉーあんどろいど


set stmt [$db prepare  {UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id}]
set yomi [encoding convertto cp932  {あたらしいよみがな} ]
set id 7
$stmt execute
$stmt close

SQL実行に失敗しました。ロールバックします。

言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 7 言語名 {Mind for Android} よみがな まいんどふぉーあんどろいど
```
最初のパラメータ化された結合クエリーは問題なく実行されましたが、次のUPDATE文でエラーが出ています。昨年C言語のODBCインターフェースを検証した際にMySql側の文字コードはCP932を指定していますので、接続文字列の末尾にはCP932を指定してDB日本語名、テーブル名日本語名、列名日本語名のSELECT文は正常に実行されています。
当初、文字列のバインドパラメータにエンコードは指定せずエラーとなったので、追加してみています。


エラーの詳細をモニタすると現状下記のとおりです。
```cmd:
コマンドの評価実行に失敗しました。[MySQL][ODBC 8.0(w) Driver][mysqld-8.3.0]Incorrect string value: '\x81\x91????...' for column '繧医∩縺後↑' at row 1
(executing the statement)
    while executing
"::oo::Obj33::Stmt::2 resultSetCreate ::oo::Obj36::ResultSet::1 ::oo::Obj33::Stmt::2"
    ("uplevel" body line 1)
    invoked from within
"uplevel 1  [list  [self] resultSetCreate  [namespace current]::ResultSet::[incr resultSetSeq]  [self] {*}$args]"
    (class "::tdbc::statement" method "execute" line 2)
    invoked from within
"$stmt execute "

set stmt [$db prepare  {UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id}]
set yomi [encoding convertto cp932  {あたらしいよみがな} ]
set id 7
$stmt execute
$stmt close
```
SHIFT-JIS（MS）で文字コード指定された  「{あたらしいよみがな}」の内容が文字として読み取れないというエラーのように読み取れます。中かっこをダブルクォーテーションに変更したりしてもいまのところ変化なしです。

ダメ元で下記のエンコード指定を試行錯誤的にUTF-8指定にしてみますと
```mind :odebctcl.src
-    「 [encoding convertto cp932 」を　コマンドトークンを追加し
+    「 [encoding convertto utf-8 」を　コマンドトークンを追加し
```

UPDATE文は動作して、後続のINSERT文２つも正常動作してトランザクションはコミットしますが、最初のUPDATE文のよみがなの更新内容が文字化けしますね。よみがな列の文字コードはCP932指定です。

```cmd:
set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7


言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 7 言語名 {Mind for Android} よみがな まいんどふぉーあんどろいど


set stmt [$db prepare  {UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id}]
set yomi [encoding convertto utf-8  {あたらしいよみがな} ]
set id 7
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO 開発言語名 (開発言語ID,開発言語名) VALUES (:dgid,:dgnm)}]
set dgid 10
set dgnm [encoding convertto utf-8  {Tcl/Tk} ]
$stmt execute
$stmt close


set stmt [$db prepare  {INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (:gid,:dgid)}]
set dgid 10
set gid 1
$stmt execute
$stmt close

言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 1 言語名 Mind よみがな まいんど 開発言語ID 10 開発言語名 Tcl/Tk
言語ID 7 言語名 {Mind for Android} よみがな ???????????????????????????
```

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。PostgreSQLはSQLテキスト内のWHERE句の日本語列名にダブルクオーテーション括りが必要でしたので、Mysqlより手がかかるかもしれません。
