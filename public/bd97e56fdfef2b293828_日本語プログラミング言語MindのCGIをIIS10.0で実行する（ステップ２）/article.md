# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ２です。MindCGIの実行シーケンスについてMind開発者の@killyさんにご解説していただきだいぶ様子がわかりましたので、IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法を確定いたしました。今回はデフォルトのwwwrootではなく独自に作成したフォルダで検証します。

# 前提条件
Windows11 Pro 22H2 22621.4169
Mind Version 8.0.08 for Windows
Internet Information Servicies 10.0

# 環境の構成
[C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87)のフォルダ環境をほぼそのまま使います。

C#とkestrelで実行していた場合は、アプリ本体の中間コードファイルmcoはプロジェクトルートに置かないと実行できませんでしたが、今回はCGI実行フォルダに引っ越しています。mcoのないcgiファイルは引っ越し未完了のものです。

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

\kestrelcgi\cgiのアクセス権は下図のようになっています。BUILTIN\IIS_IUSRに読み取りと実行可の権限が付与しされました。このあたりはフォルダをアプリケーション化するとつけられるようです。

```powershell:
PS C:\developments\vscode\kestrelcgi> Get-ChildItem -Force -Recurse |where { $_.mode -match “d” } |Get-Acl | Select-object @{Label=”Path”;Expression={Convert-Path $_.Path}}, Owner, AccessToString | Format-List

Path           : C:\developments\vscode\kestrelcgi\cgi
Owner          : DESKTOP-078KPRA\mylifewithviolin
AccessToString : BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\Administrators Allow  FullControl
                 NT AUTHORITY\SYSTEM Allow  FullControl
                 BUILTIN\Users Allow  ReadAndExecute, Synchronize
                 NT AUTHORITY\Authenticated Users Allow  Modify, Synchronize
                 NT AUTHORITY\Authenticated Users Allow  -536805376

Path           : C:\developments\vscode\kestrelcgi\wwwroot
Owner          : DESKTOP-078KPRA\mylifewithviolin
AccessToString : BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\Administrators Allow  FullControl
                 NT AUTHORITY\SYSTEM Allow  FullControl
                 BUILTIN\Users Allow  ReadAndExecute, Synchronize
                 NT AUTHORITY\Authenticated Users Allow  Modify, Synchronize
                 NT AUTHORITY\Authenticated Users Allow  -536805376
```

# Mind CGIアプリケーションの作成

今回もMind9のCGIサンプルをそのまま動かしますが、動かすのは実行パス設定した下記の３機能です。
「CGIで出力するhtmlドキュメント」helloweb.cgi
「標準CGI変数の確認」showvars.cgi.cgi
「フォームのテスト」cgi/test-form.cgi

cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされています。

# Webサーバー設定

IISの導入オプション状態とアプリケーションプールの状態は[前回の記事](https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

「インターネットインフォメーションサービス(IIS)マネージャ」を開きます。「Default Web Site」をクリックしてから、右側の「サイトの編集」の「基本設定」をクリックして、物理パスを今回のWWWrootに変更します。

![mindcgi20.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/f9d43f99-0657-ab87-4d9f-481c31018ecf.png)

「Default Web Site」を右クリックして「仮想ディレクトリの追加」を選択して、仮想ディレクトリの設定を下図のように行います。

![mindcgi21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4695cebc-0998-c4bb-c89a-e4864853e5e5.png)

作成された仮想ディレクトリcgiのノードをクリックして機能ペインを下図の状態とします。ここで、「ハンドラーマッピング」をクリックしておきます。

![mindcgi22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6e016ccd-ea0f-259a-3e13-c86038a544fa.png)

右側の操作ペインの「機能を開く」をクリックします。下図の状態となります。

![mindcgi23.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d4e68c50-5cce-e33c-b892-cfaf81a2b6d0.png)

右側の操作ペインの「モジュールマップの追加」をクリックします。（これが正解でした。開いたダイアログはすべてブランクですが下図の状態のように設定します。「実行可能ファイル（オプション）」はブランクのままがキモです。:santa_tone2:

![mindcgi24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d955a485-1c00-4fd4-8bf8-7b516545cf85.png)

「モジュールマップの追加」ダイアログの「要求の制限」ボタンをクリックします。「要求の制限」ダイアログの「アクセス」タブだけ下図のように「実行」に変更します。既定は「スクリプト」

![mindcgi25.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c6c8b86c-18a9-7028-fa95-6ce862783fcd.png)

「OK」でダイアログを閉じていくと機能ペインは下図の状態となります。

![mindcgi26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/037f462d-3da6-a2b4-06c4-68a50076b2ad.png)

まだCGIは有効になっていませんので、この行を選択したまま右側の操作ペインの「機能のアクセス許可の編集」をクリックします。下図のダイアログが開きますので、ここで「実行」にもチェックします。（既定では「実行」にはチェックがついていません。）

![mindcgi45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/10bdce92-75d1-a1f0-b572-b10f55f0bc3b.png)


ここまでできたら、次はホームノードをクリックします。（コンピュータ名になっている場合が多いようです。）下図は機能ペインの「ISAPIおよびCGI機能の制限」をクリックしてある状態です。右側の操作ペインの「機能を開く」をクリックします。

![mindcgi26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2f5aaaa4-1a42-1d61-1e7a-27f4e3982554.png)

下図の状態となりますので、右側の「追加」をクリックします。

![mindcgi27.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9f125bea-42e5-2f57-918d-f8c52e0d5012.png)

「ISAPIおよびCGI機能の制限」ダイアログが開きますので、mrunt160.exeのパスを追加して、「拡張パスの実行を許可する」にチェックを入れてダイアログを閉じます。

![mindcgi28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/eaf5f249-4df4-11bb-8856-55be142979c1.png)

つづいて、実行したいcgiのファイルのパスを同じように追加します。ここもキモです。:santa_tone2:

![mindcgi29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7d65ea92-13e6-9c02-b5ce-ae02e1db3bfe.png)

ワイルドカードを指定すると怒られるので、ここは個別に追加しないといけません。

以上の設定が完了しましたら、IIS全体または仮想サイトを再起動します。今回はアプリケーション化を行わず仮想ディレクトリのままで検証してみました。


# 実行開始
３機能とも正常動作しました！:joy:

「CGIで出力するhtmlドキュメント」helloweb.cgi
![mindcgi46.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/a111d232-4372-bbcb-607e-88d62acfb6f6.png)

「標準CGI変数の確認」showvars.cgi.cgi
![mindcgi47.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/efbd232a-2ddd-bf23-d917-562dbbb2ea9c.png)

「フォームのテスト」cgi/test-form.cgi
![mindcgi48.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/baef7e9b-e10c-bbe6-7951-be7d22dd0662.png)

# おわりに
いかがでしたでしょうか？説明を書くのにスクショをたくさんとったので少し疲れました:relaxed:なにかの役にたてば幸いです。
さて、これはいちおう序の口で、なんかアプリを書くのが目標なのですが、少し休憩します。kestrelはなぜパラメータがうまく渡らないのか気になります。
