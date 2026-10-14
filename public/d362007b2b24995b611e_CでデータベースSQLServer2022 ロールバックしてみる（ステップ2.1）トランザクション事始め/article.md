# はじめに
この記事のお題は「CでデータベースSQLServer2022 ロールバックしてみる（ステップ2.1）」です。ステップ2.1とはODBCトランザクション制御の事始めを言います。

ODBCなので、低レイヤーよりで実装するとこうなんだくらいの感覚で、サンプルとしてお読みいただければ幸いです。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[（ステップ2.0）](https://qiita.com/mylifewithviolin/items/03d941fb67424fb64877)をご参照ください。

# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。ソースコード全体はこの記事の最後に記載しました。

learn.microsoft.comの日本語サイトの下記に公開されているC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

ODBCプログラミングの情報は古いバージョンに準拠した内容しか記載されていない場合が多いので、念のためODBC規格元のマイクロソフトの関数レファレンスは読んでおいた方がよいです。上記のサンプルにはトランザクション制御の実装はなさそうでした。

## 実行検証用のCのコンソールアプリケーション
こちらは[（ステップ2.0）](https://qiita.com/mylifewithviolin/items/03d941fb67424fb64877)をご参照ください。

下記のようなトランザクションを実行しています。
```:トランザクション前
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど | <NULL> |     <NULL> |  
```
```:トランザクション後
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |          3 |       Java |
```
トランザクションは下記の内訳となります。
1)開発言語テーブルに言語ID=7、開発言語ID=3のレコードを挿入したのでMind for Androidの開発言語がNULLからJavaに変わった
2)言語名テーブルの言語ID=7のよみがなを更新したので、Mind for Androidのよみがなが「まいんどふぉーあんどろいど」から「まいんど」に変わった。
3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除したので、Mindの開発言語Forthの行が消えた。

# 実行結果
## トランザクション失敗ロールバック
前回は動作していなかったロールバックを検証します。3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除する際に、存在しない列名言語ID2=1をあたえてここで失敗を起こします。


では、実行してみましょう。
```
 DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
SUCCESS OPEN
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
paramCountStr --> 1
paramNumber --> 3
param --> まいんど
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
言語ID|     言語ID 言語名|     言語名 よみがな|   よみがな 開発言語ID| 開発言語ID 開発言語名| 開発言語名
|
 1|          1 Ｍｉｎｄ|   Ｍｉｎｄ まいんど|   まいんど 1|          1 C|          C
|
 1|          1 Ｍｉｎｄ|   Ｍｉｎｄ まいんど|   まいんど 7|          7 Forth|      Forth
|
 1|          1 Ｍｉｎｄ|   Ｍｉｎｄ まいんど|   まいんど 8|          8 Mind|       Mind
|
 7|          7 Mind for Android| Mind for Android まいんどふぉーあんどろいど| まいんどふぉーあんどろいど <NULL>|     <NULL> <NULL>|     <NULL>
|
 AutoCommit Off  --> 0
SQLSetConnectAttr --> 0
paramCountInt --> 1
paramNumber --> 1
param --> 7
paramCountInt --> 2
paramNumber --> 2
param --> 3
SQLText --> INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
paramCountStr --> 1
paramNumber --> 1
param --> まいんど
paramCountInt --> 1
paramNumber --> 2
param --> 7
SQLText --> UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
SQLGetConnectAttr --> 0
AutoCommit--> 0
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?
SQLExecDirect --> -1
SQLStatus --> S0022 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]列名 '言語ID2' が無効です。
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
RollbackTran  --> 1
SQLEndTran  --> 0
AutoCommit On --> 1
SQLSetConnectAttr --> 0
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
resultset --> free
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど |     <NULL> |     <NULL> |
 paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 17020) は、コード 0 で終了しました。
```

DELETEの実行で失敗が起きていることがわかります。
```
SQLText --> DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?
SQLExecDirect --> -1
SQLStatus --> S0022 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]列名 '言語ID2' が無効です。
```

では、以下にSELECTの結果だけを抽出します。

```:トランザクション前
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど | <NULL> |     <NULL> |  
```
```:トランザクション後
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど | <NULL> |     <NULL> | 
```
無事に挿入と更新の結果も反映されず元の状態となっていることが確認できました。トランザクションはロールバックしたことがわかります。:tada:

# おわりに
ようやくこぎつけました。道のりはまだ長いです。しばらくお休みします。

# 参考情報
ヘッダファイルです。
```c:mssqlodbc32.h
#pragma once

#ifdef _EXPORTING
#define FUNC_DECLSPEC    __declspec(dllexport)
#else
#define FUNC_DECLSPEC    __declspec(dllimport)
#endif

//DBを開く
FUNC_DECLSPEC int openDb(char* datasouce);
//SELECTを実行する
FUNC_DECLSPEC char** exec(char* select);
//DBを閉じる
FUNC_DECLSPEC void closeDb();
//ステートメントをセットする
FUNC_DECLSPEC void setStatement(char* stmt);
//SQLパラメータ整数をバインドする
FUNC_DECLSPEC int bindParameterInt(int param);
//SQLパラメータ文字列をバインドする
FUNC_DECLSPEC int bindParameterStr(char* param);
//結果セットを取得する
FUNC_DECLSPEC char** getResultset();
//SQLコマンド実行する
FUNC_DECLSPEC int execCommand();
//自動コミットを設定する
FUNC_DECLSPEC int setAutoCommit(int sw);
//自動コミットを取得する
FUNC_DECLSPEC int getAutoCommit();
//トランザクションを終了する
FUNC_DECLSPEC int endTransaction(int sw);
```

dll本体のソースコード全文です。
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
    CHAR*               wszBuffer;              // display buffer
    SQLLEN              indPtr;                 // size or null 
    BOOL                fChar;                  // character col?
    struct STR_BINDING* sNext;                  // linked list
} BINDING;

// 配列を動的に確保する  
char** resultset;

char* statement;//パラメータ化ステートメント
int paramNumber;//パラメータナンバー ODBCは順序依存
int paramCountInt;//整数パラメータカウンタ　上限あり
int paramCountStr;//文字列パラメータカウンタ 上限あり
// パラメータ配列を動的に確保する  
char** paramsetStr;

#define PARAM_CHAR_MAX 10

void resetCounters(int sw);
int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLCHAR datasouce[]);
int closeConn(HENV* henv, HDBC* hdbc);
char** doSelect(HSTMT hstmt, SQLCHAR select[]);
void dispSQLStatus();
void DisplayResults(HSTMT hStmt, SQLSMALLINT cCols);
void AllocateBindings(HSTMT hStmt, SQLSMALLINT cCols, BINDING** ppBinding, SQLSMALLINT* pDisplay);
void DisplayTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding);
void AllocateResults(HSTMT hStmt, SQLSMALLINT cCols);
int AddTitles(HSTMT hStmt, DWORD cDisplaySize, BINDING* pBinding);
int getStringSize(char* str);

#define _EXPORTING


#include "mssqlodbc32.h"

HENV    henv;    //環境ハンドル
HDBC    hdbc;    //接続ハンドル
HSTMT   hstmt;   //ステートメントハンドル

//DBを開く
__declspec(dllexport) int openDb(char* datasouce) {
    RETCODE    ret;
    setlocale(LC_ALL, "Japanese_Japan.932");

    printf("DSText --> %s", datasouce);
    printf("\n");    
    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret != 0) {
        return -1;
    }

    //パラメータカウンタを初期化
    resetCounters(0);
    paramsetStr = calloc(PARAM_CHAR_MAX, sizeof(char*));//文字列パラメータ配列を初期化
    if (!(paramsetStr)) {
        fprintf(stderr, "Out of memory!\n");
        return -100;
    }
    return 0;
}

//DBを閉じる
__declspec(dllexport) void closeDb() {
    RETCODE    ret;
    if (paramsetStr) {
        free(paramsetStr);  // パラメータ配列のメモリの解放  
        printf("paramsetStr --> free\n");
    }
    if (resultset) {
        free(resultset);  // 結果セット配列のメモリの解放  
        printf("resultset --> free\n");
    }

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

//SELECTを実行する
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
    if (resultset) {
        free(resultset);  // 配列のメモリの解放  
        printf("resultset --> free\n");
    }
    //照会する
    char** resultset=doSelect(hstmt, (SQLCHAR*)select);

    return resultset;
}

//ステートメントをセットする
__declspec(dllexport) void setStatement(char* stmt) {
    statement=stmt;
}

#define PARAM_INT_MAX 10          
SQLINTEGER    paramInt[PARAM_INT_MAX];//最大10
SQLINTEGER    paramInd[PARAM_INT_MAX];//最大10
//SQLパラメータ整数をバインドする
__declspec(dllexport) int bindParameterInt(int param){
    SQLRETURN    rc;
    int index = paramCountInt;
    paramCountInt++;
    paramNumber++;
    printf("paramCountInt --> %d\n", paramCountInt);
    printf("paramNumber --> %d\n", paramNumber);
    if (paramCountInt > PARAM_INT_MAX){
        fprintf(stderr, "Out of index!\n");
        return -100;
    }
    printf("param --> %d\n", param);
    // Bind the parameters.  
    rc=SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER,
        10, 0, &paramInt[index], 0, &paramInd[index]);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramInd[index] = 0;
    paramInt[index] = param;
    return 0;
}

SQLINTEGER    paramStrInd[PARAM_CHAR_MAX];//最大10
//SQLパラメータ文字列をバインドする
__declspec(dllexport) int bindParameterStr(char* param) {
    //setlocale(LC_ALL, "Japanese_Japan.932");
    SQLRETURN    rc;
    int index = paramCountStr;
    paramCountStr++;
    paramNumber++;
    printf("paramCountStr --> %d\n", paramCountStr);
    printf("paramNumber --> %d\n", paramNumber);
    if (paramCountStr > PARAM_CHAR_MAX) {
        fprintf(stderr, "Out of index!\n");
        return -100;;
    }

    paramsetStr[index] = calloc(getStringSize(param), sizeof(char));
    if (!(paramsetStr[index])) { return -1; }
    printf("param --> %s\n", param);
    // Bind the parameters.  
    rc = SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR,
        getStringSize(param)-1, 0, paramsetStr[index], getStringSize(param), &paramStrInd[index]);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramStrInd[index] = SQL_NTS;
    strcpy_s((char*)paramsetStr[index] , getStringSize(param), param);
    return 0;
}

//結果セットを取得する
__declspec(dllexport) char** getResultset() {
    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText --> %s", statement);
    printf("\n");
    if (resultset) {
        free(resultset);  // 配列のメモリの解放  
        printf("resultset --> free\n");
    }

    //照会する
    char** resultset = doSelect(hstmt, (SQLCHAR*)statement);
    //パラメータカウンタを初期化
    resetCounters(1);
    return resultset;
}

//SQLコマンド実行する
__declspec(dllexport) int execCommand() {
    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText --> %s", statement);
    printf("\n");
    SQLRETURN    rc;
    rc = SQLExecDirect(hstmt, statement, SQL_NTS);
    printf("SQLExecDirect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    //パラメータカウンタを初期化
    resetCounters(1);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return 0;
}

//自動コミットを設定する
__declspec(dllexport) int setAutoCommit(int sw) {
    
    SQLRETURN    rc;
    if (sw) {
        printf("AutoCommit On --> %d\n", sw);
        rc = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, (int*)SQL_AUTOCOMMIT_ON, SQL_IS_INTEGER);
    }
    else {
        printf("AutoCommit Off  --> %d\n", sw);
        rc = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
    }
    printf("SQLSetConnectAttr --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return 0;
}
//自動コミットを取得する
__declspec(dllexport) int getAutoCommit() {

    SQLRETURN    rc;
    SQLINTEGER   autocommit;
    rc = SQLGetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, &autocommit, 0, NULL);
    printf("SQLGetConnectAttr --> %d\n", rc);
    printf("AutoCommit--> %d\n", autocommit);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return 0;
}
//トランザクションを終了する
__declspec(dllexport) int endTransaction(int sw) {

    SQLRETURN    rc,rc2;
    SQLSMALLINT   completionType;
    if (sw) {
        completionType = SQL_COMMIT;
        printf("CommitTran  --> %d\n", completionType);
    }    else{
        completionType = SQL_ROLLBACK;
        printf("RollbackTran  --> %d\n", completionType);
    }
    rc = SQLEndTran(SQL_HANDLE_DBC, hdbc, completionType);
    printf("SQLEndTran  --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    rc2=setAutoCommit(1);
    if (rc2 != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return 0;
}

//ここからエクスポートしない関数
//パラメータカウンタを初期化
void resetCounters(int sw) {
    if (sw) {
        for (int i = 0; i < paramCountInt; i++){
            paramInt[i] = 0;
        }
        for (int i = 0; i < paramCountStr; i++) {
            free(paramsetStr[i]);
            paramsetStr[i]=NULL;//文字列ポインタも初期化
        }
    }
    paramNumber = 0;//パラメータナンバを初期化
    paramCountInt = 0;//整数パラメータカウンタを初期化
    paramCountStr = 0;//文字列パラメータカウンタを初期化
    printf("paramCountInt --> %d\n", paramCountInt);
    printf("paramCountStr --> %d\n", paramCountStr);
    printf("paramNumber --> %d\n", paramNumber);
}
//接続を開く
int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLCHAR datasouce[]) {
    SQLRETURN    rc;

    //環境ハンドルを割り振る
    rc = SQLAllocEnv(henv);
    printf("SQLAllocEnv --> %d\n", rc);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //接続ハンドルを割り振る
    rc = SQLAllocConnect(*henv, hdbc);
    printf("SQLAllocConnect --> %d\n", rc);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    rc = SQLDriverConnect(*hdbc,
        NULL,
        datasouce,
        SQL_NTS,
        NULL,
        0,
        NULL,
        SQL_DRIVER_NOPROMPT);// SQL_DRIVER_COMPLETE_REQUIRED
    printf("SQLConnect --> %d\n", rc);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    rc = SQLAllocStmt(*hdbc, hstmt);
    printf("SQLAllocStmt --> %d\n", rc);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

 
    return 0;
}

//接続を閉じる
int closeConn(HENV* henv, HDBC* hdbc) {
    SQLRETURN    rc;


    //サーバーから切断
    rc = SQLDisconnect(*hdbc);
    printf("SQLDisconnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //接続ハンドルの解放
    rc = SQLFreeConnect(*hdbc);
    printf("SQLFreeConnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //環境ハンドルの解放
    rc = SQLFreeEnv(*henv);
    printf("SQLFreeEnv --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    return 0;
}

//照会する
char** doSelect(HSTMT hstmt, SQLCHAR select[]) {
    SQLRETURN rc;

    rc = SQLExecDirect(hstmt, select, SQL_NTS);
    printf("SQLExecDirect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return resultset; }

    SQLSMALLINT sNumResults;
    SQLNumResultCols(hstmt, &sNumResults);
    if (sNumResults > 0) {
        AllocateResults(hstmt, sNumResults);
        //DisplayResults(hstmt, sNumResults);
    }
    SQLCloseCursor(hstmt);

    return resultset;
}

void dispSQLStatus() {
    SQLCHAR SqlState[6], Msg[SQL_MAX_MESSAGE_LENGTH];
    SQLINTEGER    NativeError;
    SQLSMALLINT   i, MsgLen;
    SQLRETURN     rc;
    SQLLEN numRecs = 0;
    SQLGetDiagField(SQL_HANDLE_STMT, hstmt, 0, SQL_DIAG_NUMBER, &numRecs, 0, 0);
    // Get the status records.
    i = 1;
    while (i <= numRecs && (rc = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt, i, SqlState, &NativeError,
        Msg, sizeof(Msg), &MsgLen)) != SQL_NO_DATA) {
        printf("SQLStatus --> %s %s\n", SqlState, Msg);
        //DisplayError(SqlState, NativeError, Msg, MsgLen);
        i++;
    }
}

#define DISPLAY_MAX 400          // Arbitrary limit on column width to display
#define DISPLAY_FORMAT_EXTRA 3  // Per column extra display bytes (| <data> )
#define DISPLAY_FORMAT      "%c %*.*s "
#define DISPLAY_FORMAT_C    "%c %-*.*s "
#define NULL_SIZE           6   // <NULL>
#define SQL_QUERY_SIZE      1000 // Max. Num characters for SQL Query passed in.

#define PIPE                '|'
SHORT   gHeight = 80;       // Users screen height


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
    //setlocale(LC_ALL, "Ja_jp.UTF8");

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
                        //size_t colLength2 = sizeof(pThisBinding->wszBuffer);
                        resultset[colIndex] = calloc(colLength, sizeof(char));
                        snprintf(resultset[colIndex], colLength,"%s", pThisBinding->wszBuffer);
                        //snprintf(resultset[colIndex], colLength, pThisBinding->fChar ? DISPLAY_FORMAT_C : DISPLAY_FORMAT,
                        //    PIPE,
                        //    pThisBinding->cDisplaySize,
                        //    pThisBinding->cDisplaySize,
                        //    pThisBinding->wszBuffer);
                    }
                    else {
                        resultset[colIndex] = calloc(colLength, sizeof(char));
                        snprintf(resultset[colIndex], colLength, "%s","<NULL>");
                        //snprintf(resultset[colIndex], NULL_SIZE, DISPLAY_FORMAT_C,
                        //    PIPE,
                        //    pThisBinding->cDisplaySize,
                        //    pThisBinding->cDisplaySize,
                        //    "<NULL>");
                    }
                    colIndex++;
                }
                //printf(" %c\n", PIPE);
                resultset[colIndex] = calloc(colLength, sizeof(char));
                snprintf(resultset[colIndex], colLength, "\n");
                //snprintf(resultset[colIndex], colLength, " %c\n", PIPE);
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
        snprintf(resultset[colIndex], sizeof(wszTitle), "%s",wszTitle);
        ////snprintf(resultset[colIndex], sizeof(wszTitle),DISPLAY_FORMAT_C,
        ////    PIPE,
        ////    pBinding->cDisplaySize,
        ////    pBinding->cDisplaySize,
        ////    wszTitle);
        colIndex++;
    }

    //printf(" %c", PIPE);
    //printf("\n");
    resultset[colIndex] = calloc(colLength, sizeof(char));
    //snprintf(resultset[colIndex], sizeof(wszTitle), " %c\n", PIPE);
    snprintf(resultset[colIndex], sizeof(wszTitle), "\n");
    colIndex++;

    return colIndex;
}

int getStringSize(char* str) {
    int size = 0;
    while (str[size] != '\0') {
        size++;
    }
    return size+1;//NULL終端含める
}


```

</details>
