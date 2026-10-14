# はじめに

この記事のお題はMindでデータベースPostgreSQL16.1にクエリーしてみる（ステップ1.6）」です。ステップ1.6は「CでデータベースMySQL8.3 クエリーしてみる（ステップ1.6）結果セット文字列返し書式解除」と同レベルを意味します。

ステップ1.5では結果セットの文字列返しの際にDLL側でパイプを付ける書式制御を残していましたが、1.6はそれをとりましたという意味です。今回はMind側で書式制御してみます。


## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86

# お題のデータべース
データベース名 日本語プログラミング言語
テーブル構成は[C（ステップ0.0）](https://qiita.com/mylifewithviolin/items/415ec4bf87219935a3c0)をご参照ください。
EncordingはUTF8、文字タイプはJapanese_Japan.932(Shift-JIS)、照合順序はJapanese_Japan.932です。

# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)を
ソースコードは[C（ステップ1.3）dll化SJIS対応](https://qiita.com/mylifewithviolin/items/8e39900a0559f12eb367)と[C（ステップ1.5）結果セット文字列返し対応](https://qiita.com/mylifewithviolin/items/35e696bfb54e1fccbd50)と[CでデータベースMySQL8.3 クエリーしてみる（ステップ1.6）結果セット文字列返し書式解除](https://qiita.com/mylifewithviolin/items/46a7fde102c7e883f7b4)をご参照ください。

### C状態での変更点
DLLは1.6からの変更点はありません。検証用コンソールアプリケーションはMind側と同様に接続文字列を変更し、SELECT文の列名のダブルクォーテーション囲みを行って検証しました。


## Mind
Mindのソース全体像は[Mind（ステップ1.0）](https://qiita.com/mylifewithviolin/items/7901da4001cada906663)と[Mind（ステップ1.1）](https://qiita.com/mylifewithviolin/items/037f32b8ed78b1b2de7c)をご参照ください。
ODBC接続文字列を変更しました。データベース名とテーブル名は日本語で問題ありませんでしたが、列名はダブルクオーテーションで囲わないとエラーになってしまいました。
また、パイプ「|」を各列の値の間に挿入しています。

```mind:mssqlodbc.src
メインとは
    datasourceは　文字列定数　「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;&00&&00&」
    SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE "言語ID" IN (1,7)&00&

    retは　		　　変数
	resultSetは　	変数
	iは　		　　変数

	API初期処理しておき　retに　入れ
	[ret ≠ 0]　ならば　終わり　つぎに

	datasourceで　DB接続し　retに　入れ
	[ret = 0]　ならば 「DB接続　成功」を　一行表示し　
		SELECTで　SQL実行し resultSetに　入れ
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
DSText --> Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=mind;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 0
SQLAllocStmt --> 0
DB接続　成功
SQLText(char) --> SELECT * FROM 言語名 WHERE "言語ID" IN (1,7)
SQLText --> SELECT * FROM 言語名 WHERE "言語ID" IN (1,7)
SQLExecDirect --> 0
|言語ID|言語名|公開年|よみがな|
|1|Mind|1985|まいんど|
|7|Mind for Android|2012|まいんどふぉーあんどろいど|
resultset --> free
SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE
ODBCライブラリを破棄する

C:\pmind\sample>
```
無事に正常動作しました！:tada:
当初、言語IDの列名でひっかかっていることがなかなかわからず、ちょっとあせりました。（接続まではすんなり成功したのですが、その後のSELECT文実行でSQLExecDirectが-1を返していました。）偶然、PostgreSQL管理ツールのpgAdmin4で定義SQLを生成させたら、DB名、テーブル名、列名がすべてダブルクオーテーションで囲われていたので、囲ってみたらあっさり動きました。

# おわりに
次回はクエリのパラメータ化またはトランザクション制御に進行したいですが、ちょっとお休みします。たぶん。

# 参考情報
PostgreSQLのODBCドライバーは下記のサイトよりダウンロードしました。サーバー本体の32bitサポートは終了していますが、ドライバの32bitサポートは継続しているようです。

https://www.postgresql.org/ftp/odbc/versions/msi/
