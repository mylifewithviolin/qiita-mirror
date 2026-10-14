# はじめに
いろいろ課題を残しつつもMindでリレーショナルデータベースのトランザクションを書けるようになってきましたので、トランザクションスコープで囲ってSQLを実行した際に、エラーがおきたときに戻り値評価のままですと分岐が入れ子になりやすいので、なにかよい方法ないですかねと@killyさんに伺ったところご提案いただきましたので、それでインスパイアされた内容をここに記します。

## 想定読者
日本語プログラミング言語Mindのユーザーさん
Java/C#など一般的な実装言語のライブラリでデータベース処理を書いている実装ご担当者の方は**対象外**です。usingで囲ったりtry catchで囲ったり、インタセプタで処理したりとかいろいろかと思いますので気にしないでください。


# お題のソースコード
## Mind
Mindのソース全体像は[MindでデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/47edb441d94d2aa7f0a5)をご参照ください。killyさんのご提案内容が２つ、この記事のコメントで書かれていて２つ目が本記事のお題です。

お題のソースは下記のとおりです。

```mind:mssqlodbc.src
メインとは
    ※略※

	本体とは

		API初期処理しておき　retに　入れ
		[ret ≠ 0]　ならば　終わり　つぎに

		datasourceで　DB接続し　
		成功ならばここから

			SELECTで　SQL文をセットし
			1で　整数のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			結果セット取得し resultSetに　入れ　結果セットを表示する

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
			結果セット取得し resultSetに　入れ　結果セットを表示する

			DB切断し

		ここまで実行可能です

		API破棄処理すること。

```



# 解説
少しソースコードを解説します。
```mind:
成功ならばここから
```
や、接続のスコープ範囲の下記の単語と
```mind:
ここまで実行可能です
```
トランザクションスコープの下記の単語は
```mind:
ここまでトランザクションスコープです
```
下記のMind標準単語のエイリアスです。
```mind:mssqlodbc.src
成功ならばここからは　　　　　　　回数指定と		等価。
ここまで実行可能ですは			繰り返すと	　　等価。
ここまでトランザクションスコープですは	繰り返すと	等価。
```


```mind:
成功ならばここから
```
上記の単語の手前の
```mind:
DB接続し
```
```mind:
トランザクションを開始し
```
はAPI関数の戻り値を反転させて、成功したときに1を、失敗したときは0を返すようにしました。それにより、成功したときだけスコープ範囲を１回実行可能、失敗したときはスコープ範囲を空振りさせています。
```mind:
DB接続とは 	　（接続文字列　→　1:成功/0:失敗）			
	retは	変数
	openDbで　API関数を呼び出し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
	さもなければ　「DB接続　失敗」を　一行表示し
	つぎに
	[ret = 0]を　返す。

トランザクションを開始とは	 	　（・　→ 1:成功/0:失敗）	
	retは	変数
	0で　コミットモードをセットし　retに　入れ
	[ret = 0]を　返す。
```

```mind:
	SQLコマンド実行し　retに　入れ
	[ret ≠ 0]　ならば　Tranスコープを抜け出し
	つぎに
```
上記の「Tranスコープを抜け出し」は、もうお気づきの方も多い方と思いますが
```mind:
Tranスコープを抜け出すとは　打ち切りと　	等価。
```
「打ち切り」のエイリアスです。ここは「打ち切り」でも通じるかもしれませんね。

# 実行結果
実行結果は（ステップ2.0）の記事と同じ想定なのですが、下記のところまでしか動きませんでした。:joy:動かないところでも記事にしてしまういい度胸。

```
C:\pmind\sample>mssqlodbc10.exe
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
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言 語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0

C:\pmind\sample>
```
局所単語の「結果セットを表示する」が動いていない感じで、その直前までのAPIのデバッグコンソール出力は正常っぽい。（つづく）

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

## 参考情報
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
「endTransaction」。
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
関数の個数は　定数　関数名の　要素数。
関数アドレスは　関数の個数の　変数。
結果セット型は　型紙
　　　列データは　変数
　　　全体は
　　　1000の　列データ。


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
	openDbで　API関数を呼び出し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
	さもなければ　「DB接続　失敗」を　一行表示し
	つぎに
	[ret = 0]を　返す。
成功ならばここからは	回数指定と		等価。
ここまで実行可能ですは			繰り返すと	等価。
SQL実行とは 				execで　		API関数を呼び出す。
DB切断とは		    $$NULLと  	closeDbで　		API関数を呼び出す。
SQL文をセットとは 			setStatementで　	API関数を呼び出す。
整数のSQLパラメータをセットとは		bindParameterIntで　	API関数を呼び出す。
文字列のSQLパラメータをセットとは	bindParameterStrで　	API関数を呼び出す。
結果セット取得とは	    $$NULLと 	getResultsetで　	API関数を呼び出す。
SQLコマンド実行とは	    $$NULLと 	execCommandで　		API関数を呼び出す。
コミットモードをセットとは 		setAutoCommitで　	API関数を呼び出す。
トランザクションを終了とは 		endTransactionで　	API関数を呼び出す。

トランザクションを開始とは	 	　（・　→ 1:成功/0:失敗）	
	retは	変数
	0で　コミットモードをセットし　retに　入れ
	[ret = 0]を　返す。
Tranスコープを抜け出すとは　打ち切りと　	等価。
ここまでトランザクションスコープですは	繰り返すと	等価。
トランザクションをコミットとは		1で　トランザクションを終了する。
トランザクションをロールバックとは 	0で　トランザクションを終了する。

メインとは
	datasourceは　文字列定数　「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;&00&」
	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
					「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
					「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)&00&」
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)&00&」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?&00&」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?&00&」

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

		datasourceで　DB接続し　
		成功ならばここから

			SELECTで　SQL文をセットし
			1で　整数のSQLパラメータをセットし
			7で　整数のSQLパラメータをセットし
			結果セット取得し resultSetに　入れ　結果セットを表示する

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
			結果セット取得し resultSetに　入れ　結果セットを表示する

			DB切断し

		ここまで実行可能です

		API破棄処理すること。



```
</details>
