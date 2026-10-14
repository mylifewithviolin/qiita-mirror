# はじめに
日本語プログラミング言語Mindの小技「UTF8→SJIS変換」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# 対応バージョン
本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版は「UTF8→EUC変換」が対応していると思いますが、本記事では特に検証を行っておりません。

□Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# この小技に関連するMind言語マニュアル
この小技に関連するMind言語仕様の記述はMindプログラミングマニュアルに記載はありません。mind8またはmind9のsrclibフォルダの下記のテキストファイル
srclib\unicode-manual.txt
またはQiitaの下記の記事が該当します。
[MindでUnicodeの文字列を扱う方法（2024.01.14改訂）- Qiita](https://qiita.com/killy/items/7a103e01561bf6a053d7)

>■変換単語一覧
>
>　　　　　　　　　　[unidecode.src管轄]
>
>　Unicodeデコードテーブルを読み出し　（・　→　[ErrorMessage]、真偽）
>　　　　
成功したときは真のみが、失敗したときはエラーメッセージと偽が積まれてリターンします。スタック数がアンバランスなので注意。

>　ＵＴＦ８→Native変換
　（文字列　→　文字列）
　　　「ＵＴＦ８→ＥＵＣ変換」または
　 　「ＵＴＦ８→ＳＪＩＳ変換」でも可
   
# 小技の解説
Windows版Mindの文字コードはSHIFT-JISとなっておりますので、UTF-8の文字列を扱うには変換が必要となります。Mind8/9ではソースコードファイルが提供されたライブラリとなっていて、変換テーブルの添付が必須となります。

# Mindプログラムソース
対応例としては下記の記事のSQLite3のODBC接続検証の記事で文字コード変換が未対応でしたので、これを対応してみます。
[日本語プログラミング言語MindでSQL実行 C言語DLL拡張単語odbcライブラリ（SQLite３の検証）- Qiita](https://qiita.com/mylifewithviolin/items/e701fda39574ed0778ae)

## Mindライブラリのインクルード
```mind:testodbccsqlite2.src
"../srclib/unidecode.src"を　コンパイル。
"../srclib/uniencode.src"を　コンパイル。
```
unidecode.srcの「Unicodeデコードテーブルを読み出し」とuniencode.srcの「Unicodeエンコードテーブルを読み出し」が常にEUC向けのテーブルファイルを読みに行こうとし、Windows版のMind8/9βにはEUC向けのテーブルファイル未提供のためエラーとなるようです。とりあえずEUC向けのテーブルファイルを読みに行いく箇所をコメントアウトしています。

**2026/08/05 追記**
この記事はMind9リリース直前に書かれています。Mind9リリース版ではbinフォルダにEUC向けのテーブルファイルが提供されています。

### ODBCライブラリ
```mind:testodbccsqlite2.src
"odbcc"を　コンパイルする。
```
Mindで実装されたODBCライブラリ本体のソースコードは[Mind7/8/9β odbcライブラリC言語DLL拡張単語のアップデート（結果セット取得の9βTcl互換調整）](https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a)をご参照ください。

### SQLite3版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。SQLite3の場合は、日本語テーブル名、列名をすべてダブルクォーテーションで囲いました。

下記の点が[こちらの記事版](https://qiita.com/mylifewithviolin/items/e701fda39574ed0778ae)との違いとなります。

```mind:testodbccsqlite2.src
"../srclib/unidecode.src"を　コンパイル。
"../srclib/uniencode.src"を　コンパイル。

UTF8変換テーブルを読み出しするとは		（・　→  ・）
	Unicodeエンコードテーブルを読み出しし　偽？
　　ならば　重大エラー
    つぎに
	Unicodeデコードテーブルを読み出しし　偽？
　　ならば　重大エラー
    つぎに。

UTF8結果セットを表示するとは		（・　→  ・）
	resultSetは　	変数
	iは　		変数
	resultSetに　入れ
	[resultSet ≠ 0]　ならば

		[i := 1]
		ここから
			resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
			「|」を　表示し
			resultSetの　列データ（i）を　Mind文字列に変換し　ＵＴＦ８→ＳＪＩＳ変換し 表示し
			iを　一つ増加し
		繰り返し
	つぎに。
```
<details><summary>テストコードtestodbccsqlite2（全文）</summary>

```mind:testodbccsqlite2.src

"odbcc"を　コンパイルする。
"../srclib/unidecode.src"を　コンパイル。
"../srclib/uniencode.src"を　コンパイル。

datasourceSqliteは 文字列定数 「DRIVER={SQLite3 ODBC Driver};Database=c:\sqlite3\日本語プログラミング言語.db;」。

UTF8変換テーブルを読み出しするとは		（・　→  ・）
	Unicodeエンコードテーブルを読み出しし　偽？
　　ならば　重大エラー
    つぎに
	Unicodeデコードテーブルを読み出しし　偽？
　　ならば　重大エラー
    つぎに。

UTF8結果セットを表示するとは		（・　→  ・）
	resultSetは　	変数
	iは　		変数
	resultSetに　入れ
	[resultSet ≠ 0]　ならば

		[i := 1]
		ここから
			resultSetの　列データ（i）が ０に　等しい　ならば　打ち切り　つぎに
			「|」を　表示し
			resultSetの　列データ（i）を　Mind文字列に変換し　ＵＴＦ８→ＳＪＩＳ変換し 表示し
			iを　一つ増加し
		繰り返し
	つぎに。

メインとは
　　SELECTは　　　文字列定数　「SELECT LN."言語ID",LN."言語名",LN."よみがな",LN."公開年",DLN."開発言語ID",DLN."開発言語名" FROM "言語名" AS LN 」続
        「LEFT JOIN "開発言語" AS DL ON LN."言語ID" = DL."言語ID" 」続
        「LEFT JOIN "開発言語名" AS DLN ON DLN."開発言語ID"=DL."開発言語ID" WHERE LN."言語ID" IN (?,?)」	
	INSERTは　　　文字列定数　「INSERT INTO "開発言語" ("言語ID","開発言語ID") VALUES (?,?)」
	UPDATEは　　　文字列定数　「UPDATE "言語名" SET よみがな = ? WHERE "言語ID" = ?」
	DELETEは　　　文字列定数　「DELETE "開発言語" WHERE "言語ID" = ? AND "開発言語ID" = ?」
	成否は　		変数


	UTF8変換テーブルを読み出し
	API初期処理しておき　成功に　等しい　でなければ　終わり　つぎに

	datasourceSqliteで　DB接続し　成否に　入れ　成否が　成功に　等しい　でなければ　成否を　数値表示し　終わり　つぎに


		SELECTで　SQL文をセットし
		1で　整数のSQLパラメータをセットし
		7で　整数のSQLパラメータをセットし
		結果セット取得し UTF8結果セットを表示する

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
		項目名と共に結果セット取得し UTF8結果セットを表示する

		DB切断し


	API破棄処理すること。
```
</details>

# コンパイル結果

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccsqlite2 file

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\Mind9-beta-7\bin\mindex.exe --> testodbccsqlite2.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9\odbc>mind testodbccsqlite2 file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> biginteger.exe
```

# 実行結果
つづいて実行してみます。Mind9βの結果です。記述は割愛していますがMind8も同じです。
```cmd:
 C:\developments\vscode\mind9\odbc のディレクトリ

2025/12/29  21:04           131,072 sjis-uni-encode.bin
2025/12/29  21:04           131,072 uni-sjis-decode.bin
               2 個のファイル             262,144 バイト
```
実行フォルダには上記の変換テーブルファイルが格納されているとします。片方は使用していませんが、とりあえずセットで取り扱うとしておきます。Tcl版ODBCで使えそうな感じ。

```cmd:
C:\developments\vscode\mind9\odbc>testodbccsqlite2
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
|1|Ｍｉｎｄ|まいんど|1985|1|C|
|1|Ｍｉｎｄ|まいんど|1985|8|Mind|
|1|Ｍｉｎｄ|まいんど|1985|10|Tcl/Tk|
|7|Mind for Android|まいんど|2012|3|Java|
S1000 UNIQUE constraint failed: 開発言語.言語ID, 開発言語.開発言語ID (19)
||||N|J|J|
|1|Ｍｉｎｄ|まいんど|1985|1|C|
|1|Ｍｉｎｄ|まいんど|1985|8|Mind|
|1|Ｍｉｎｄ|まいんど|1985|10|Tcl/Tk|
|7|Mind for Android|まいんど|2012|3|Java|
ODBCライブラリを破棄する

C:\developments\vscode\mind9\odbc>
```
無事にSQLite3テーブル内の日本語情報を正常表示できました。

```
||||N|J|J|
```
2回目のSELECTの結果セットは「項目名と共に結果セット取得」としていますが、この項目名はMind側で出力しているので、UTF8変換が混線した結果です。


```
S1000 UNIQUE constraint failed: 開発言語.言語ID, 開発言語.開発言語ID (19)
```
こちらはINSERT文がユニーク制限でエラーとなっている状態で、これはデータの状態から正常な状態です。重複データを削除しておけばよいのですが、それはまた別の機会で:relaxed:

# 参考情報
日本語プログラミング言語MindのC言語DLL拡張単語odbcライブラリSQLite３の検証した記事

https://qiita.com/mylifewithviolin/items/e701fda39574ed0778ae


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
