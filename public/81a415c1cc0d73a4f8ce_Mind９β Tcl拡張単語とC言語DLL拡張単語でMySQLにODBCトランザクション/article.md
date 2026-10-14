# はじめに
Mind９βを開発元@killyさんの御厚意によりご提供いただきましたので、Mind９βのTcl拡張単語でTclのOdbc接続をSQLServer、MySql、PostgreSQLで評価し、また従来のMind7/8用に実装したC言語DLL拡張単語のodbc接続が動作することをSQLServerとPostgreSQLで確認しました。


今回はTcl評価時と同じSQLテキストを使ってC言語でのOdbc接続をMySQLに対して行ってみます。Tclの場合はUPDATE文の更新文字列をプレースホルダに設定するところでうまくいっておりませんでした。この挙動がなにに由来するものなのかを切り分ける意図もあってC言語拡張単語でも挙動を見てみたいというのがこの一連の記事の目的の１つでもあります。

# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022

MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32

下記のRDBにも対応はしていますが、今回検証環境はMySQLです。
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86


# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはMySQLです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
### ODBCライブラリ
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## Mind
### ODBCライブラリ
Mind側のODBCライブラリのソースコードはお手数ですが[こちらの記事](https://qiita.com/mylifewithviolin/items/21fa8a6e7531c7d67196)をご参照ください。

### MySQL版テスト用コード
書き味はPostgreSQL版と同じですがPostgreSQLのSQL文では日本語項目名をダブルクォーテーションで囲いましたので、MySQLはその必要がないのでその点が異なっています。、(C言語のODBCのプレースホルダーは「？」で動作するのでSQL文の内容はTcl版のMySQL版とそこ以外が同じ）

```mind:testmysqlodbcc.src
"odbcc"を　コンパイルする。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=mind;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;」。


メインとは

	※SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」
    　　SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
    「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
    「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」
　　INSERT1は　　　文字列定数　「INSERT INTO 開発言語名 (開発言語ID,開発言語名) VALUES (?,?)」
　　INSERT2は　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
　　UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
　　DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」
	成否は　		変数

	API初期処理しておき　成功に　等しい　でなければ　終わり　つぎに

	datasourceMysqlで　DB接続し　成功に　等しい　でなければ　終わり　つぎに


		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し 結果セットを表示する

		トランザクションを開始し

        ここからトランザクションの　スコープ開始

            UPDATEで　SQL文をセットし
            「あたらしいよみがな」で　文字列のSQLパラメータをセットし
            7で　整数のSQLパラメータをセットし
            SQLコマンド実行し　成否に　入れ
            成否が　成功に　等しい　でなければ　スコープを抜け出し	
            つぎに

			INSERT1で　SQL文をセットし
            10で　整数のSQLパラメータをセットし
            "Tcl/Tk"で　文字列のSQLパラメータをセットし
			SQLコマンド実行し　成否に　入れ
			成否が　成功に　等しい　でなければ　スコープを抜け出し
			つぎに

            INSERT2で　SQL文をセットし
            1で　整数のSQLパラメータをセットし
            10で　整数のSQLパラメータをセットし
			SQLコマンド実行し　成否に　入れ
			成否が　成功に　等しい　でなければ　スコープを抜け出し
			つぎに
	
		ここまでスコープ

		成否が　成功に　等しい　
        ならば コミットし
		さもなければ	　
			SQLエラー取得し Mind文字列に変換し　一行表示し
			ロールバックし
		つぎに

		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し 結果セットを表示する

		DB切断し


	API破棄処理すること。
```

# ビルド結果
ではビルドします。
```
C:\developments\vscode\mind9>mind testmysqlodbcc file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> testmysqlodbcc.exe
```

今回もすぐに成功です。実際問題SQL文以外はPostgreSQL版と同じです。

# 実行結果
ではつづいて実行してみます。
```
C:\developments\vscode\mind9>testmysqlodbcc          
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
S1000 [MySQL][ODBC 8.0(w) Driver][mysqld-8.3.0]Incorrect string value: '\x82\xA0\x82\xBD\x82\xE7...' for column 'よみがな' at row 1
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
ODBCライブラリを破棄する
```
UPDATE文で失敗しました！C言語DLL拡張単語でODBCと通信している場合はShiftJISのMind文字列にC言語文字列のnullターミネータを付加して渡しており、ODBCドライバの接続文字列にはコードページオプションでShiftJIS指定(CP932)しているので、SELECTで返ってくる文字列やSQL文の日本語テーブル名、項目名指定は問題なく動いております。

Tcl拡張単語の方ではMind側でShiftJISのMind文字列をUTF-8に変換してTclインタプリタに渡しているので、コードページオプションでShiftJIS指定はせずに、SELECTで返ってくる文字列やSQL文の日本語テーブル名、項目名指定は問題なく動いております。

エラーメッセージで引用されている'\x82\xA0\x82\xBD\x82\xE7...'はCP932の「あたらしい」の先頭３文字に相当しますので、ShiftJISで伝わっていることがわかります。

ここで急に[こちらの記事](https://qiita.com/mylifewithviolin/items/0348cd16a5f7774b1dff)でMySQL側の文字コードをUTF8にしていたことを思い出しましたので、再度CP932に戻します。

```
mysql> ALTER DATABASE 日本語プログラミング言語 CHARACTER SET cp932;
Query OK, 1 row affected (0.01 sec)

mysql> status
--------------
C:\Program Files\MySQL\MySQL Server 8.3\bin\mysql.exe  Ver 8.3.0 for Win64 on x86_64 (MySQL Community Server - GPL)

Connection id:          48
Current database:       日本語プログラミング言語
Current user:           root@localhost
SSL:                    Cipher in use is TLS_AES_128_GCM_SHA256
Using delimiter:        ;
Server version:         8.3.0 MySQL Community Server - GPL
Protocol version:       10
Connection:             localhost via TCP/IP
Server characterset:    utf8mb4
Db     characterset:    cp932
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
TCP port:               3306
Binary data as:         Hexadecimal
Uptime:                 26 days 11 hours 50 min 44 sec

Threads: 4  Questions: 1353  Slow queries: 0  Opens: 382  Flush tables: 3  Open tables: 231  Queries per second avg: 0.000
--------------
mysql> ALTER TABLE 言語名 CONVERT TO CHARACTER SET cp932;
Query OK, 2 rows affected (0.11 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> SELECT COLUMN_NAME, CHARACTER_SET_NAME, COLLATION_NAME
    -> FROM INFORMATION_SCHEMA.COLUMNS
    -> WHERE TABLE_SCHEMA = '日本語プログラミング言語'
    -> AND TABLE_NAME = '言語名';
+--------------+--------------------+-------------------+
| COLUMN_NAME  | CHARACTER_SET_NAME | COLLATION_NAME    |
+--------------+--------------------+-------------------+
| よみがな     | cp932              | cp932_japanese_ci |
| 公開年       | NULL               | NULL              |
| 言語ID       | NULL               | NULL              |
| 言語名       | cp932              | cp932_japanese_ci |
+--------------+--------------------+-------------------+
4 rows in set (0.00 sec)
```
# 実行結果（DB文字コード変更後）
では、この状態で再実行します。
```
C:\developments\vscode\mind9>testmysqlodbcc
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|10|Tcl/Tk|
|7|Mind for Android|あたらしいよみがな|3|Java|
ODBCライブラリを破棄する
```
無事に成功しました！
では、この状態で再実行します。ＰＫ違反で失敗します。
```
C:\developments\vscode\mind9>testmysqlodbcc
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|10|Tcl/Tk|
|7|Mind for Android|あたらしいよみがな|3|Java|
23000 [MySQL][ODBC 8.0(w) Driver][mysqld-8.3.0]Duplicate entry '10' for key '開発言語名.PRIMARY'
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|10|Tcl/Tk|
|7|Mind for Android|あたらしいよみがな|3|Java|
ODBCライブラリを破棄する
```

よみがなが変更されたままの状態からの再実行なので、ロールバックしたかがわかりずらいですが、意図した動きのようです。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。とりあえずC言語DLL拡張単語では意図した文字コード設定で正常動作しましたのでひと安心です。残る課題は（それぞれでたくさんあるのですが）TclでMySqlの文字コード問題となります。MySQLのCLIで今回Statusを実行してみましたが、DB以外でも文字コード設定の余地がありそうなので、もう少しこの点深堀してみます。
