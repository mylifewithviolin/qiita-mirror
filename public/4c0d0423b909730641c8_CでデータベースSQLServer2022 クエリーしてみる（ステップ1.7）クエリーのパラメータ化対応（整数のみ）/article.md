# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ1.7）」です。ステップ1.7とは最初のステップのまだまだ道半ばを意味します。

ODBCなので、SQLServer以外のオープンソースDB、MySQL、PostgreSQLにも接続してみてよろこんでいましたが、ついにやりたくはない課題、クエリーのパラメータ化対応です。JavaのMyBatisとか、.NETのEntityFrameworkとか、便利な機能満載の環境に慣れきってしまうと、けっこう難儀な実装が予想されます。業務系システムエンジニアやデベロッパーは通常このあたりには力を使わないので、低レイヤーよりで実装するとこうなんだくらいの感覚でサンプルとしてお読みいただければ幸いです。


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
ソースコードは[C（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)と[C（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)と[CでデータベースMySQL8.3 クエリーしてみる（ステップ1.6）結果セット文字列返し書式解除](https://qiita.com/mylifewithviolin/items/46a7fde102c7e883f7b4)をご参照ください。

learn.microsoft.comの日本語サイトの下記に公開されているC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

ODBCプログラミングの情報は古いバージョンに準拠した内容しか記載されていない場合が多いので、念のためODBC規格元のマイクロソフトの関数レファレンスは読んでおいた方がよいです。上記のサンプルはパラメータバインドは使用していないようでした。

 https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqlbindparameter-function?view=sql-server-ver16

https://learn.microsoft.com/ja-jp/sql/odbc/reference/develop-app/binding-parameter-markers?view=sql-server-ver16

## C状態での変更点
下記のエクスポート関数を追加しました。
**setStatement** 　　　　ステートメントをセットする
**bindParameterInt** 　　SQLパラメータ整数をバインドする
**getResultset**     　　　　 結果セットを取得する
また従来関数のDBを開く**openDb**の中で、暫定的にパラメータナンバの初期化コードを追記しています。
### setStatement
パラメータのプレースフォルダを保持するSQL文を保持しておきます。

```c:mssqlodbc32.c
char* statement;//パラメータ化ステートメント

//ステートメントをセットする
__declspec(dllexport) void setStatement(char* stmt) {
    statement=stmt;
}
```
### bindParameterInt
整数型のパラメータをバインドします。ユーザーアプリケーション側にSQLBindParameterの引数群を露出させないため、型別の関数を用意する予定です。今回は整数のみ。
また、関数レファレンスのサンプルコードではバインドする変数を固定で宣言していますが、実際にはパラメータ数不定となるので、動的にバッファ域を確保する感じになっていくと思われます。今回は簡易版ということで整数配列でおちゃを濁しています。今回の実装では整数パラメータが最大10までという制約を持つことになります。

```c:mssqlodbc32.c
int paramCount;//パラメータカウント ODBCは順序依存
#define INT_PARAM_MAX 10   //最大10       
SQLINTEGER    paramInt[INT_PARAM_MAX];
SQLINTEGER    paramInd[INT_PARAM_MAX];

//SQLパラメータ整数をバインドする
__declspec(dllexport) int bindParameterInt(int param){
    SQLRETURN    rc;
    int index = paramNumber;
    paramNumber++;
    if (paramNumber > INT_PARAM_MAX){
        fprintf(stderr, "Out of index!\n");
        exit(-100);
    }
    paramInd[index] = 0;
    printf("paramNumber --> %d\n", paramNumber);
    // Bind the parameters.  
    rc=SQLBindParameter(hstmt, paramNumber, SQL_PARAM_INPUT, SQL_C_ULONG, SQL_INTEGER,
        10, 0, &paramInt[index], 0, &paramInd[index]);
    if (rc != SQL_SUCCESS) { return -1; }

    paramInt[index] = param;
    return 0;
}
```

### getResultset
結果セットを取得するは、内部的には従来の doSelectをstatement変数を渡して実行しているだけです。
```c:mssqlodbc32.c
//結果セットを取得する
__declspec(dllexport) char** getResultset() {
    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText --> %s", statement);
    printf("\n");
    //照会する
    char** resultset = doSelect(henv, hdbc, hstmt, (SQLCHAR*)statement);

    return resultset;
}
```

### openDb
 従来関数のDBを開く**openDb**の中で、暫定的にパラメータナンバの初期化コードを追記しています。
```diff_c:mssqlodbc32.c
HENV    henv;    //環境ハンドル
HDBC    hdbc;    //接続ハンドル
HSTMT   hstmt;   //ステートメントハンドル

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
+   paramNumber = 0;//パラメータナンバを初期化
    return 0;
}
 ```

 ## 実行検証用のCのコンソールアプリケーション
SELECT文のIN句のリテラル数字２つをパラメータのプレースフォルダ?に書き換えています。このSELECT文文字列をDLL側にセットした後、整数型パラメータのバインド関数を２回実行してから、SELECT文を実行しています。整数型パラメータのバインド関数はエラーを返す場合がありますが、ここでは割愛しています。

```diff_c:consoleApp.c
#include "mssqlodbc32.h"

#define DISPLAY_FORMAT      "%c %*.*s "
#define PIPE                '|'

void main() {
	char datasouce[] = "Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
+	char select[] = "SELECT * FROM 言語名 WHERE 言語ID IN (?,?)";
-	char select[] = "SELECT * FROM 言語名 WHERE 言語ID IN (1,7)";

	int ret=openDb(datasouce);
	if (ret == 0) {
		printf("SUCCESS OPEN\n");
+ 		setStatement(select);
+		bindParameterInt(1);
+		bindParameterInt(7);

+		char** resultset=getResultset(select);
-		char** resultset=exec(select);
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
FUNC_DECLSPEC void setStatement(char* stmt);
FUNC_DECLSPEC int bindParameterInt(int param);
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
paramNumber --> 1
paramNumber --> 2
SQLText --> SELECT * FROM 言語名 WHERE 言語ID IN (?,?)
SQLExecDirect --> 0
|     言語ID |     言語名 |     公開年 |   よみがな |
 |          1 |   Ｍｉｎｄ |       1985 |   まいんど |
 |          7 | Mind for Android |       2012 | まいんどふぉーあんどろいど |
 resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 10788) は、コード 0 で終了しました。
```
無事に返ってきました:tada:

# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、次回はトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。
