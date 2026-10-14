# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ３です。IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法をステップ２までで確定いたしました。今回はCSSのインクルードを試みます。


 前提条件
Windows11 Pro 22H2 22621.4169
Mind Version 8.0.08 for Windows
Internet Information Servicies 10.0

# 環境の構成
[C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87)のフォルダ環境をほぼそのまま使います。

C#とkestrelで実行していた場合は、アプリ本体の中間コードファイルmcoはプロジェクトルートに置かないと実行できませんでしたが、前回はCGI実行フォルダに引っ越しています。

```cmd:
C:\developments\vscode\kestrelcgi
├─cgi
│      test-form-submit.cgi
│      test-form-submit.mco
│      test-form.cgi
│      test-form.mco
└─wwwroot
    │  favicon.ico
    │  index.html
    ├─css
    │      site.css
    ├─js
    │      site.js
    └─lib
        ├─bootstrap
        │  └─dist
        │      ├─css
        │      └─js
        ├─jquery
        ├─jquery-validation
        └─jquery-validation-unobtrusive
```


# Mind CGIアプリケーションの作成

今回はMind8のCGIサンプルを少し修正して動かしますが、動かすのは実行パス設定した下記の機能です。
「フォームのテスト」cgi/test-form.cgi

cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされています。

## Mind CGIライブラリの修正
ソースコード提供されているCGIライブラリのheader.srcを修正します。

「ＣＳＳデータ１、２、３」という文字列実体変数を追加。
「ｈｔｍｌ５をＤＯＣＴＹＰＥデータ設定」という単語を追加。
「ｈｔｍｌヘッダ出力０」という単語内で「ＣＳＳデータ１、２、３」の出力処理を追加します。

```mind:cgilib/header.src
※～略～
ＭＥＴＡデータ１とは　  　　文字列実体　長さ　１２８。
ＭＥＴＡデータ２とは　  　　文字列実体　長さ　１２８。
ＤＯＣＴＹＰＥデータとは　　文字列実体　長さ　１２８。
ＣＳＳデータ１とは　  　　　文字列実体　長さ　１２８。※追加
ＣＳＳデータ２とは　  　　　文字列実体　長さ　１２８。※追加
ＣＳＳデータ３とは　  　　　文字列実体　長さ　１２８。※追加
ＢＯＤＹデータとは　　　　　文字列実体　長さ　１２８。
ヘッダ内平仮名は　　　　　　文字列実体　長さ　　８０。

※～略～
ｈｔｍｌ５をＤＯＣＴＹＰＥデータ設定とは　（・　→　・）　　※新デフォルト　※Pmod　※追加
     	「<!DOCTYPE html>」を
	ＤＯＣＴＹＰＥデータに　入れる。
    
※～略～
	ローカル。

ｈｔｍｌヘッダ出力０とは　（タイトル、スタック検査指定　→　・）
		タイトルは　文字列
		スタック検査指定は　　変数
		スタックエラー検出は　変数
	タイトルと　スタック検査指定に　入れ
	スタック検査指定
		ならば　スタック検査０し　偽？を　スタックエラー検出に　入れ
		つぎに
　　※～略～
	※
		「<TITLE>」を　表示し　タイトルを　表示し
					「</TITLE>」を　一行表示し
		ＣＳＳデータ１が　非空列？
			ならば　※注：TITLEより後に※
				ＣＳＳデータ１を　一行表示し
			つぎに
		ＣＳＳデータ２が　非空列？
			ならば　※注：TITLEより後に※
				ＣＳＳデータ２を　一行表示し
			つぎに
		ＣＳＳデータ３が　非空列？
			ならば　※注：TITLEより後に※
				ＣＳＳデータ３を　一行表示し
			つぎに
			「</HEAD>」を　一行表示し
		改行し
		ヘッダ出力済み・ｈｔｍｌヘッダを
		　ｈｔｍｌヘッダ出力済みに　入れ
	つぎに
	※
    ※～略～
    	※
　　（スタック検査）
	スタック検査指定
	ならば　スタックエラー検出
		ならば　「<br><br><h3>エラー：スタックがずれてい」続
			「ます(ｈｔｍｌヘッダ出力時)</h3>」を　表示し
		つぎに
	つぎに。
```

ソースコード提供されているCGIライブラリのcgilib.srcも若干修正します。
「ＣＧＩＬＩＢ初期化０」という単語内で「ｈｔｍｌ４．０をＤＯＣＴＹＰＥデータ設定し」をコメントアウトして「ｈｔｍｌ５をＤＯＣＴＹＰＥデータ設定し」を実行するように追記します。

```mind:cgilib/cgilib.src
※～略～
ＣＧＩＬＩＢ初期化０とは　本定義　　（file/ckaridef.srcにて仮定義）
	ｍｉｍｅセパレータ文字列作成し
	エラー出力を標準出力に切り替え
	ＢＡＳＥ６４テーブル初期化０し
	ｈｔｍｌ５をＤＯＣＴＹＰＥデータ設定し	※Pmod
※	ｈｔｍｌ４．０をＤＯＣＴＹＰＥデータ設定し
※	ｈｔｍｌ３．２をＤＯＣＴＹＰＥデータ設定し
※	ｈｔｍｌ２．０をＤＯＣＴＹＰＥデータ設定し
	ＤＯＳ環境
		ならば　ｓｊｉｓをｃｈａｒｓｅｔ設定し
		さもなければ
			ｅｕｃをｃｈａｒｓｅｔ設定し
		つぎに
	ヘッダ内平仮名を初期設定し
	名前と値の強制格納プールを獲得し	※2001/08/19
	「</HTML>」を　／ｈｔｍｌ定数に　入れ
	デフォルトのｎｐｈヘッダを　ｎｐｈヘッダ行に　入れ
	。
※～略～
```

## Mind CGIライブラリのコンパイル
### Mind8
```cmd:
C:\developments\vscode\mind9\cgilib>mind cgilib socketlibg obj\        

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
```

下位ライブラリはsocketlibgを指定してください。fileでもビルド通過しますが、この新しいcgilibを下位指定してビルド結果の拡張子がexeではなくcgiとなるのはこのsocketlibgの指定によるものです。


## Mind サンプルの修正
内容にオリジナルとの有意差はないのですが、生成されるhtmlを少し増やしています。
ＣＳＳデータ１と２にCSSへのリンクパスを設定しています。

```mind:cgilib\sample\test-form.src
メインとは
	「<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />」を　ＣＳＳデータ１に　入れ
	「<link rel="stylesheet" href="/css/site.css" />」を　ＣＳＳデータ２に　入れ
	「フォームのテスト」で　ｈｔｍｌヘッダを出力し

	Ｈ３開始　「お名前とご年齢を教えてください」を　表示し　Ｈ３終り
	ＢＲ
	ＢＲ

	「<FORM method="post" action="test-form-submit.cgi">」を　一行表示し
	「<INPUT type=hidden name="jcode-a" value="あ">」を　一行表示し
	「<div class="mb-3">」を　一行表示し
	「<label for="nameInput" class="form-label">」を　表示し
	「お名前：」を　表示し
	「</label>」を　一行表示し
	「<input type="text" name="name" placeholder="麻引堵太郎"><br>」を　一行表示し
	「<div id="nameHelp" class="form-text">(日本語でどうぞ)</div>」を　一行表示し
	「</div>」を　一行表示し
	「<div class="mb-3">」を　一行表示し
	「<label for="ageinput" class="form-label">」を　表示し
	「ご年齢：」を　表示し
	「</label>」を　一行表示し
	「<input type="text" name="age" placeholder="40"><br>」を　一行表示し
	ＢＲ
	「</div>」を　一行表示し
	「<INPUT TYPE="submit" name="send" VALUE="Send" class="btn btn-primary btn-lg">」を　一行表示し
	「  」を　表示し
	「<INPUT TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-warning btn-lg"><br>」を　一行表示し

	「</FORM>」を　一行表示する。

```
formのサブミット側のCGIにも、ＣＳＳデータ１と２にCSSへのリンクパスを設定しています。
```mind:cgilib\sample\test-form-submit.src
メインとは
	「<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />」を　ＣＳＳデータ１に　入れ
	「<link rel="stylesheet" href="/css/site.css" />」を　ＣＳＳデータ２に　入れ
	「フォームのテスト(フォームの受け取り)」で　ｈｔｍｌヘッダを出力し

	Ｈ３中央開始　「フォームデータを受け取りました」を　表示し　Ｈ３終り
	ＢＲ
	ＢＲ
```
## Mind 修正アプリのコンパイル
### Mind8
```cmd:
C:\developments\vscode\mind9\cgilib>mind sample\test-form obj\cgilib


日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindexcgi.exe --> sample\test-form.cgi

C:\developments\vscode\mind9\cgilib>mind sample\test-form-submit obj\cgilib  

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindexcgi.exe --> sample\test-form-submit.cgi
```

IIS配下のcgiフォルダに上記cgiファイルに対応した中間コードファイルmcoをコピーします。

# Webサーバー設定
IISの導入オプション状態とアプリケーションプールの状態は[こちらの記事](https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

# 実行開始
正常動作しました！:joy:


「フォームのテスト」cgi/test-form.cgi
![IIS10mindcgicss.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/8cc3f9e4-50b2-4c51-87c7-f7c697b4f674.jpeg)

「フォームの受け取り」cgi/test-form-submit.cgi
![IIS10mindcgicss2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/51e80cf4-23ff-46e4-baca-3b4193e120a4.jpeg)


# おわりに
いかがでしたでしょうか？:relaxed:なにかの役にたてば幸いです。

