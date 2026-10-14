# はじめに
日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ１です。MindCGIの実行シーケンスについて、Mind開発者の@killyさんにご解説していただき、IIS（Windowsに古くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法を確定いたしました。


# 前提条件
Windows11 Pro 22H2 22621.4169
Mind Version 8.0.08 for Windows
Internet Information Servicies 10.0

# 環境の構成
今回はIISをインストールすると作成されるInetpub\wwwroot配下で実行します。IIS実行アカウントなどの構成が不十分の環境の場合は実行を拒否されますので、今回はなるべくデフォルトで実行できる環境を確認します。

```cmd:
C:\inetpub>tree

C:.
├─custerr
│  └─ja-JP
├─history
├─logs
├─temp
│  ├─appPools
│  └─IIS Temporary Compressed Files
└─wwwroot
    └─sample
```

wwwroot配下のアクセス権は下図のようになっています。

```powershell:
PS C:\inetpub> Get-ChildItem -Force -Recurse |where { $_.mode -match “d” } |Get-Acl | Select-object @{Label=”Path”;Expression={Convert-Path $_.Path}}, Owner, AccessToString | Format-List

Path           : C:\inetpub\wwwroot
Owner          : NT AUTHORITY\SYSTEM
AccessToString : BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\IIS_IUSRS Allow  -1610612736
                 NT SERVICE\TrustedInstaller Allow  FullControl
                 NT SERVICE\TrustedInstaller Allow  268435456
                 NT AUTHORITY\SYSTEM Allow  FullControl
                 NT AUTHORITY\SYSTEM Allow  268435456
                 BUILTIN\Administrators Allow  FullControl
                 BUILTIN\Administrators Allow  268435456
                 BUILTIN\Users Allow  ReadAndExecute, Synchronize
                 BUILTIN\Users Allow  -1610612736
                 CREATOR OWNER Allow  268435456
                 
Path           : C:\inetpub\wwwroot\sample
Owner          : BUILTIN\Administrators
AccessToString : BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\IIS_IUSRS Allow  -1610612736
                 NT SERVICE\TrustedInstaller Allow  FullControl
                 NT SERVICE\TrustedInstaller Allow  268435456
                 NT AUTHORITY\SYSTEM Allow  FullControl
                 NT AUTHORITY\SYSTEM Allow  268435456
                 BUILTIN\Administrators Allow  FullControl
                 BUILTIN\Administrators Allow  268435456
                 BUILTIN\Users Allow  ReadAndExecute, Synchronize
                 BUILTIN\Users Allow  -1610612736
                 CREATOR OWNER Allow  268435456

Path           : C:\inetpub\wwwroot\sample\uploaded
Owner          : BUILTIN\Administrators
AccessToString : BUILTIN\IIS_IUSRS Allow  ReadAndExecute, Synchronize
                 BUILTIN\IIS_IUSRS Allow  -1610612736
                 NT SERVICE\TrustedInstaller Allow  FullControl
                 NT SERVICE\TrustedInstaller Allow  268435456
                 NT AUTHORITY\SYSTEM Allow  FullControl
                 NT AUTHORITY\SYSTEM Allow  268435456
                 BUILTIN\Administrators Allow  FullControl
                 BUILTIN\Administrators Allow  268435456
                 BUILTIN\Users Allow  ReadAndExecute, Synchronize
                 BUILTIN\Users Allow  -1610612736
                 CREATOR OWNER Allow  268435456
```

# Mind CGIアプリケーションの作成

今回もMind9のCGIサンプルをそのまま動かしますが、動かすのは実行パスを設定する下記の３機能だけです。
「CGIで出力するhtmlドキュメント」helloweb.cgi
「標準CGI変数の確認」showvars.cgi.cgi
「フォームのテスト」cgi/test-form.cgi

ただし、sampleフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\sample
サンプルファイルをビルド済ですべてコピーしてあります。

# Webサーバー（IIS）設定

IISはインストール済ですが、どのような状態でインストールしたかを確認するため、「コントロールパネル」を開いて、「Windowsの機能の有効化または無効化」パネルを開きます。

![mindcgi18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/624bdbc7-86ee-424e-b9fa-fd7ebb91153b.png)

今回はCGIのためだけに導入しますので、なるべくよけいなのははずしています。

「インターネットインフォメーションサービス(IIS)マネージャ」を開きます。アプリケーションプールは当初MindCGIが動かせなかったときはいろいろいじり倒していたのですが、今回動作検証とれた設定はデフォルトでした。32ビットアプリケーションの有効化も行っていません。（CGIなのでプロセス空間またぐため基本的には関係ないはずではありますね。）

![mindcgi19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/93482993-70a5-9409-7180-c9a1c6bce423.png)

ホームノードをクリックします。（コンピュータ名になっている場合が多いようです。）下図は機能ペインの「ISAPIおよびCGI機能の制限」をクリックしてある状態です。この状態で右側の操作ペインの「機能を開く」をクリックします。

![mindcgi30.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/386cefe6-e346-ba98-a909-43fb54c9e849.png)

下図の状態となりますので、右側の「追加」をクリックします。

![mindcgi31.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/842bfed5-5043-537d-5bdd-3ca6a74731fe.png)

「ISAPIおよびCGI機能の制限」ダイアログが開きますので、mrunt160.exeのパスを追加して、「拡張パスの実行を許可する」にチェックを入れてダイアログを閉じます。

![mindcgi32.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/97658570-5202-77f1-b143-b28ecd542c1e.png)

つづいて、実行したいcgiのファイルのパスを同じように追加します。ここがキモでした。:santa_tone2:これから説明するハンドラーマッピングのダイアログでは実行ファイルは拡張子がdllまたはexeのファイルしか選択できず、Mindのcgiファイルを実行設定でず、にっちもさっちもいかなくなるのですが、ここで登録できます。

ここではワイルドカードは使えないので一ファイルづつの設定となります。オプションで「特定できないCGIモジュールを許可する」というのがあるのですが、それはまた別の機会で。１つづつcgiファイルを登録しなければならないのはいかがなものかという感覚もあるかもしれませんが、わたし的にはWeb配信フォルダ下で実行ファイルが動作するというのはちょっとこわい感じもするので好感がもてます。

「Default Web Site」ノードをクリックすると、既定で「C:\inetpub\wwwroot」とバインドされていますので、「sample」フォルダノードが出現します。「sample」フォルダノードをクリックすると機能ペインが下図のようになります。（ハンドラーマッピングをクリックしてフォーカスをあてています。）

![mindcgi33.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5f59b2f5-a03a-700c-94e7-2220ed9fd195.png)

右側の操作ペインの「機能を開く」をクリックします。下図の状態となります。既定ではCGIは無効化されています。この機能を編集するのが最短ですので、無効化されているCGI-exe行をダブルクリックします。

![mindcgi34.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/8b073696-fb9f-ccf9-0fe1-f6b1bebac2ff.png)

「モジュールマップの追加」ダイアログが開きますので、要求のパスを「*.exe」から「*.cgi」に変更します。「要求の制限」ボタンをクリックして「要求の制限」ダイアログの「アクセス」タブだけ図示していますが、すべて既定です。

![mindcgi35.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/f766acc7-3e6a-e788-63d0-ff16eb799068.png)

※参考※　右側の操作ペインの「モジュールマップの追加」をクリックして追加する場合は、既定では「スクリプト」になっています。

「OK」でダイアログを閉じていくと機能ペインは下図の状態となります。

![mindcgi36.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/761e54a4-665e-16bd-bd56-c3894aae7de5.png)

まだCGIは有効になっていませんので、この行を選択したまま右側の操作ペインの「機能のアクセス許可の編集」をクリックします。下図のダイアログが開きますので、ここで「実行」にもチェックします。

![mindcgi37.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/1d14d504-b9e2-3b1a-4400-2593be020032.png)

下図の状態となります。

![mindcgi38.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/bdc8e131-cc71-7b43-c4c9-db99fd598ec4.png)


この状態から、「sample」ノードを右クリックして現れるショートカットメニューで「アプリケーションへの変換」をクリックしてください。

![mindcgi39.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ac5b1901-d830-6356-4136-3d5ea83a9363.png)

ちょっとわかりにくいのですが、「sample」ノードのアイコンが茶色のフォルダアイコンから地球？っぽい青いアイコンに変化しています。この点なのですが、当初アプリケーション化しなくても動かくかなと思っていたのですが、動きませんでした。
まあ、アプリケーションの追加でフォルダを選択するよりフォルダを右クリックして「アプリケーションへの変換」のが若干手順は短いです。

そしてこの状態から、「ホーム」ノードを右クリックして現れるショートカットメニューで「停止」をクリックし（ショートカットメニューは閉じますので）再度右クリックして「開始」をクリックしてIISを再起動してください。

# 実行開始
３機能とも正常動作しました！:joy::tada::confetti_ball:

![mindcgi40.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7eb8434c-bd4d-0931-cf18-c13653713059.png)

「CGIで出力するhtmlドキュメント」helloweb.cgi
![mindcgi41.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/699a4f56-2fa8-8ee1-d41b-81bef572a4d1.png)

「標準CGI変数の確認」showvars.cgi.cgi
![mindcgi42.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/1f4e442b-1453-0132-8b38-4fa53e97aee2.png)

「フォームのテスト」cgi/test-form.cgi
![mindcgi43.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/20a7c732-632c-ff8e-e8be-85186bee0bef.png)


# おわりに
いかがでしたでしょうか？04Webserverに比べると圧倒的に設定手順が多いですが、GUIで操作する分にはそうでもないとも思われます。（説明を書くにはスクショがたくさん必要でめんどうですが）

WindowsNT4.0(Server)のオプションパックで登場したIIS4.0も、Windows2000（Server）のIIS5.0でかなりインターネットに公開されはじめたころ、めちゃめちゃ攻撃されて脆弱性てんこもりみたいない状況に陥り、IIS6.0/7.0でけっこう安定したかなという（あくまでわたしの感想）印象です。

なかなかIIS10.0でMindCGIが動かせずめげてたのですが、ようやく動いた晴れの姿が見れてうれしいです:santa_tone2:

@killyさん、いろいろお手数をお掛けしました。次回はinetpub外の構成を試みてます。


## 補足

sampleフォルダにCGIの設定を行った状態での実行結果です。動かないといってもmrunt160.exeランタイムは実行されているみたいで、mcoファイル名が正常にとれていない感じでした。

![mindcgi44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6e08aa0e-ec9a-9421-89d9-ed36e0cb33cf.png)
