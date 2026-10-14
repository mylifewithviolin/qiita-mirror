# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ1.1）」です。ステップ1.1とは最初のステップちょい先を意味します。

[（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)ではODBC接続、SELECT実行・結果表示、切断の実装をDLLにして、コンソールアプリケーションから単純に実行しました。今回はSELEC文をコンソールアプリケーションから渡せるようにします。

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

# 配置情報
 ソリューション、プロジェクトの配置については[（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。
 
# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているソースコードの流用です。どのように改変していったかは（ステップ0.5）以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16


# C状態での変更点
exec関数の引数をワイド文字のポインタにして、内部に文字列のコンソール出力を追加。ロケールはSJISにしました。

```c:mssqlodbc32.c
#define _EXPORTING

#include "mssqlodbc32.h"

__declspec(dllexport) void exec(wchar_t* select){
    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText --> %ws\n", select);
    //照会する
    doSelect(henv, hdbc, hstmt, select);
    return;
}
```
実行検証用のCのコンソールアプリケーション
```c:consoleApp.c
#include "mssqlodbc32.h"

void main() {
	wchar_t select[] = L"SELECT * FROM 言語名";
	openDb();
	exec(select);
	closeDb();
}
```

Cのdll（ダイナミックリンクライブラリ）のヘッダファイル
```c:mssqlodbc32.h
#pragma once

#ifdef _EXPORTING
#define FUNC_DECLSPEC    __declspec(dllexport)
#else
#define FUNC_DECLSPEC    __declspec(dllimport)
#endif

FUNC_DECLSPEC void openDb();

FUNC_DECLSPEC void exec(wchar_t* select);

FUNC_DECLSPEC void closeDb();
```

 # 実行結果
 それでは実行してみます。

```
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText --> SELECT * FROM 言語名
SQLExecDirect --> 0
| 言語ID        | 言語名                  | 公開年         | よみがな                  |
|           1 |                 Ｍｉｎｄ |        1985 |                 まいんど  |
|           2 |                  ＴＴＳ |        2000 |             てぃーてぃーえす  |
|           3 |                 ひまわり |        2001 |                 ひまわり  |
|           4 |                 ドリトル |        2003 |                 どりとる  |
|           5 |                 なでしこ |        2004 |                 なでしこ  |
|           6 |                 プロデル |        2007 |                 ぷろでる  |
|           7 |     Mind fro Android |        2012 |        まいんどふぉーあんどろいど  |
|           8 |                  スミレ |        2018 |                  すみれ  |
|           9 |                なでしこ３ |        2018 |               なでしこさん  |
|          10 |                 スミレ畑 |        2020 |               すみればたけ  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
```
動きました。SELECT文の日本語も正常に引き渡されているようでした。

  # おわりに
C言語でのdll作成の情報は少ないので何かの参考になれば幸いです。また、次回は接続文字列や戻り値を返すように変更して参ります。結果セットを返すようになるのはだいぶ先です。
