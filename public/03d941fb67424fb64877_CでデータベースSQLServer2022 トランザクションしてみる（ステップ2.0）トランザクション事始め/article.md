# はじめに
この記事のお題は「CでデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）」です。ステップ2.0とはODBCトランザクション制御の事始めを言います。

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
こんなテーブル構成のデータベースを作成しております。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)


# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を
ソースコードは[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.8）クエリーのパラメータ化対応（整数+文字列）](https://qiita.com/mylifewithviolin/items/558d182ae1845547d00a)以前の記事をご参照ください。

learn.microsoft.comの日本語サイトの下記に公開されているC++用ソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

ODBCプログラミングの情報は古いバージョンに準拠した内容しか記載されていない場合が多いので、念のためODBC規格元のマイクロソフトの関数レファレンスは読んでおいた方がよいです。上記のサンプルにはトランザクション制御の実装はなさそうでした。

https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqlendtran-function?view=sql-server-ver16

https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqlsetconnectattr-function?view=sql-server-ver16

 ## 実行検証用のCのコンソールアプリケーション
今回の記事より、実行検証用のCのコンソールアプリケーション上で実行するSQLコマンドが複数になりましたので、まずコンソールアプリのMain関数の様子からご紹介します。

最初、更新前に結合を含むSELECT文を1回実行し、その後トランザクションを開始し、INSERT文を1回実行し、UPDATE文を1回実行し、、DELETE文を1回実行し、その後エラーがなければトランザクションをコミット、エラーがあればトランザクションをロールバックすると書いています。JavaやC#ではC++由来のtry catch文で例外処理として書いているところですが、関数戻り値で書いています。
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
		printf("ERROR OPEN\n"); return;
	}
	printf("SUCCESS OPEN\n");

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
		if (ret == 0) {
			setStatement(delete);
			bindParameterInt(1);
			bindParameterInt(7);
			ret = execCommand();
		}
	}
	if (ret == 0) {
		endTransaction(1);//トランザクション.コミット
	}else {
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

	closeDb();
}
```

# 実行結果
## トランザクション成功コミット
では、今回はDLL側ソースの改変点をご説明する前に、まず実行してみましょう。
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
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど |     <NULL> |     <NULL> |
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
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
CommitTran  --> 0
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
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android |   まいんど |          3 |       Java |
 paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 5240) は、コード 0 で終了しました。
```
無事に返ってきました:tada:
トランザクション前後のSELECTの結果の違いが大事です。デバッグ用の出力が増えてしまってわかりずらくなっていますが、以下にSELECTの結果だけを抽出します。

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
トランザクションは下記の内訳のためすべて正常に作用したことがわかります。
1)開発言語テーブルに言語ID=7、開発言語ID=3のレコードを挿入したのでMind for Androidの開発言語がNULLからJavaに変わった
2)言語名テーブルの言語ID=7のよみがなを更新したので、Mind for Androidのよみがなが「まいんどふぉーあんどろいど」から「まいんど」に変わった。
3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除したので、Mindの開発言語Forthの行が消えた。

## トランザクション失敗ロールバック
続いて、ロールバックを検証します。3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除する際に、存在しない列名言語ID2=1をあたえてここで失敗を起こします。各テーブルのレコードの状態は初期状態に戻しおきます。
```c:consoleApp.c
	char delete[] = "DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?";
```

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
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど |     <NULL> |     <NULL> |
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
 |          7 | Mind for Android |   まいんど |          3 |       Java |
 paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 9704) は、コード 0 で終了しました。
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
 |          7 | Mind for Android |   まいんど |          3 |       Java |
```
削除は失敗していますが、挿入と更新は結果が反映されたままになってしましました。トランザクションはロールバックしていないことがわかります。

ログの出力上はオートコミットはOFFにされ（SQLSetConnectAttrが成功）、 RollbackTranでSQLEndTranが成功とはなっています。
```
 AutoCommit Off  --> 0
 SQLSetConnectAttr --> 0
//トランザクション
 RollbackTran  --> 1
SQLEndTran  --> 0
AutoCommit On --> 1
SQLSetConnectAttr --> 0
```
ODBC関数にBeginTranのようなものはなく、自動コミットモードをOFFにすると、トランザクションの開始となり、トランザクションのコミットとロールバックは直接SQLコマンドでCOMMIT、ROLLBACKを実行してはならず、必ずODBC関数のEndTranを介して行うにという仕様に準じています。

# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、実はロールバックが実行されない問題の以前で、トランザクションが正常に実行されるところまで到達するのにいくつかの実装課題がありました。開いたカーソルは明示的に閉じないといけないとか。わかってしまえばあたりまえのことですが、ODBC関数がどのくらいやってくれるのかは未知なので。サンプルには記述はなかったようです。いいわけ。

ということからログ出力の実装も増やしてSQLERRORとしてなにが起きたかを出力するようにしたとかあるのですが、いったんソースコードの解説はこのロールバック問題が解決したらあらためて行います。

https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqlclosecursor-function?view=sql-server-ver16


# 2024/01/29追記
とりあえずこのバージョンでのSQLコマンドの実行状態をSQLServerプロファイラでキャプチャしてみました。イベントクラスにはトランザクション関連イベントを追加しています。
トランザクションは開始されていましたが、ロールバックのつもりがEndTran関数へのcompletionTypeが常にコミットになっている凡ミスでした。ちょっと不細工でしたが解決してよかったよかった。SQLServerプロファイラけっこう好きです。


