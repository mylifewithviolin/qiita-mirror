# はじめに
API側でエラーコードとエラーメッセージをアプリケーションに返せるようになりましたので、それを利用できるようにします。また、前回までヌル終端文字列を文字列定数の末尾に記述していましたので、そこも改修しました。

# お題のソースコード
## エラーメッセージ
原型の全体イメージがないとわかりずらいかと思いますが、いちおう以下がポイントです。

```mind:mssqlodbc.src
関数名は　文字列定数配列
「openDb」
「closeDb」
    ※～略～※
「endTransaction」
「getErrorMsg」。
openDbは　		　　定数　1。
closeDbは　		　　定数　2。
    ※～略～※
getErrorMsgは　		定数　11。

    ※～略～※
SQLエラー取得とは	    $$NULLと 	getErrorMsgで　		API関数を呼び出す。
    ※～略～※

メインとは
    ※～略～※
		ここまでトランザクションスコープです

		[ret = 0]　ならば トランザクションをコミットし
		さもなければ	　
			SQLエラー取得し Mind文字列に変換し　一行表示し
			トランザクションをロールバックし
		つぎに
    ※～略～※
	ここまで実行可能です

	API破棄処理すること。
```
## C文字列終端
文字列実体変数に0を一文字追加で対応するようにしました。いちおう以下がポイントです。

```mind:mssqlodbc.src
    ※～略～※
接続文字列最大長は　　定数　400バイト。
SQL文字列最大長は　　 定数　2000バイト。
パラメータ文字列最大長は　定数　400バイト。

DB接続とは 	　（接続文字列　→　1:成功/0:失敗）			
	retは	変数
	connectStrは　文字列実体　長さ　接続文字列最大長
	connectStrに　入れ
	0を　connectStrに　一文字追加し
	connectStrと　openDbで　API関数を呼び出し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
	さもなければ　「DB接続　失敗」を　一行表示し
	つぎに
	[ret = 0]を　返す。
 
 SQL文をセットとは （SQL文字列　→　0:成功/0以外:失敗）
	commandStrは　文字列実体　長さ　SQL文字列最大長
	commandStrに　入れ
	0を　commandStrに　一文字追加し			
	commandStrと　setStatementで　	API関数を呼び出す。

文字列のSQLパラメータをセットとは （文字列　→　0:成功/0以外:失敗）
	parameterStrは　文字列実体　長さ　パラメータ文字列最大長
	parameterStrに　入れ
	0を　parameterStrに　一文字追加し		
	parameterStrと　bindParameterStrで　	API関数を呼び出す。

     ※～略～※

メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」
 	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
					「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
					「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」
     ※～略～※

			UPDATEで　SQL文をセットし
			「まいんど」で　文字列のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			SQLコマンド実行し　retに　入れ
			[ret ≠ 0]　ならば　Tranスコープを抜け出し	
			つぎに
     ※～略～※ 
```
API呼び出し単語内で対応しましたので、地味に呼び出し単語に渡す文字列にはnull終端不要になりました。

# 実行結果（1回目）
まず1回目です。API側のデバッグ出力は無効化されていますので、接続状況と結果セットだけがアプリケーション側でコンソール出力されます。

```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|7|Forth|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんど ふぉー あんどろいど|<NULL>|<NULL>|
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんど|3|Java|
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に動作しました。定数にnull終端がなくても動作していることがわかります。

# 実行結果（2回目）
続けて同じSQLを投げてみます。今度は1回目でインサートされたレコードとPK制約違反でエラーになる想定です。
```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんど|3|Java|
23000 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]制約 'PK_開発言語' の PRIMARY KEY 違反。オブジェクト 'dbo.開発言語' には重複するキーを挿入できません。重複するキーの値は (7, 3) です。
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんど|3|Java|
ODBCライブラリを破棄する

C:\pmind\sample>
```
こんどはエラーコードとエラーメッセージが出力されました。

# おわりに
道のりはまだ長いです。次は日付型のパラメータバインドの予定ですが、しばらくお休みします。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# 参考情報

<details><summary>ソースコード全文</summary>

```mind:mssqlodbc.src
DLLは　			変数。
DLLパスは　文字列定数	"C:\developments\mssqlodbc32\Debug\mssqlodbc32.dll"。
関数名は　文字列定数配列
「openDb」
「closeDb」
「exec」
「setStatement」
「bindParameterInt」
「bindParameterStr」
「getResultset」
「execCommand」
「setAutoCommit」
「endTransaction」
「getErrorMsg」。
openDbは　		定数　1。
closeDbは　		定数　2。
execは　		定数　3。
setStatementは　	定数　4。
bindParameterIntは　	定数　5。
bindParameterStrは　	定数　6。
getResultsetは　	定数　7。
execCommandは　		定数　8。
setAutoCommitは　	定数　9。
endTransactionは　	定数　10。
getErrorMsgは　		定数　11。
関数の個数は　定数　関数名の　要素数。
関数アドレスは　関数の個数の　変数。
結果セット型は　型紙
　　　列データは　変数
　　　全体は
　　　1000の　列データ。
接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　定数　2000バイト。
パラメータ文字列最大長は　定数　400バイト。

ODBCライブラリをロードとは　（・　→　真偽）
     DLLパスで　モジュールをロードし　
　　 DLLに　入れ
     DLLが　ゼロ以外を　返すこと。

ODBCライブラリを破棄とは　（・　→　・）
     DLLが　ゼロ以外
          ならば　DLLで　モジュールを解放し
               DLLを　クリアする
          つぎに。

ODBC関数アドレス群を取得とは　（・　→　・）
	関数の個数を
	回数指定し
		DLLと　関数名（回数）で　モジュールの関数アドレスを得て
		　関数アドレス（回数）に　入れ
		エラー？
			ならば　打ち切り
			つぎに
	繰り返し。

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

API関数を呼び出しとは　（引数、番号　→　結果）
	関数アドレス（スタック）で　アドレス指定でＡＰＩ呼出１すること。

DB接続とは 	　（接続文字列　→　1:成功/0:失敗）			
	retは	変数
	connectStrは　文字列実体　長さ　接続文字列最大長
	connectStrに　入れ
	0を　connectStrに　一文字追加し
	connectStrと　openDbで　API関数を呼び出し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
	さもなければ　「DB接続　失敗」を　一行表示し
	つぎに
	[ret = 0]を　返す。
成功ならばここからは	回数指定と	等価。
ここまで実行可能ですは	繰り返すと	等価。

SQL実行とは 	　（SQL文字列　→　0:成功/0以外:失敗）
	commandStrは　文字列実体　長さ　SQL文字列最大長
	commandStrに　入れ
	0を　commandStrに　一文字追加し
	commandStrと　execで　		API関数を呼び出す。
DB切断とは		    $$NULLと  	closeDbで　		API関数を呼び出す。
SQL文をセットとは （SQL文字列　→　0:成功/0以外:失敗）
	commandStrは　文字列実体　長さ　SQL文字列最大長
	commandStrに　入れ
	0を　commandStrに　一文字追加し			
	commandStrと　setStatementで　	API関数を呼び出す。
整数のSQLパラメータをセットとは		bindParameterIntで　	API関数を呼び出す。
文字列のSQLパラメータをセットとは （文字列　→　0:成功/0以外:失敗）
	parameterStrは　文字列実体　長さ　パラメータ文字列最大長
	parameterStrに　入れ
	0を　parameterStrに　一文字追加し		
	parameterStrと　bindParameterStrで　	API関数を呼び出す。
結果セット取得とは	    $$NULLと 	getResultsetで　	API関数を呼び出す。
SQLコマンド実行とは	    $$NULLと 	execCommandで　		API関数を呼び出す。
コミットモードをセットとは 		setAutoCommitで　	API関数を呼び出す。
トランザクションを終了とは 		endTransactionで　	API関数を呼び出す。
SQLエラー取得とは	    $$NULLと 	getErrorMsgで　		API関数を呼び出す。

トランザクションを開始とは	 （・　→ 1:成功/0:失敗）	
	retは	変数
	0で　コミットモードをセットし　retに　入れ
	[ret = 0]を　返す。
Tranスコープを抜け出すとは　		打ち切りと　	等価。
ここまでトランザクションスコープですは	繰り返すと	等価。
トランザクションをコミットとは		1で　トランザクションを終了する。
トランザクションをロールバックとは 	0で　トランザクションを終了する。
結果セットを表示するとは	（・　→  ・）
	resultSetは　	変数
	iは　		変数
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
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」
	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
					「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
					「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」

	retは　		変数


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
			「まいんど」で　文字列のSQLパラメータをセットし
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
		さもなければ	　
			SQLエラー取得し Mind文字列に変換し　一行表示し
			トランザクションをロールバックし
		つぎに

		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し 結果セットを表示する

		DB切断し

	ここまで実行可能です

	API破棄処理すること。

```

</details>
