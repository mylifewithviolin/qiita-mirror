# はじめに

この記事のお題はCでデータベースMySQL8.3にクエリーしてみる（ステップ1.6）」です。ステップ1.6はSQLServer2022にクエリーしてみるの（ステップ1.5）とほぼ同レベルを意味します。0.1の違いは結果セットの文字列返しの際に従来DLL側でパイプを付ける書式制御を残していましたが、今回はそれをとりますという意味です。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[C（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。
文字コードはcp932(Shift-JIS)、照合順序はその既定です。

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているSQLServerのODBCドライバを使ったC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

 
# C状態での変更点
## AllocateResults AddTitles
従来のDisplayResultsとDisplayTitlesのprintfの書式制御を使いまわしてsnprintfで文字列配列に値を格納していましたが、その書式制御をなくしました。
strcpy_sに書き換えてみたりしたのですが、とりあえずsnprintfのままです。
```C
//結果を生成する
void AllocateResults(HSTMT hStmt, SQLSMALLINT cCols) {

    BINDING* pFirstBinding, * pThisBinding;
    SQLSMALLINT     cDisplaySize;
    SQLRETURN       rc = SQL_SUCCESS;
    int             iCount = 0;
    size_t maxRows = SQL_QUERY_SIZE;
    size_t colLength = DISPLAY_MAX;  // 文字配列の要素数 

    AllocateBindings(hStmt, cCols, &pFirstBinding, &cDisplaySize);

    setlocale(LC_ALL, "Japanese_Japan.932");

    resultset = calloc(maxRows, sizeof(char*));
    if (resultset) {

        int colIndex = AddTitles(hStmt, cDisplaySize + 1, pFirstBinding);

        // Fetch and display the data
        int fNoData = 0;
        do {
            // Fetch a row
            rc = SQLFetch(hStmt);
            if (rc == SQL_NO_DATA_FOUND) {
                fNoData = 1;
            }
            else {

                // Display the data.   Ignore truncations
                for (pThisBinding = pFirstBinding;
                    pThisBinding;
                    pThisBinding = pThisBinding->sNext) {

                    if (pThisBinding->indPtr != SQL_NULL_DATA)
                    {
                        resultset[colIndex] = calloc(colLength, sizeof(char));
                        snprintf(resultset[colIndex], colLength,"%s", pThisBinding->wszBuffer);
                    }
                    else {
                        resultset[colIndex] = calloc(colLength, sizeof(char));
                        snprintf(resultset[colIndex], colLength, "%s","<NULL>");
                    }
                    colIndex++;
                }
                resultset[colIndex] = calloc(colLength, sizeof(char));
                snprintf(resultset[colIndex], colLength, "\n");
                colIndex++;
            }
        } while (!fNoData);

    }
    // Clean up the allocated buffers
    while (pFirstBinding)
    {
        pThisBinding = pFirstBinding->sNext;
        free(pFirstBinding->wszBuffer);
        free(pFirstBinding);
        pFirstBinding = pThisBinding;
    }
}

int AddTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding)
{
    CHAR           wszTitle[DISPLAY_MAX];
    SQLSMALLINT     iCol = 1;
    size_t colLength = DISPLAY_MAX;  // 文字配列の要素数 
    int colIndex = 0;
    for (; pBinding; pBinding = pBinding->sNext)
    {

        SQLColAttribute(hStmt,
            iCol++,
            SQL_DESC_NAME,
            wszTitle,
            sizeof(wszTitle), // Note count of bytes!
            NULL,
            NULL);

        resultset[colIndex] = calloc(colLength, sizeof(char));
        snprintf(resultset[colIndex], sizeof(wszTitle), "%s",wszTitle);
        colIndex++;
    }

    resultset[colIndex] = calloc(colLength, sizeof(char));
    snprintf(resultset[colIndex], sizeof(wszTitle), "\n");
    colIndex++;

    return colIndex;
}

```

# 実行結果
では実行してみましょう。
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
言語ID言語名公開年よみがな
1Mind1985まいんど
7Mind for Android2012まいんどふぉーあんどろいど
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に返ってきています。この状態では単純な文字列配列として返ってきています。このままでは少しみづらいので、コンソールアプリ側で少し書式制御を追加します。

## 実行検証用のCのコンソールアプリケーション

```diff_c:consoleApp.c
#include "mssqlodbc32.h"

+ #define DISPLAY_FORMAT      "%c %*.*s "
+ #define PIPE                '|'

void main() {
	char datasouce[] = "Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932";
	char select[] = "SELECT * FROM 言語名 WHERE 言語ID IN (1,7)";

	int ret=openDb(datasouce);
	if (ret == 0) {
		printf("SUCCESS OPEN\n");
		char** resultset=exec(select);
		if (resultset) {
			int i = 0;
			while (resultset[i] != '\0') {
-				printf("%s", resultset[i]);  // 出力 
+				printf(DISPLAY_FORMAT, PIPE,10,30, resultset[i]);  // 出力  
				i++;
			}
		}

		closeDb();
	}
	else {
		printf("ERROR OPEN\n"); return;
	}

}  
```
# 実行結果
では実行してみましょう。
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
|     言語ID |     言語名 |     公開年 |   よみがな |
 |          1 |       Mind |       1985 |   まいんど |
 |          7 | Mind for Android |       2012 | まいんどふぉーあんどろいど |
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```

DLL側で書式制御していたよりはきれいではないですが、ざっくりアプリ側で書式を追加することができました。

# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、次回はクエリのパラメータ化またはトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。
