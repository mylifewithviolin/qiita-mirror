# はじめに
この記事のお題はMindでデータベースSQLServer2022にクエリーしてみる（ステップ1.5）」です。ステップ1.5とは最初のステップの道半ばを意味します。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)という記事で単純なODBC接続、SELECT実行・結果表示、切断の実装をDLLにした状態から結果セットを文字列配列で返すようにしましたので、それらをMindから実行してみます。

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
ソースコードは[C（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)と[C（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)をご参照ください。

## Mind
Mindのソース全体像は[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。

Mindのソースはメインは「SQL実行」にresultsetのアドレスを返し、それをMindの型紙の先頭アドレスとして列データとして読み取り、Mind文字列に変換してコンソール出力しています。列データの最後にはNULL終端をC側でセットしていますので、それを検知したらループ終了です。

```mind:mssqlodbc.src
DLLは　		変数。
openDbは　	変数。
closeDbは  　	変数。
execは  　	変数。
結果セット型は　型紙
　　　列データは　変数
　　　全体は
　　　1000の　列データ。

※略

API初期処理とは　（・　→　0/1）

　　　　「ODBCライブラリをロードする」を　一行表示し
　　　　ODBCライブラリをロードし　偽？　ならば 「ロード失敗」を　一行表示し　1を　返し　終わり
　　　　 つぎに
　　　　「ロード成功」を　一行表示し


　　　　「関数アドレス群を取得」を　一行表示し
　　　　ODBC関数アドレス群を取得し　エラー？　ならば 「取得失敗」を　一行表示し　
	ODBCライブラリを破棄してから　1を　返し　終り
　　　　 つぎに
　　　　「取得成功」を　一行表示し　0を　返す。


DB接続とは
	openDbで　アドレス指定でＡＰＩ呼出１する。
SQL実行とは
	execで　アドレス指定でＡＰＩ呼出１する。
DB切断とは
	$$NULLと closeDbで　アドレス指定でＡＰＩ呼出１する。

メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;&00&」
	SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)&00&」

	retは　		変数
	resultSetは　	変数
	iは　		変数

	API初期処理しておき　retに　入れ
	[ret ≠ 0]　ならば　終わり　つぎに

	datasourceで　DB接続し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
		SELECTで　SQL実行し resultSetに　入れ
		[resultSet ≠ 0]　ならば
			[i := 1]
			ここから
				resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
				resultSetの　列データ（i）を　Mind文字列に変換し　表示し
				iを　一つ増加し
			繰り返し
		つぎに
		DB切断し
	さもなければ　「DB接続　失敗」を　一行表示し　
	つぎに

	API破棄処理すること。
```
列項目名と列の値をパイプ区切りの文字列配列で返してきます。列項目ヘッダや１行分の列値の文字列配列の間に改行だけからなる文字列配列を返していますので、改行処理はとくにMind側は意識していません。

# 実行結果
では実行します。
 ```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
DB接続　成功
SQLText(char) --> SELECT * FROM 言語名 WHERE 言語ID IN (1,7)
SQLText --> SELECT * FROM 言語名 WHERE 言語ID IN (1,7)
SQLExecDirect --> 0
| 言語ID      | 言語名               | 公開年      | よみがな              |
|           1 |             Ｍｉｎｄ |        1985 |             まいんど  |
|           7 |     Mind fro Android |        2012 | まいんどふぉーあんどろいど  |
resultset --> beforefree
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に正常動作しました！:tada:SELECT文のWHERE句は言語ID IN (1,7)として2行返るようにしています。ほんとは「まいんどふぉーあんどろいど」で「ろいど」が切れてますが、C側の問題です。とりあえずよしとさせていただきます。
## 2024/01/15 追記
「ろいど」が切れてたのはDB側で「よみがな」列の型をnvarchar(20)にしたせいでした。最初に作成したときnvarchar(50)にしていたのですが、どこからのタイミングで(20)にしてしまいました。この数字が文字数ではなくバイトペア数ということを忘れてました。いま(30)にして足りているようです。

# おわりに
次回はクエリのパラメータ化またはトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。
いったん、年末に想定していたイメージまで到達しました。Mind側ではあまり書かなくてもよいようにC側をつくりこんでいますが、結果セットに型情報がなくて文字列返しだけですと、LLスクリプト言語経由と大差ない状況です。あくまで興味本位です。

# 参考情報

https://qiita.com/killy/items/92f90986d11465084968
