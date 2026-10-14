# はじめに
この記事のお題は「なでしこ３でデータベースSQLServer2022にクエリーしてみる（ステップ-１.0）」です。ステップ-１.0ということはまだうまくいってないことを意味します。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
nadesiko version 3.4.5 nadesiko3win32-3.4.5
Node.js v20.10.0.
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
こんなテーブル構成のデータベースを作成しております。
データベース名は「日本語プログラミング言語」です。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

 # お題のソースコード
 下記のようなシンプルなサンプル状態で実行結果を確認しようとしました。
 
#### なでしこ3
```mind:mssql.nako
!「nadesiko3-mssql」を取り込む。
接続STR=「DSN=mssql;UID=sa;PWD=mind」
逐次実行。
　　先に、接続STRをMSSQL逐次開く。
　　次に、「SELECT * FROM 言語名 WHERE 言語ID IN (?,?,?)」を[3,5,9]でMSSQL逐次実行。
　　次に、対象を表示。
　　次に、MSSQL逐次閉じる。
　　次に、「完了」と表示。
ここまで。
```
# dsn
データソースはこんな感じです。
```mind:mssql.dsn
[ODBC]
DRIVER=ODBC Driver 17 for SQL Server
UID=SA
TransparentNetworkIPResolution=Disabled
AnsiNPW=No
QuotedId=No
TrustServerCertificate=No
DATABASE=日本語プログラミング言語
WSID=DESKTOP-078KPRA
APP=MicrosoftR WindowsR Operating System
Trusted_Connection=No
SERVER=DESKTOP-078KPRA\SQLEXPRESS
Description=JPL
```
# プラグインのインストール
HPにはplugin_mssqlと記載されていたので、それで試みたら失敗しました。npm上ではnadesiko3-mssqlと記載されていましたので、そちらで成功したようです。

```cmd
C:\nadesiko\sample1>npm install plugin_mssql
npm notice
npm notice New patch version of npm available! 10.2.3 -> 10.2.5
npm notice Changelog: https://github.com/npm/cli/releases/tag/v10.2.5
npm notice Run npm install -g npm@10.2.5 to update!
npm notice
npm ERR! code E404
npm ERR! 404 Not Found - GET https://registry.npmjs.org/plugin_mssql - Not found
npm ERR! 404
npm ERR! 404  'plugin_mssql@*' is not in this registry.
npm ERR! 404
npm ERR! 404 Note that you can also install from a
npm ERR! 404 tarball, folder, http url, or git url.

npm ERR! A complete log of this run can be found in: C:\Users\AppData\Local\npm-cache\_logs\2023-12-19T12_42_33_742Z-debug-0.log

C:\nadesiko\sample1>
C:\nadesiko\sample1>npm install nadesiko3-mssql

added 2 packages, and removed 325 packages in 10s

C:\nadesiko\sample1>
```
このインストールでnode_modulesの中がきれいさっぱりされた感じでしたのでnadesiko3win32-3.4.5から復元しました。
配置はこんな感じです。
```
C:\nadesiko\node_modules\msnodesqlv8
C:\nadesiko\node_modules\nadesiko3
C:\nadesiko\node_modules\nadesiko3-mssql
C:\nadesiko\sample1\mssql.nako.bat
C:\nadesiko\sample1\mssql.nako.bak
C:\nadesiko\sample1\mssql.nako
C:\nadesiko\sample1\mssql.dsn
```
 
 # 実行結果
 それでは実行してみます。
 ```cmd
 C:\nadesiko\sample1>mssql.nako.bat
[エラー]ファイル『file://C:\nadesiko\node_modules\nadesiko3-mssql\src\plugin_mssql.js』が読み込めません。Error: None of the binaries loaded successfully. Is your node version either latest 4, 5, 6, 7, 8 or 9 ?
---
続行するには何かキーを押してください . . .

C:\nadesiko\sample1>
```

C:\nadesiko\node_modules\nadesiko3-mssql\src\plugin_mssql.jsは存在していますが、このメッセージは依存モジュールのmsnodesqlv8が動作しない場合に出るメッセージのようです。


 # おわりに
 すみません、タイムアウトです。ゼロからマイナスに叩き落されたような感じですが、次回ゼロまで挽回できるだろうか。nadesiko3-mssqlの中には環境チェック用のjsもあるようなので、そちらで動くかどうかとかも確認してみます。

# 余談
msnodesqlv8のtool\build.batを実行してみましたが失敗しました。

<details><summary>実行結果</summary>

```
C:\nadesiko\node_modules\msnodesqlv8\tool>build.bat
C:\nadesiko\node_modules\msnodesqlv8\tool>set path=C:\Program v20.10.0/include/node/openssl/archs/solaris64-x86_64-gcc/no-asm/include/openssl/crypto.h
....略....
g'C:\\Users\\yoshiaki\\AppData\\Roaming\\npm\\node_modules\\node-gyp\\gyp\\gyp_main.py',


added 380 packages, and audited 381 packages in 1m

57 packages are looking for funding
  run `npm fund` for details

11 vulnerabilities (6 moderate, 3 high, 2 critical)

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
npm ERR! Missing script: "tsc"
npm ERR!
npm ERR! To see a list of scripts, run:
npm ERR!   npm run

npm ERR! A complete log of this run can be found in: C:\Users\yoshiaki\AppData\Local\npm-cache\_logs\2023-12-19T13_51_58_191Z-debug-0.log

C:\nadesiko\node_modules>

```
</details>
