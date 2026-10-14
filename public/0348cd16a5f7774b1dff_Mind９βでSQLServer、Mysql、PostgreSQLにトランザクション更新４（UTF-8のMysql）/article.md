# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind９βのTclとのインターフェース単語を使い、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しております。[こちらの記事](https://qiita.com/mylifewithviolin/items/55449e8abead929ec167)でCp932文字コードのMysqlを検証しましたが、いまいちうまくいかなかったので今回はUTF-8のMySqlで検証します。SQLServerとPostgreSQLはうまくいっています。


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

MySQLワークベンチからも文字コードをCp932(MSのSJIS)からUTF-8に変更してみましたが、いまいち確信がもてないのでCLIからも確認しました。

```cmd:
mysql> ALTER DATABASE 日本語プログラミング言語 CHARACTER SET utf8;
Query OK, 1 row affected, 1 warning (0.02 sec)

mysql> ALTER TABLE 言語名 CONVERT TO CHARACTER SET utf8;
Query OK, 0 rows affected, 1 warning (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 1
--------------
C:\Program Files\MySQL\MySQL Server 8.3\bin\mysql.exe  Ver 8.3.0 for Win64 on x86_64 (MySQL Community Server - GPL)

Connection id:          21
Current database:       日本語プログラミング言語
Current user:           root@localhost
SSL:                    Cipher in use is TLS_AES_128_GCM_SHA256
Using delimiter:        ;
Server version:         8.3.0 MySQL Community Server - GPL
Protocol version:       10
Connection:             localhost via TCP/IP
Server characterset:    utf8mb4
Db     characterset:    utf8mb3
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
TCP port:               3306
Binary data as:         Hexadecimal
Uptime:                 23 hours 12 min 0 sec

Threads: 4  Questions: 670  Slow queries: 0  Opens: 266  Flush tables: 3  Open tables: 156  Queries per second avg: 0.008
--------------

mysql>  show variables like 'char%';
+--------------------------+---------------------------------------------------------+
| Variable_name            | Value                                                   |
+--------------------------+---------------------------------------------------------+
| character_set_client     | utf8mb4                                                 |
| character_set_connection | utf8mb4                                                 |
| character_set_database   | utf8mb3                                                 |
| character_set_filesystem | binary                                                  |
| character_set_results    | utf8mb4                                                 |
| character_set_server     | utf8mb4                                                 |
| character_set_system     | utf8mb3                                                 |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 8.3\share\charsets\ |
+--------------------------+---------------------------------------------------------+
8 rows in set, 1 warning (0.01 sec)

mysql> SELECT COLUMN_NAME, CHARACTER_SET_NAME, COLLATION_NAME
    -> FROM INFORMATION_SCHEMA.COLUMNS
    -> WHERE TABLE_SCHEMA = '日本語プログラミング言語'
    -> AND TABLE_NAME = '言語名';
+--------------+--------------------+--------------------+
| COLUMN_NAME  | CHARACTER_SET_NAME | COLLATION_NAME     |
+--------------+--------------------+--------------------+
| よみがな     | utf8mb3            | utf8mb3_general_ci |
| 公開年       | NULL               | NULL               |
| 言語ID       | NULL               | NULL               |
| 言語名       | utf8mb3            | utf8mb3_general_ci |
+--------------+--------------------+--------------------+
4 rows in set (0.00 sec)
```
# お題のソースコード

## ライブラリ
たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)をご参照ください。

今回は下記の単語にエンコードUTF-8を指定しています。ここにエンコードを指定しない場合はUPDATE文が動作しません。

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
たいへんお手数ですが、全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/2cdd4e77d7f8ae0e1e3d)をご参照ください。

接続文字列datasourceMysqlから「charset=cp932」を削除しています。今回はトランザクション部分はUPDATE文だけとしています。SELECT文も簡単にしています。

```mind:testodebctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。

TCLのODBCでトランザクションするとは　（・　→　・）
    SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな FROM 言語名 AS LN 」続
    「WHERE LN.言語ID IN (:id1,:id2)」
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
        "yomi"と　"\u3042\u305F\u3089\u3057\u3044\u3088\u307F\u304C\u306A"で　文字列のSQLパラメータをセットし
        "id"と　7で　整数のSQLパラメータをセットし
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
    エラーをモニタし
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
「あたらしいよみがな」という文字列はUTF-8コード列としてみています。

# お題のMind9βでの実行の様子
それでは実行してみます。

```cmd:

set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな FROM 言語名 AS LN WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7


言語ID 1 言語名 Mind よみがな まいんど
言語ID 7 言語名 {Mind for Android} よみがな まいんどふぉーあんどろいど


set stmt [$db prepare  {UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id}]
set yomi [encoding convertto utf-8 "\u3042\u305F\u3089\u3057\u3044\u3088\u307F\u304C\u306A"]
set id 7
$stmt execute
$stmt close

言語ID 1 言語名 Mind よみがな まいんど
言語ID 7 言語名 {Mind for Android} よみがな ???????????????????????????
```
結果はCp932で接続していた場合と変わりありませんでした。

encoding convertto utf-8または
encoding convertfrom utf-8の指定は必須で、この指定がないとMySql側のドライバがパラメータの文字列を解釈できずエラーとなります。

指定した場合はエラーとはならないのですが、更新された文字が文字化けします。

encoding convertto utf-8の場合は「???????????????????????????」
encoding convertfrom utf-8の場合は「B_?WD?Lj」と表示されます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。MySQLで日本語が更新できないというのはよくある話ですが、今回はTclインタプリタが介在しているので、少し謎な状態となっています。直接TclインタプリタのCLIから実行してみたりする必要があるかもしれません。しばらく本件お休みとして頭を冷やします。
