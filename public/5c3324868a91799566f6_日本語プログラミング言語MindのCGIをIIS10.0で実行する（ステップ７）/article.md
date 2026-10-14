# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ７です。IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法をステップ２までで確定いたしました。ステップ６でプレースホルダ付きのHTMLにCSSとjavaScriptファイルのインクルードを試みましたが、今回はMind７．５から導入されたコールバック処理単語でHTMLのプレースホルダを動的に書き換える処理を検証しみます。

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
│      test-form.html
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

今回もMind8のCGIサンプルを少し修正して動かしますが、動かすのは実行パスに設定した下記の機能です。
「フォームのテスト」cgi/test-form.cgi

cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされるとします。



## Mind サンプルの修正
内容にオリジナルとの有意差はないのですが、test-form.htmlにBodyの内容を通常のHTMLで記述し、一部の文字列をコールバックに対応したプレースホルダで記述しておきます。プレースホルダはHTMLのコメントタグとなります。include.htmlのtitleのプレースホルダもHTMLのコメントタグとなります。

```html:include.html
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" href="/lib/bootstrap/dist/css/bootstrap.min.css" />
<link rel="stylesheet" href="/css/site.css" />
<title><!--here title--></title>
</head>
```

```html:test-form.html
<body>
<H3><!--here guide--></H3><BR>
<BR>
<FORM method="post" action="test-form-submit.cgi">
<INPUT type=hidden name="jcode-a" value="あ">
<div class="mb-3">
<label for="nameInput" class="form-label"><!--here name--></label>
<input type="text" name="name" placeholder="麻引堵太郎"><br>
<div id="nameHelp" class="form-text"><!--here japanese--></div>
</div>
<div class="mb-3">
<label for="ageinput" class="form-label"><!--here age--></label>
<input type="text" name="age" placeholder="40"><br>
<BR>
</div>
<INPUT TYPE="submit" name="send" VALUE="Send" class="btn btn-warning btn-lg">
  <INPUT TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-primary btn-lg"><br>
</FORM>
</body>
```
ボディタグはtest-form.htmlに記述しました。include2.htmlはJSのインクルードなので、プレースホルダなしの通常の「このファイルをインクルード」を使います。

```html:include2.html
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>

```

```mind:cgilib\sample\test-form.src
コールバック・titleとは　（・　→　結果）
	「フォームのテスト」を　返すこと。

コールバック・guideとは　（・　→　結果）
	「お名前とご年齢を教えてください」を　返すこと。

コールバック・nameとは　（・　→　結果）
	「氏名：」を　返すこと。

コールバック・ageとは　（・　→　結果）
	「年齢：」を　返すこと。

コールバック・japaneseとは　（・　→　結果）
　　「(日本語でどうぞ)」を　返すこと。

コールバックとは　（引数　→　結果）
	文字列事例をとる
		「title」なら　　	コールバック・title
		「guide」なら　　	コールバック・guide
		「name」なら　　	コールバック・name
		「age」なら　　		コールバック・age
		「japanese」なら　	コールバック・japanese
		例外なら			コールバックエラー定数
	事例終り。

メインとは
	ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌし

	「include.html」を　"ALL"と　コールバックの　Ｍコードで　
						このファイルをインクルード２し
	「test-form.html」を　"ALL"と　コールバックの　Ｍコードで　
						このファイルをインクルード２し
	「include2.html」を　このファイルをインクルードする。
```
include.htmlはいくつかの機能で共通となる場合があるため、test-form.htmlとは分離しています。ここは解説資料ですと上記のように分割してインクルードすることは想定外かもしれません。「ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌ」を実行していますが、下記のメタタグが出力されなかったのでinclude.htmlに記載しています。
```html:
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
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

```

IIS配下のcgiフォルダに上記cgiファイルに対応した中間コードファイルmcoをコピーします。追加したtest-form.htmlや修正したinclude.htmlも忘れずに。

# Webサーバー設定
IISの導入オプション状態とアプリケーションプールの状態は[こちらの記事](https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

# 実行開始
正常動作しました！:joy:CSSも反映されています。

![mindcgistep7.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/fc50c76d-ac4c-443f-91fb-f1d2b85c9be1.jpeg)


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
<label for="nameInput" class="form-label">氏名：</label>
<input type="text" name="name" placeholder="麻引堵太郎"><br>
<div id="nameHelp" class="form-text">(日本語でどうぞ)</div>
</div>
<div class="mb-3">
<label for="ageinput" class="form-label">年齢：</label>
<input type="text" name="age" placeholder="40"><br>
<BR>
</div>
<INPUT TYPE="submit" name="send" VALUE="Send" class="btn btn-warning btn-lg">
  <INPUT TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-primary btn-lg"><br>
</FORM>
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>

</BODY>
</HTML>
```
jsのインクルードは\</BODY>タグの内側に出力されました。test-form.htmlに記述したのは「\</body>」なので、こちらは抑止されてMindランタイムcgiライブラリが「\</BODY>」を出力したようです。

# おわりに
いかがでしたでしょうか？:relaxed:なにかの役にたてば幸いです。文字列を置換するだけなら「このファイルを置換しながらインクルードする」でもよい気がしますが、コールバックでインクルードの場合は、プレースホルダのキー名の次の空白区切りの文字を引数としてスタックに置けるというのがあるようなので、次回はそちらを検証してみます。
