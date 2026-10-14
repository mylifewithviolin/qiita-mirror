# はじめに
日本語プログラミング言語なでしこ３のGo言語版が正式にリリースされたようですので、さっそくVSCodeのターミナルからインストールして動かしてみました。

# なでしこ３(Go版)のインストール
下記の２種がインストールされるようでした。CLIとGUIは別コンパイラのようです。
なでしこ3 CLI版 (gonako v3.8.4)
なでしこ3 GUI版 (gonako-gui v3.8.4)

## なでしこ３(Go版)のVSCodeのターミナルからのインストール
お手数ですが詳しくは[こちらの記事](https://qiita.com/mylifewithviolin/items/2a67a4fd44b997a2bc89)をご参照ください。

https://qiita.com/mylifewithviolin/items/2a67a4fd44b997a2bc89

## なでしこ３(Go版)のgitレポジトリのローカルクローン
[こちらの記事](https://qiita.com/mylifewithviolin/items/e13c206648f232796c6c)でなでしこ３(Go版)でなでしこソースをGoソースにトランスコンパイルしたのですが、それをGoでビルドするには少しランタイムモジュールの準備が必要であることが判明。

https://qiita.com/mylifewithviolin/items/e13c206648f232796c6c

ということで、本記事ではなでしこ(Go版)のgitレポジトリのローカルクローン作成から始めます。

```cmd
C:\nadesiko3>git --version
git version 2.47.1.windows.1
```

とりあえず、いつ入れたか（あるいは入ったか）わからないのですが、gitは2.47.1が入っていることを確認。下記のコマンドでレポジトリのローカルクローンを作成します。仕事では多数あるリポジトリの状態をぱっと見るため基本sourcetreeですが、今回はgitのcliで作ります。

```cmd
C:\nadesiko3>git clone https://github.com/kujirahand/nadesiko3go.git
Cloning into 'nadesiko3go'...
remote: Enumerating objects: 4491, done.
remote: Counting objects: 100% (70/70), done.
remote: Compressing objects: 100% (48/48), done.
remote: Total 4491 (delta 27), reused 28 (delta 22), pack-reused 4421 (from 2)
Receiving objects: 100% (4491/4491), 2.51 MiB | 2.62 MiB/s, done.
Resolving deltas: 100% (2750/2750), done.
```
できました:tada:
```cmd
C:\nadesiko3>tree   
C:.
└─nadesiko3go
    ├─.github
    │  └─workflows
    ├─benchmark
    │  ├─js
    │  └─py
    ├─cmd
    │  ├─gonako
    │  ├─gonako-cui
    │  ├─gonako-gui
    │  │  ├─ai-template
    │  │  └─ui
    │  │      ├─bundled
    │  │      ├─macapp
    │  │      │  └─Contents
    │  │      │      └─Resources
    │  │      ├─samples
    │  │      └─wnako3
    │  └─gonako-wasm
    │      └─web
    ├─docs
    ├─install
    ├─internal
    │  ├─ast
    │  ├─bundle
    │  ├─commanddiff
    │  ├─commanddoc
    │  ├─compat
    │  ├─compiler
    │  ├─csvlib
    │  ├─deskutil
    │  ├─dncl
    │  ├─doctest
    │  ├─errs
    │  ├─event
    │  ├─format
    │  ├─gogen
    │  ├─guilib
    │  ├─host
    │  ├─imagelib
    │  ├─indent
    │  ├─ir
    │  ├─lexer
    │  │  └─josi
    │  ├─mathlib
    │  ├─nodelib
    │  ├─officelib
    │  ├─ops
    │  ├─parser
    │  ├─pdflib
    │  ├─prepare
    │  ├─re
    │  ├─sqlitelib
    │  ├─stdlib
    │  ├─value
    │  │  └─text
    │  ├─version
    │  ├─vm
    │  └─wasmrt
    ├─pkg
    │  └─runtime
    ├─scripts
    └─testdata
        ├─compat
        │  ├─cases
        │  └─expected
        └─doctest
            ├─core
            └─node
```

docs\gogen.mdというファイルにgogenについて解説されていました。
この他、どこを見たか忘れましたが、goのバージョンは1.27.0と書いてあったような気がしましたので、とりあえずGoのバージョンアップに進みます。

AGENTS.mdとかもあるので、やっぱりAIドリブンな開発には移行されているような感じですね。

## Goのバージョンアップ
現在入っているのは1.17ですので1.27.0に上げます。

```psPS C:\nadesiko3> winget upgrade GoLang.Go
'msstore' ソースでは、使用する前に次の契約を表示する必要があります。
Terms of Transaction: https://aka.ms/microsoft-store-terms-of-transaction
ソースが正常に機能するには、現在のマシンの 2 文字の地理的リージョンをバックエンド サービスに送信する必要があります (例: "US")。

すべてのソース契約条件に同意しますか?
[Y] はい  [N] いいえ: Y
見つかりました Go Programming Language [GoLang.Go] バージョン 1.27.0
このアプリケーションは所有者からライセンス供与されます。
Microsoft はサードパーティのパッケージに対して責任を負わず、ライセンスも付与しません。
ダウンロード中 https://go.dev/dl/go1.27.0.windows-amd64.msi
  ██████████████████████████████  63.0 MB / 63.0 MB
インストーラーハッシュが正常に検証されました
パッケージのインストールを開始しています...
インストールが完了しました
PS C:\Users\yoshiaki> go version
go version go1.27.0 windows/amd64
```

とりあえず無事にバージョンアップ完了しました。

## go.modの配置
なでしこ３のソースとなでしこ(Go版)が生成したGoソースのカレントフォルダに
```cmd
c:\developments\vscode\gonako>dir
2026/09/14  22:36             9,698 count3.go
2026/09/14  22:25               699 count3.nako
```
go.modというコンフィグレーションファイルを格納します。
```go:go.mod
module gonako

go 1.26.0

require github.com/kujirahand/nadesiko3go v0.0.0
replace github.com/kujirahand/nadesiko3go => C:\nadesiko3\nadesiko3go
```

replaceのアロー演算子みたいなのの先にはGitレポジトリクローンのパスを記述します。
この状態で一度ビルドを実行しますと下記のように言われますので
```cmd
c:\developments\vscode\gonako>go build count3.go
go: updates to go.mod needed; to update it:
        go mod tidy
```
下記のコマンドで依存関係を構成します。
```cmd
c:\developments\vscode\gonako>go mod tidy
```
するとgo.modの内容が下記のように更新されます。
```go:go.mod
module gonako

go 1.26.0

require github.com/kujirahand/nadesiko3go v0.0.0

require (
	github.com/dustin/go-humanize v1.0.1 // indirect
	github.com/ebitengine/purego v0.10.1 // indirect
	github.com/go-pdf/fpdf v0.9.0 // indirect
	github.com/google/uuid v1.6.0 // indirect
	github.com/mattn/go-isatty v0.0.24 // indirect
	github.com/ncruces/go-strftime v1.0.0 // indirect
	github.com/remyoudompheng/bigfft v0.0.0-20230129092748-24d4a6f8daec // indirect
	github.com/richardlehane/mscfb v1.0.7 // indirect
	github.com/richardlehane/msoleps v1.0.6 // indirect
	github.com/tiendc/go-deepcopy v1.7.2 // indirect
	github.com/xuri/efp v0.0.1 // indirect
	github.com/xuri/excelize/v2 v2.11.0 // indirect
	github.com/xuri/nfp v0.0.2-0.20250530014748-2ddeb826f9a9 // indirect
	golang.design/x/clipboard v0.9.0 // indirect
	golang.design/x/x11 v0.2.0 // indirect
	golang.org/x/crypto v0.53.0 // indirect
	golang.org/x/exp/shiny v0.0.0-20250606033433-dcc06ee1d476 // indirect
	golang.org/x/image v0.46.0 // indirect
	golang.org/x/mobile v0.0.0-20250606033058-a2a15c67f36f // indirect
	golang.org/x/net v0.56.0 // indirect
	golang.org/x/sys v0.48.0 // indirect
	golang.org/x/text v0.42.0 // indirect
	modernc.org/libc v1.75.7 // indirect
	modernc.org/mathutil v1.7.1 // indirect
	modernc.org/memory v1.12.1 // indirect
	modernc.org/sqlite v1.59.0 // indirect
)

replace github.com/kujirahand/nadesiko3go => C:\nadesiko3\nadesiko3go
```


# なでしこ３(Go版)がトランスコンパイルしたGoソースをGoでビルド
これで準備は整った気がしますのでGoでビルドしてみます。

```cmd
c:\developments\vscode\gonako>go build count3.go

c:\developments\vscode\gonako>
```

こんどはなんにも言われなかったのでたぶん成功。

```cmd
c:\developments\vscode\gonako>dir
2026/09/19  22:25        30,711,808 count3.exe
2026/09/14  22:36             9,698 count3.go
2026/09/14  22:25               699 count3.nako
2026/09/19  22:22             1,418 go.mod
2026/09/19  22:22             7,619 go.sum
```
実行形式exeファイルできてました！:tada::tada:

実行してみます！
```cmd
c:\developments\vscode\gonako>count3   
処理回数：100000000回
処理時間：0ミリ秒
```

動きました！:tada::tada::tada:

処理時間の出力が動いていないっぽいのはなでしこ３(Go版)でランしたときからなので、おっかけ解消を試みてみます。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
