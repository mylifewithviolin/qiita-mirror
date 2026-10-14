# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ-0.5）」です。ステップ-0.5ということはもう一声ということを意味します。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2


# お題のデータべース
データベース名 sample
テーブル名 language 
|項目名|項目型|
|:-:|:-:|
|id| int  |
| name  |  nvarchar(50) |

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているソースコードを使用します。しかし、このオリジナル状態ではちょっとソースコードの全貌を認識するのが煩雑となるので、前回からはかなりシンプル化した状態で接続を試みまていま。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

 これはC++で書かれていますが、前々記事の少しの変更でCで動きます。この記事の当座の目標はある言語用にSQLSeverのODBCを介した操作をCのライブラリとしておくことでした。
前回の記事では、あくまでC言語の状態でコマンドプロンプトからSQL文の入力を受け付けしたりするところなどをざっくり除去しました。

# dsn
今回の記事の状態より、DSNではなくDriver指定の接続文字列で接続できるようになりました。接続文字列情報は下記のサイトを参考にしています。

https://www.connectionstrings.com/microsoft-odbc-driver-17-for-sql-server/

https://learn.microsoft.com/ja-jp/sql/relational-databases/native-client/applications/using-connection-string-keywords-with-sql-server-native-client?view=sql-server-ver16#odbc-driver-connection-string-keywords


# C状態での変更点

mainは下記のようにしました。接続文字列情報の型をSQLWCHARにしました。これで接続するようになりました。

```c:mssql4.c
void main() {
    RETCODE    ret;
    HENV    henv;    //環境ハンドル
    HDBC    hdbc;    //接続ハンドル
    HSTMT   hstmt;   //ステートメントハンドル

    SQLWCHAR datasouce[] = L"Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=sample;UID=sa;PWD=****;";
    SQLWCHAR select[] = L"SELECT * FROM language";

    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }else{
        printf("ERROR OPEN\n"); return;
    }
    //照会する
     doSelect(henv, hdbc, hstmt, select);

    //接続を閉じる
    ret = closeConn(&henv, &hdbc);
    if (ret == 0){
        printf("SUCCESS CLOSE\n");
    }else{
        printf("ERROR CLOSE\n"); return;
    }
    return;    

}
```
下記の記事を参考にしています。

https://segakuin.com/c/odbc/

https://www.kkaneko.jp/cc/mysql/odbcvisualcpp.html

https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16


```c:mssql4.c
//接続を開く
int openConn(HENV * henv, HDBC * hdbc, HSTMT * hstmt, SQLWCHAR datasouce[]) {
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
```

接続文字列で接続するようになりましたので、SQLDriverConnectの最後の引数のオプションをSQL_DRIVER_NOPROMPTにしてデータソースの選択ダイアログを開かなくしました。それに伴いウィンドウハンドルの取得もやめています。

他に、結果を表示するDisplayResults()の中で、項目名表示DisplayTitles()を復活しました。DisplayTitles()はTRYODBC構文を除去した以外はオリジナルのままです。


 # 実行結果
 それでは実行してみます。今回はデータソース選択ダイアログは開きません。
 ```cmd:
 SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLExecDirect --> 0
| id          | name                                                |
|           1 |                                                  C  |
|           2 |                                                C++  |
|           3 |                                               Java  |
|           4 |                                                 C#  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\odbcsql\x64\Debug\odbcsql.exe (プロセス 9328) は、コード 0 で終了しました。
デバッグが停止したときに自動的にコンソールを閉じるには、[ツール] -> [オプション] -> [デバッグ] -> [デバッグの停止時に自 動的にコンソールを閉じる] を有効にします。
このウィンドウを閉じるには、任意のキーを押してください...
 ```

 無事に結果が返りました。

 # おわりに
 すみません、タイムアウトです。次回は日本語に対応させていきます。日本語文字列のデータベース接続、テーブル名項目名への照会は今回状態でも実行できているようですが、結果表示処理がまだ対応していません。C言語でのODBCでのSQLServer接続の情報は少ないので何かの参考になれば幸いです。

# 参考情報
  
<details><summary>ソースコード全文</summary>

```c:mssql4.c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<windows.h>
#include<sql.h>
#include<sqlext.h>
#include <tchar.h>
#include <sal.h>

typedef struct STR_BINDING {
    SQLSMALLINT         cDisplaySize;           // size to display
    WCHAR* wszBuffer;                           // display buffer
    SQLLEN              indPtr;                 // size or null 
    BOOL                fChar;                  // character col?
    struct STR_BINDING* sNext;                  // linked list
} BINDING;


int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLWCHAR datasouce[]);
int closeConn(HENV* henv, HDBC* hdbc);
void doSelect(HENV henv, HDBC hdbc, HSTMT hstmt, SQLWCHAR select[]);
void DisplayResults(HSTMT hStmt, SQLSMALLINT cCols);
void AllocateBindings(HSTMT hStmt,SQLSMALLINT cCols,BINDING** ppBinding,SQLSMALLINT* pDisplay);
void DisplayTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding);


void main() {
    RETCODE    ret;
    HENV    henv;    //環境ハンドル
    HDBC    hdbc;    //接続ハンドル
    HSTMT   hstmt;   //ステートメントハンドル

    SQLWCHAR datasouce[] = L"Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=sample;UID=sa;PWD=mind;";
    SQLWCHAR select[] = L"SELECT * FROM language";

    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }else{
        printf("ERROR OPEN\n"); return;
    }
    //照会する
     doSelect(henv, hdbc, hstmt, select);

    //接続を閉じる
    ret = closeConn(&henv, &hdbc);
    if (ret == 0){
        printf("SUCCESS CLOSE\n");
    }else{
        printf("ERROR CLOSE\n"); return;
    }
    return;    

}

//接続を開く
int openConn(HENV * henv, HDBC * hdbc, HSTMT * hstmt, SQLWCHAR datasouce[]) {
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
void doSelect(HENV henv, HDBC hdbc, HSTMT hstmt, SQLWCHAR select[]) {
    SQLRETURN rc;

    rc = SQLExecDirect(hstmt, (wchar_t*)select, SQL_NTS);
    printf("SQLExecDirect --> %d\n", rc);

    SQLSMALLINT sNumResults;
    SQLNumResultCols(hstmt, &sNumResults);
    if (sNumResults > 0){
        DisplayResults(hstmt, sNumResults);
    }

    return;
}



#define DISPLAY_MAX 50          // Arbitrary limit on column width to display
#define DISPLAY_FORMAT_EXTRA 3  // Per column extra display bytes (| <data> )
#define DISPLAY_FORMAT      L"%c %*.*s "
#define DISPLAY_FORMAT_C    L"%c %-*.*s "
#define NULL_SIZE           6   // <NULL>
#define SQL_QUERY_SIZE      1000 // Max. Num characters for SQL Query passed in.

#define PIPE                L'|'
SHORT   gHeight = 80;       // Users screen height

//結果を表示する
void DisplayResults(HSTMT hStmt,SQLSMALLINT cCols){

    BINDING* pFirstBinding, * pThisBinding;
    SQLSMALLINT     cDisplaySize;
    SQLRETURN       rc = SQL_SUCCESS;
    int             iCount = 0;

    AllocateBindings(hStmt, cCols, &pFirstBinding, &cDisplaySize);
    DisplayTitles(hStmt, cDisplaySize + 1, pFirstBinding);

    // Fetch and display the data
    int fNoData = 0;
    do {
        // Fetch a row
        rc = SQLFetch(hStmt);
        if (rc == SQL_NO_DATA_FOUND) {
            fNoData = 1;
        }else {

            // Display the data.   Ignore truncations
            for (pThisBinding = pFirstBinding;
                pThisBinding;
                pThisBinding = pThisBinding->sNext) {
                if (pThisBinding->indPtr != SQL_NULL_DATA)
                {
                    wprintf(pThisBinding->fChar ? DISPLAY_FORMAT_C : DISPLAY_FORMAT,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        pThisBinding->wszBuffer);
                } else {
                    wprintf(DISPLAY_FORMAT_C,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        L"<NULL>");
                }
            }
            wprintf(L" %c\n", PIPE);
        }
    } while (!fNoData);

    wprintf(L"%*.*s", cDisplaySize + 2, cDisplaySize + 2, L" ");
    wprintf(L"\n");

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
            fwprintf(stderr, L"Out of memory!\n");
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

        pThisBinding->wszBuffer = (WCHAR*)malloc((cchDisplay + 1) * sizeof(WCHAR));
        if (!(pThisBinding->wszBuffer))
        {
            fwprintf(stderr, L"Out of memory!\n");
            exit(-100);
        }

        SQLBindCol(hStmt,
            iCol,
            SQL_C_TCHAR,
            (SQLPOINTER)pThisBinding->wszBuffer,
            (cchDisplay + 1) * sizeof(WCHAR),
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

void DisplayTitles(HSTMT hStmt,DWORD cDisplaySize, BINDING* pBinding)
{
    WCHAR           wszTitle[DISPLAY_MAX];
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

        wprintf(DISPLAY_FORMAT_C,
            PIPE,
            pBinding->cDisplaySize,
            pBinding->cDisplaySize,
            wszTitle);
    }

    wprintf(L" %c", PIPE);
    wprintf(L"\n");

    return;
}
```

</details>
