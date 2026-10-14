# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ0.5）」です。ステップ0.5とは最初のステップちょい手前を意味します。


[Cのdllのヘッダの書き方という記事](https://qiita.com/mylifewithviolin/items/5e93a9ed8f50db00f608)で単純なコンソール出力の機能をdll化してコンソールアプリから実行検証しましたが、本記事では前回までに確立したODBC接続、SELECT実行・結果表示、切断の実装をDLLにしてみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[前回記事（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。

# 配置情報
 ソリューション、プロジェクトの配置についてご説明します。
 こんな感じです。mssqlodbc32.hはConsoleApp側にもコピーして配置しています。
```
 C:.
│  mssqlodbc32.sln
│
├─ConsoleApp
│  │  ConsoleApp.vcxproj
│  │  consoleApp.c
│  │  mssqlodbc32.h
│  └─Debug
│
├─Debug
│      ConsoleApp.exe
│      ConsoleApp.pdb
│      mssqlodbc32.dll
│      mssqlodbc32.exp
│      mssqlodbc32.lib　←コンソールアプリ側のリンカ入力に設定
│      mssqlodbc32.pdb
│
└─mssqlodbc32
    │  mssqlodbc32.vcxproj
    │  mssqlodbc32.c
    │  mssqlodbc32.h
    └─Debug
```

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているソースコードの流用です。どのように改変していったかは前回以前の記事をご参照ください。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16


 # C状態での変更点
今回はmainの代わりにdllexportされたexec()をエントリポイントとしています。中身は前回記事とまったく同一で、引用している下請け関数も同一です。

```c:mssqlodbc32.c
#define _EXPORTING

#include "mssqlodbc32.h"

__declspec(dllexport) void exec(){
    RETCODE    ret;
    HENV    henv;    //環境ハンドル
    HDBC    hdbc;    //接続ハンドル
    HSTMT   hstmt;   //ステートメントハンドル

    SQLWCHAR datasouce[] = L"Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
    SQLWCHAR select[] = L"SELECT * FROM 言語名";

    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }
    else {
        printf("ERROR OPEN\n"); return;
    }
    //照会する
    doSelect(henv, hdbc, hstmt, select);

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

実行検証用のCのコンソールアプリケーション
```c:consoleApp.c
#include<stdio.h>

#include "mssqlodbc32.h"

void main() {
	exec();
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

FUNC_DECLSPEC void exec();
```

 # 実行結果
 それでは実行してみます。
 ```cmd:
 SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLExecDirect --> 0
| 言語ID        | 言語名                  | 公開年         | よみがな                  |
|           1 |                 Ｍｉｎｄ |        1985 |                 まいんど  |
|           2 |                  ＴＴＳ |        2000 |             てぃーてぃーえす  |
|           3 |                 ひまわり |        2001 |                 ひまわり  |
|           4 |                 ドリトル |        2003 |                 どりとる  |
|           5 |                 なでしこ |        2004 |                 なでしこ  |
|           6 |                 プロデル |        2007 |                 ぷろでる  |
|           7 |     Mind for Android |        2012 |        まいんどふぉーあんどろいど  |
|           8 |                  スミレ |        2018 |                  すみれ  |
|           9 |                なでしこ３ |        2018 |               なでしこさん  |
|          10 |                 スミレ畑 |        2020 |               すみればたけ  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\mssqlodbc32\Debug\ConsoleApp.exe (プロセス 15476) は、コード 0 で終了しました。
デバッグが停止したときに自動的にコンソールを閉じるには、[ツール] -> [オプション] -> [デバッグ] -> [デバッグの停止時に自 動的にコンソールを閉じる] を有効にします。
このウィンドウを閉じるには、任意のキーを押してください...
 ```
 無事に結果が返りました。ここまではある意味、事前検証されていたので、予想どおりの結果です。しかし、ステップ1.0に到達するには、現在の１枚岩的状態をODBC接続、SELECT実行・結果表示、切断の３つのエクスポート関数に分割する必要があります。

今回の検証目的としては、ODBC接続、SELECT実行・結果表示、切断を３つの関数に分けた際に、これらの３関数で連携している環境ハンドラ、接続ハンドラ、ステートメントハンドラといったドライバが採番している識別番号をクライアントには返したくないという課題があります。

これらの変数をDLLのモジュール変数とした場合、それらはグローバルヒープのような空間に保持されるのか、それとも関数コールの都度リセットされてしまうのかといったあたりが気がかりです。

この点を検証するため、本来は接続情報やSELECT文はクライアントから与えるものなのですが、今回はその点ざっくり割愛して現状のままDLL側での埋め込みとします。環境ハンドラ、接続ハンドラ、ステートメントハンドラをクライアントに返さず保持できるか検証してみます。


 # C状態での変更点（関数分割）
ハンドラ３つはグローバル変数としました。
ODBC接続、SELECT実行・結果表示、切断の３つのエクスポート関数に分割しました。
```c:mssqlodbc32.c
#define _EXPORTING

#include "mssqlodbc32.h"

HENV    henv;    //環境ハンドル
HDBC    hdbc;    //接続ハンドル
HSTMT   hstmt;   //ステートメントハンドル

__declspec(dllexport) void openDb() {
    SQLWCHAR datasouce[] = L"Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
    RETCODE    ret;
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
__declspec(dllexport) void exec(){

    SQLWCHAR select[] = L"SELECT * FROM 言語名";
    //照会する
    doSelect(henv, hdbc, hstmt, select);
    return;
}
```

実行検証用のCのコンソールアプリケーション
```c:consoleApp.c
#include "mssqlodbc32.h"

void main() {
	openDb();
	exec();
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

FUNC_DECLSPEC void exec();

FUNC_DECLSPEC void closeDb();
```

 # 実行結果
 それでは実行してみます。

 
 結果のイメージは同一なので割愛しますが、いちおう動きました。スレッドセーフなのかどうかがちょっと今回判別がついておりませんが、いったんこれでよしとします。

  # おわりに
C言語でのdll作成の情報は少ないので何かの参考になれば幸いです。また、次回は本来のお題の日本語プログラミング言語MindからCのdllを介してSQLServerにクエリするに入って参ります。
