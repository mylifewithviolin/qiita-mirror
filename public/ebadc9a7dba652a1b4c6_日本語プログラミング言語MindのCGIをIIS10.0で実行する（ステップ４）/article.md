# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ４です。IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法をステップ２までで確定いたしました。今回はjavaScriptファイルのインクルードを試みます。


 前提条件
Windows11 Pro 22H2 22621.4317
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

今回もMind8のCGIサンプルを少し修正して動かしますが、動かすのは実行パス設定した下記の機能です。
「フォームのテスト」cgi/test-form.cgi

cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
からmrunt160.exeランタイムがコピーされています。

## Mind CGIライブラリの修正
ソースコード提供されているCGIライブラリのheader.srcを修正します。

「ＪＳデータ１、２、３」という文字列実体変数を追加。
「ｈｔｍｌフッタ出力」という単語内で「ＪＳデータ１、２、３」の出力処理を追加します。

```mind:cgilib/header.src
※～略～
ＭＥＴＡデータ１とは　  　　文字列実体　長さ　１２８。
ＭＥＴＡデータ２とは　  　　文字列実体　長さ　１２８。
ＤＯＣＴＹＰＥデータとは　　文字列実体　長さ　１２８。
ＣＳＳデータ１とは　  　　　文字列実体　長さ　１２８。
ＣＳＳデータ２とは　  　　　文字列実体　長さ　１２８。
ＣＳＳデータ３とは　  　　　文字列実体　長さ　１２８。
ＢＯＤＹデータとは　　　　　文字列実体　長さ　１２８。
ヘッダ内平仮名は　　　　　　文字列実体　長さ　　８０。
ＪＳデータ１とは　  　　　　文字列実体　長さ　１２８。※追加
ＪＳデータ２とは　  　　　　文字列実体　長さ　１２８。※追加
ＪＳデータ３とは　  　　　　文字列実体　長さ　１２８。※追加

    
※～略～
ｈｔｍｌフッタ出力とは　（・　→　・）
	ＣＧＩＬＩＢ緊急処理中が　偽？
		ならば　スタック検査０し　偽？
			ならば　「<br><br><h3>エラー：スタックがずれてい」続
				「ます(CGI終了時)</h3>」を　表示し
			つぎに
		つぎに
	ＪＳデータ１が　非空列？
		ならば　※注：</BODY>より前に※
			ＪＳデータ１を　一行表示し
		つぎに
	ＪＳデータ２が　非空列？
		ならば　※注：</BODY>より前に※
			ＪＳデータ２を　一行表示し
		つぎに
	ＪＳデータ３が　非空列？
		ならば　※注：</BODY>より前に※
			ＪＳデータ３を　一行表示し
		つぎに
	ｈｔｍｌヘッダ出力済みが　ゼロ？
		ならば　終り
		つぎに
　　（－－ｈｔｍｌヘッダが出力されている－－）
	改行し
	ｈｔｍｌヘッダ出力済みが　ヘッダ出力済み・ｂｏｄｙ　以上
		ならば　「</BODY>」を　一行表示し
	　　　　	ヘッダ出力済み・ｈｔｍｌヘッダを
			　　　　　　　　ｈｔｍｌヘッダ出力済みに　入れ
		つぎに
	／ｈｔｍｌ定数を　一行表示し
	ｈｔｍｌヘッダ出力済みを　クリアする。

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
ＪＳデータ１と２と３にjavascriptファイルへのソースパスを設定しています。

```mind:cgilib\sample\test-form.src
メインとは
	「<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />」を　ＣＳＳデータ１に　入れ
	「<link rel="stylesheet" href="/css/site.css" />」を　ＣＳＳデータ２に　入れ
    「<script src="/lib/jquery/dist/jquery.min.js"></script>」を　ＪＳデータ１に　入れ
	「<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>」を　ＪＳデータ２に　入れ
	「<script src="/js/site.js"></script>」を　ＪＳデータ３に　入れ
    
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

## Mind 修正アプリのコンパイル
### Mind8
```cmd:
C:\developments\vscode\mind9\cgilib>mind sample\test-form obj\cgilib


日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindexcgi.exe --> sample\test-form.cgi

```

IIS配下のcgiフォルダに上記cgiファイルに対応した中間コードファイルmcoをコピーします。

# Webサーバー設定
IISの導入オプション状態とアプリケーションプールの状態は[こちらの記事](https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

# 実行開始
Javascriptファイルがインクルードされているのを確認しました！:joy:


「フォームのテスト」cgi/test-form.cgi
![IIS10mindcgijs.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/b3413c2b-272b-4b10-958a-284deb4a4129.jpeg)

</From>タグの直後にインクリードされています。

![IIS10mindcgijs2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5ab83c0c-22c8-4c8d-93c5-0ce2bb2274c0.jpeg)

DOCTYPEをHTML5にしたせいか<html>タグに言語属性がないという警告が出ていますので、追って対応します。


# おわりに
いかがでしたでしょうか？:relaxed:なにかの役にたてば幸いです。

