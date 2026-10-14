# はじめに

諸般の流れからMind7とMind8、そしてMind９β、いずれでもビルドできる環境をVSCodeで構築してみようと思います。昨年はMind7とMind8用にタスクをそれぞれわけて設定しておりましたが、今回はもっとお手軽に同じソースを各バージョンのMindコンパイラで共通してビルドできる環境をVSCodeで構築してみます。Mind7とMind8、Mind９βで互換性があるソースであることが前提です。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.98.0
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows
Mind Version 8.11 for Windows(9beta6)

## VSCodeの拡張機能
mind-extension-preview 0.0.1

# Mind各バージョンのインストールパス

下記のように各バージョンのMindがインストールされているとします。
## Mind7
```:
C:\mind7
```
## Mind8
```:
C:\pmind
```
## Mind9β6
```:
C:\mind9-beta\mind9-beta
```

# VSCodeのプロジェクトフォルダ
Mindのソースコードファイルの格納パスとなります。
下記のように構成されているとします。

```:
C:\developments\vscode\mind9
```

# VSCodeの起動

コマンドプロンプトでこのフォルダをカレントフォルダとしてVSCodeを起動します。
```:
C:\developments\vscode\mind9>code .

```
下図のような感じでVSCodeが起動します。
このとき、既定のターミナルはPowershellの場合が多いです。下図は実はこれからご説明する方法で３つのコマンドプロンプトを追加済の状態です。

![vscodeallmind1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c3dab1ca-3d85-41fa-aa33-4be15ab5c6a4.png)

## コマンドプロンプトターミナルを３つ開く

上図の右端の＋記号をクリックすると下図のようなショートカットメニューが開きます。ここで「Command Prompt」をクリックします。

![vscodeallmind2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4a2c0c9c-df99-4b19-8e1b-2206b69ba526.png)

これを３回繰り返してください。最初の図と同じ状態になります。

## ３つのコマンドプロンプトターミナルでusemindユーティリティを実行

それぞれのコマンドプロンプトターミナルで各バージョンのusemindユーティリティを実行します。下図はMind7の場合です。
![vscodeallmind3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/abd65007-b282-49f1-ab2d-71c1e6170186.png)

## Mind7
```:
Microsoft Windows [Version 10.0.22621.4317]
(c) Microsoft Corporation. All rights reserved.

C:\developments\vscode\mind9>c:\mind7\usemind
Mind7 developing ready.
C:\developments\vscode\mind9>
```
## Mind8
```:
Microsoft Windows [Version 10.0.22621.4317]
(c) Microsoft Corporation. All rights reserved.

C:\developments\vscode\mind9>c:\pmind\usemind
myfolder=pmind\
myfolder=pmind
newpath=[]
Mindの開発環境を設定しました。

c:\pmind>
```
## Mind9 β6
```:
Microsoft Windows [Version 10.0.22621.4317]
(c) Microsoft Corporation. All rights reserved.

C:\developments\vscode\mind9>c:\mind9-beta\mind9-beta\usemind
myfolder=-beta\
myfolder=-beta
newpath=[]
Mindの開発環境を設定しました。

c:\mind9-beta\mind9-beta>
```
Mind8と9のユーティリティはカレントディレクトリをインストールフォルダに移動しますので、ソースコードが格納されているプロジェクトフォルダへカレントディレクトリを戻しておいてください。

これでビルド準備完了です。

## ３つのコマンドプロンプトターミナルで各バージョンのMindコンパイラを実行
３つのコマンドプロンプトターミナルで各バージョンのMindコンパイラを実行します。ビルド結果はそれぞれ上書きされますので注意してください。実行する場合はビルドしたターミナルで対象アセンブリを実行します。

## Mind7
```:

C:\developments\vscode\mind9>mind testodbcc file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:***********
コンパイル中 -...-
コンパイルエラー：ソース行の長さが158桁を越えており、処理できません。
　　モジュール名：testodbcc.src

C:\developments\vscode\mind9>
```
このエラーは少し記憶がありますが、とりあえず無視します。コンパイルはできていますね。

## Mind8
先に述べましたがユーティリティがカレントフォルダを移動させていますので、元に戻してからコンパイラ起動します。

```:
c:\pmind>cd C:\developments\vscode\mind9

C:\developments\vscode\mind9>mind testodbcc file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> testodbcc.exe

C:\developments\vscode\mind9>
```
## Mind9 β6
Mind9もユーティリティがカレントフォルダを移動させていますので、元に戻してからコンパイラ起動します。
```:
c:\mind9-beta\mind9-beta>cd C:\developments\vscode\mind9

C:\developments\vscode\mind9>mind testodbcc file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\mind9-beta\bin\mindex.exe --> testodbcc.exe

C:\developments\vscode\mind9>
```

## ３つのコマンドプロンプトターミナルで各バージョンのMindアプリを実行
３つのコマンドプロンプトターミナルで各バージョンのMindアプリを実行します。エビデンスはMind9で他は割愛いたします。

繰り返しになりますがビルド結果（中間コードアセンブリ）はそれぞれ上書きされますので注意してください。実行する場合はビルドしたターミナルで、かつ別のバージョンのビルドを行っていない状態で対象アセンブリを実行します。

```:
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

C:\developments\vscode\mind9>
```

# おわりに
以上です。なにかの参考になれば幸いです。VSCodeでのMindソースコード編集もエクステンションのおかげでだいぶ楽になりました。みなさまもぜひお試しください。
