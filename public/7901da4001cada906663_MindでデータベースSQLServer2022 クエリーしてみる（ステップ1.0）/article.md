# はじめに
この記事のお題はMindでデータベースSQLServer2022にクエリーしてみる（ステップ1.0）」です。ステップ1.0とは最初のステップを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ0.5）dll化](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにしていますので、今回はそのエクスポート関数をMindから実行してみます。

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
テーブル構成は[（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。

# お題のソースコード
## C
C側のソースコード、プロジェクト配置構成は[（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## Mind
Mindのソースは下記のとおりです。

### メイン
まずメインです。なるべくシンプルな雰囲気になるようにしています。
```mind:mssqlodbc.src
メインとは

	API初期処理しておき

	DB接続し
	SQL実行し
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
　　　　ODBC関数アドレス群を取得し
　　　　「取得成功」を　一行表示する。
```
### API破棄処理
```mind:mssqlodbc.src
API破棄処理とは　（・　→　・）
　　　　「ODBCライブラリを破棄する」を　一行表示し
　　　　ODBCライブラリを破棄する。
```

DB接続し、SQL実行し、DB切断するは、API関数をそれぞれ実行している箇所です。
### DB接続
```mind:mssqlodbc.src
DB接続とは
	$$NULLと openDbで　アドレス指定でＡＰＩ呼出１する。
```
### SQL実行
```mind:mssqlodbc.src
SQL実行とは
	$$NULLと execで　アドレス指定でＡＰＩ呼出１する。
```
### DB切断
```mind:mssqlodbc.src
DB切断とは
	$$NULLと closeDbで　アドレス指定でＡＰＩ呼出１する。
```

# 実行結果
ソースコードの説明はここまでとして、まずは実行してみます。ほんとに動くのか！？

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
ODBCライブラリを破棄する

C:\pmind\sample>
```
 無事に結果が返りました。:tada:Mindで（厳密にはまだコンソール出力しているのはC側ですが）SQLが返るの初めてみました！:joy:

# お題のソースコード（下働き部分）
「API初期処理」は下働きとして下記の「ODBCライブラリをロード」と」ODBC関数アドレス群を取得」を実行しています。

### ODBCライブラリをロード
```mind:mssqlodbc.src
ODBCライブラリをロードとは　（・　→　真偽）
     "C:\developments\mssqlodbc32\Debug\mssqlodbc32.dll"で　モジュールをロードし　
　　 DLLに　入れ
     DLLが　ゼロ以外を　返すこと。
```

### ODBC関数アドレス群を取得
```mind:mssqlodbc.src
ODBC関数アドレス群を取得とは　（・　→　・）
　　　　DLLと　"openDb"で　モジュールの関数アドレスを得て　openDbに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに
　　　　DLLと　"closeDb"で　モジュールの関数アドレスを得て closeDbに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに
　　　　DLLと　"exec"で　モジュールの関数アドレスを得て execに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに。

```
「API破棄処理」は「ODBCライブラリを破棄」を実行しています。
### ODBCライブラリを破棄
```mind:mssqlodbc.src
ODBCライブラリを破棄とは　（・　→　・）
     DLLが　ゼロ以外
          ならば　DLLで　モジュールを解放し
               DLLを　クリアする
          つぎに。
```
下記のグローバル変数を宣言して、DLLのハンドラやその関数のアドレスを保持しています。
### グローバル変数
```mind:mssqlodbc.src
DLLは　		変数。
openDbは　	変数。
closeDbは  　変数。
execは  　	変数。
```

# おわりに
今回はMind側からの引数やC側からの戻り値受け取りは無い状態で単純に実行できるかを検証しました。次回は接続文字列やSELECT文をMind側に保持してCのDLLへ渡して実行してみます。

# 参考情報

https://qiita.com/killy/items/842a12aeace63eb04e48

https://qiita.com/killy/items/b8885275df42c9e0c8f1
  
<details><summary>ソースコード全文</summary>

```mind:mssqlodbc.src
DLLは　		変数。
openDbは　	変数。
closeDbは  　	変数。
execは  　	変数。

ODBCライブラリをロードとは　（・　→　真偽）
     "C:\developments\mssqlodbc32\Debug\mssqlodbc32.dll"で　モジュールをロードし　
　　 DLLに　入れ
     DLLが　ゼロ以外を　返すこと。

ODBCライブラリを破棄とは　（・　→　・）
     DLLが　ゼロ以外
          ならば　DLLで　モジュールを解放し
               DLLを　クリアする
          つぎに。

ODBC関数アドレス群を取得とは　（・　→　・）
　　　　DLLと　"openDb"で　モジュールの関数アドレスを得て　openDbに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに
　　　　DLLと　"closeDb"で　モジュールの関数アドレスを得て closeDbに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに
　　　　DLLと　"exec"で　モジュールの関数アドレスを得て execに　入れ
　　　　エラー？　ならば　終り
　　　　つぎに。


API初期処理とは　（・　→　・）

　　　　「ODBCライブラリをロードする」を　一行表示し
　　　　ODBCライブラリをロードし　偽？　ならば 「ロード失敗」を　一行表示し　終り
　　　　 つぎに
　　　　「ロード成功」を　一行表示し


　　　　「関数アドレス群を取得」を　一行表示し
　　　　ODBC関数アドレス群を取得し
　　　　「取得成功」を　一行表示する。

API破棄処理とは　（・　→　・）
　　　　「ODBCライブラリを破棄する」を　一行表示し
　　　　ODBCライブラリを破棄する。


DB接続とは
	$$NULLと openDbで　アドレス指定でＡＰＩ呼出１する。
SQL実行とは
	$$NULLと execで　アドレス指定でＡＰＩ呼出１する。
DB切断とは
	$$NULLと closeDbで　アドレス指定でＡＰＩ呼出１する。

メインとは

	API初期処理しておき

	DB接続し
	SQL実行し
	DB切断し

	API破棄処理すること。
```

</details>
