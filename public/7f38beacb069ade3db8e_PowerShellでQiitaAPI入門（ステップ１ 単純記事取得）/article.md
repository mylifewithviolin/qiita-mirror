# はじめに
PowerShellでQiitaAPI入門のステップ１です。とりあえずまずは単純な記事取得から。既に高度に使いこなされている方にはあたりまえすぎる話ですが、公式解説はチームに関連した機能が詳しく解説されていて、基本的な使用例とかはすっとばされている感じがしたので、このあたりわかりにくくて手が出せにくかった方を対象にしつつ自分用のメモを兼ねます。

https://qiita.com/api/v2/docs

# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ１）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1

## 自分のユーザー情報取得（認証無）
認証されない状態でのユーザー情報取得です。他のユーザーの公開情報も取得できます。

### コマンド文
```powershell:
Invoke-RestMethod "https://qiita.com/api/v2/users/(自分のQiitaアカウント)"
```
### 実行結果
```powershell:
PS C:\pmind> Invoke-RestMethod "https://qiita.com/api/v2/users/mylifewithviolin"

description         : フリーランスのシステムエンジニアです。
                      趣味はバイオリンとピアノを習うこと。弾くことではないようです。
                      I like beautiful Japanese language, whether natural or structured. Because it has beautiful chara
                      cter types and attractive pronunciation sounds.
facebook_id         :
followees_count     : 54
followers_count     : 49
github_login_name   : mylifewithviolin
id                  : mylifewithviolin
items_count         : 273
linkedin_id         :
location            :
name                :
organization        : アプリ工房いずみ
permanent_id        : 3118036
profile_image_url   : https://avatars.githubusercontent.com/u/123276433?v=4
team_only           : False
twitter_screen_name :
website_url         : http://mylifewithviolin.blog.fc2.com/

```
## 自分のユーザー情報取得（認証有）
認証された状態でのユーザー情報取得です。公開情報より多い属性はimage_monthly_upload_limit と　image_monthly_upload_remaining　の２つ。実行結果では伏字にしていますが、実際にはバイト数っぽい数字が出力されます。

### コマンド文
```powershell:
# ヘッダー
$headers = @{
    Authorization = 'Bearer (アクセストークン)'
}
Invoke-RestMethod "https://qiita.com/api/v2/authenticated_user"  -Headers $headers
```

認証用のアクセストークンはアカウントの設定画面の「アプリケーション」で、「個人用アクセストークン」の「新しくトークンを発行する」から発行できます。トークンには
□read_qiita
□read_qiita_team
□write_qiita
□write_qiita_team
の４つのスコープを設定できます。（それぞれにチェック）

### 実行結果
```powershell:
PS C:\pmind> Invoke-RestMethod "https://qiita.com/api/v2/authenticated_user"  -Headers $headers


description                    : フリーランスのシステムエンジニアです。
                                 趣味はバイオリンとピアノを習うこと。弾くことではないようです。
                                 I like beautiful Japanese language, whether natural or structured. Because it has beau
                                 tiful character types and attractive pronunciation sounds.
facebook_id                    :
followees_count                : 54
followers_count                : 49
github_login_name              : mylifewithviolin
id                             : mylifewithviolin
items_count                    : 273
linkedin_id                    :
location                       :
name                           :
organization                   : アプリ工房いずみ
permanent_id                   : 3118036
profile_image_url              : https://avatars.githubusercontent.com/u/123276433?v=4
team_only                      : False
twitter_screen_name            :
website_url                    : http://mylifewithviolin.blog.fc2.com/
image_monthly_upload_limit     : ***********
image_monthly_upload_remaining : *******
```

以下は認証なしの公開情報の取得となります。


## 自分の記事取得（ページネーション指定無）
記事取得をデフォルトの件数で取得すると大量の記事テキストが受信されますので、いったん変数に結果を格納するとします。のちにこの変数を使っていろいろ操作します。

### コマンド文
```powershell:
$res = Invoke-RestMethod "https://qiita.com/api/v2/users/(自分のQiitaアカウント)/items"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/users/mylifewithviolin/items"
PS C:\pmind> $rest.count
20
```
20記事返っています。$restを出力すると大量のテキストでコンソールが流れます。ここでは割愛します。


## 記事取得（記事ID指定）
特定の記事の内容を取得するには記事IDを指定します。

### コマンド文
```powershell:
$res = Invoke-RestMethod "https://qiita.com/api/v2/items/(記事ID)"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/items/bd97e56fdfef2b293828"
```

### 実行結果（取得内容）
長いので閉じておきます。

<details><summary>取得内容</summary>

```powershell:
PS C:\pmind> $rest


rendered_body         : <h1 data-sourcepos="1:1-1:14">
                        <span id="はじめに" class="fragment"></span><a href="#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB"><i
                        class="fa fa-link"></i></a>はじめに</h1>
                        <p data-sourcepos="2:1-2:493">日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ２
                        です。MindCGIの実行シーケンスについてMind開発者の<a href="/killy" class="user-mention js-hoverc
                        ard" title="killy" data-hovercard-target-type="user" data-hovercard-target-name="killy">@killy<
                        /a>さんにご解説していただきだいぶ様子がわかりましたので、IIS（Windowsに古くから備わるWebサーバ
                        ーサービスで今回のバージョンは10.0）での設定方法を確定いたしました。今回はデフォルトのwwwrootで
                        はなく独自に作成したフォルダで検証します。</p>
                        <h1 data-sourcepos="5:1-5:14">
                        <span id="前提条件" class="fragment"></span><a href="#%E5%89%8D%E6%8F%90%E6%9D%A1%E4%BB%B6"><i
                        class="fa fa-link"></i></a>前提条件</h1>
                        <p data-sourcepos="6:1-8:35">Windows11 Pro 22H2 22621.4169<br>
                        Mind Version 8.0.08 for Windows<br>
                        Internet Information Servicies 10.0</p>
                        <h1 data-sourcepos="10:1-10:17">
                        <span id="環境の構成" class="fragment"></span><a href="#%E7%92%B0%E5%A2%83%E3%81%AE%E6%A7%8B%E6
                        %88%90"><i class="fa fa-link"></i></a>環境の構成</h1>
                        <p data-sourcepos="11:1-11:152"><a href="https://qiita.com/mylifewithviolin/items/f8730d2ff1ed6
                        1828a87.md" id="reference-9a9e00ccc1b218c5a95f">C#とkestrelで実行する</a>のフォルダ環境をほぼそ
                        のまま使います。</p>
                        <p data-sourcepos="13:1-13:306">C#とkestrelで実行していた場合は、アプリ本体の中間コードファイル
                        mcoはプロジェクトルートに置かないと実行できませんでしたが、今回はCGI実行フォルダに引っ越してい
                        ます。mcoのないcgiファイルは引っ越し未完了のものです。</p>
                        <div class="code-frame" data-lang="cmd" data-sourcepos="15:1-48:3"><div class="highlight"><pre>
                        <code>C:\developments\vscode\kestrelcgi
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
                        </code></pre></div></div>
                        <p data-sourcepos="50:1-50:256">\kestrelcgi\cgiのアクセス権は下図のようになっています。BUILTIN\
                        IIS_IUSRに読み取りと実行可の権限が付与しされました。このあたりはフォルダをアプリケーション化す
                        るとつけられるようです。</p>
                        <div class="code-frame" data-lang="powershell" data-sourcepos="52:1-74:3"><div class="highlight
                        "><pre><code><span class="n">PS</span><span class="w"> </span><span class="nx">C:\developments\
                        vscode\kestrelcgi</span><span class="err">&gt;</span><span class="w"> </span><span class="nx">G
                        et-ChildItem</span><span class="w"> </span><span class="nt">-Force</span><span class="w"> </spa
                        n><span class="nt">-Recurse</span><span class="w"> </span><span class="o">|</span><span class="
                        n">where</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span cl
                        ass="bp">$_</span><span class="o">.</span><span class="nf">mode</span><span class="w"> </span><
                        span class="o">-match</span><span class="w"> </span><span class="err">“</span><span class="n">
                        d</span><span class="err">”</span><span class="w"> </span><span class="p">}</span><span class=
                        "w"> </span><span class="o">|</span><span class="n">Get-Acl</span><span class="w"> </span><span
                         class="o">|</span><span class="w"> </span><span class="n">Select-object</span><span class="w">
                         </span><span class="p">@{</span><span class="nx">Label</span><span class="o">=</span><span cla
                        ss="err">”</span><span class="nx">Path</span><span class="err">”</span><span class="p">;</spa
                        n><span class="nx">Expression</span><span class="o">=</span><span class="p">{</span><span class
                        ="n">Convert-Path</span><span class="w"> </span><span class="bp">$_</span><span class="o">.</sp
                        an><span class="nf">Path</span><span class="p">}},</span><span class="w"> </span><span class="n
                        x">Owner</span><span class="p">,</span><span class="w"> </span><span class="nx">AccessToString<
                        /span><span class="w"> </span><span class="err">|</span><span class="w"> </span><span class="nx
                        ">Format</span><span class="err">-</span><span class="nx">List</span><span class="w">

                        </span><span class="nx">Path</span><span class="w">           </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">C</span><span class="err">:\</span><span class="nx">de
                        velopments</span><span class="err">\</span><span class="nx">vscode</span><span class="err">\</s
                        pan><span class="nx">kestrelcgi</span><span class="err">\</span><span class="nx">cgi</span><spa
                        n class="w">
                        </span><span class="nx">Owner</span><span class="w">          </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">DESKTOP</span><span class="err">-</span><span class="m
                        i">078</span><span class="nx">KPRA</span><span class="err">\</span><span class="nx">mylifewithv
                        iolin</span><span class="w">
                        </span><span class="nx">AccessToString</span><span class="w"> </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">IIS_IUSRS</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </spa
                        n><span class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span c
                        lass="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">IIS_IUSRS</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </spa
                        n><span class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span c
                        lass="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">Administrators</span><span class="w"> </span><span class="nx">Allow</span><span class="w">
                        </span><span class="nx">FullControl</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">SYSTEM</span><span class="w"> </span><sp
                        an class="nx">Allow</span><span class="w">  </span><span class="nx">FullControl</span><span cla
                        ss="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">Users</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </span><s
                        pan class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span class
                        ="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">Authenticated</span><span class="w"> </s
                        pan><span class="nx">Users</span><span class="w"> </span><span class="nx">Allow</span><span cla
                        ss="w">  </span><span class="nx">Modify</span><span class="p">,</span><span class="w"> </span><
                        span class="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">Authenticated</span><span class="w"> </s
                        pan><span class="nx">Users</span><span class="w"> </span><span class="nx">Allow</span><span cla
                        ss="w">  </span><span class="err">-</span><span class="mi">536805376</span><span class="w">

                        </span><span class="nx">Path</span><span class="w">           </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">C</span><span class="err">:\</span><span class="nx">de
                        velopments</span><span class="err">\</span><span class="nx">vscode</span><span class="err">\</s
                        pan><span class="nx">kestrelcgi</span><span class="err">\</span><span class="nx">wwwroot</span>
                        <span class="w">
                        </span><span class="nx">Owner</span><span class="w">          </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">DESKTOP</span><span class="err">-</span><span class="m
                        i">078</span><span class="nx">KPRA</span><span class="err">\</span><span class="nx">mylifewithv
                        iolin</span><span class="w">
                        </span><span class="nx">AccessToString</span><span class="w"> </span><span class="err">:</span>
                        <span class="w"> </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">IIS_IUSRS</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </spa
                        n><span class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span c
                        lass="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">IIS_IUSRS</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </spa
                        n><span class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span c
                        lass="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">Administrators</span><span class="w"> </span><span class="nx">Allow</span><span class="w">
                        </span><span class="nx">FullControl</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">SYSTEM</span><span class="w"> </span><sp
                        an class="nx">Allow</span><span class="w">  </span><span class="nx">FullControl</span><span cla
                        ss="w">
                                         </span><span class="nx">BUILTIN</span><span class="err">\</span><span class="n
                        x">Users</span><span class="w"> </span><span class="nx">Allow</span><span class="w">  </span><s
                        pan class="nx">ReadAndExecute</span><span class="p">,</span><span class="w"> </span><span class
                        ="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">Authenticated</span><span class="w"> </s
                        pan><span class="nx">Users</span><span class="w"> </span><span class="nx">Allow</span><span cla
                        ss="w">  </span><span class="nx">Modify</span><span class="p">,</span><span class="w"> </span><
                        span class="nx">Synchronize</span><span class="w">
                                         </span><span class="nx">NT</span><span class="w"> </span><span class="nx">AUTH
                        ORITY</span><span class="err">\</span><span class="nx">Authenticated</span><span class="w"> </s
                        pan><span class="nx">Users</span><span class="w"> </span><span class="nx">Allow</span><span cla
                        ss="w">  </span><span class="err">-</span><span class="mi">536805376</span><span class="w">
                        </span></code></pre></div></div>
                        <h1 data-sourcepos="76:1-76:43">
                        <span id="mind-cgiアプリケーションの作成" class="fragment"></span><a href="#mind-cgi%E3%82%A2%E
                        3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E4%BD%9C%E6%88%90"><i cl
                        ass="fa fa-link"></i></a>Mind CGIアプリケーションの作成</h1>
                        <p data-sourcepos="78:1-81:47">今回もMind9のCGIサンプルをそのまま動かしますが、動かすのは実行パ
                        ス設定した下記の３機能です。<br>
                        「CGIで出力するhtmlドキュメント」helloweb.cgi<br>
                        「標準CGI変数の確認」showvars.cgi.cgi<br>
                        「フォームのテスト」cgi/test-form.cgi</p>
                        <p data-sourcepos="83:1-84:135">cgiフォルダにはMind8インストールフォルダ配下のC:\pmind\cgilib\s
                        ample<br>
                        からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされています
                        。</p>
                        <h1 data-sourcepos="86:1-86:23">
                        <span id="webサーバー設定" class="fragment"></span><a href="#web%E3%82%B5%E3%83%BC%E3%83%90%E3%
                        83%BC%E8%A8%AD%E5%AE%9A"><i class="fa fa-link"></i></a>Webサーバー設定</h1>
                        <p data-sourcepos="88:1-88:188">IISの導入オプション状態とアプリケーションプールの状態は<a href=
                        "https://qiita.com/mylifewithviolin/items/3bd9f099e2f48af7dbb6" id="reference-2fc5a6dfde14ab355
                        d14">前回の記事</a>をご参照ください。</p>
                        <p data-sourcepos="90:1-90:286">「インターネットインフォメーションサービス(IIS)マネージャ」を開
                        きます。「Default Web Site」をクリックしてから、右側の「サイトの編集」の「基本設定」をクリック
                        して、物理パスを今回のWWWrootに変更します。</p>
                        <p data-sourcepos="92:1-92:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqi
                        ita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Ff9d43f99-0657-ab87-4d9f-481c310
                        18ecf.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=2463a0829b692e8f596c53b187
                        74f627" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.net
                        /https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Ff9d43f99-0657-
                        ab87-4d9f-481c31018ecf.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=2463a0829
                        b692e8f596c53b18774f627" alt="mindcgi20.png" srcset="https://qiita-user-contents.imgix.net/http
                        s%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Ff9d43f99-0657-ab87-
                        4d9f-481c31018ecf.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=m
                        ax&amp;s=8e3d0d1cbb359d4a0b192d2f53db4f32 1x" data-canonical-src="https://qiita-image-store.s3.
                        ap-northeast-1.amazonaws.com/0/3118036/f9d43f99-0657-ab87-4d9f-481c31018ecf.png" loading="lazy"
                        ></a></p>
                        <p data-sourcepos="94:1-94:172">「Default Web Site」を右クリックして「仮想ディレクトリの追加」
                        を選択して、仮想ディレクトリの設定を下図のように行います。</p>
                        <p data-sourcepos="96:1-96:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqi
                        ita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F4695cebc-0998-c4bb-c89a-e486485
                        3e5e5.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=912cfbeb0a99a2014146579221
                        0c38cc" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.net
                        /https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F4695cebc-0998-
                        c4bb-c89a-e4864853e5e5.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=912cfbeb0
                        a99a20141465792210c38cc" alt="mindcgi21.png" srcset="https://qiita-user-contents.imgix.net/http
                        s%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F4695cebc-0998-c4bb-
                        c89a-e4864853e5e5.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=m
                        ax&amp;s=972d8a5f1a46687f2f6995e224977e87 1x" data-canonical-src="https://qiita-image-store.s3.
                        ap-northeast-1.amazonaws.com/0/3118036/4695cebc-0998-c4bb-c89a-e4864853e5e5.png" loading="lazy"
                        ></a></p>
                        <p data-sourcepos="98:1-98:207">作成された仮想ディレクトリcgiのノードをクリックして機能ペインを
                        下図の状態とします。ここで、「ハンドラーマッピング」をクリックしておきます。</p>
                        <p data-sourcepos="100:1-100:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F6e016ccd-ea0f-259a-3e13-c8603
                        8a544fa.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=5a2bbb0875a0b7d01ac66701
                        96fc9d2a" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F6e016ccd-ea0
                        f-259a-3e13-c86038a544fa.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=5a2bbb0
                        875a0b7d01ac6670196fc9d2a" alt="mindcgi22.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F6e016ccd-ea0f-259
                        a-3e13-c86038a544fa.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=41a45e3d4f673e78350829b9f8cf62b9 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/6e016ccd-ea0f-259a-3e13-c86038a544fa.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="102:1-102:108">右側の操作ペインの「機能を開く」をクリックします。下図の状態
                        となります。</p>
                        <p data-sourcepos="104:1-104:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd4e68c50-5cce-e33c-b892-cfaf8
                        1a2b6d0.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=870bcb3ab30180bc5670f7df
                        79d41a09" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd4e68c50-5cc
                        e-e33c-b892-cfaf81a2b6d0.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=870bcb3
                        ab30180bc5670f7df79d41a09" alt="mindcgi23.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd4e68c50-5cce-e33
                        c-b892-cfaf81a2b6d0.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=75a812e82f802da39c91ba093970c436 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/d4e68c50-5cce-e33c-b892-cfaf81a2b6d0.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="106:1-106:331">右側の操作ペインの「モジュールマップの追加」をクリックします
                        。（これが正解でした。開いたダイアログはすべてブランクですが下図の状態のように設定します。「実
                        行可能ファイル（オプション）」はブランクのままがキモです。<img alt=":santa_tone2:" class="emoji
                        " height="20" src="https://cdn.qiita.com/emoji/twemoji/unicode/1f385-1f3fc.png" title=":santa_t
                        one2:" width="20" loading="lazy"></p>
                        <p data-sourcepos="108:1-108:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd955a485-1c00-4fd4-8bf8-7b516
                        545cf85.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=6d7c391af3645350d1142bc6
                        e4e996db" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd955a485-1c0
                        0-4fd4-8bf8-7b516545cf85.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=6d7c391
                        af3645350d1142bc6e4e996db" alt="mindcgi24.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fd955a485-1c00-4fd
                        4-8bf8-7b516545cf85.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=550a4a8c9a52b32efc0fb6eaec8e76d8 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/d955a485-1c00-4fd4-8bf8-7b516545cf85.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="110:1-110:264">「モジュールマップの追加」ダイアログの「要求の制限」ボタンを
                        クリックします。「要求の制限」ダイアログの「アクセス」タブだけ下図のように「実行」に変更します
                        。既定は「スクリプト」</p>
                        <p data-sourcepos="112:1-112:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fc6c8b86c-18a9-7028-fa95-6ce86
                        2783fcd.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=70213e494dae2fff0725a631
                        6de3521e" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fc6c8b86c-18a
                        9-7028-fa95-6ce862783fcd.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=70213e4
                        94dae2fff0725a6316de3521e" alt="mindcgi25.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fc6c8b86c-18a9-702
                        8-fa95-6ce862783fcd.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=94d03fcdd00c3d24fca7863290008550 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/c6c8b86c-18a9-7028-fa95-6ce862783fcd.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="114:1-114:98">「OK」でダイアログを閉じていくと機能ペインは下図の状態となりま
                        す。</p>
                        <p data-sourcepos="116:1-116:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F037f462d-3da6-a2b4-06c4-68a50
                        076b2ad.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0e97b1036d8de21ca698fe68
                        cab6def1" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F037f462d-3da
                        6-a2b4-06c4-68a50076b2ad.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0e97b10
                        36d8de21ca698fe68cab6def1" alt="mindcgi26.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F037f462d-3da6-a2b
                        4-06c4-68a50076b2ad.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=58314d25e755cb3ad62e8ead53c5e346 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/037f462d-3da6-a2b4-06c4-68a50076b2ad.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="118:1-118:351">まだCGIは有効になっていませんので、この行を選択したまま右側の
                        操作ペインの「機能のアクセス許可の編集」をクリックします。下図のダイアログが開きますので、ここ
                        で「実行」にもチェックします。（既定では「実行」にはチェックがついていません。）</p>
                        <p data-sourcepos="120:1-120:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F10bdce92-75d1-a1f0-b572-b10f5
                        5f0bc3b.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0715c5dc5cf8b18bafd7dcb9
                        c8726f29" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F10bdce92-75d
                        1-a1f0-b572-b10f55f0bc3b.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0715c5d
                        c5cf8b18bafd7dcb9c8726f29" alt="mindcgi45.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F10bdce92-75d1-a1f
                        0-b572-b10f55f0bc3b.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=9d968d38ab87e778838cc26ebd88121a 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/10bdce92-75d1-a1f0-b572-b10f55f0bc3b.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="123:1-123:335">ここまでできたら、次はホームノードをクリックします。（コンピ
                        ュータ名になっている場合が多いようです。）下図は機能ペインの「ISAPIおよびCGI機能の制限」をクリ
                        ックしてある状態です。右側の操作ペインの「機能を開く」をクリックします。</p>
                        <p data-sourcepos="125:1-125:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F2f5aaaa4-1a42-1d61-1e7a-27f4e
                        3982554.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=eb3156af2437962aabba5985
                        dd82181a" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F2f5aaaa4-1a4
                        2-1d61-1e7a-27f4e3982554.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=eb3156a
                        f2437962aabba5985dd82181a" alt="mindcgi26.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F2f5aaaa4-1a42-1d6
                        1-1e7a-27f4e3982554.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=e3abf517b025dda1a5730678d202b2ac 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/2f5aaaa4-1a42-1d61-1e7a-27f4e3982554.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="127:1-127:87">下図の状態となりますので、右側の「追加」をクリックします。</p>
                        <p data-sourcepos="129:1-129:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F9f125bea-42e5-2f57-918d-f8c52
                        e0d5012.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=d2a6c94fe2cadb9c7d76534c
                        dfae4fa8" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F9f125bea-42e
                        5-2f57-918d-f8c52e0d5012.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=d2a6c94
                        fe2cadb9c7d76534cdfae4fa8" alt="mindcgi27.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F9f125bea-42e5-2f5
                        7-918d-f8c52e0d5012.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=59d6c64c5ccc44398ac6e4dbd668264f 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/9f125bea-42e5-2f57-918d-f8c52e0d5012.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="131:1-131:218">「ISAPIおよびCGI機能の制限」ダイアログが開きますので、mrunt16
                        0.exeのパスを追加して、「拡張パスの実行を許可する」にチェックを入れてダイアログを閉じます。</p>
                        <p data-sourcepos="133:1-133:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Feaf5f249-4df4-11bb-8856-55be1
                        42979c1.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=ff406fb312aecc6240ae0539
                        8f0f92cd" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Feaf5f249-4df
                        4-11bb-8856-55be142979c1.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=ff406fb
                        312aecc6240ae05398f0f92cd" alt="mindcgi28.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Feaf5f249-4df4-11b
                        b-8856-55be142979c1.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=ab9d5d05d918850be20eb8247ded4b10 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/eaf5f249-4df4-11bb-8856-55be142979c1.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="135:1-135:130">つづいて、実行したいcgiのファイルのパスを同じように追加します
                        。ここもキモです。<img alt=":santa_tone2:" class="emoji" height="20" src="https://cdn.qiita.com
                        /emoji/twemoji/unicode/1f385-1f3fc.png" title=":santa_tone2:" width="20" loading="lazy"></p>
                        <p data-sourcepos="137:1-137:126"><a href="https://qiita-user-contents.imgix.net/https%3A%2F%2F
                        qiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F7d65ea92-13e6-9c02-b5ce-ae02e
                        1db3bfe.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0b9c17fb46e67eee8e7e3057
                        7497e837" target="_blank" rel="nofollow noopener"><img src="https://qiita-user-contents.imgix.n
                        et/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F7d65ea92-13e
                        6-9c02-b5ce-ae02e1db3bfe.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=0b9c17f
                        b46e67eee8e7e30577497e837" alt="mindcgi29.png" srcset="https://qiita-user-contents.imgix.net/ht
                        tps%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2F7d65ea92-13e6-9c0
                        2-b5ce-ae02e1db3bfe.png?ixlib=rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit
                        =max&amp;s=7dbe7d4b6c46e44eea635a289f2f9a29 1x" data-canonical-src="https://qiita-image-store.s
                        3.ap-northeast-1.amazonaws.com/0/3118036/7d65ea92-13e6-9c02-b5ce-ae02e1db3bfe.png" loading="laz
                        y"></a></p>
                        <p data-sourcepos="139:1-139:114">ワイルドカードを指定すると怒られるので、ここは個別に追加しな
                        いといけません。</p>
                        <p data-sourcepos="141:1-141:210">以上の設定が完了しましたら、IIS全体または仮想サイトを再起動し
                        ます。今回はアプリケーション化を行わず仮想ディレクトリのままで検証してみました。</p>
                        <h1 data-sourcepos="144:1-144:14">
                        <span id="実行開始" class="fragment"></span><a href="#%E5%AE%9F%E8%A1%8C%E9%96%8B%E5%A7%8B"><i
                        class="fa fa-link"></i></a>実行開始</h1>
                        <p data-sourcepos="145:1-145:47">３機能とも正常動作しました！<img alt=":joy:" class="emoji" hei
                        ght="20" src="https://cdn.qiita.com/emoji/twemoji/unicode/1f602.png" title=":joy:" width="20" l
                        oading="lazy"></p>
                        <p data-sourcepos="147:1-148:126">「CGIで出力するhtmlドキュメント」helloweb.cgi<br>
                        <a href="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-
                        1.amazonaws.com%2F0%2F3118036%2Fa111d232-4372-bbcb-607e-88d62acfb6f6.png?ixlib=rb-4.0.0&amp;aut
                        o=format&amp;gif-q=60&amp;q=75&amp;s=7def8e0b0fe0acbad2393e5ed0fc95e7" target="_blank" rel="nof
                        ollow noopener"><img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store
                        .s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fa111d232-4372-bbcb-607e-88d62acfb6f6.png?ixlib
                        =rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=7def8e0b0fe0acbad2393e5ed0fc95e7" alt="mi
                        ndcgi46.png" srcset="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.a
                        p-northeast-1.amazonaws.com%2F0%2F3118036%2Fa111d232-4372-bbcb-607e-88d62acfb6f6.png?ixlib=rb-4
                        .0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=max&amp;s=dcb5c07aa153d6109b1506c
                        30d30cc47 1x" data-canonical-src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3
                        118036/a111d232-4372-bbcb-607e-88d62acfb6f6.png" loading="lazy"></a></p>
                        <p data-sourcepos="150:1-151:126">「標準CGI変数の確認」showvars.cgi.cgi<br>
                        <a href="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-
                        1.amazonaws.com%2F0%2F3118036%2Fefbd232a-2ddd-bf23-d917-562dbbb2ea9c.png?ixlib=rb-4.0.0&amp;aut
                        o=format&amp;gif-q=60&amp;q=75&amp;s=6b63f4a1b16aaba4bb6455a9abc15c67" target="_blank" rel="nof
                        ollow noopener"><img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store
                        .s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fefbd232a-2ddd-bf23-d917-562dbbb2ea9c.png?ixlib
                        =rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=6b63f4a1b16aaba4bb6455a9abc15c67" alt="mi
                        ndcgi47.png" srcset="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.a
                        p-northeast-1.amazonaws.com%2F0%2F3118036%2Fefbd232a-2ddd-bf23-d917-562dbbb2ea9c.png?ixlib=rb-4
                        .0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=max&amp;s=f97f734d95b8735141d9ab0
                        e9790c581 1x" data-canonical-src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3
                        118036/efbd232a-2ddd-bf23-d917-562dbbb2ea9c.png" loading="lazy"></a></p>
                        <p data-sourcepos="153:1-154:126">「フォームのテスト」cgi/test-form.cgi<br>
                        <a href="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-
                        1.amazonaws.com%2F0%2F3118036%2Fbaef7e9b-e10c-bbe6-7951-be7d22dd0662.png?ixlib=rb-4.0.0&amp;aut
                        o=format&amp;gif-q=60&amp;q=75&amp;s=11ca2b8a86373f2bd1526c27b14733a9" target="_blank" rel="nof
                        ollow noopener"><img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store
                        .s3.ap-northeast-1.amazonaws.com%2F0%2F3118036%2Fbaef7e9b-e10c-bbe6-7951-be7d22dd0662.png?ixlib
                        =rb-4.0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;s=11ca2b8a86373f2bd1526c27b14733a9" alt="mi
                        ndcgi48.png" srcset="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.a
                        p-northeast-1.amazonaws.com%2F0%2F3118036%2Fbaef7e9b-e10c-bbe6-7951-be7d22dd0662.png?ixlib=rb-4
                        .0.0&amp;auto=format&amp;gif-q=60&amp;q=75&amp;w=1400&amp;fit=max&amp;s=1fa6f4db89e66151288f2fe
                        69d1e84a5 1x" data-canonical-src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3
                        118036/baef7e9b-e10c-bbe6-7951-be7d22dd0662.png" loading="lazy"></a></p>
                        <h1 data-sourcepos="156:1-156:14">
                        <span id="おわりに" class="fragment"></span><a href="#%E3%81%8A%E3%82%8F%E3%82%8A%E3%81%AB"><i
                        class="fa fa-link"></i></a>おわりに</h1>
                        <p data-sourcepos="157:1-158:208">いかがでしたでしょうか？説明を書くのにスクショをたくさんとっ
                        たので少し疲れました<img alt=":relaxed:" class="emoji" height="20" src="https://cdn.qiita.com/e
                        moji/twemoji/unicode/263a-fe0f.png" title=":relaxed:" width="20" loading="lazy">なにかの役にた
                        てば幸いです。<br>
                        さて、これはいちおう序の口で、なんかアプリを書くのが目標なのですが、少し休憩します。kestrelはな
                        ぜパラメータがうまく渡らないのか気になります。</p>

body                  : # はじめに
                        日本語プログラミング言語MindのCGIをIIS10.0で実行するのステップ２です。MindCGIの実行シーケンスに
                        ついてMind開発者の@killyさんにご解説していただきだいぶ様子がわかりましたので、IIS（Windowsに古
                        くから備わるWebサーバーサービスで今回のバージョンは10.0）での設定方法を確定いたしました。今回は
                        デフォルトのwwwrootではなく独自に作成したフォルダで検証します。


                        # 前提条件
                        Windows11 Pro 22H2 22621.4169
                        Mind Version 8.0.08 for Windows
                        Internet Information Servicies 10.0

                        # 環境の構成
                        [C#とkestrelで実行する](https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87.md)のフォ
                        ルダ環境をほぼそのまま使います。

                        C#とkestrelで実行していた場合は、アプリ本体の中間コードファイルmcoはプロジェクトルートに置かな
                        いと実行できませんでしたが、今回はCGI実行フォルダに引っ越しています。mcoのないcgiファイルは引っ
                        越し未完了のものです。

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

                        \kestrelcgi\cgiのアクセス権は下図のようになっています。BUILTIN\IIS_IUSRに読み取りと実行可の権限
                        が付与しされました。このあたりはフォルダをアプリケーション化するとつけられるようです。

                        ```powershell:
                        PS C:\developments\vscode\kestrelcgi> Get-ChildItem -Force -Recurse |where { $_.mode -match “d
                        ” } |Get-Acl | Select-object @{Label=”Path”;Expression={Convert-Path $_.Path}}, Owner, Acces
                        sToString | Format-List

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
                        からmrunt160.exeランタイムと上記cgiファイルに対応した中間コードファイルmcoがコピーされています
                        。

                        # Webサーバー設定

                        IISの導入オプション状態とアプリケーションプールの状態は[前回の記事](https://qiita.com/mylifewit
                        hviolin/items/3bd9f099e2f48af7dbb6)をご参照ください。

                        「インターネットインフォメーションサービス(IIS)マネージャ」を開きます。「Default Web Site」をク
                        リックしてから、右側の「サイトの編集」の「基本設定」をクリックして、物理パスを今回のWWWrootに変
                        更します。

                        ![mindcgi20.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/f9d43f99-0
                        657-ab87-4d9f-481c31018ecf.png)

                        「Default Web Site」を右クリックして「仮想ディレクトリの追加」を選択して、仮想ディレクトリの設
                        定を下図のように行います。

                        ![mindcgi21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4695cebc-0
                        998-c4bb-c89a-e4864853e5e5.png)

                        作成された仮想ディレクトリcgiのノードをクリックして機能ペインを下図の状態とします。ここで、「ハ
                        ンドラーマッピング」をクリックしておきます。

                        ![mindcgi22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6e016ccd-e
                        a0f-259a-3e13-c86038a544fa.png)

                        右側の操作ペインの「機能を開く」をクリックします。下図の状態となります。

                        ![mindcgi23.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d4e68c50-5
                        cce-e33c-b892-cfaf81a2b6d0.png)

                        右側の操作ペインの「モジュールマップの追加」をクリックします。（これが正解でした。開いたダイア
                        ログはすべてブランクですが下図の状態のように設定します。「実行可能ファイル（オプション）」はブ
                        ランクのままがキモです。:santa_tone2:

                        ![mindcgi24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d955a485-1
                        c00-4fd4-8bf8-7b516545cf85.png)

                        「モジュールマップの追加」ダイアログの「要求の制限」ボタンをクリックします。「要求の制限」ダイ
                        アログの「アクセス」タブだけ下図のように「実行」に変更します。既定は「スクリプト」

                        ![mindcgi25.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c6c8b86c-1
                        8a9-7028-fa95-6ce862783fcd.png)

                        「OK」でダイアログを閉じていくと機能ペインは下図の状態となります。

                        ![mindcgi26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/037f462d-3
                        da6-a2b4-06c4-68a50076b2ad.png)

                        まだCGIは有効になっていませんので、この行を選択したまま右側の操作ペインの「機能のアクセス許可の
                        編集」をクリックします。下図のダイアログが開きますので、ここで「実行」にもチェックします。（既
                        定では「実行」にはチェックがついていません。）

                        ![mindcgi45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/10bdce92-7
                        5d1-a1f0-b572-b10f55f0bc3b.png)


                        ここまでできたら、次はホームノードをクリックします。（コンピュータ名になっている場合が多いよう
                        です。）下図は機能ペインの「ISAPIおよびCGI機能の制限」をクリックしてある状態です。右側の操作ペ
                        インの「機能を開く」をクリックします。

                        ![mindcgi26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2f5aaaa4-1
                        a42-1d61-1e7a-27f4e3982554.png)

                        下図の状態となりますので、右側の「追加」をクリックします。

                        ![mindcgi27.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9f125bea-4
                        2e5-2f57-918d-f8c52e0d5012.png)

                        「ISAPIおよびCGI機能の制限」ダイアログが開きますので、mrunt160.exeのパスを追加して、「拡張パス
                        の実行を許可する」にチェックを入れてダイアログを閉じます。

                        ![mindcgi28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/eaf5f249-4
                        df4-11bb-8856-55be142979c1.png)

                        つづいて、実行したいcgiのファイルのパスを同じように追加します。ここもキモです。:santa_tone2:

                        ![mindcgi29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7d65ea92-1
                        3e6-9c02-b5ce-ae02e1db3bfe.png)

                        ワイルドカードを指定すると怒られるので、ここは個別に追加しないといけません。

                        以上の設定が完了しましたら、IIS全体または仮想サイトを再起動します。今回はアプリケーション化を行
                        わず仮想ディレクトリのままで検証してみました。


                        # 実行開始
                        ３機能とも正常動作しました！:joy:

                        「CGIで出力するhtmlドキュメント」helloweb.cgi
                        ![mindcgi46.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/a111d232-4
                        372-bbcb-607e-88d62acfb6f6.png)

                        「標準CGI変数の確認」showvars.cgi.cgi
                        ![mindcgi47.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/efbd232a-2
                        ddd-bf23-d917-562dbbb2ea9c.png)

                        「フォームのテスト」cgi/test-form.cgi
                        ![mindcgi48.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/baef7e9b-e
                        10c-bbe6-7951-be7d22dd0662.png)

                        # おわりに
                        いかがでしたでしょうか？説明を書くのにスクショをたくさんとったので少し疲れました:relaxed:なにか
                        の役にたてば幸いです。
                        さて、これはいちおう序の口で、なんかアプリを書くのが目標なのですが、少し休憩します。kestrelはな
                        ぜパラメータがうまく渡らないのか気になります。

coediting             : False
comments_count        : 0
created_at            : 2024-11-13T22:13:55+09:00
group                 :
id                    : bd97e56fdfef2b293828
likes_count           : 1
private               : False
reactions_count       : 0
stocks_count          : 2
tags                  : {@{name=Cgi; versions=System.Object[]}, @{name=Webアプリケーション; versions=System.Object[]},
                        @{name=mind; versions=System.Object[]}, @{name=日本語プログラミング; versions=System.Object[]}.
                        ..}
title                 : 日本語プログラミング言語MindのCGIをIIS10.0で実行する（ステップ２）
updated_at            : 2024-11-15T21:58:50+09:00
url                   : https://qiita.com/mylifewithviolin/items/bd97e56fdfef2b293828
user                  : @{description=フリーランスのシステムエンジニアです。
                        趣味はバイオリンとピアノを習うこと。弾くことではないようです。
                        I like beautiful Japanese language, whether natural or structured. Because it has beautiful cha
                        racter types and attractive pronunciation sounds.; facebook_id=; followees_count=54; followers_
                        count=49; github_login_name=mylifewithviolin; id=mylifewithviolin; items_count=273; linkedin_id
                        =; location=; name=; organization=アプリ工房いずみ; permanent_id=3118036; profile_image_url=htt
                        ps://avatars.githubusercontent.com/u/123276433?v=4; team_only=False; twitter_screen_name=; webs
                        ite_url=http://mylifewithviolin.blog.fc2.com/}
page_views_count      :
team_membership       :
organization_url_name :
slide                 : False

```

</details>


## 自分の記事取得（ページネーション指定有）
### コマンド文
```powershell:
$res = Invoke-RestMethod "https://qiita.com/api/v2/users/(自分のQiitaアカウント)/items?page=(ページ位置)&per_page=(1ページあたりの記事数)"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/users/mylifewithviolin/items?page=1&per_page=10"
PS C:\pmind> $rest.count
10
```

10記事返っています。$restを出力すると大量のテキストでコンソールが流れます。ここでは割愛します。

# おわりに
いかがでしたか？参考になれば幸いです。
