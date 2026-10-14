# はじめに
この記事のお題はMindでデータベースSQLServer2022にクエリーしてみる（ステップ1.3）」です。ステップ1.3とはまだ最初のステップのあたりを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態から接続文字列とSELECT文をSJISで受け取り内部的に正常動作するようにしましたので、それらをMindから実行してみます。

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
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を
ソースコードは[C（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)をご参照ください。

## Mind
Mindのソース全体像は[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。

Mindのソースはメインは接続文字列を定義し、「DB接続」がスタックよりそれを受け取れるようにしました。Mind文字列のNULL終端は前回と同じリテラル埋め込みです。

```mind:mssqlodbc.src
DB接続とは
	openDbで　アドレス指定でＡＰＩ呼出１する。
SQL実行とは
	execで　アドレス指定でＡＰＩ呼出１する。
DB切断とは
	$$NULLと closeDbで　アドレス指定でＡＰＩ呼出１する。

メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;&00&」
	SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID=1&00&」

	API初期処理しておき

	datasourceで　DB接続し
	SELECTで　SQL実行し

	DB切断し
	API破棄処理すること。
```

# 実行結果
では実行します。
 ```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLText --> SELECT * FROM 言語名 WHERE 言語ID=1
SQLExecDirect --> 0
| 言語ID      | 言語名               | 公開年      | よみがな              |
|           1 |             Ｍｉｎｄ |        1985 |             まいんど  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事にMind文字列の接続情報とSELECT文で正常動作しました！:tada:

# おわりに
Mind側で文字列のユニコード化する方向性は環境が整うまでおあずけとし、次回は戻り値の受け取りに進行します。
