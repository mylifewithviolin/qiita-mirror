# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ５です。IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法をステップ２までで確定いたしました。ステップ３と４でランタイム側のCgilibのソースを少し改修してCSSとjavaScriptファイルのインクルードを試みましたが、Mind開発者の@killyさんよりメイン側だけで対応できるのではというサジェストをいただきましたので、今回はその方向を検証してみます。

前提条件
Windows11 Pro 22H2 22621.4317
Mind Version 8.0.08 for Windows
Internet Information Servicies 10.0

# 環境の構成
[C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87)のフォルダ環境をほぼそのまま使います。

C#とkestrelで実行していた場合は、アプリ本体の中間コードファイルmcoはプロジェクトルートに置かないと実行できませんでしたが、IISの場合はCGI実行フォルダに引っ越しています。

```cmd:
C:\developments\vscode\kestrelcgi
├─cgi
│      include.html
│      include2.html
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

今回はMind8のCGIサンプルを少し修正して動かしますが、動かすのは実行パスに設定した下記の機能です。
「フォームのテスト」cgi/test-form.cgi

cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされるとします。



## Mind サンプルの修正
内容にオリジナルとの有意差はないのですが、生成されるhtmlを少し増やしています。
ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌでヘッダタグの出力を抑制して、
Content-type: text/html; charset=shift_jis
だけの出力とし、ヘッダタグを含むinclude.htmlを別ファイルで作成しておき、それをインクルードします。

```html:include.html
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />
<link rel="stylesheet" href="/css/site.css" />
<title>フォームのテスト</title>
</head>
<body>
```
<body>タグが出力されないようなので、include.htmlに含めています。
ヘッダタグ内ではなく、ボディのロードが終わった場合にJavascriptをロードしたい場合は下記のように別のインクルードファイルにしておきます。

```html:include2.html
</body>
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>

```
```mind:cgilib\sample\test-form.src
メインとは
	ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌし
　　「include.html」を　このファイルをインクルードし

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

	「</FORM>」を　一行表示し
	「include2.html」を　このファイルをインクルードする。
```
メインの末尾でJsの「include2.html」をインクルードしています。
formのサブミット側のCGIにも、同様にしています。
```mind:cgilib\sample\test-form-submit.src
	ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌし
　　「include.html」を　このファイルをインクルードし

	Ｈ３中央開始　「フォームデータを受け取りました」を　表示し　Ｈ３終り
	ＢＲ
	ＢＲ
```
## Mind 修正アプリのコンパイル
### Mind8
```cmd:
C:\developments\vscode\mind9\cgilib>mind sample\test-form cgilib


日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindexcgi.exe --> sample\test-form.cgi

C:\developments\vscode\mind9\cgilib>mind sample\test-form-submit cgilib  

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

![mindcgistep5.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/bea51c51-1f1e-4207-b848-9a1f0409834e.jpeg)


下記はソース表示したHTMLです。
```html:
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />
<link rel="stylesheet" href="/css/site.css" />
<title>フォームのテスト</title>
</head>
<body>
<H3>お名前とご年齢を教えてください</H3><BR>
<BR>
<FORM method="post" action="test-form-submit.cgi">
<INPUT type=hidden name="jcode-a" value="あ">
<div class="mb-3">
<label for="nameInput" class="form-label">お名前：</label>
<input type="text" name="name" placeholder="麻引堵太郎"><br>
<div id="nameHelp" class="form-text">(日本語でどうぞ)</div>
</div>
<div class="mb-3">
<label for="ageinput" class="form-label">ご年齢：</label>
<input type="text" name="age" placeholder="40"><br>
<BR>
</div>
<INPUT TYPE="submit" name="send" VALUE="Send" class="btn btn-primary btn-lg">
  <INPUT TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-warning btn-lg"><br>
</FORM>
</body>
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>

</HTML>
```

# おわりに
いかがでしたでしょうか？:relaxed:なにかの役にたてば幸いです。タイトルは置換してインクルードを使えばそこだけ値を変えられる共通テンプレにできそうです。
