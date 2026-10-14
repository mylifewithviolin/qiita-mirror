# はじめに
この記事のお題は「MindでデータベースSQLServer2022にクエリーしてみる（ステップ1.8）」です。

[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.8）クエリーのパラメータ化対応（整数+文字列）](https://qiita.com/mylifewithviolin/items/558d182ae1845547d00a)という記事でSELECT実行の際に整数に加えて文字列もパラメータ化されたステートメントに対応させましたので、それらをMindから実行してみます。また、Cの記事ではWhere句の整数IN句を文字列Like句に置き換えてしまいましたが、Mindからでは両方組み合わせてみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[C（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。

# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を、
ソースコードは[CでデータベースSQLServer2022 クエリーしてみる（ステップ1.7）クエリーのパラメータ化対応（整数のみ）](https://qiita.com/mylifewithviolin/items/4c0d0423b909730641c8)をご参照ください。

## Mind
Mindのソース全体像は[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。

SELECT文のIN句のリテラル数字２つをパラメータのプレースフォルダ「?」にした上で文字列のLIKE雲追加しています。このSELECT文文字列をDLL側にセットした後、整数型パラメータのバインド関数を２回実行してから文字列型パラメータのバインド関数を１回実行してから、SELECT文を実行しています。この実行順序をプレースフォルダ「?」の並び順に揃えなければならないのはODBCの仕様です。それぞれのパラメータのバインド関数はエラーを返す場合がありますが、ここでは割愛しています。

```mind:mssqlodbc.src
DLLは　				変数。
openDbは　			変数。
closeDbは  　		変数。
execは  　			変数。
setStatementは  　	変数。
bindParameterIntは  変数。
bindParameterStrは  変数。
getResultsetは  　	変数。
結果セット型は　		型紙
　　　列データは　	変数
　　　全体は
　　　1000の　列データ。

※略※

ODBC関数アドレス群を取得とは　（・　→　・）
　　　　DLLと　"openDb"で　モジュールの関数アドレスを得て　openDbに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"closeDb"で　モジュールの関数アドレスを得て closeDbに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"exec"で　モジュールの関数アドレスを得て execに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"setStatement"で　モジュールの関数アドレスを得て setStatementに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"bindParameterInt"で　モジュールの関数アドレスを得て bindParameterIntに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"bindParameterStr"で　モジュールの関数アドレスを得て bindParameterStrに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"getResultset"で　モジュールの関数アドレスを得て getResultsetに　入れ
　　　　エラー？　ならば　終り　つぎに。


※略※
SQL文をセットとは
	setStatementで　アドレス指定でＡＰＩ呼出１する。
整数のSQLパラメータをセットとは
	bindParameterIntで　アドレス指定でＡＰＩ呼出１する。
文字列のSQLパラメータをセットとは
	bindParameterStrで　アドレス指定でＡＰＩ呼出１する。 
結果セット取得とは
	$$NULLと getResultsetで　アドレス指定でＡＰＩ呼出１する。

メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;&00&」
	SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (?,?) OR よみがな LIKE ? +'%'&00&」

	retは　		変数
	resultSetは　	変数
	iは　		変数

	API初期処理しておき　retに　入れ
	[ret ≠ 0]　ならば　終わり　つぎに

	datasourceで　DB接続し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
		SELECTで　SQL文をセットし

		5で　整数のSQLパラメータをセットし
		6で　整数のSQLパラメータをセットし
		「まいんど&00&」で　文字列のSQLパラメータをセットし

		結果セット取得し resultSetに　入れ
		[resultSet ≠ 0]　ならば
			[i := 1]
			ここから
				resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
				「|」を　表示し
				resultSetの　列データ（i）を　Mind文字列に変換し　表示し
				iを　一つ増加し
			繰り返し
		つぎに
		DB切断し
	さもなければ　「DB接続　失敗」を　一行表示し　
	つぎに

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
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
DB接続　成功
paramCountInt --> 1
paramNumber --> 1
param --> 5
paramCountInt --> 2
paramNumber --> 2
param --> 6
paramCountStr --> 1
paramNumber --> 3
param --> まいんど
SQLText --> SELECT * FROM 言語名 WHERE 言語ID IN (?,?) OR よみがな LIKE ? +'%'
SQLExecDirect --> 0
|言語ID|言語名|公開年|よみがな|
|1|Ｍｉｎｄ|1985|まいんど|
|5|なでしこ|2004|なでしこ|
|6|プロデル|2007|ぷろでる|
|7|Mind for Android|2012|まいんどふぉーあんどろいど|
paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に正常動作しました！:tada:
ここでの注意事項としては、バインドする文字列パラメータの文字列にもC言語文字列用のNULL終端のセットを忘れないこと。
```mind:mssqlodbc.src
「まいんど&00&」で　文字列のSQLパラメータをセットし
```

このあたり、のちのち忘れそうになりがちなので、Mind側でライブラリ化するとしたら、そのレベルで暗黙にセットされているみたいな世界にするとよさそうです。

# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、次回はトランザクション制御に進行します。たぶん。（C側は既にだいぶ書いてあります。文字列パラメータはさすがになにかUPDATEするとき、文字列が渡せないとなんですのでということで急遽別クチで対応しました。）
