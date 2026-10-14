# はじめに
この記事のお題は「CでデータベースSQLServer2022にクエリーしてみる（ステップ1.8）」です。ステップ1.8とはクエリーのパラメータ化対応（整数+文字列）をぼちぼち行っています。

ODBCなので、低レイヤーよりで実装するとこうなんだくらいの感覚でサンプルとしてお読みいただければ幸いです。


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
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を
ソースコードは[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.7）クエリーのパラメータ化対応（整数のみ）
](https://qiita.com/mylifewithviolin/items/4c0d0423b909730641c8)以前の記事をご参照ください。

learn.microsoft.comの日本語サイトの下記に公開されているC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

ODBCプログラミングの情報は古いバージョンに準拠した内容しか記載されていない場合が多いので、念のためODBC規格元のマイクロソフトの関数レファレンスは読んでおいた方がよいです。上記のサンプルはパラメータバインドは使用していないようでした。
下記の記事は結果としてたいへん参考になりました。他に記述例のサンプルがみあたりませんでした。整数と文字列のパラメータの実装例が例示してあります。

https://learn.microsoft.com/ja-jp/sql/odbc/reference/develop-app/binding-parameter-markers?view=sql-server-ver16

## C状態での変更点
下記のエクスポート関数を追加しました。
**bindParameterStr** 　　SQLパラメータ文字列をバインドする

また従来関数のDBを開く**openDb**の中で、暫定的に文字列ポインタ配列の初期化コードを、**closeDb**の中で同解放を追記しています。
**bindParameterInt** 　　SQLパラメータ整数をバインドする
の内容も少し調整しています。

### bindParameterStr
文字列型のパラメータをバインドします。ユーザーアプリケーション側にSQLBindParameterの引数群を露出させないため、型別の関数を用意する予定の第2弾です。
また、今回の実装でも文字列ポインタ配列が最大10までという制約を持つことになります。整数配列も文字列ポインタ配列もメモリ量はたいしたことないので10は少なすぎるかもしれません。

```c:mssqlodbc32.c
int paramCountStr;//文字列パラメータカウンタ 上限あり
// パラメータ配列を動的に確保する  
char** paramsetStr;
#define PARAM_CHAR_MAX 10

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
    if (rc != SQL_SUCCESS) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramStrInd[index] = SQL_NTS;
    strcpy_s((char*)paramsetStr[index] , getStringSize(param), param);
    return 0;
}
```
### openDb
 「DBを開く」**openDb**の中で、暫定的に初期化コードを追記しています。
```diff_c:mssqlodbc32.c
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
   paramNumber = 0;//パラメータナンバを初期化
+  paramCountInt = 0;//整数パラメータカウンタを初期化
+  paramCountStr = 0;//文字列パラメータカウンタを初期化
+  paramsetStr = calloc(PARAM_CHAR_MAX, sizeof(char*));//文字列パラメータ配列を初期化
+  if (!(paramsetStr)) {
+    fprintf(stderr, "Out of memory!\n");
+    return -100;
+  }
    return 0;
}
```

### closeDb
「DBを閉じる」**closeDb**の中でメモリ解放を追記しています。

```diff_c:mssqlodbc32.c
//DBを閉じる
__declspec(dllexport) void closeDb() {
    RETCODE    ret;

+    free(paramsetStr);  // 配列のメモリの解放  
    printf("paramsetStr --> free\n");

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
 ```

 ### bindParameterInt
整数型のパラメータをバインドします。前回はこれしかなかったので、ODBCのプレースフォルダの順番カウンタが配列カウンタを兼ねていましたが、今回は文字列用と整数用でそれぞれ最大値を持ちますので、カウンタをわけています。

```diff_c:mssqlodbc32.c
#define PARAM_INT_MAX 10          
SQLINTEGER    paramInt[PARAM_INT_MAX];//最大10
SQLINTEGER    paramInd[PARAM_INT_MAX];//最大10
//SQLパラメータ整数をバインドする
__declspec(dllexport) int bindParameterInt(int param){
    SQLRETURN    rc;
+   int index = paramCountInt;
+   paramCountInt++;
    paramNumber++;
+   printf("paramCountInt --> %d\n", paramCountInt);
    printf("paramNumber --> %d\n", paramNumber);
    if (paramCountInt > PARAM_INT_MAX){
        fprintf(stderr, "Out of index!\n");
        return -100;
    }
    printf("param --> %d\n", param);
    // Bind the parameters.  
    rc=SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER,
        10, 0, &paramInt[index], 0, &paramInd[index]);
    if (rc != SQL_SUCCESS) { return -1; }
    //バッファをバインドした後に値をセットしてOK
    paramInd[index] = 0;
    paramInt[index] = param;
    return 0;
}
```
 ## 実行検証用のCのコンソールアプリケーション
SELECT文のWHERE句の条件をよみがなのLIKEに変更しています。ワイルドカードの%は下図のようにパラメータプレースフォルダ?の外で文字列連結すると動作しました。パラメータ文字列の中に記述すると動きませんでした。（条件不成立となって項目名だけが返ってきました。）

```diff_c:consoleApp.c
#include "mssqlodbc32.h"

#define DISPLAY_FORMAT      "%c %*.*s "
#define PIPE                '|'

void main() {
	char datasouce[] = "Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
-	char select[] = "SELECT * FROM 言語名 WHERE 言語ID IN (?,?)";
+	char select[] = "SELECT * FROM 言語名 WHERE よみがな LIKE ? + '%'";

	int ret=openDb(datasouce);
	if (ret == 0) {
		printf("SUCCESS OPEN\n");
 		setStatement(select);
-		bindParameterInt(1);
-		bindParameterInt(7);
+       bindParameterStr("まいんど");
		char** resultset=getResultset();
		if (resultset) {
			int i = 0;
			while (resultset[i] != '\0') {
				printf(DISPLAY_FORMAT, PIPE,10,30, resultset[i]);  // 出力  
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
```diff_c:mssqlodbc32.h
#pragma once

#ifdef _EXPORTING
#define FUNC_DECLSPEC    __declspec(dllexport)
#else
#define FUNC_DECLSPEC    __declspec(dllimport)
#endif

FUNC_DECLSPEC void openDb(char* datasouce);
FUNC_DECLSPEC char** exec(char* select);
FUNC_DECLSPEC void closeDb();
FUNC_DECLSPEC void setStatement(char* stmt);
FUNC_DECLSPEC int bindParameterInt(int param);
+FUNC_DECLSPEC int bindParameterStr(char* param);
FUNC_DECLSPEC char** getResultset();

```
# 実行結果
では実行してみましょう。
 ```
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
paramCountStr --> 1
paramNumber --> 1
param --> まいんど
SQLText --> SELECT * FROM 言語名 WHERE よみがな LIKE ? + '%'
SQLExecDirect --> 0
|     言語ID |     言語名 |     公開年 |   よみがな |
 |          1 |   Ｍｉｎｄ |       1985 |   まいんど |
 |          7 | Mind for Android |       2012 | まいんどふぉーあんどろいど |
 paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 9196) は、コード 0 で終了しました。
```
無事に返ってきました:tada:

# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、次回はトランザクション制御に進行します。たぶん。（既にわりと書いてあります。）
