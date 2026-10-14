# はじめに
Mind7/8用に実装したC言語DLL拡張単語によるodbcのC言語インターフェースはMind９βでも動作することを確認しています。
本記事ではそのバージョンのDLLをMindから呼び出した結果の検証です。検証データベースはMySQL8.3です。


# 前提条件
Windows11 Pro 22H2 22621.4169
mind version7.5/version 8.07/version9-BETA-7

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
MySQL Community Server 8.3.0 winx64
mysql-connector-odbc-8.0.35-win32

下記のRDBにも対応はしていますが、今回検証環境はMSSQLです。
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
postgresql-16.1-1-windows-x64
psqlodbc_16_00_0000-x86


# お題のデータべース
Mysql、SQLServer、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはMysqlです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## DLLライブラリ本体
Cで実装されたDLLライブラリ本体のソースコードは[CでODBCデータベース実装 SQLServer2022（ステップ3）結果セットを項目名情報無で返す](https://qiita.com/mylifewithviolin/items/9a1bd4c75a2a3be543f0)をご参照ください。

## Mind
### ライブラリ
従来の項目名も返す「結果セットを返す」は「項目名と共に結果セットを返す」に変更されました。新しい「結果セットを返す」は項目名を返しません。

```mind:odbcc.src
        未定義条件コンパイル　定数。
Mind7は　　　　	数値　	１。
定数は　		　　数値と　等価。
        条件コンパイル終り。
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
「getErrorMsg」
「getResultsetWithColumnName」。

openDbは　						定数　1。
closeDbは　						定数　2。
execは　						定数　3。
setStatementは　				定数　4。
bindParameterIntは　			定数　5。
bindParameterStrは　			定数　6。
getResultsetは　				定数　7。
execCommandは　					定数　8。
setAutoCommitは　				定数　9。
endTransactionは　				定数　10。
getErrorMsgは　					定数　11。
getResultsetWithColumnNameは　	定数　12。

関数の個数は　		定数　関数名の　要素数。
関数アドレスは　	関数の個数の　変数。
結果セット型は　	型紙
　　　列データは　	変数
　　　全体は
　　　1000の　列データ。

接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　	定数　2000バイト。
パラメータ文字列最大長は　定数　400バイト。

成功は　定数　０。
失敗は　定数　１。

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

API破棄処理とは　			（・　→　・）
　　「ODBCライブラリを破棄する」を　一行表示し
　　ODBCライブラリを破棄する。

API初期処理とは　			（・　→　0:成功/1:失敗）

　　「ODBCライブラリをロードする」を　一行表示し
　　ODBCライブラリをロードし　偽？　
	ならば 「ロード失敗」を　一行表示し　失敗を　返し　終わり
　　つぎに
　　「ロード成功」を　一行表示し
　　「関数アドレス群を取得」を　一行表示し
　　ODBC関数アドレス群を取得し　エラー？　
		ならば 「取得失敗」を　一行表示し　
				ODBCライブラリを破棄してから　失敗を　返し　終り
　　　　 つぎに
　　　　「取得成功」を　一行表示し　成功を　返す。

API関数を呼び出しとは　		（引数、番号　→　結果）
	関数アドレス（スタック）で　アドレス指定でＡＰＩ呼出１すること。

DB接続とは 	　				（接続文字列　→　0:成功/0以外:失敗）			
	成否は	変数
	connectStrは　文字列実体　長さ　接続文字列最大長
	connectStrに　入れ
	0を　connectStrに　一文字追加し
	connectStrと　openDbで　API関数を呼び出し　成否に　入れ
	成否が　成功に　等しい　ならば 「DB接続　成功」を　一行表示し　
	さもなければ　「DB接続　失敗」を　一行表示し
	つぎに
	成否を　返す。


SQL実行とは 	　				（SQL文字列　→　0:成功/0以外:失敗）
	commandStrは　文字列実体　長さ　SQL文字列最大長
	commandStrに　入れ
	0を　commandStrに　一文字追加し
	commandStrと　execで　		API関数を呼び出す。

DB切断とは		    			（・　→　0:成功/0以外:失敗）
	$$NULLと  	closeDbで　		API関数を呼び出す。
	
SQL文をセットとは				（SQL文字列　→　0:成功/0以外:失敗）
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

結果セット取得とは 				（・　→　0:成功/0以外:失敗）
		    $$NULLと 	getResultsetで　	API関数を呼び出す。
項目名と共に結果セット取得とは 	 （・　→　0:成功/0以外:失敗）
		    $$NULLと 	getResultsetWithColumnNameで　	API関数を呼び出す。
SQLコマンド実行とは 			（文字列　→　0:成功/0以外:失敗）
		    $$NULLと 	execCommandで　		API関数を呼び出す。
SQLエラー取得とは		　		（・　→　0:成功/0以外:失敗）
	$$NULLと 	getErrorMsgで　		API関数を呼び出す。

結果セットを表示するとは		（・　→  ・）
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

	
コミットモードをセットとは		（・　→　0:成功/0以外:失敗）
	setAutoCommitで　	API関数を呼び出す。
トランザクションを終了とは 		（・　→　0:成功/0以外:失敗）
	endTransactionで　	API関数を呼び出す。


トランザクションを開始とは	 	（・　→ 0:成功/0以外:失敗）	
0で　コミットモードをセットする。

コミットとは	 				　　（・　→ 0:成功/0以外:失敗）		
1で　トランザクションを終了する。
ロールバックとは 		 		（・　→ 0:成功/0以外:失敗）
0で　トランザクションを終了する。

ここからトランザクションは　	　　定数　１。
スコープ開始とは　			　　回数指定と　	等価。
スコープを抜け出すとは　		　　打ち切りと　	等価。
ここまでスコープは			　　繰り返すと		等価。
```

### MySQL版テスト用コード
2回目のSELECTの結果セットは従来動作を移行した「項目名と共に結果セット取得」としています。

※テストコード（アプリケーション側）の書き味はC言語拡張による場合とTcl言語拡張による場合とかなり同じコードで書けるようにしています。Mind7の場合はSQL文字列定数を分割する必要があります。

```mind:testodbcc.src

"odbcc"を　コンパイルする。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。

メインとは　（・　→　・）

	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
				「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
				「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」	
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」
	成否は　		変数

	API初期処理しておき　成功に　等しい　でなければ　終わり　つぎに

	datasourceMysqlで　DB接続し　成功に　等しい　でなければ　終わり　つぎに


	SELECTで　SQL文をセットし
	1で　整数のSQLパラメータをセットし
	7で　整数のSQLパラメータをセットし
	結果セット取得し 結果セットを表示する

	トランザクションを開始し

	ここからトランザクションの　スコープ開始

		INSERTで　SQL文をセットし
		7で　整数のSQLパラメータをセットし
		3で　整数のSQLパラメータをセットし
		SQLコマンド実行し　成否に　入れ
		成否が　成功に　等しい　でなければ　スコープを抜け出し
		つぎに

		UPDATEで　SQL文をセットし
		「まいんど」で　文字列のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		SQLコマンド実行し　成否に　入れ
		成否が　成功に　等しい　でなければ　スコープを抜け出し	
		つぎに

		DELETEで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		SQLコマンド実行し　成否に　入れ
		成否が　成功に　等しい　でなければ　スコープを抜け出し	
		つぎに

	ここまでスコープ


	成否が　成功に　等しい　
	ならば コミットし
	さもなければ	　
		SQLエラー取得し Mind文字列に変換し　一行表示し
		ロールバックし
	つぎに

	SELECTで　SQL文をセットし
	1で　整数のSQLパラメータをセットし
	7で　整数のSQLパラメータをセットし
	項目名と共に結果セット取得し 結果セットを表示する

	DB切断し


	API破棄処理すること。
```


# ビルド結果
ではビルドします。
## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccmysql file

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\Mind9-beta-7\bin\mindex.exe --> testodbccmysql.exe       
```
## Mind8
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccmysql file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> testodbccmysql.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccmysql file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> testodbccmysql.exe
```
# 実行結果
ではつづいて実行してみます。
```
C:\developments\vscode\mind9\odbc>testodbccmysql          
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|10|Tcl/Tk|
|7|MindforAndroid|あたらしいよみがな|3|Java|
23000 [MySQL][ODBC 8.0(w) Driver][mysqld-8.3.0]Duplicate entry '7-3' for key '開発言語.PRIMARY'
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Mind|まいんど|1|C|
|1|Mind|まいんど|8|Mind|
|1|Mind|まいんど|10|Tcl/Tk|
|7|MindforAndroid|あたらしいよみがな|3|Java|
ODBCライブラリを破棄する

C:\developments\vscode\mind9\odbc>
```
１回目の結果セット表示は項目名を返していません。
２回目の結果セット表示は従来通り項目名を返しています。
最初のINSERT文実行は主キー制約例外で失敗しているため
次のUPDATE文は実行されていません。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。

日本語プログラミング言語Mindはいわゆる標準公式ライブラリでのデータベースアクセスライブラリは提供されていないのですが、Mind処理単語はC言語（またはTcl言語Mind7,9の場合）で拡張することができますのでこれを使ってもデータベースアクセスライブラリを拡張実装してMindから直接SQLを実行することはできます。
この記事はC言語で拡張した事例の記事となります。
