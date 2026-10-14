# はじめに
この記事のお題はC++でデータベースSQLServer2022にクエリーしてみる（ステップ-2.0）」です。ステップ-2.0ということはまだうまくいってないことを意味します。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 sample
テーブル名 language 
|項目名|項目型|
|:-:|:-:|
|id| int  |
| name  |  nvarchar(50) |

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているソースコードを使用します。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

このサンプルソースは下記のように紹介されています。
>2013 年 10 月から 2019 年 7 月までの間に、このサンプルの C++ ODBC アプリケーションは 47,300 回ダウンロードされました。

# dsn
データソースはこんな感じです。
```mind:mssql2.dsn
 [ODBC]
DRIVER=ODBC Driver 17 for SQL Server
UID=sa
TrustServerCertificate=No
DATABASE=sample
WSID=DESKTOP-078KPRA
Trusted_Connection=No
SERVER=DESKTOP-078KPRA\SQLEXPRESS
Description=test
```


 # 実行結果
 それでは実行してみます。
 コマンドプロンプトが開いた後、下図のようなデータソース選択ダイアログが開きますのであらかじめ用意しておいたDSNファイルを選択します。
![odbc.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/64835c35-2381-08f2-9c4a-d9ec9f42c3fc.jpeg)

パスワードを入力します。言語はjapaneseを選択できます。
![odbc2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/b5d1afec-8102-1125-5a6d-958928de7444.jpeg)

ダイアログを[OK]で閉じますと、コマンドプロンプトに「Connected!」と出力されれば接続しています。その手前の２行が文字化けしていますが、とりあえず無視です。続いてSQLを投入します。
![odbc3.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/28d1a1b7-6779-7a71-dad7-b5740a81ce79.jpeg)


無事に結果が返りました。着色されたコンソールをWindowsで初めてみました。

 # おわりに
 すみません、タイムアウトです。実は日本語のDBも用意していたのですが、オリジナルソースのままでは日本語が通らないようでした。ゼロからマイナスに叩き落されたような感じですが、次回ゼロまで挽回できるだろうか。

# 余談
オリジナルソースのままでは下記のヶ所(pwszConnStr = L"";)がポインタに定数を代入しようとして型不一致エラーでビルドエラーとなりましたので、下記のように応急処置しております。

```cpp
if (argc > 1)
    {
        pwszConnStr = *++argv;
    }
    else
    {
        //pwszConnStr = L"";
        pwszConnStr = *++argv;
    }
```
