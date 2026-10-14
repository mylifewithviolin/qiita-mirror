# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ８です。IISでの設定方法をステップ２までで確定いたしました。ステップ７でind７．５から導入されたコールバック処理単語でHTMLのプレースホルダを動的に書き換える処理を検証しましたが、前回は単純な文字列置換でしたので、今回はプルダウン要素を動的に生成することを検証してみます。

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
内容的にオリジナルと大差はないのですが、今回は性別の選択プルダウンを追加します。このOPTIONタグをコールバックに対応したプレースホルダで記述しておきます。MindCGIのプレースホルダはHTMLのコメントタグとなります。前回のラベルの置換はすべてリテラルに戻し、テキストボックスタグに表示されるplaceholderの内容を動的に置換できるようにします。

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
include.htmlはいくつかの機能で共通となる場合があるため、test-form.htmlとは分離しています。MindCGIソースのメインで「ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌ」を実行していますが、下記のメタタグが出力されなかったのでinclude.htmlに記載しています。
```html:
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
```
test-formのhtmlテンプレートです。ラベルの内容はリテラルに戻しています。

```html:test-form.html
<body>
<h3>お名前とご年齢を教えてください</h3><br>
<br>
<form method="post" action="test-form-submit.cgi">
<input type=hidden name="jcode-a" value="あ">
<div class="mb-3">
<label for="nameInput" class="form-label">氏名：</label>
<!--here name-input-->
<div id="nameHelp" class="form-text">&emsp;(日本語でどうぞ)</div>
</div>
<div class="mb-3">
<label for="ageinput" class="form-label">年齢：</label>
<!--here age-input--><br>
</div>
<div class="mb-3">
<label for="genderinput" class="form-label">性別：</label>
<select name="genders" id="gender-select">
  <!--here gender-options-->
</select><br>
</div>
<br><br>
  <input TYPE="submit" name="send" VALUE="Send" class="btn btn-warning btn-lg">
  <input TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-primary btn-lg"><br>
</form>
</body>
```

```html:include2.html
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>
```
テキストボックスタグに表示されるplaceholderの内容を動的に置換できるようにコールバック単語で処理させていますが、このサンプルではplaceholderの内容はMindソース側のハードコーディングです。

```mind:cgilib\sample\test-form.src
性別選択肢とは　文字列定数配列
「--　選択してください　--」
「女性」
「男性」。

コールバック・titleとは　（・　→　結果）
	「フォームのテスト」を　返すこと。

コールバック・name-inputとは　（・　→　結果）
		氏名入力は　文字列実体
	氏名入力に　「<input type="text" name="name" placeholder="」を　入れ
	氏名入力に　「麻引堵太郎」を　追加し
	氏名入力に　「">」を　追加し　
	氏名入力を　返すこと。

コールバック・age-inputとは　（・　→　結果）
		年齢入力は　文字列実体
	年齢入力に　「<input type="text" name="age" placeholder="」を　入れ
	40を　文字列変換し　
	年齢入力に　追加し
	年齢入力に　「">」を　追加し　
	年齢入力を　返すこと。

コールバック・gender-optionsとは　（・　→　結果）
		性別選択は　文字列実体　長さ　360桁
	性別選択に　「」を　入れ
	性別選択肢の　要素数で　回数指定し
		性別選択に　「<option value="」を　追加し
		回数が　１に　等しい
		でなければ
			回数から　１を　引いて　文字列変換し
			性別選択に　追加し	
		つぎに
		性別選択に　「">」を　追加し
		性別選択に　性別選択肢（回数）を　追加し
		性別選択に　「</option>」を　追加し
    繰り返す
	性別選択を　返すこと。



コールバックとは　（引数　→　結果）
	文字列事例をとる
		「title」なら　　		コールバック・title
		「name-input」なら　　	コールバック・name-input 
		「age-input」なら　　	コールバック・age-input
		「gender-options」なら　コールバック・gender-options
		例外なら				コールバックエラー定数
	事例終り。

メインとは
	ｍｉｍｅヘッダ出力・ｔｅｘｔ／ｈｔｍｌし

	「include.html」を　"ALL"と　コールバックの　Ｍコードで　
						このファイルをインクルード２し
	「test-form.html」を　"ALL"と　コールバックの　Ｍコードで　
						このファイルをインクルード２し
	「include2.html」を　このファイルをインクルードする。
```
コールバック・gender-optionsが性別選択プルダウンのOPTIONタグを動的に構成しているところです。選択肢の内容は文字列定数配列としていますが、このあたりは本格的に実装するならばデータベースのマスタから取得したりするとよさそうです。

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

IIS配下のcgiフォルダに上記cgiファイルに対応した中間コードファイルmcoをコピーします。修正したtest-form.htmlも忘れずに。

# Webサーバー設定
IISの導入オプション状態とアプリケーションプールの状態は[こちらの記事](https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

# 実行開始
正常動作しました！:joy:

![mindcgistep8.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/20c8ee6b-4862-4b47-940a-5bf260ec3a9c.jpeg)



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
<h3>お名前とご年齢を教えてください</h3><br>
<br>
<form method="post" action="test-form-submit.cgi">
<input type=hidden name="jcode-a" value="あ">
<div class="mb-3">
<label for="nameInput" class="form-label">氏名：</label>
<input type="text" name="name" placeholder="麻引堵太郎"><div id="nameHelp" class="form-text">&emsp;(日本語でどうぞ)</div>
</div>
<div class="mb-3">
<label for="ageinput" class="form-label">年齢：</label>
<input type="text" name="age" placeholder="40"><br>
</div>
<div class="mb-3">
<label for="genderinput" class="form-label">性別：</label>
<select name="genders" id="gender-select">
  <option value="">--　選択してください　--</option><option value="1">女性</option><option value="2">男性</option></select><br>
</div>
<br><br>
  <input TYPE="submit" name="send" VALUE="Send" class="btn btn-warning btn-lg">
  <input TYPE="reset" name="reset" VALUE="Clear" class="btn btn-outline-primary btn-lg"><br>
</form>
<script src="/lib/jquery/dist/jquery.min.js"></script>
<script src="/lib/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
<script src="/js/site.js"></script>

</BODY>
</HTML>
```
jsのインクルードは\</BODY>タグの内側に出力されました。test-form.htmlに記述したのは「\</body>」なので、こちらは抑止されてMindランタイムcgiライブラリが「\</BODY>」を出力したようです。

# おわりに
いかがでしたでしょうか？:relaxed:なにかの役にたてば幸いです。プルダウンの選択肢を動的に生成することができました。応用としてはラジオボタンやチェックボックスなども同様に生成できそうです。
