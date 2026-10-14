# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind９βのTclとのインターフェース単語でTclのOdbc接続をSQLServer、MySql、PostgreSQLで評価してまいりました。また従来のMind7/8用に実装したC言語DLL拡張単語のodbcのC言語インターフェースが動作することをSQLServerで確認しました。今回はTcl評価時と同じSQLテキストを使ってC言語でのOdbc接続をPostgreSQLに対して行ってみます。


# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022

postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86

下記のRDBにも対応はしていますが、今回検証環境はPostgreSQLです。
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはPostgreSQLです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## Mind
### ライブラリ
ライブラリのソースコードはお手数ですが[こちらの記事](https://qiita.com/mylifewithviolin/items/21fa8a6e7531c7d67196)をご参照ください。

### PostgreSQL版テスト用コード
基本的な書き味はSQLServer版と同じですが、SQLコマンドテキストの内容はTcl版のPostgreSQL版とほぼ同じにしています。ほぼというのは、C言語のODBCのプレースホルダーは「？」で動作しましたので、その点が異なっています。

```mind:testpsgodbcc.src
"odbcc"を　コンパイルする。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=mind;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;」。


メインとは

	※SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」
    　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
    「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
    「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (?,?)」
　　INSERT1は　　　文字列定数　「INSERT INTO "開発言語名" ("開発言語ID","開発言語名") VALUES (?,?)」
　　INSERT2は　　　文字列定数　「INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (?,?)」
　　UPDATEは　　　文字列定数　「UPDATE "言語名" SET "よみがな" = ? WHERE "言語ID" = ?」
　　DELETEは　　　文字列定数　「DELETE "開発言語" WHERE "言語ID" = ? AND "開発言語ID" = ?」
	成否は　		変数

	API初期処理しておき　成功に　等しい　でなければ　終わり　つぎに

	datasourcePgsqlで　DB接続し　成功に　等しい　でなければ　終わり　つぎに


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
C:\developments\vscode\mind9>mind testpsgodbcc file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> testpsgodbcc.exe
```

今回はすぐに成功しました。

# 実行結果
ではつづいて実行してみます。データベースの状態は過日のTcl版での成功済状態ですので、UPDATEの後のINSERT1がPK制約でエラーとなり、UPDATEがロールバックされる想定です。
```
C:\developments\vscode\mind9>testpsgodbcc
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|1|C|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
23505 ERROR: 重複したキー値は一意性制約"開発言語名_pkey"違反となります
DETAIL: キー ("開発言語ID")=(10) はすでに存在します。;
Error while executing the query
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|1|C|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
ODBCライブラリを破棄する
```
無事にロールバック成功しました。「Mind for Android」のよみがなが更新されていませんね。次にデータべースの状態から重複要素を削除して再実行します。
```
C:\developments\vscode\mind9>testpsgodbcc
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|1|C|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|10|Tcl/Tk|
|7|Mind for Android|あたらしいよみがな|3|Java|
ODBCライブラリを破棄する
```
無事にトランザクションコミットしました。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
