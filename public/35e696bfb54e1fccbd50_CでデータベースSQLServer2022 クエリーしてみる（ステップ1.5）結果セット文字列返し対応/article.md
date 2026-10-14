# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ1.5）」です。ステップ1.5とは最初のステップの道半ばを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態から接続文字列、SELECT文をSJIS文字列で引数渡しするようにしています。今回は結果セットを文字列で返してみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

# C状態での変更点
## exec関数
exec関数の戻り値をダブルアスタリスクの文字配列ポインタのポインタとしました。
```c:mssqlodbc32.c
// 配列を動的に確保する  
char** resultset;

__declspec(dllexport) char** exec(char* select) {

    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText(char) --> ");
    int i = 0;
    while (select[i] != '\0') {
        printf("%c", select[i]);
        i++;
    }
    printf("\n");
    printf("SQLText --> %s", select);
    printf("\n");
    //照会する
    char** resultset=doSelect(henv, hdbc, hstmt, (SQLCHAR*)select);

    return resultset;
}
```
## 実行検証用のCのコンソールアプリケーション
あとで詳しく説明しますが、従来はexec関数の内部でコンソール出力していましたが、このバージョンからは列項目名と列の値をパイプ区切りの文字列配列で返してきます。そのため、コンソール出力はコンソールアプリケーション側の処理としています。列項目ヘッダや１行分の列値の文字列配列の間に改行だけからなる文字列配列を返していますので、改行処理はとくにアプリ側は意識していません。

```c:consoleApp.c
#include "mssqlodbc32.h"

void main() {
	char datasouce[] = "Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
	char select[] = "SELECT * FROM 言語名 WHERE 言語ID IN (1,7)";

	int ret=openDb(datasouce);
	if (ret == 0) {
		printf("SUCCESS OPEN\n");
		char** resultset=exec(select);
		if (resultset) {
			int i = 0;
			while (resultset[i] != '\0') {
				printf("%s", resultset[i]);  // 出力  
				i++;
			}
		}

		closeDb();
	}
	else {
		printf("ERROR OPEN\n"); return;
	}
```

## ヘッダファイル
```c:mssqlodbc32.h
#pragma once

#ifdef _EXPORTING
#define FUNC_DECLSPEC    __declspec(dllexport)
#else
#define FUNC_DECLSPEC    __declspec(dllimport)
#endif

FUNC_DECLSPEC void openDb(char* datasouce);

FUNC_DECLSPEC char** exec(char* select);

FUNC_DECLSPEC void closeDb();
```
# 実行結果
exec関数のメインの処理関数doSelectが文字列配列のポインタ（文字配列ポインタのポインタ）を返すようにしてあり、内部で従来はDisplayResultsとDisplayTitlesを呼んでいましたが、このバージョンではAllocateResultsとAddTitlesという別関数を呼ぶようにしました。それは後から説明するとして、まずはここで実行してみます。
```
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID IN (7)
SQLText --> SELECT * FROM 言語名 WHERE 言語ID IN (7)
SQLExecDirect --> 0
| 言語ID      | 言語名               | 公開年      | よみがな              |
|           7 |     Mind for Android |        2012 | まいんどふぉーあんどろいど  |
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 9720) は、コード 0 で終了しました。
```

動きました。SELECT文のWHERE句は言語ID IN (1,7)として2行返るようにしています。ほんとは「まいんどふぉーあんどろいど」で「ろいど」が切れてますが、とりあえずよしとさせていただきます。
## 2024/01/15 追記
「ろいど」が切れてたのは「よみがな」列の型をnvarchar(20)にしたせいでした。最初に作成したときnvarchar(50)にしていたのですが、どこからのタイミングで20にしてしまいました。この数字が文字数ではなくバイトペア数ということを忘れてました。いま(30)にして足りているようです。

# 細かな変更点
結果セットのメモリ開放はDB切断処理内で実行しています。
結果セットのメモリ獲得と結果セットのコピーはdoSelect内のAllocateResults関数内で行っています。
## closeConn doSelect
```C
int closeConn(HENV* henv, HDBC* hdbc) {
    SQLRETURN    rc;

    free(resultset);  // 配列のメモリの解放  
    printf("resultset --> free\n");

    //サーバーから切断
    rc = SQLDisconnect(*hdbc);
    printf("SQLDisconnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    //接続ハンドルの解放
    rc = SQLFreeConnect(*hdbc);
    printf("SQLFreeConnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    //環境ハンドルの解放
    rc = SQLFreeEnv(*henv);
    printf("SQLFreeEnv --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    return 0;
}

//照会する
char** doSelect(HENV henv, HDBC hdbc, HSTMT hstmt, SQLCHAR select[]) {
    SQLRETURN rc;

    rc = SQLExecDirect(hstmt, select, SQL_NTS);
    printf("SQLExecDirect --> %d\n", rc);

    SQLSMALLINT sNumResults;
    SQLNumResultCols(hstmt, &sNumResults);
    if (sNumResults > 0) {
        AllocateResults(hstmt, sNumResults);
    }

    return resultset;
}

```
## AllocateResults AddTitles
従来のDisplayResultsとDisplayTitlesのprintfの書式制御を使いまわしてsnprintfで文字列配列に値を格納しています。
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

                    resultset[colIndex] = calloc(colLength, sizeof(char));
                    if (pThisBinding->indPtr != SQL_NULL_DATA)
                    {
                        snprintf(resultset[colIndex], colLength, pThisBinding->fChar ? DISPLAY_FORMAT_C : DISPLAY_FORMAT,
                            PIPE,
                            pThisBinding->cDisplaySize,
                            pThisBinding->cDisplaySize,
                            pThisBinding->wszBuffer);
                    }
                    else {
                        snprintf(resultset[colIndex], NULL_SIZE, DISPLAY_FORMAT_C,
                            PIPE,
                            pThisBinding->cDisplaySize,
                            pThisBinding->cDisplaySize,
                            "<NULL>");
                    }
                    colIndex++;
                }
                //printf(" %c\n", PIPE);
                resultset[colIndex] = calloc(colLength, sizeof(char));
                snprintf(resultset[colIndex], colLength, " %c\n", PIPE);
                colIndex++;
            }
        } while (!fNoData);

        //printf("%*.*s", cDisplaySize + 2, cDisplaySize + 2, " ");
        //printf("\n");
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
        snprintf(resultset[colIndex], sizeof(wszTitle),DISPLAY_FORMAT_C,
            PIPE,
            pBinding->cDisplaySize,
            pBinding->cDisplaySize,
            wszTitle);
        colIndex++;
    }

    //printf(" %c", PIPE);
    //printf("\n");
    resultset[colIndex] = calloc(colLength, sizeof(char));
    snprintf(resultset[colIndex], sizeof(wszTitle), " %c\n", PIPE);
    colIndex++;

    return colIndex;
}
```
# おわりに
次回はクエリのパラメータ化またはトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。
