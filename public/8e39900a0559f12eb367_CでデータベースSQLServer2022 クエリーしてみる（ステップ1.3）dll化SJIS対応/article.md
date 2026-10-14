# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ1.3）」です。ステップ1.3とは最初のステップちょい先を意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.1）dll化select文渡し](https://qiita.com/mylifewithviolin/items/1e9a2bb4d4936f82993d)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態からSELECT文を引数渡しするようにしています。その後Mind対応のためにエキスポート関数の引数型のみをwchar_t*からchar*に変えてとりあえずMind文字列は正常に引き渡されたのですが、ODBC関数がワイド文字（ユニコード）系のままでしたので正常動作しませんでした。今回は中身のワイド文字（ユニコード）関連記述をいったんオミットしてSJISが動作するように改変します。

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
## openDb関数とexec関数
openDb関数とexec関数の引数を通常の文字ポインタにして、ロケールはSJISにしました。また、ここが重要な点ですが、#include<sql.h>の上に#undef UNICODEを記述し、ODBC関数のワイド文字版への再定義を無効化しました。

```c:mssqlodbc32.c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<windows.h>
#include <tchar.h>
#include <sal.h>
#include <locale.h>
#undef UNICODE
#include<sql.h>
#include<sqlext.h>

#define _EXPORTING

#include "mssqlodbc32.h"
__declspec(dllexport) void openDb(char* datasouce) {
    RETCODE    ret;
    setlocale(LC_ALL, "Japanese_Japan.932");

    printf("DSText --> %s", datasouce);
    printf("\n");    
    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }
    else {
        printf("ERROR OPEN\n"); return;
    }
}
   __declspec(dllexport) void exec(char* select) {

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
    doSelect(henv, hdbc, hstmt, (SQLCHAR*)select);

    return;
}
```
## 実行検証用のCのコンソールアプリケーション
接続情報とSELECT文はコンソールアプリ側で定義を持たせています。ここでもワイド文字指定のリテラルL指定はやめて通常の文字リテラルとしています。
```c:consoleApp.c
#include "mssqlodbc32.h"

void main() {
	char datasouce[] = "Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
	char select[] = "SELECT * FROM 言語名 WHERE 言語ID=1";
	openDb(datasouce);
	exec(select);
	closeDb();
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

FUNC_DECLSPEC void exec(char* select);

FUNC_DECLSPEC void closeDb();
```

 # 実行結果
 他に従来結果の出力コードにはワイド文字相当の記述ヶ所が多数存在しており、それらを通常文字に書き換えています。それは後から説明するとして、まずはここで実行してみます。
```
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLText --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLExecDirect --> 0
| 言語ID      | 言語名               | 公開年      | よみがな              |
|           1 |             Ｍｉｎｄ |        1985 |             まいんど  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 10848) は、コード 0 で終了しました。
```

動きました。データソースとSELECT文の日本語も正常に引き渡されているようです。SQLDriverConnectとSQLExecDirectのODBC関数もANSIモードで動作しました。

# 細かな変更点
下記の構造体でワイド文字指定していたヶ所は通常の文字指定に訂正しました。ほんとうは変数名からもwとった方がよいでしょう。文字リテラルはまめにLがついているので除去しました。wprintfはprintfに訂正しました。
```
typedef struct STR_BINDING {
    SQLSMALLINT         cDisplaySize;           // size to display
    CHAR*               wszBuffer;              // display buffer
    SQLLEN              indPtr;                 // size or null 
    BOOL                fChar;                  // character col?
    struct STR_BINDING* sNext;                  // linked list
} BINDING;

#define DISPLAY_FORMAT      "%c %*.*s "
#define DISPLAY_FORMAT_C    "%c %-*.*s "
```
DLL化した状態からのソースコード全文は掲載していませんでしたので、今回参考に掲載しましたので、興味のある方はそちらを見てください。

# おわりに
とりあえず引数を渡して実行する方はSJIS日本語文字列で正常動作するようになりましたので、次回は戻り値の返しに進行します。

# 参考情報
dll本体のソースコード全文です。ヘッダファイルと検証用コンソールアプリは本文掲載内容がすべてです。  
<details><summary>ソースコード全文</summary>

```c:mssqlodbc32.c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<windows.h>
#include <tchar.h>
#include <sal.h>
#include <locale.h>
#undef UNICODE
#include<sql.h>
#include<sqlext.h>


typedef struct STR_BINDING {
    SQLSMALLINT         cDisplaySize;           // size to display
    CHAR* wszBuffer;                           // display buffer
    SQLLEN              indPtr;                 // size or null 
    BOOL                fChar;                  // character col?
    struct STR_BINDING* sNext;                  // linked list
} BINDING;


int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLCHAR datasouce[]);
int closeConn(HENV* henv, HDBC* hdbc);
void doSelect(HENV henv, HDBC hdbc, HSTMT hstmt, SQLCHAR select[]);
void DisplayResults(HSTMT hStmt, SQLSMALLINT cCols);
void AllocateBindings(HSTMT hStmt, SQLSMALLINT cCols, BINDING** ppBinding, SQLSMALLINT* pDisplay);
void DisplayTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding);

#define _EXPORTING


#include "mssqlodbc32.h"

HENV    henv;    //環境ハンドル
HDBC    hdbc;    //接続ハンドル
HSTMT   hstmt;   //ステートメントハンドル

__declspec(dllexport) void openDb(char* datasouce) {
    RETCODE    ret;
    setlocale(LC_ALL, "Japanese_Japan.932");

    printf("DSText --> %s", datasouce);
    printf("\n");    
    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }
    else {
        printf("ERROR OPEN\n"); return;
    }

    return;
}

__declspec(dllexport) void closeDb() {
    RETCODE    ret;
    //接続を閉じる
    ret = closeConn(&henv, &hdbc);
    if (ret == 0) {
        printf("SUCCESS CLOSE\n");
    }
    else {
        printf("ERROR CLOSE\n"); return;
    }

    return;
}
__declspec(dllexport) void exec(char* select) {

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
    doSelect(henv, hdbc, hstmt, (SQLCHAR*)select);

    return;
}

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
    if (rc != 1) { return -1; }

    rc = SQLAllocStmt(*hdbc, hstmt);
    printf("SQLAllocStmt --> %d\n", rc);
    if (rc != SQL_SUCCESS) { return -1; }

    return 0;
}

//接続を閉じる
int closeConn(HENV* henv, HDBC* hdbc) {
    SQLRETURN    rc;

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
void doSelect(HENV henv, HDBC hdbc, HSTMT hstmt, SQLCHAR select[]) {
    SQLRETURN rc;

    rc = SQLExecDirect(hstmt, select, SQL_NTS);
    printf("SQLExecDirect --> %d\n", rc);

    SQLSMALLINT sNumResults;
    SQLNumResultCols(hstmt, &sNumResults);
    if (sNumResults > 0) {
        DisplayResults(hstmt, sNumResults);
    }

    return;
}



#define DISPLAY_MAX 50          // Arbitrary limit on column width to display
#define DISPLAY_FORMAT_EXTRA 3  // Per column extra display bytes (| <data> )
#define DISPLAY_FORMAT      "%c %*.*s "
#define DISPLAY_FORMAT_C    "%c %-*.*s "
#define NULL_SIZE           6   // <NULL>
#define SQL_QUERY_SIZE      1000 // Max. Num characters for SQL Query passed in.

#define PIPE                '|'
SHORT   gHeight = 80;       // Users screen height

//結果を表示する
void DisplayResults(HSTMT hStmt, SQLSMALLINT cCols) {

    BINDING* pFirstBinding, * pThisBinding;
    SQLSMALLINT     cDisplaySize;
    SQLRETURN       rc = SQL_SUCCESS;
    int             iCount = 0;

    AllocateBindings(hStmt, cCols, &pFirstBinding, &cDisplaySize);

    setlocale(LC_ALL, "Japanese_Japan.932");
    DisplayTitles(hStmt, cDisplaySize + 1, pFirstBinding);

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
                    printf(pThisBinding->fChar ? DISPLAY_FORMAT_C : DISPLAY_FORMAT,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        pThisBinding->wszBuffer);
                }
                else {
                    printf(DISPLAY_FORMAT_C,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        "<NULL>");
                }
            }
            printf(" %c\n", PIPE);
        }
    } while (!fNoData);

    printf("%*.*s", cDisplaySize + 2, cDisplaySize + 2, " ");
    printf("\n");

    // Clean up the allocated buffers
    while (pFirstBinding)
    {
        pThisBinding = pFirstBinding->sNext;
        free(pFirstBinding->wszBuffer);
        free(pFirstBinding);
        pFirstBinding = pThisBinding;
    }
}

//バインドを割り当てる
void AllocateBindings(HSTMT         hStmt,
    SQLSMALLINT   cCols,
    BINDING** ppBinding,
    SQLSMALLINT* pDisplay)
{
    SQLSMALLINT     iCol;
    BINDING* pThisBinding, * pLastBinding = NULL;
    SQLLEN          cchDisplay, ssType;
    SQLSMALLINT     cchColumnNameLength;

    *pDisplay = 0;

    for (iCol = 1; iCol <= cCols; iCol++)
    {
        pThisBinding = (BINDING*)(malloc(sizeof(BINDING)));
        if (!(pThisBinding))
        {
            fprintf(stderr, "Out of memory!\n");
            exit(-100);
        }

        if (iCol == 1)
        {
            *ppBinding = pThisBinding;
        }
        else
        {
            pLastBinding->sNext = pThisBinding;
        }
        pLastBinding = pThisBinding;

        SQLColAttribute(hStmt,
            iCol,
            SQL_DESC_DISPLAY_SIZE,
            NULL,
            0,
            NULL,
            &cchDisplay);

        SQLColAttribute(hStmt,
            iCol,
            SQL_DESC_CONCISE_TYPE,
            NULL,
            0,
            NULL,
            &ssType);

        pThisBinding->fChar = (ssType == SQL_CHAR ||
            ssType == SQL_VARCHAR ||
            ssType == SQL_LONGVARCHAR);

        pThisBinding->sNext = NULL;

        // Arbitrary limit on display size
        if (cchDisplay > DISPLAY_MAX)
            cchDisplay = DISPLAY_MAX;

        pThisBinding->wszBuffer = (CHAR*)malloc((cchDisplay + 1) * sizeof(CHAR));
        if (!(pThisBinding->wszBuffer))
        {
            fprintf(stderr, "Out of memory!\n");
            exit(-100);
        }

        SQLBindCol(hStmt,
            iCol,
            SQL_C_TCHAR,
            (SQLPOINTER)pThisBinding->wszBuffer,
            (cchDisplay + 1) * sizeof(CHAR),
            &pThisBinding->indPtr);


        SQLColAttribute(hStmt,
            iCol,
            SQL_DESC_NAME,
            NULL,
            0,
            &cchColumnNameLength,
            NULL);

        pThisBinding->cDisplaySize = max((SQLSMALLINT)cchDisplay, cchColumnNameLength);
        if (pThisBinding->cDisplaySize < NULL_SIZE)
            pThisBinding->cDisplaySize = NULL_SIZE;

        *pDisplay += pThisBinding->cDisplaySize + DISPLAY_FORMAT_EXTRA;

    }

    return;
}

void DisplayTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding)
{
    CHAR           wszTitle[DISPLAY_MAX];
    SQLSMALLINT     iCol = 1;

    for (; pBinding; pBinding = pBinding->sNext)
    {

        SQLColAttribute(hStmt,
            iCol++,
            SQL_DESC_NAME,
            wszTitle,
            sizeof(wszTitle), // Note count of bytes!
            NULL,
            NULL);

        printf(DISPLAY_FORMAT_C,
            PIPE,
            pBinding->cDisplaySize,
            pBinding->cDisplaySize,
            wszTitle);
    }

    printf(" %c", PIPE);
    printf("\n");

    return;
}

```

</details>
