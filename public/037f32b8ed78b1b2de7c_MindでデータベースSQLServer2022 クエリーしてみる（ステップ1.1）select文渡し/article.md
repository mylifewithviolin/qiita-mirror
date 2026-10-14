# はじめに
この記事のお題はMindでデータベースSQLServer2022にクエリーしてみる（ステップ1.1）」です。ステップ1.1とはまだ最初のステップで足踏みを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.1）dll化select文渡し](https://qiita.com/mylifewithviolin/items/1e9a2bb4d4936f82993d)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態からSELECT文を引数渡しするようにしていますので、今回はそのエクスポート関数をMindから実行してみます。

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
Mindのソースは下記のとおりです。

### メイン
まずメインです。なるべくシンプルな雰囲気になるようにしています。Mind文字列のNULL終端はいちばんお手軽な方法のやつです。

```mind:mssqlodbc.src
メインとは
	SELECTは　　　文字列定数　「SELECT * FROM 言語名&00&」
	API初期処理しておき

	DB接続し
	SELECTで　SQL実行し
	DB切断し

	API破棄処理すること。
```
「API初期処理」と「API破棄処理」はCのDLLをロードして関数アドレスを取得する処理とDLLをアンロードする処理です。
### API初期処理
```mind:mssqlodbc.src
API初期処理とは　（・　→　・）

　　　　「ODBCライブラリをロードする」を　一行表示し
　　　　ODBCライブラリをロードし　偽？　ならば 「ロード失敗」を　一行表示し　終り
　　　　 つぎに
　　　　「ロード成功」を　一行表示し

　　　　「関数アドレス群を取得」を　一行表示し
　　　　ODBC関数アドレス群を取得し　エラー？　ならば 「取得失敗」を　一行表示し　終り
　　　　 つぎに
　　　　「取得成功」を　一行表示する。
```
### SQL実行
```mind:mssqlodbc.src
SQL実行とは
	execで　アドレス指定でＡＰＩ呼出１する。
```
その他のソースコードは[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)をご参照ください。

# 実行結果
それでは実行してみます。ほんとに動くのか！？
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
SQLText --> SQLExecDirect --> -1
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
動きませんでした！？:joy:　C側はSELECT文を認識していないようです。

```c:mssqlodbc32.c
#define _EXPORTING

#include "mssqlodbc32.h"

__declspec(dllexport) void exec(wchar_t* select){
    setlocale(LC_ALL, "Japanese_Japan.932");
    printf("SQLText --> %ws\n", select);//☆この時点で文字列が出力されていない
    //照会する
    doSelect(henv, hdbc, hstmt, select);
    return;
}
```
# おわりに
ごめんなさい。タイムアウトです。次回は問題解決を試みます。MindはANSI系のSJISかもしれないのでC側でワイド文字とか使っちゃいけないのかもしれません。
