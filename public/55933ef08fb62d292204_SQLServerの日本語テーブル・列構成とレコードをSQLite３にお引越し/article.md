# はじめに
SQLServer、Mysql、PostgreSQLのODBCドライバ向けのC言語ライブラリを日本語プログラミング言語Mind用に実装していますが、SQLiteも少し対応してみようかなという気がしてきましたので、まずはスキーマとレコードの準備の備忘録です。

# 前提条件
Windows11 Pro 22H2 22621.4317

SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
SQLite version 3.43.2 2023-10-10 12:14:04



# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。それを各データベース用に作成して検証に利用します。今回はSQLite3用に同じものを作成します。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

各テーブルの列の型はたいしたものを使っていませんので、SQLiteの列型でもだいじょうぶでした。

# SQLite

SQLiteはODBCドライバーに付属のものを使用しています。

```
C:\Program Files\SQLite ODBC Driver for Win64>sqlite3
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite>
```

http://www.ch-werner.de/sqliteodbc/


Current version
sqliteodbc.exe
sqliteodbc_w64.exe　←こちらをダウンロード


# お題のデータべース作成

SQLServer、Mysql、PostgreSQLではGUIの管理ツールがありますが、SQLiteはなさそうなので、とりあえずSQLServerManagementStudioでSQLServerのテーブルのDDLをリバース作成して、それをCopilotにSQLite３用に書き換えてもらいました。

## データべースのファイルを作成

下記のコマンドでお題のデータべースのファイルを作成します。
```
sqlite3 "C:\sqlite3\日本語プログラミング言語.db"
```

データベースファイルを格納するフォルダは事前に作成しておかないと、.tablesコマンド実行の時点でファイルができていないことが判明します。
```
C:\Program Files\SQLite ODBC Driver for Win64>sqlite3 "C:\sqlite3\日本語プログラミング言語.db"
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
sqlite> .tables
Error: unable to open database "C:\sqlite3\日本語プログラミング言語.db": unable to open database file
```
.tablesコマンドでCLIプロンプトが返ったらとりあえずできている証拠。

```
C:\Program Files\SQLite ODBC Driver for Win64>sqlite3 "C:\sqlite3\日本語プログラミング言語.db"
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
sqlite> .tables
sqlite>
```
dirコマンドで確認してみますと、実際にファイルができていました。
※dirコマンドのコンソール出力結果は一部省略しています。
```
c:\sqlite3>dir        .
2026/07/24  22:55            40,960 日本語プログラミング言語.db
```
## データべースのテーブルを作成

生成AIに翻訳してもらったSQLServerのDDLのSQLite3バージョンです。
```
CREATE TABLE "言語名" (
    "言語ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "言語名" TEXT NOT NULL,
    "公開年" INTEGER,
    "よみがな" TEXT
);

CREATE TABLE "後継言語" (
    "言語ID" INTEGER NOT NULL,
    "後継言語ID" INTEGER NOT NULL,
    PRIMARY KEY ("言語ID", "後継言語ID")
);

CREATE TABLE "姉妹言語" (
    "言語ID" INTEGER NOT NULL,
    "姉妹言語ID" INTEGER NOT NULL,
    PRIMARY KEY ("言語ID", "姉妹言語ID")
);

CREATE TABLE "開発言語" (
    "言語ID" INTEGER NOT NULL,
    "開発言語ID" INTEGER NOT NULL,
    PRIMARY KEY ("言語ID", "開発言語ID")
);

CREATE TABLE "開発言語名" (
    "開発言語ID" INTEGER NOT NULL,
    "開発言語名" TEXT NOT NULL,
    "自言語ID" INTEGER,
    PRIMARY KEY ("開発言語ID")
);
```

下記のようにCLIに貼り付けます。
```
C:\Program Files\SQLite ODBC Driver for Win64>sqlite3 "C:\sqlite3\日本語プログラミング言語.db"
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
sqlite> .tables
sqlite> CREATE TABLE "言語名" (
(x1...>     "言語ID" INTEGER PRIMARY KEY AUTOINCREMENT,
(x1...>     "言語名" TEXT NOT NULL,
(x1...>     "公開年" INTEGER,
(x1...>     "よみがな" TEXT
(x1...> );
sqlite>
sqlite> CREATE TABLE "後継言語" (
(x1...>     "言語ID" INTEGER NOT NULL,
(x1...>     "後継言語ID" INTEGER NOT NULL,
(x1...>     PRIMARY KEY ("言語ID", "後継言語ID")
(x1...> );
sqlite>
sqlite> CREATE TABLE "姉妹言語" (
(x1...>     "言語ID" INTEGER NOT NULL,
(x1...>     "姉妹言語ID" INTEGER NOT NULL,
(x1...>     PRIMARY KEY ("言語ID", "姉妹言語ID")
(x1...> );
sqlite>
sqlite> CREATE TABLE "開発言語" (
(x1...>     "言語ID" INTEGER NOT NULL,
(x1...>     "開発言語ID" INTEGER NOT NULL,
(x1...>     PRIMARY KEY ("言語ID", "開発言語ID")
(x1...> );
sqlite>
sqlite> CREATE TABLE "開発言語名" (
(x1...>     "開発言語ID" INTEGER NOT NULL,
(x1...>     "開発言語名" TEXT NOT NULL,
(x1...>     "自言語ID" INTEGER,
(x1...>     PRIMARY KEY ("開発言語ID")
(x1...> );
sqlite>
```
.tablesコマンドでテーブルができていることを確認します。
```
sqlite> .tables
姉妹言語     言語名        開発言語名
後継言語     開発言語
sqlite>
```

## データべースのデータをコピー

SQLServer上で実行するとSQLite3のINSERT INTO文を結果セットで返してくれるSELECT文をCopilotに作ってもらいました。
テーブルのCreate文を翻訳してもらっているのでスムーズでした。

```
SELECT
    'INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES ('
    + CAST(言語ID AS NVARCHAR(10)) + ', '
    + '''' + 言語名 + ''', '
    + CAST(公開年 AS NVARCHAR(10)) + ', '
    + '''' + よみがな + ''''
    + ');'
FROM 言語名;

SELECT
    'INSERT INTO "開発言語" ("言語ID", "開発言語ID") VALUES ('
    + CAST(言語ID AS NVARCHAR(10)) + ', '
    + CAST(開発言語ID AS NVARCHAR(10))
    + ');'
FROM 開発言語;

SELECT
    'INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES ('
    + CAST(開発言語ID AS NVARCHAR(10)) + ', '
    + '''' + 開発言語名 + ''', '
    + COALESCE(CAST(自言語ID AS NVARCHAR(10)), 'NULL')
    + ');'
FROM 開発言語名;

SELECT
    'INSERT INTO "後継言語" ("言語ID", "後継言語ID") VALUES ('
    + CAST(言語ID AS NVARCHAR(10)) + ', '
    + CAST(後継言語ID AS NVARCHAR(10))
    + ');'
FROM 後継言語;

SELECT
    'INSERT INTO "姉妹言語" ("言語ID", "姉妹言語ID") VALUES ('
    + CAST(言語ID AS NVARCHAR(10)) + ', '
    + CAST(姉妹言語ID AS NVARCHAR(10))
    + ');'
FROM 姉妹言語;
```

SQLServer上で実行した結果は下記の感じ。
```
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (1, 'C', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (2, 'C#', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (3, 'Java', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (4, 'VisualBasic', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (5, 'Delphi', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (6, 'VisualBasic.net', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (7, 'Forth', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (8, 'Mind', 1);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (9, 'Node.js', NULL);
INSERT INTO "開発言語名" ("開発言語ID", "開発言語名", "自言語ID") VALUES (10, 'Tcl/Tk', NULL);
```

これらをSQLite3のCLIに貼り付けます。上記のサンプルは「開発言語名」のレコードですが、下記のサンプルは「開発言語」のレコードです。
```
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (1, 'Ｍｉｎｄ', 1985, 'まいんど');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (2, 'ＴＴＳ', 2000, 'てぃーてぃーえす');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (3, 'ひまわり', 2001, 'ひまわり');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (4, 'ドリトル', 2003, 'どりとる');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (5, 'なでしこ', 2004, 'なでしこ');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (6, 'プロデル', 2007, 'ぷろでる');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (7, 'Mind for Android', 2012, 'まいんど');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (8, 'スミレ', 2018, 'すみれ');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (9, 'なでしこ３', 2018, 'なでしこさん');
sqlite> INSERT INTO "言語名" ("言語ID", "言語名", "公開年", "よみがな") VALUES (10, 'スミレ畑', 2020, 'すみればたけ');
```
無事にSELEC文の成功です。

```
sqlite> SELECT * FROM "言語名";
1|Ｍｉｎｄ|1985|まいんど
2|ＴＴＳ|2000|てぃーてぃーえす
3|ひまわり|2001|ひまわり
4|ドリトル|2003|どりとる
5|なでしこ|2004|なでしこ
6|プロデル|2007|ぷろでる
7|Mind for Android|2012|まいんど
8|スミレ|2018|すみれ
9|なでしこ３|2018|なでしこさん
10|スミレ畑|2020|すみればたけ
```

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。

SQLServerやSQLite3はAIもみっちり学習している感じで、ストレスを感じませんでした。エージェントにローカルのSQLServerの接続情報を与えれば、わりと全自動でできそうな勢いでした。
