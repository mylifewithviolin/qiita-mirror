# はじめに
この記事のお題はMindでデータベースSQLServer2022にクエリーしてみる（ステップ1.2）」です。ステップ1.2とはまだ最初のステップで足踏みを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.1）dll化select文渡し](https://qiita.com/mylifewithviolin/items/1e9a2bb4d4936f82993d)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態からSELECT文を引数渡しするようにしていますので、引き続きそのエクスポート関数をMindから実行してみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.07 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[C（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。

# お題のソースコード
## C
C側のソースコード、プロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)と[C（ステップ1.1）dll化select文渡し](https://qiita.com/mylifewithviolin/items/1e9a2bb4d4936f82993d)をご参照ください。

## Mind
Mindのソースは[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。

# C側の変更点

C側のエクスポート関数の引数を通常の文字ポインタにして、内部に文字配列のコンソール出力を追加してMind文字列がどのようにわたっているのか詳しくモニタできるようにしました。ロケールはSJISのままです。

```c:mssqlodbc32.c
#define _EXPORTING

#include "mssqlodbc32.h"

__declspec(dllexport) void exec(char* select) {

    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText(char) --> ");
    int i = 0;
    while (select[i] != '\0') {
        printf("%c", select[i]);
        i++;
    }
    printf("\n");
    printf("SQLText --> %ws", (wchar_t*)select);
    printf("\n");
    //照会する
    doSelect(henv, hdbc, hstmt, (SQLWCHAR*)select);

    return;
```

実行検証用のCのコンソールアプリケーション
```c:consoleApp.c
#include "mssqlodbc32.h"

void main() {
	wchar_t select[] = L"SELECT * FROM 言語名 WHERE 言語ID=1";
	openDb();
	exec((char*)select);
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

FUNC_DECLSPEC void exec(char* select);

FUNC_DECLSPEC void closeDb();
```
# 実行結果
## Cコンソールアプリ
 それではまず検証用のCコンソールアプリで実行してみます。
 ```
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText(char) --> S
SQLText --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLExecDirect --> 0
| 言語ID        | 言語名                  | 公開年         | よみがな                  |
|           1 |                 Ｍｉｎｄ |        1985 |                 まいんど  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
 ```
SELECT文は正常に実行されましたが、CHAR配列のループは正常に出力されませんでした。コンソールアプリ側ではワイド文字でリテラルをつくって、エクスポート関数を通過させるときだけCHARポインタでキャストして警告を抑止しているだけなので、中身はワイド文字のままですね。ワイド文字用の書式でのコンソール出力も正常に出力されています。

## Mind
ではMindから実行してみます。MindのソースはSELECT文リテラルにWHERE句追加しただけです。Mind文字列のNULL終端は前回と同じリテラル埋め込みです。

```mind:mssqlodbc.src
メインとは
	SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID=1&00&」
	API初期処理しておき

	DB接続し
	SELECTで　SQL実行し
	DB切断し

	API破棄処理すること。
```

では実行します。
 ```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLText -->
SQLExecDirect --> -1
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
CHAR配列のループは正常に出力されました。Mind文字列は正常に終端されているようです。
ちなみにエクスポート関数の引数型をワイド文字のポインタのままの場合は、下図のように文字化けしていました。
```
SQLText(char) --> SLC  RM血膜ｨ
```

C側ではSQLServerのODBCドライバに対応したODBC関数に渡す日本語文字列はSQLWCHAR型でキャストしているので、単なるキャストで実行できるようにするには文字列自体がワイド文字でなければならないようです。

```
    //照会する
    doSelect(henv, hdbc, hstmt, (SQLWCHAR*)select);
```

従って、この状況を打開するにはMind側もユニコード文字に変換する必要がありそうです。実は@killyさんのご支援をいただいており、srclib/uniencode.srcを使えばMind文字列をユニコードに変換できるという情報を事前にいただいていたのですがmind-for-windows-8.0.08アーカイブのsrclibは空だったというのが本日のオチでございます。

```
 C:\environment\mind-for-windows-8.0.08\pmind\srclib のディレクトリ

2018/12/01  09:48    <DIR>          .
2024/01/13  00:09    <DIR>          ..
               0 個のファイル                   0 バイト
               2 個のディレクトリ  22,092,648,448 バイトの空き領域

C:\environment\mind-for-windows-8.0.08\pmind\srclib>
```
mind-for-linux-8.0.08.tgzのsrclibも空っぽい:joy:
```
\\wsl.localhost\Ubuntu\home\puremind\pmind\srclib
```
# おわりに
ごめんなさい。タイムアウトです。Mind文字列のユニコード化の環境が整うまでは、日本字のやりとりはいったん棚上げというのもありかもしれません。

https://qiita.com/killy/items/5107d9d28df249e4aea7
