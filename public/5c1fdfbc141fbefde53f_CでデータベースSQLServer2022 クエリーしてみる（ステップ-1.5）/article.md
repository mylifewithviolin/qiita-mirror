# はじめに
この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ-1.5）」です。ステップ-1.5ということはまだうまくいってないことを意味します。

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

これはC++で書かれていますが、後で述べます少しの変更でCで動きます。この記事の当座の目標はある言語用にSQLSeverのODBCを介した操作をCのライブラリとしておくことでした。ですので、C++での動作確認は現状有姿の挙動を最短で検証するためで、C++での深追いを目指してはおりません。

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
# C++からCへの変更点

前提としてMSC++2022で動作するようにするための変更点は、[C++の記事](https://qiita.com/mylifewithviolin/items/21add985700d3e60629f)の余談を確認しておいてください。

Visual StudioでC++のソースコード（ここではodbcsql.cpp）を名前を付けて保存でodbcsql.cに変更して保存します。(ファイル拡張子をcppからcに変更)

ソリューションエクスプローラで[全てのファイルを表示]アイコンをクリックして、プロジェクト外のファイルも表示します。
odbcsql.cppを右クリックして「プロジェクトから除外」します。
odbcsql.cを右クリックして「プロジェクトへ追加」します。

そのままではけっこうな数のビルドエラーが出ますが、元を正すとすると4か所くらいです。
```c:odbcsql.c
    //bool fNoData = false;
    int fNoData = 0;
    do {
        // Fetch a row

        if (iCount++ >= gHeight - 2)
        {
            int     nInputChar;
            //bool    fEnterReceived = false;
            int    fEnterReceived = 0;
            while (!fEnterReceived)
            {
                wprintf(L"              ");
                SetConsole(cDisplaySize + 2, TRUE);
                wprintf(L"   Press ENTER to continue, Q to quit (height:%hd)", gHeight);
                SetConsole(cDisplaySize + 2, FALSE);

                nInputChar = _getch();
                wprintf(L"\n");
                if ((nInputChar == 'Q') || (nInputChar == 'q'))
                {
                    goto Exit;
                }
                else if ('\r' == nInputChar)
                {
                    //fEnterReceived = true;
                    fEnterReceived = 1;
                }
                // else loop back to display prompt again
            }

            iCount = 1;
            DisplayTitles(hStmt, cDisplaySize + 1, pFirstBinding);
        }

        TRYODBC(hStmt, SQL_HANDLE_STMT, RetCode = SQLFetch(hStmt));

        if (RetCode == SQL_NO_DATA_FOUND)
        {
            //fNoData = true;
            fNoData = 1;
        }
        else
        {
```
Cにはbooleanがないので、とりあえずint型にして0:false 1:trueとしています。もう少し力めば列挙型とかにすべきところかもしれません。

 # 実行結果
 それでは実行してみます。
 コマンドプロンプトが開いた後、下図のようなデータソース選択ダイアログが開きますのであらかじめ用意しておいたDSNファイルを選択します。
![odbc.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/64835c35-2381-08f2-9c4a-d9ec9f42c3fc.jpeg)

パスワードを入力します。言語はjapaneseを選択できます。
![odbc2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/b5d1afec-8102-1125-5a6d-958928de7444.jpeg)

ダイアログを[OK]で閉じますと、コマンドプロンプトに「Connected!」と出力されれば接続しています。その手前の２行が文字化けしていますが、とりあえず無視です。続いてSQLを投入します。
![odbc3.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/28d1a1b7-6779-7a71-dad7-b5740a81ce79.jpeg)


無事に結果が返りました。

 # おわりに
 すみません、タイムアウトです。このままCの状態でODBCダイアログが開くところはソースコード上の接続文字列とかに書き換えたいです。また日本語に対応させていきます。
