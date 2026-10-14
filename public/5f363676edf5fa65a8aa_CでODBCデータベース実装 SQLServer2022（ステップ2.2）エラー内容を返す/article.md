# はじめに
この記事のお題は「CでODBCデータベース実装 SQLServer2022（ステップ2.2）エラー内容を返す」です。前回まではデバッグ用のログ出力が出しっぱなしでしたので。今回はCのプリプロセッサのディレクティブでそれらを無効化し、エラーコードとエラーメッセージをアプリケーションに返せるようにします。

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
## Cのプロジェクト配置構成
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。ソースコード全体はこの記事の最後に記載しました。

## 実行検証用のCのコンソールアプリケーション
アプリケーション側でエラー内容を表示するようにしました。DLL側のデバッグ用出力は無効化しています。
```c:consoleApp.c
#include<stdio.h>

#include "mssqlodbc32.h"

#define DISPLAY_FORMAT      "%c %*.*s "
#define PIPE                '|'

void main() {
	char datasouce[] = "Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";

	char select[] = "\
SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN \
LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID \
LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID \
WHERE LN.言語ID IN (?,?)";
	char insert[] = "INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)";
	char update[] = "UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?";
	char delete[] = "DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?";

	int ret=openDb(datasouce);
	if (ret != 0) {
		errMsg = getErrorMsg();
		printf("%s\n", errMsg); return;
	}

	setStatement(select);
	bindParameterInt(1);
	bindParameterInt(7);

	char** resultset=getResultset(select);
	//char** resultset = exec(select);
	if (resultset) {
		int i = 0;
		while (resultset[i] != '\0') {
			printf(DISPLAY_FORMAT, PIPE,10,30, resultset[i]);  // 出力  
			i++;
		}
	}
	setAutoCommit(0);//自動コミット無効=トランザクション開始

	setStatement(insert);
	bindParameterInt(7);
	bindParameterInt(3);
	ret = execCommand();
	if (ret == 0) {
		setStatement(update);
		bindParameterStr("まいんど");
		bindParameterInt(1);
		ret = execCommand();
	}
	if (ret == 0) {
		endTransaction(1);//トランザクション.コミット
	}else {
 		errMsg= getErrorMsg();
		printf("%s\n", errMsg);
		endTransaction(0);//トランザクション.ロールバック
	}

	resultset = getResultset(select);
	if (resultset) {
		int i = 0;
		while (resultset[i] != '\0') {
			printf(DISPLAY_FORMAT, PIPE, 10, 30, resultset[i]);  // 出力  
			i++;
		}
	}

	ret = closeDb();
	if (ret != 0) {
		errMsg = getErrorMsg();
		printf("%s\n", errMsg); return;
	}
}
```

# 実行結果（1回目）
まず1回目です。デバッグ出力は無効化されていますので、結果セットだけがアプリケーション側でコンソール出力されています。
```
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |     <NULL> |     <NULL> |
 |     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |          3 |       Java |

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 10468) は、コード 0 で終了しました
```
開発言語テーブルへのレコードのインサートが成功していますので、結果セットは変化しています。
# 実行結果（2回目）
続けて同じSQLを投げてみます。今度は1回目でインサートされたレコードとPK制約違反でエラーになる想定です。
```
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |          3 |       Java |
 23000 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]制約 'PK_開発言語' の PRIMARY KEY 違反。オブジェクト 'dbo. 開発言語' には重複するキーを挿入できません。重複するキーの値は (7, 3) です。
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |          3 |       Java |

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 9864) は、コード 0 で終了しました。
```
エラーステータスコードとエラーメッセージの内容をアプリケーション側で出力できました。

# おわりに
道のりはまだ長いです。次は日付型のパラメータバインドの予定ですが、しばらくお休みします。

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
FUNC_DECLSPEC int closeDb();
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
//エラーメッセージを取得する
FUNC_DECLSPEC char* getErrorMsg();
```
クローズDBも自動コミットを無効化した状態で実行するとエラーとなることがわかりましたので、戻り値を返すように修正されています。

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

#define DEBUG
#undef  DEBUG
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
char* sqlErrorMsg;//エラーメッセージ

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
    RETCODE    rc;
    setlocale(LC_ALL, "Japanese_Japan.932");
#ifdef DEBUG
    printf("DSText --> %s", datasouce);
    printf("\n");
#endif
    //接続を開く
    rc = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //パラメータカウンタを初期化
    resetCounters(0);
    paramsetStr = calloc(PARAM_CHAR_MAX, sizeof(char*));//文字列パラメータ配列を初期化
    if (!(paramsetStr)) {
        fprintf(stderr, "Out of memory!\n");
        return -100;
    }
    return SQL_SUCCESS;
}

//DBを閉じる
__declspec(dllexport) int closeDb() {
    RETCODE    rc;
    if (paramsetStr) {
        free(paramsetStr);  // パラメータ配列のメモリの解放
#ifdef DEBUG
        printf("paramsetStr --> free\n");
#endif
    }
    if (resultset) {
        free(resultset);  // 結果セット配列のメモリの解放  
#ifdef DEBUG
        printf("resultset --> free\n");
#endif
    }
    if (sqlErrorMsg) {
        free(sqlErrorMsg);  // エラーメッセージのメモリの解放  
#ifdef DEBUG
        printf("sqlErrorMsg --> free\n");
#endif
    }
    //接続を閉じる
    rc = closeConn(&henv, &hdbc);
#ifdef DEBUG
    if (rc == 0) {
        printf("SUCCESS CLOSE\n");
    }
    else {
        printf("ERROR CLOSE\n"); return;
    }
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return SQL_SUCCESS;
}

//SELECTを実行する
__declspec(dllexport) char** exec(char* select) {

    setlocale(LC_ALL, "Japanese_Japan.932");
#ifdef DEBUG
    printf("SQLText(char) --> ");
    int i = 0;
    while (select[i] != '\0') {
        printf("%c", select[i]);
        i++;
    }
    printf("\n");
    printf("SQLText --> %s", select);
    printf("\n");
#endif
    if (resultset) {
        free(resultset);  // 配列のメモリの解放  
#ifdef DEBUG
        printf("resultset --> free\n");
#endif
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
#ifdef DEBUG
    printf("paramCountInt --> %d\n", paramCountInt);
    printf("paramNumber --> %d\n", paramNumber);
#endif
    if (paramCountInt > PARAM_INT_MAX){
        fprintf(stderr, "Out of index!\n");
        return -100;
    }
#ifdef DEBUG
    printf("param --> %d\n", param);
#endif
    // Bind the parameters.  
    rc=SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER,
        10, 0, &paramInt[index], 0, &paramInd[index]);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramInd[index] = 0;
    paramInt[index] = param;
    return SQL_SUCCESS;
}

SQLINTEGER    paramStrInd[PARAM_CHAR_MAX];//最大10
//SQLパラメータ文字列をバインドする
__declspec(dllexport) int bindParameterStr(char* param) {
    //setlocale(LC_ALL, "Japanese_Japan.932");
    SQLRETURN    rc;
    int index = paramCountStr;
    paramCountStr++;
    paramNumber++;
#ifdef DEBUG
    printf("paramCountStr --> %d\n", paramCountStr);
    printf("paramNumber --> %d\n", paramNumber);
#endif
    if (paramCountStr > PARAM_CHAR_MAX) {
        fprintf(stderr, "Out of index!\n");
        return -100;;
    }

    paramsetStr[index] = calloc(getStringSize(param), sizeof(char));
    if (!(paramsetStr[index])) { return -1; }
#ifdef DEBUG
    printf("param --> %s\n", param);
#endif
    // Bind the parameters.  
    rc = SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR,
        getStringSize(param)-1, 0, paramsetStr[index], getStringSize(param), &paramStrInd[index]);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramStrInd[index] = SQL_NTS;
    strcpy_s((char*)paramsetStr[index] , getStringSize(param), param);
    return SQL_SUCCESS;
}

//結果セットを取得する
__declspec(dllexport) char** getResultset() {
    setlocale(LC_ALL, "Japanese_Japan.932");
#ifdef DEBUG
    printf("SQLText --> %s", statement);
    printf("\n");
#endif
    if (resultset) {
        free(resultset);  // 配列のメモリの解放  
#ifdef DEBUG
        printf("resultset --> free\n");
#endif
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
#ifdef DEBUG
    printf("SQLText --> %s", statement);
    printf("\n");
#endif
    SQLRETURN    rc;
    rc = SQLExecDirect(hstmt, statement, SQL_NTS);
#ifdef DEBUG
    printf("SQLExecDirect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    //パラメータカウンタを初期化
    resetCounters(1);
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return SQL_SUCCESS;
}

//自動コミットを設定する
__declspec(dllexport) int setAutoCommit(int sw) {
    
    SQLRETURN    rc;
    if (sw) {
#ifdef DEBUG
        printf("AutoCommit On --> %d\n", sw);
#endif
        rc = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, (int*)SQL_AUTOCOMMIT_ON, SQL_IS_INTEGER);
    }
    else {
#ifdef DEBUG
        printf("AutoCommit Off  --> %d\n", sw);
#endif
        rc = SQLSetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER);
    }
#ifdef DEBUG
    printf("SQLSetConnectAttr --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return SQL_SUCCESS;
}
//自動コミットを取得する
__declspec(dllexport) int getAutoCommit() {

    SQLRETURN    rc;
    SQLINTEGER   autocommit;
    rc = SQLGetConnectAttr(hdbc, SQL_ATTR_AUTOCOMMIT, &autocommit, 0, NULL);
#ifdef DEBUG
    printf("SQLGetConnectAttr --> %d\n", rc);
    printf("AutoCommit--> %d\n", autocommit);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return SQL_SUCCESS;
}
//トランザクションを終了する
__declspec(dllexport) int endTransaction(int sw) {

    SQLRETURN    rc,rc2;
    SQLSMALLINT   completionType;
    if (sw) {
        completionType = SQL_COMMIT;
#ifdef DEBUG
        printf("CommitTran  --> %d\n", completionType);
#endif
    }    else{
        completionType = SQL_ROLLBACK;
#ifdef DEBUG
        printf("RollbackTran  --> %d\n", completionType);
#endif
    }
    rc = SQLEndTran(SQL_HANDLE_DBC, hdbc, completionType);
#ifdef DEBUG
    printf("SQLEndTran  --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    rc2=setAutoCommit(1);
#ifdef DEBUG
    if (rc2 != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }
    return SQL_SUCCESS;
}


//エラーメッセージを取得する
__declspec(dllexport) char* getErrorMsg() {

    SQLCHAR SqlState[6], SqlMsg[SQL_MAX_MESSAGE_LENGTH];
    SQLINTEGER    NativeError;
    SQLSMALLINT   i, MsgLen;
    SQLRETURN     rc;
    SQLLEN numRecs = 0;
    if (sqlErrorMsg) {
        free(sqlErrorMsg);  // エラーメッセージのメモリの解放  
    }
    SQLGetDiagField(SQL_HANDLE_STMT, hstmt, 0, SQL_DIAG_NUMBER, &numRecs, 0, 0);
    int Stlength;
    i = 1;
    while (i <= numRecs && (rc = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt, i, SqlState, &NativeError,
        SqlMsg, sizeof(SqlMsg), &MsgLen)) != SQL_NO_DATA) {
        Stlength= MsgLen + 6 + 2;
        sqlErrorMsg = calloc(Stlength, sizeof(char));
        snprintf(sqlErrorMsg, Stlength, "%s %s", SqlState, SqlMsg);
        //最初の1件を返す
        return sqlErrorMsg;
    }
    return NULL;
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
#ifdef DEBUG
    printf("paramCountInt --> %d\n", paramCountInt);
    printf("paramCountStr --> %d\n", paramCountStr);
    printf("paramNumber --> %d\n", paramNumber);
#endif
}
//接続を開く
int openConn(HENV* henv, HDBC* hdbc, HSTMT* hstmt, SQLCHAR datasouce[]) {
    SQLRETURN    rc;

    //環境ハンドルを割り振る
    rc = SQLAllocEnv(henv);
#ifdef DEBUG
    printf("SQLAllocEnv --> %d\n", rc);
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //接続ハンドルを割り振る
    rc = SQLAllocConnect(*henv, hdbc);
#ifdef DEBUG
    printf("SQLAllocConnect --> %d\n", rc);
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    rc = SQLDriverConnect(*hdbc,
        NULL,
        datasouce,
        SQL_NTS,
        NULL,
        0,
        NULL,
        SQL_DRIVER_NOPROMPT);// SQL_DRIVER_COMPLETE_REQUIRED
#ifdef DEBUG
    printf("SQLConnect --> %d\n", rc);
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    rc = SQLAllocStmt(*hdbc, hstmt);
#ifdef DEBUG
    printf("SQLAllocStmt --> %d\n", rc);
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

 
    return 0;
}

//接続を閉じる
int closeConn(HENV* henv, HDBC* hdbc) {
    SQLRETURN    rc;

    //サーバーから切断
    rc = SQLDisconnect(*hdbc);
#ifdef DEBUG
    printf("SQLDisconnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //接続ハンドルの解放
    rc = SQLFreeConnect(*hdbc);
#ifdef DEBUG
    printf("SQLFreeConnect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    //環境ハンドルの解放
    rc = SQLFreeEnv(*henv);
#ifdef DEBUG
    printf("SQLFreeEnv --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
    if (!(rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO)) { return -1; }

    return 0;
}

//照会する
char** doSelect(HSTMT hstmt, SQLCHAR select[]) {
    SQLRETURN rc;

    rc = SQLExecDirect(hstmt, select, SQL_NTS);
#ifdef DEBUG
    printf("SQLExecDirect --> %d\n", rc);
    if (rc != SQL_SUCCESS) dispSQLStatus();
#endif
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
#ifdef DEBUG
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
#endif

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
