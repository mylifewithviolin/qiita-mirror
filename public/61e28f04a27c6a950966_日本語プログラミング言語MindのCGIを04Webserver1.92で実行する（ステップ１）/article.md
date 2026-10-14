# はじめに
日本語プログラミング言語MindのCGIをそのレファレンス環境である04Webserverで実行するのステップ１です。[C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87.md)のは割と手がかかりそうなので、Mind開発者の@killyさんのご提案に従い、いったん確実に動作する環境で完走状態を確認いたします。

# 前提条件
Windows11 Pro 22H2 22621.4169
Mind Version 8.0.08 for Windows
04Webserver 1.92

# 環境の構成
[C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87.md)のフォルダ環境をそのまま使います。C#とkestrelで実行していた場合は、アプリ本体の中間コードファイルmcoはプロジェクトルートに置かないと実行できませんでしたが、今回はCGI実行フォルダに引っ越しています。mcoのないcgiファイルは引っ越し未完了のものです。

```cmd:
C:\developments\vscode\kestrelcgi
├─cgi
│      helloMind.cgi
│      helloMind.mco
│      helloweb.cgi
│      helloweb.mco
│      mrunt160.exe
│      showvars.cgi
│      showvars.mco
│      test-cookie-submit.cgi
│      test-cookie.cgi
│      test-form-submit.cgi
│      test-form-submit.mco
│      test-form.cgi
│      test-form.mco
│      testupl.cgi
└─wwwroot
    │  favicon.ico
    │  helloweb.html
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

# Webサーバー設定

@Mind-Club_2017さんの [こちらの記事](https://qiita.com/Mind-Club_2017/items/0fdad646aff08a87618d)を参考に、04Webserverを構成します。

スタートメニューから
「04WebServer サーバコントローラ」を起動します。
わたしの環境ではポート番号80がIIS10.0に使われているため、サーバー情報パネルに、04Webserverの起動失敗が赤字で表示されました。

## サーバ設定
「サーバ設定」を選び、「ネットワーク設定」の「ポート番号」を既定の80から8080に変更しました。他は既定のままです。
「サーバ再起動」で正常起動しました。

### SSI/CGIの設定
既定のままです。（SSI使用予定ないためshtmlのみのままです。）

## ドキュメントルートの設定
「ディレクトリ設定」を選び、「ドキュメントルート」をダブルクリックします。下記以外の項目は既定のままです。

### 基本設定

|項目名|設定値|備考|
|:-:|:-:|:-:|
|説明|ドキュメントルート|既定値|
|ServerPath|/|既定値|
|LocalPath|C:\developments\vscode\kestrelcgi\wwwroot||

### 詳細設定

|項目名|設定値|備考|
|:-:|:-:|:-:|
|SSI/CGIを許可|ノーチェック|既定値|


## CGI実行パスの設定
「ディレクトリ設定」を選び、左上あたりの「新規」をクリックします。下記以外の項目は既定のままです。

### 基本設定

|項目名|設定値|備考|
|:-:|:-:|:-:|
|説明|CGI||
|ServerPath|/cgi||
|LocalPath|C:\developments\vscode\kestrelcgi\cgi||

### 詳細設定

|項目名|設定値|備考|
|:-:|:-:|:-:|
|SSI/CGIを許可|チェック|有効|

# Mind CGIアプリケーションの作成

今回もMind9のCGIサンプルをそのまま動かしてみます。
「CGIで出力するhtmlドキュメント」helloweb.cgi
「標準CGI変数の確認」showvars.cgi.cgi
「フォームのテスト」cgi/test-form.cgi

# 実行開始
３機能とも正常動作しました！:joy:

![mindcgi14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/60768d32-7b2b-cf11-04f0-5c6baf127c6b.png)

![mindcgi15.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/403bd5ed-4880-7217-16aa-78b0aeb8b1b1.png)


![mindcgi16.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/b282362a-151e-ee52-3c3c-413a38c0491e.png)


# おわりに
いかがでしたでしょうか？04Webserverを初めて操作しましたが、設定が簡単ですばらしいですね。この記事を書くために一度閉じていたサーバーコントローラを再度起動しようとすると、バックグラウンドプロセスとしてはサーバー本体とサーバーコントローラが起動するのですが、設定コントローラのアプリケーションウィンドウが開かなくなりました。アンインストールして再インストールしても回復していません:joy:設定はアンインストールしても残っているようで、Mindの環境は動作しています。

## 補足

とりあえずわたしの環境では互換性設定を下図の状態としましたところ、設定コントローラウィンドウが展開するようになりました。カラーモード制限するをチェックしない場合はXpSP3でも展開しなかったので、互換モードよりグラフィックまわりでなにかトラブっていたのかもしれません。

![mindcgi17.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/57d0e6b9-6587-4829-4f93-f3dffc1d85b4.png)

## 補足２
上記のオプションすべて解除して既定に戻したところでも正常展開しました。再インストールしても再起動しても治らなかった現象ですが、とりあえず一時的な不具合が上記のオプション変更で解消されて、後は治った状態が維持されたのかもしれません:joy:プロセスとしては起動してもウィンドウが展開しない現象に見舞われた場合は有効かもです。
