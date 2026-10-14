# はじめに
今回はプロデルでデータベースSQLServer2022のステップ３で、トランザクションを構成して更新途中で例外を発生させてロールバックを確認してみます。

https://qiita.com/advent-calendar/2023/produire


## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Produire Version 2.0.1197 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
こんなテーブル構成のデータベースを作成しております。
データベース名は「日本語プログラミング言語」です。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
#### プロデル
```mind:mssq3.rdr
※コンソール
【conn:SQLServerデータベース】

【sql1:文字列】は、「UPDATE 言語名 SET よみがな =@p2 WHERE 言語ID =@p1」
【sql2:文字列】は、「INSERT INTO 後継言語  (言語ID,後継言語ID) VALUES (@p1, @p2)」
【sql3:文字列】は、「
SELECT LN.言語名,LN.公開年,LN.よみがな,KLN.言語名 AS 後継言語名 
FROM 言語名 AS LN
LEFT JOIN 後継言語　AS KL ON LN.言語ID=KL.言語ID
LEFT JOIN 言語名　AS KLN ON KL.後継言語ID=KLN.言語ID
WHERE LN.言語ID =@p1」

メイン実行する。
メイン実行する手順
	接続構成する
	connへ接続する
	connでトランザクションを開始する
	 「トランザクションを開始する」をコンソールへ表示して改行する
	例外監視
  		トランザクションを実行する
	   	connでトランザクションを完了する
	   	 「トランザクションをコミットする」をコンソールへ表示して改行する
　　	発生した場合
		connでトランザクションを取り消す
		 「トランザクションをロールバックする」をコンソールへ表示して改行する
		エラーを、コンソール出力する
		監視終わり	
    	
    	更新結果をコンソール出力する
	connから切断する
終わり

トランザクションを実行する手順
	param1は｛@p1=2,@p2=「ティーティーエス」｝
	param2は｛@p1=2,@p2=6｝

	sql1をparam1としてconnで実行して、結果1とする
	結果1をコンソールへ表示して改行する	
	sql2をparam2としてconnで実行して、結果2とする
	結果2をコンソールへ表示して改行する	 
終わり

更新結果をコンソール出力する手順
	param3は｛@p1=2｝
	connからsql3をparam3として取得して、結果3とする
	結果3の内容をコンソールへ表示して改行する

終わり

【エラー】を、コンソール出力する手順
	「エラー番号：」＆ エラーの番号＆ 「　エラー内容：」＆ エラーのメッセージをコンソールへ表示して改行する
終わり

接続構成する手順
	connというSQLServerデータベースを作る
	connのデータソースは「DESKTOP-078KPRA\SQLEXPRESS」
	connのデータベースは「日本語プログラミング言語」
	connのWindows認証は、○
終わり

```
https://produ.irelang.jp/docs/data/db/dbsqlserver.htm

↑こちらの詳しい説明を拝見して書いています。今回は途中経過をコンソール出力し、例外が発生したらエラー内容もコンソールに出力するようにしてみました。

# 実行前のデータ状態
実行する前にデータの状態を確認しましょう。

```
SELECT [言語ID]
      ,[言語名]
      ,[公開年]
      ,[よみがな]
  FROM [日本語プログラミング言語].[dbo].[言語名]
  
言語ID	言語名	公開年	よみがな
1	Ｍｉｎｄ	1985	まいんど
2	ＴＴＳ	　　2000	てぃーてぃーえす
3	ひまわり	2001	ひまわり
4	ドリトル	2003	どりとる
5	なでしこ	2004	なでしこ
6	プロデル	2007	ぷろでる
7	Mind fro Android	2012	まいんどふぉーあんどろいど
8	スミレ	　　2018	すみれ
9	なでしこ３	2018	なでしこさん
10	スミレ畑	2020	すみればたけ
```
```
SELECT [言語ID]
      ,[後継言語ID]
  FROM [日本語プログラミング言語].[dbo].[後継言語]
  
言語ID	後継言語ID
2	8
3	5
```
前回記事で挿入されたTTSの後継言語のプロデルの方はいったん削除しています。ソースコードの結果確認用の結合クエリーをこの状態で実行すると下図のようになります。
```
SELECT LN.言語名,LN.公開年,LN.よみがな,KLN.言語名 AS 後継言語名 
FROM 言語名 AS LN
LEFT JOIN 後継言語　AS KL ON LN.言語ID=KL.言語ID
LEFT JOIN 言語名　AS KLN ON KL.後継言語ID=KLN.言語ID
WHERE LN.言語ID =2

言語名	公開年	よみがな	後継言語名
ＴＴＳ	2000	てぃーてぃーえす	スミレ
```

# 実行結果
それでは実行してみましょう。コンパイルはプロデルデザイナで実行ファイルの作成するで行っています。
```
C:\produire\sample2>mssql3
トランザクションを開始する
1
1
トランザクションをコミットする
{{ＴＴＳ,2000,ティーティーエス,プロデル},{ＴＴＳ,2000,ティーティーエス,スミレ}}

C:\produire\sample2>
```

ちょっとわかりやすくするため結果を改行してみます。

```
{
{ＴＴＳ,2000,ティーティーエス,プロデル},
{ＴＴＳ,2000,ティーティーエス,スミレ}
}
```
ＴＴＳのよみがながカタカナに変更されて、後継言語のプロデルも追加されました。:tada:

# ロールバックさせる
では、ここで本記事のお題のロールバックを確認してみましょう。いったんＴＴＳのよみがなをひらがなに戻します。後継言語のプロデルレコードは残しておきます。

ソースコードの結果確認用結合クエリーを実行すると下図の状態です。
```
言語名	公開年	よみがな	後継言語名
ＴＴＳ	2000	てぃーてぃーえす	プロデル
ＴＴＳ	2000	てぃーてぃーえす	スミレ
```

この状態からもう一度アプリを実行してみましょう。そうすると、最初ＴＴＳのよみがなの更新は成功しますが、後継言語のインサートでは主キー制約により重複エラーの例外が発生してよみがなの更新がロールバックされてひらがなが維持された状態で２件結果が返るはずです。

では実行してみましょう。
```
C:\produire\sample2>mssql3
トランザクションを開始する
1
トランザクションをロールバックする
エラー番号：2　エラー内容：制約 'PK_後継言語' の PRIMARY KEY 違反。オブジェクト 'dbo.後継言語' には重複するキーを挿入で きません。重複するキーの値は (2, 6) です。
ステートメントは終了されました。
SqlException 制約 'PK_後継言語' の PRIMARY KEY 違反。オブジェクト 'dbo.後継言語' には重複するキーを挿入できません。重複 するキーの値は (2, 6) です。
ステートメントは終了されました。
   場所 System.Data.SqlClient.SqlConnection.OnError(SqlException exception, Boolean breakConnection, Action`1 wrapCloseInAction)
   場所 System.Data.SqlClient.TdsParser.ThrowExceptionAndWarning(TdsParserStateObject stateObj, Boolean callerHasConnectionLock, Boolean asyncClose)
   場所 System.Data.SqlClient.TdsParser.TryRun(RunBehavior runBehavior, SqlCommand cmdHandler, SqlDataReader dataStream, BulkCopySimpleResultSet bulkCopyHandler, TdsParserStateObject stateObj, Boolean& dataReady)
   場所 System.Data.SqlClient.SqlCommand.FinishExecuteReader(SqlDataReader ds, RunBehavior runBehavior, String resetOptionsString, Boolean isInternal, Boolean forDescribeParameterEncryption, Boolean shouldCacheForAlwaysEncrypted)
   場所 System.Data.SqlClient.SqlCommand.RunExecuteReaderTds(CommandBehavior cmdBehavior, RunBehavior runBehavior, Boolean returnStream, Boolean async, Int32 timeout, Task& task, Boolean asyncWrite, Boolean inRetry, SqlDataReader ds, Boolean describeParameterEncryptionRequest)
   場所 System.Data.SqlClient.SqlCommand.RunExecuteReader(CommandBehavior cmdBehavior, RunBehavior runBehavior, Boolean returnStream, String method, TaskCompletionSource`1 completion, Int32 timeout, Task& task, Boolean& usedCache, Boolean asyncWrite, Boolean inRetry)
   場所 System.Data.SqlClient.SqlCommand.InternalExecuteNonQuery(TaskCompletionSource`1 completion, String methodName, Boolean sendToPipe, Int32 timeout, Boolean& usedCache, Boolean asyncWrite, Boolean inRetry)
   場所 System.Data.SqlClient.SqlCommand.ExecuteNonQuery()
   場所 Produire.Data.データベースエンジン.3(IDbCommand 0)

[エラー番号2] [トランザクションを実行する:39行目]
{{ＴＴＳ,2000,てぃーてぃーえす,プロデル},{ＴＴＳ,2000,てぃーてぃーえす,スミレ}}

C:\produire\sample2>
```
しっかりスタックトレースも出力されていますね。
ちょっとわかりやすくするため結果を改行してみます。

```
{
{ＴＴＳ,2000,てぃーてぃーえす,プロデル},
{ＴＴＳ,2000,てぃーてぃーえす,スミレ}
}
```
# おわりに
次回は未定（ネタ切れ）です。どうしよう！？もう少しDBでひっぱりたい！:santa_tone2:
