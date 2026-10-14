# はじめに
この記事のお題は「MindデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）」です。

[CでデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/03d941fb67424fb64877)という記事でODBC関数のCライブラリをトランザクション対応させましたので、それらをMindから実行してみます。ただし、そちらの記事にも書きましたが、まだロールバックは動作していません。Mind的にはSELECTに続いてINSERT,UPDATE,DELETEがパラメータバインドで連続して動作したので、ひとまずまとめます。

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
こんなテーブル構成のデータベースを作成しております。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。最新のソースコードは少々お待ちください。


## Mind
Mindのソース全体像は下記のとおりです。結果セットの出力処理は局所単語にしてみました。Javascript(Typescript)やGoのクロージャみたいなものですね。Mindのがずっと先でしたので、Javascriptではじめてクロージャを実装したとき、「まるでMindみたい」という感想をもったわたしはかなりめずらしいくちかもしれません。

```mind:mssqlodbc.src
メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;&00&」
	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
					「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
					「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)&00&」
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)&00&」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?&00&」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?&00&」

	retは　		変数
	resultSetは　	変数
	iは　		変数

	結果セットを表示するとは
		[resultSet ≠ 0]　ならば
			[i := 1]
			ここから
				resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
				「|」を　表示し
				resultSetの　列データ（i）を　Mind文字列に変換し　表示し
				iを　一つ増加し
			繰り返し
		つぎに

	本体とは

		API初期処理しておき　retに　入れ
		[ret ≠ 0]　ならば　終わり　つぎに

		datasourceで　DB接続し　retに　入れ
		[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
		さもなければ　「DB接続　失敗」を　一行表示し　API破棄処理してから　終わり
		つぎに

		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し resultSetに　入れ　結果セットを表示する

		トランザクションを開始し

		INSERTで　SQL文をセットし
		7で　整数のSQLパラメータをセットし
		3で　整数のSQLパラメータをセットし
		SQLコマンド実行し　retに　入れ
		[ret = 0]　ならば
			UPDATEで　SQL文をセットし
			「まいんど&00&」で　文字列のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			SQLコマンド実行し　retに　入れ
			[ret = 0]　ならば
				DELETEで　SQL文をセットし
				1で　整数のSQLパラメータをセットし
				7で　整数のSQLパラメータをセットし
				SQLコマンド実行し　retに　入れ
				[ret = 0]　ならば
				つぎに
			つぎに
		つぎに

		[ret = 0]　ならば トランザクションをコミットし
		さもなければ	　トランザクションをロールバックし
		つぎに

		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し resultSetに　入れ　結果セットを表示する

		DB切断し
		API破棄処理すること。
```
今回は各SQLコマンドの戻り値を評価して後続処理を実行するか否かを分岐してしまっていますが、この書き方ですと実行文が増えるとネストがどんどん深くなってしまいますので、エラーが起きたらトランザクションの分岐点までジャンプできるとよいですね。


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
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんど|3|Java|
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

## Mind側ライブラリ相当ソース
下記はまだ分割コンパイルできるようファイル分割していませんが、ライブラリとなる範囲のソースです。ODBC関数をMind側で直接呼び出すという書き方もありますが、各ODBC関数の引数型がけっこう難解なので、C側である程度つくりこんでMind側との変数のやりとりを単純化しています。

```mind:mssqlodbc.src
DLLは　			変数。
openDbは　		変数。
closeDbは  　		変数。
execは  　		変数。
setStatementは  　	変数。
bindParameterIntは  　	変数。
bindParameterStrは  　	変数。
getResultsetは  　	変数。
execCommandは  　	変数。
setAutoCommitは  　	変数。
endTransactionは  　	変数。
結果セット型は　型紙
　　　列データは　変数
　　　全体は
　　　1000の　列データ。


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
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"execCommand"で　モジュールの関数アドレスを得て execCommandに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"setAutoCommit"で　モジュールの関数アドレスを得て setAutoCommitに　入れ
　　　　エラー？　ならば　終り　つぎに
　　　　DLLと　"endTransaction"で　モジュールの関数アドレスを得て endTransactionに　入れ
　　　　エラー？　ならば　終り　つぎに。

API破棄処理とは　（・　→　・）
　　　　「ODBCライブラリを破棄する」を　一行表示し
　　　　ODBCライブラリを破棄する。

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
SQL文をセットとは
	setStatementで　アドレス指定でＡＰＩ呼出１する。
整数のSQLパラメータをセットとは
	bindParameterIntで　アドレス指定でＡＰＩ呼出１する。
文字列のSQLパラメータをセットとは
	bindParameterStrで　アドレス指定でＡＰＩ呼出１する。
結果セット取得とは
	$$NULLと getResultsetで　アドレス指定でＡＰＩ呼出１する。
SQLコマンド実行とは
	$$NULLと execCommandで　アドレス指定でＡＰＩ呼出１する。
コミットモードをセットとは
	setAutoCommitで　アドレス指定でＡＰＩ呼出１する。
トランザクションを終了とは
	endTransactionで　アドレス指定でＡＰＩ呼出１する。

トランザクションを開始とは
	0で　コミットモードをセットする。
トランザクションをコミットとは
	1で　トランザクションを終了する。
トランザクションをロールバックとは
	0で　トランザクションを終了する。

```
# おわりに
ステップバイステップの細かさにもほどがあると危惧しつつ、次回はトランザクション制御のロールバック正常動作に進行します。たぶん。
