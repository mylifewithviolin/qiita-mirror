# はじめに
[Mindでデータベース（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/47edb441d94d2aa7f0a5)という記事でMind開発者の@killyさんからいただいたご提案にインスパイアされて、[前回の記事](https://qiita.com/mylifewithviolin/items/433445095120818b8a21)でご提案内容を少しひねった変わった書き方をしてみましたところ、局所単語との相性がややわるく、完走しませんでした。今回は、局所単語の「結果セットを表示する」を別単語に置き換えて再確認しました。

# お題のソースコード
## Mind
Mindのソース全体像は[前回の記事](https://qiita.com/mylifewithviolin/items/433445095120818b8a21)をご参照ください。

お題のソースの今回の改修点は下記のとおりです。局所単語の「結果セットを表示する」を別単語に置き換えています。

```mind:mssqlodbc.src
結果セットを表示するとは
	resultSetは　	変数
	iは　			変数
	resultSetに　入れ
	[resultSet ≠ 0]　ならば

		[i := 1]
		ここから
			resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
			「|」を　表示し
			resultSetの　列データ（i）を　Mind文字列に変換し　表示し
			iを　一つ増加し
		繰り返し
	つぎに。

 メインとは
	※接続文字列、クエリー文字列略

	retは　		変数

	本体とは

		API初期処理しておき　retに　入れ
		[ret ≠ 0]　ならば　終わり　つぎに

		datasourceで　DB接続し　
		成功ならばここから

			SELECTで　SQL文をセットし
			1で　整数のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			結果セット取得し 結果セットを表示する

			トランザクションを開始し
			成功ならばここから

				INSERTで　SQL文をセットし
				7で　整数のSQLパラメータをセットし
				3で　整数のSQLパラメータをセットし
				SQLコマンド実行し　retに　入れ
				[ret ≠ 0]　ならば　Tranスコープを抜け出し
				つぎに

				UPDATEで　SQL文をセットし
				「まいんど&00&」で　文字列のSQLパラメータをセットし
				7で　整数のSQLパラメータをセットし
				SQLコマンド実行し　retに　入れ
				[ret ≠ 0]　ならば　Tranスコープを抜け出し	
				つぎに

				DELETEで　SQL文をセットし
				1で　整数のSQLパラメータをセットし
				7で　整数のSQLパラメータをセットし
				SQLコマンド実行し　retに　入れ
				[ret ≠ 0]　ならば　Tranスコープを抜け出し
				つぎに
			
	
			ここまでトランザクションスコープです

			[ret = 0]　ならば トランザクションをコミットし
			さもなければ	　トランザクションをロールバックし
			つぎに

			SELECTで　SQL文をセットし
			1で　整数のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			結果セット取得し 結果セットを表示する

			DB切断し

		ここまで実行可能です ※DB切断しなければ

		API破棄処理すること。

```



# 実行結果
実行結果は（ステップ2.1）の記事と同じ想定です。ロールバックします。デバッグ用の出力もフルでだしっぱなしです。
では、実行してみましょう。

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
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
DB接続　成功
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
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|7|Forth|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|<NULL>|<NULL>|
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
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|7|Forth|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|<NULL>|<NULL>|
paramsetStr --> free
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に動作しました。

# おわりに
書き方はいろいろあるかと思います。今回はまだメインの中で一本書きしていますが、複雑なクエリーの組み合わせになれば
クエリーの結果によってこのクエリーを実行、あのクエリーを実行と、実行するクエリも分岐したりしていきます。それらを別単語にまとめて組み合わせたりもするでしょう。
また、機会があれば書き方の工夫にトライしてみます。

killyさん、ありがとうございました。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
