# はじめに
日本語プログラミング言語Mind7/8用に実装したodbcのC言語インターフェースによるC言語DLL拡張単語はMind９βでも動作することを確認しています。SQLServer、Mysql、PostgreSQLで検証してきましたが、今回はSQLiteをMind8で検証してみます。

[SQLServerからデータの引っ越しを行ったとき](https://qiita.com/mylifewithviolin/items/55933ef08fb62d292204)クリップボード経由でINSERTのSQL文をSSMSからコピーしてSQLiteのCLIに貼り付けて実行した際は文字コードが問題になりませんでしたが、Mind用の検証データベースの文字コードはすべてShift-JISとしています。SQLiteはShift-JISには対応しておらずUTF-8固定なので、今回この点は未対応です。

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 8.07
SQLite version 3.43.2 2023-10-10 12:14:04

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022


下記のRDBに対応しています。
SQL Server 16.0.1000.6 Express Edition
MySQL Community Server 8.3.0 winx64
mysql-connector-odbc-8.0.35-win32
postgresql-16.1-1-windows-x64
psqlodbc_16_00_0000-x86


# お題のデータべース
SQLite、SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLite3です。

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
## C
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## DLLライブラリ本体
Cで実装されたDLLライブラリ本体のソースコードは[CでODBCデータベース実装 SQLServer2022（ステップ3）結果セットを項目名情報無で返す](https://qiita.com/mylifewithviolin/items/9a1bd4c75a2a3be543f0)をご参照ください。

## Mind
### ライブラリ
Mindで実装されたODBCライブラリ本体のソースコードは[Mind7/8/9β odbcライブラリC言語DLL拡張単語のアップデート（結果セット取得の9βTcl互換調整）](https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a)をご参照ください。

### SQLite3版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。SQLite3の場合は、日本語テーブル名、列名をすべてダブルクォーテーションで囲いました。

2回目のSELECTの結果セットは「項目名と共に結果セット取得」としています。

※テストコード（アプリケーション側）の書き味は本記事のC言語拡張による場合とTcl言語拡張による場合とかなり同じコードで書けるようにしています。Mind7の場合はSQL文字列定数を分割する必要があります。

```mind:testodbccsqlite.src
"odbcc"を　コンパイルする。

datasourceSqliteは 文字列定数 「DRIVER={SQLite3 ODBC Driver};Database=c:\sqlite3\日本語プログラミング言語.db;」。

メインとは
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (?,?)」	
	INSERTは　　　文字列定数　「INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE "言語名" SET よみがな = ? WHERE "言語ID" = ?」
	DELETEは　　　文字列定数　「DELETE "開発言語" WHERE "言語ID" = ? AND "開発言語ID" = ?」
	成否は　		変数

	API初期処理しておき　成功に　等しい　でなければ　終わり　つぎに

	datasourceSqliteで　DB接続し　成否に　入れ　成否が　成功に　等しい　でなければ　成否を　数値表示し　終わり　つぎに


		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し 結果セットを表示する

		トランザクションを開始し

        ここからトランザクションの　スコープ開始

			INSERTで　SQL文をセットし
			7で　整数のSQLパラメータをセットし
			3で　整数のSQLパラメータをセットし
			SQLコマンド実行し　成否に　入れ
			成否が　成功に　等しい　でなければ　スコープを抜け出し
			つぎに

			UPDATEで　SQL文をセットし
			「まいんど」で　文字列のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			SQLコマンド実行し　成否に　入れ
			成否が　成功に　等しい　でなければ　スコープを抜け出し	
			つぎに

			DELETEで　SQL文をセットし
			1で　整数のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
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
		項目名と共に結果セット取得し 結果セットを表示する

		DB切断し


	API破棄処理すること。
```

# ビルド結果
ではビルドします。

## Mind8
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccsqlite file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> testodbccsqlite.exe
```

# 実行結果
ではつづいて実行してみます。
```
C:\developments\vscode\mind9\odbc>testodbccsqlite          
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|1|C|
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|8|Mind|
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|10|Tcl/Tk|
|7|Mind for Android|縺ｾ縺・ｓ縺ｩ|2012|3|Java|
S1000 UNIQUE constraint failed: 開発言語.言語ID, 開発言語.開発言語ID (19)
|言語ID|言語名|よみがな|公開年|開発言語ID|開発言語名|
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|1|C|
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|8|Mind|
|1|・ｭ・会ｽ趣ｽл縺ｾ縺・ｓ縺ｩ|1985|10|Tcl/Tk|
|7|Mind for Android|縺ｾ縺・ｓ縺ｩ|2012|3|Java|
ODBCライブラリを破棄する

C:\developments\vscode\mind9\odbc>
```
SQLiteはShift-JISには対応しておらずUTF-8固定なので、日本語のデータはすべて文字化けています。ただし、接続文字列の日本語データベース名は認識しました。また、SELECT文中の日本語列名は認識できているようです。

```
S1000 UNIQUE constraint failed: 開発言語.言語ID, 開発言語.開発言語ID (19)
```
こちらはINSERT文がユニーク制限でエラーとなっている状態で、これはデータの状態から正常な状態です。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。

Mind用に実装したC言語DLL拡張単語odbcライブラリはShift-JISを前提にしていましたが、SQLiteのようにShift-JISに対応しないデータベースにもある程度対応できるような策を今後検討してまいります。

**2026/08/02 追記**

UTF-8文字コード変換を行ったSQLiteの記事を追加しました。

https://qiita.com/mylifewithviolin/items/97b8ca5b68373e300405
