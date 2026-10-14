# はじめに

この記事のお題はMindでデータベースMySQL8.3にクエリーしてみる（ステップ1.5）」です。ステップ1.5はSQLServer2022にクエリーしてみるの（ステップ1.5）と同レベルを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態から結果セットを文字列配列で返すようにしましたので、それを使ってMindからMySQL8.3に実行してみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[C（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。
文字コードはcp932(Shift-JIS)、照合順序はその既定です。

# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を
ソースコードは[C（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)と[C（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)をご参照ください。
### C状態での変更点
SQL Server ODBCドライバ17でのODBC関数SQLDriverConnectの成功時の戻り値がなぜか1だったのでそのように対応していたのですが、MySQL ODBCドライバ8は0になったので、その点だけ書き換えています。

```diff_c:mssqlodbc32.c
//接続を開く
int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLCHAR datasouce[]) {
    SQLRETURN    rc;

    //環境ハンドルを割り振る
    rc = SQLAllocEnv(henv);
    printf("SQLAllocEnv --> %d\n", rc);
    if (rc != 0) { return -1; }

    //接続ハンドルを割り振る
    rc = SQLAllocConnect(*henv, hdbc);
    printf("SQLAllocConnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    rc = SQLDriverConnect(*hdbc,
        NULL,
        datasouce,
        SQL_NTS,
        NULL,
        0,
        NULL,
        SQL_DRIVER_NOPROMPT);// SQL_DRIVER_COMPLETE_REQUIRED
    printf("SQLConnect --> %d\n", rc);
-    if (rc != 1) { return -1; }
+    if (rc != 0) { return -1; }
+    
    rc = SQLAllocStmt(*hdbc, hstmt);
    printf("SQLAllocStmt --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    return 0;
}
```

## Mind
Mindのソース全体像は[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。
ODBC接続文字列だけ変更しました。

```mind:mssqlodbc.src
メインとは
    	datasourceは　文字列定数　「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932&00&」
    	SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)&00&
    ※略
```

# 実行結果
では実行します。
 ```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DSText --> Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 0
SQLAllocStmt --> 0
DB接続　成功
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID IN (1,7)
SQLText --> SELECT * FROM 言語名 WHERE 言語ID IN (1,7)
SQLExecDirect --> 0
| 言語ID     | 言語名               | 公開年     | よみがな                        |
|          1 |                 Mind |       1985 |                       まいんど  |
|          7 |     Mind for Android |       2012 |     まいんどふぉーあんどろいど  |
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に正常動作しました！:tada:

# おわりに
次回はクエリのパラメータ化またはトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。

# 参考情報
当初、列名は正常に取得できるのにデータ値の日本語ひらがなが化けるという現象に遭遇したとき、接続文字列について検索した際に偶然ヒットした下記の記事のcharsetオプションのつけ具合による結果セットの変化の表がたいへん参考になりました。

https://qiita.com/t-yama-3/items/2dbd23b0b7e8dd741b41
