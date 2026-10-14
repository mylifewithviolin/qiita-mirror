# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind９βのTclとのインターフェース単語をいろいろ評価してまいりました。ここで気になるのは従来のMind7/8用に実装したC言語DLL拡張単語は動作するかということです。そこで昨年実装しておりましたodbcのC言語インターフェースが動作するか確認してみました。


# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

下記のRDBにも対応はしていますが、今回検証環境はMSSQLです。
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32
postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86


# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLServerです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## Mind
### ライブラリ
昨年書いていた単語名を少し調整して、TclOdbc版とある程度揃えました。ただし、TclOdbc版の成功が１であるのに対してOdbc版は０です。

```mind:odbcc.src
        未定義条件コンパイル　定数。
Mind7は　　　　	数値　	１。
定数は　		数値と　等価。
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
「getErrorMsg」。

openDbは　			定数　1。
closeDbは　			定数　2。
execは　			定数　3。
setStatementは　	定数　4。
bindParameterIntは　定数　5。
bindParameterStrは　定数　6。
getResultsetは　	定数　7。
execCommandは　		定数　8。
setAutoCommitは　	定数　9。
endTransactionは　	定数　10。
getErrorMsgは　		定数　11。

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

結果セット取得とは 			（・　→　0:成功/0以外:失敗）
		    $$NULLと 	getResultsetで　	API関数を呼び出す。
SQLコマンド実行とは 		（文字列　→　0:成功/0以外:失敗）
		    $$NULLと 	execCommandで　		API関数を呼び出す。
SQLエラー取得とは		　（・　→　0:成功/0以外:失敗）
	$$NULLと 	getErrorMsgで　		API関数を呼び出す。

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

	
コミットモードをセットとは	（・　→　0:成功/0以外:失敗）
	setAutoCommitで　	API関数を呼び出す。
トランザクションを終了とは 	（・　→　0:成功/0以外:失敗）
	endTransactionで　	API関数を呼び出す。


トランザクションを開始とは	 （・　→ 0:成功/0以外:失敗）	
0で　コミットモードをセットする。

コミットとは	 			（・　→ 0:成功/0以外:失敗）		
1で　トランザクションを終了する。
ロールバックとは 		 	（・　→ 0:成功/0以外:失敗）
0で　トランザクションを終了する。

ここからトランザクションは　	定数　１。
スコープ開始とは　			　　回数指定と　	等価。
スコープを抜け出すとは　		打ち切りと　	等価。
ここまでスコープは			　　繰り返すと		等価。
```

### MSSQL版テスト用コード
したがってテストコード（アプリケーション側）の書き味はC言語拡張による場合とTcl言語拡張による場合でかなり同じコードで書けるようにしています。

```mind:testodbcc.src

"odbcc"を　コンパイルする。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=mind;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=mind;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;」。


メインとは

	※SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」
	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
				「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
				「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」	
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」
	成否は　		変数

	API初期処理しておき　成功に　等しい　
        でなければ　終わり　つぎに

	datasourceSqlsvrで　DB接続し　成功に　等しい　
        でなければ　終わり　つぎに


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
		結果セット取得し 結果セットを表示する

		DB切断し


	API破棄処理すること。
```
# ビルド結果
ではビルドします。
```
C:\developments\vscode\mind9>mind testodbcc file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> testodbcc.exe
```

少しライブラリ部分は書き換えていましたので、すぐにビルド成功したわけではありませんが、無事に成功しました。

# 実行結果
ではつづいて実行してみます。
```
C:\developments\vscode\mind9>testodbcc
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|1|Ｍｉｎｄ|まいんど|10|Tcl/Tk|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
23000 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]制約 'PK_開発言語' の PRIMARY KEY 違反。オブ ジェクト 'dbo.開発言語' には重複するキーを挿入できません。重複するキーの値は (7, 3) です。
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|1|Ｍｉｎｄ|まいんど|10|Tcl/Tk|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|
ODBCライブラリを破棄する
```
SQLServerのDB状態は最後にTcl版でトランザクションを成功させた状態でしたので、PK主キー制約違反でトランザクションがロールバックしました。これは成功です。

# C2022（VisualStudio2022）で実装したDLLの依存関係
昨年実装したDLLの依存関係ですが、実は最近ユニバーサルCRTの存在に気づいたのですが、当時はあまり気にしておらず、従来のCRTで動いているMind7/8のランタイムで正常動作するのを確認しておりました。このDLLを実装しCのバージョンからして、またVisualStudio2022という環境の既定として恐らくユニバーサルCRTがリンクしているだろうと思い、念のため確認いたしました。

```
C:\developments\mssqlodbc32\Debug>dumpbin mssqlodbc32.dll /DEPENDENTS
Microsoft (R) COFF/PE Dumper Version 14.42.34438.0
Copyright (C) Microsoft Corporation.  All rights reserved.


Dump of file mssqlodbc32.dll

File Type: DLL

  Image has the following dependencies:

    ODBC32.dll
    VCRUNTIME140D.dll
    ucrtbased.dll
    KERNEL32.dll

  Summary

        1000 .00cfg
        1000 .data
        1000 .idata
        1000 .msvcjmc
        3000 .rdata
        1000 .reloc
        1000 .rsrc
        8000 .text
       10000 .textbss
```
やっぱりユニバーサルCRTがリンクされていました。
VisualStudion2022がインストールされている環境での実行ですので、vcruntime140(d).dllが既に入っているため気が付きませんでした。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。

