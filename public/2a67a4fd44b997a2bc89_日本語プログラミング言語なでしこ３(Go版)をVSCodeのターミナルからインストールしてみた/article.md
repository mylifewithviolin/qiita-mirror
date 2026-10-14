# はじめに
日本語プログラミング言語なでしこ３のGo言語版が正式にリリースされたようですので、さっそくVSCodeのターミナルからインストールしてみました。


# なでしこ(Go版)のインストール
下記の２種がインストールされるようでした。CLIとGUIは別コンパイラのようです。
なでしこ3 CLI版 (gonako v3.8.4)
なでしこ3 GUI版 (gonako-gui v3.8.4)

## なでしこ(Go版)のVSCodeのターミナルからのインストール

VSCodeのターミナル（Powershell）から下記のコマンドを実行しました。
```ps
irm https://nadesi.com/install/gonako | iex
```

下記のようなエコーが出力されてバイト数っぽい数字がカウントアップしていきます。
```ps
PS C:\developments\vscode\gonako> irm https://nadesi.com/install/gonako | iex
                                          
 Web 要求を書き込んでいます                                                      
    要求のストリームを書き込んでいます... (書き込み済みバイト数: 2233695)  

```
## インストールの完了
インストールが完了すると下記のような状態となります。

```ps
PS C:\developments\vscode\gonako> irm https://nadesi.com/install/gonako | iex
===> [1/2] なでしこ3 CLI版 (gonako v3.8.4) をダウンロード中...                   
  -> CLI版の保存完了: C:\Users\mylifewithviolin\.gonako\bin\gonako.exe                   
===> [2/2] なでしこ3 GUI版 (gonako-gui v3.8.4) をダウンロード中...               
  -> GUI版の保存完了: C:\Users\mylifewithviolin\.gonako\bin\gonako-gui.exe               
  -> デスクトップにショートカットを作成しました: C:\Users\mylifewithviolin\Desktop\なでしこ3 - gonako.lnk                                                                 
===> ユーザー環境変数 PATH に C:\Users\mylifewithviolin\.gonako\bin を追加しました。
===> インストールが完了しました！
===> 動作確認:
CLI版 (gonako): こんにちは！
PS C:\developments\vscode\gonako> 
```

環境変数を追加してくれるようです。

# なでしこ(Go版)のCLIのお試し
## VSCodeのターミナルでCLIのお試し
VSCodeのターミナルをPowershellのままでなでしこ(Go版)のCLIのお試ししてみます。
インストールのエコーでCLI版はgnako.exeっぽいので、gnakoと打てばなにかヘルプとかでるのかなと思い、打ってみました。ヘルプでました。

```ps
PS C:\developments\vscode\gonako> gonako
gonako - なでしこ3 Go言語版

使い方:
  gonako <ファイル> [引数...]       なでしこのプログラムを実行する
  gonako run <ファイル> [引数...]   なでしこのプログラムを実行する
  gonako -e <プログラム> [引数...]  その場でプログラムを実行する
  gonako build <ファイル> [オプション] 単一の実行ファイルに固める
  gonako gengo <ファイル> [オプション] Goソースに変換する（段階10・gogen）
  gonako doc <キーワード> [オプション] 命令やマニュアルを検索する
  gonako doctest [パス...]          DocTestのサンプルを実行して確かめる
  gonako compat run [--cases DIR] [--out DIR]
  gonako compat commands [--source FILE]
  gonako version                    バージョン情報を表示する

ファイル名に - を指定すると標準入力から読み込みます。

build のオプション:
  --out NAME       出力する実行ファイル名 (既定: ソース名から作る)
  --resource DIR   同梱するリソースのフォルダ
  --runtime PATH   土台にするランタイム (既定: 実行中のgonako)
                   他のOS向けのランタイムを指定すれば、そのOS向けに固められる
  --list           同梱されているリソースの一覧を表示する

doc のオプション:
  --command, -c    命令一覧(JSON)から検索する (既定)
  --web, -w        Webのマニュアル(https://nadesi.com/v3/doc/)も検索する
  --json           結果をJSONで出力する (AI向け)
  --limit N        表示する件数の上限 (既定: 20、0で全件)

doctest のオプション:
  --max N          失敗の詳細を表示する件数 (既定: 10、0で全件)
  パスを省略すると manual/plugin_system と manual/gonako と testdata/doctest を対象にします。
PS C:\developments\vscode\gonako> 
```

めちゃめちゃ気になるのはgonako gengo というオプションで、Go言語ソースへのトランスコンパイル機能もありそうな感じです。


## なでしこ１のソースをトランスコンパイルしてみる
### 選択ソート
なでしこ１ではコンパイル・実行できていた下記の選択ソートのソースがコンパイルできるか試してみます。

```nako:selectsort.nako
段ボール箱は「19
18
17
16
15
14
13
12
11
10
9
8
7
6
5」。

選択ソートする。

●選択ソートする

    「整列前　」を表示
    「要素番号　」を継続表示
    段ボール箱で反復し
        「{回数－１}  」を継続表示
    ここまで
    「」を表示
    「ボール数　」を継続表示
    段ボール箱で反復し
        「{それ}  」を継続表示
    ここまで
    「」を表示
    「」を表示

        開始要素番号は整数
        最小値要素番号は整数
        一時退避のボール数は整数
        箱要素数は整数

    段ボール箱の配列要素数を箱要素数に代入
    開始要素番号＝０
    １の間
        もし、開始要素番号＞箱要素数－１ならば、抜ける
        ここまで
        開始要素番号で線形探索し、
        それを最小値要素番号に代入
        もし、開始要素番号＜＞最小値要素番号ならば
            段ボール箱［開始要素番号］を一時退避のボール数に代入
            段ボール箱［最小値要素番号］を段ボール箱［開始要素番号］に代入
            一時退避のボール数を段ボール箱［最小値要素番号］に代入
            //処理経過表示処理ここから
            「　要素番号｛開始要素番号｝と｛最小値要素番号｝を入れ替えました。」を継続表示　
            「｛段ボール箱［開始要素番号］｝　⇔　｛段ボール箱［最小値要素番号］｝」を表示
        //処理経過表示処理ここまで
        ここまで
        開始要素番号＝開始要素番号＋１
    ここまで

    「　」を表示
    「整列後　」を表示
    「要素番号　」を継続表示
    段ボール箱で反復し
        「{回数－１}  」を継続表示
    ここまで
    「」を表示
    「ボール数　」を継続表示
    段ボール箱で反復し
        「{それ}  」を継続表示
    ここまで
    「」を表示。


現在の要素番号は整数
最小値要素番号は整数
箱要素数は整数
現在ボール数は整数
最小ボール数は整数

●線形探索（開始要素番号で）   

    最小値要素番号＝開始要素番号　
    現在の要素番号＝開始要素番号＋１
    段ボール箱の配列要素数を箱要素数に代入 
    
    １の間
        もし、現在の要素番号＞箱要素数－１ならば、抜ける
        ここまで
        現在ボール数＝段ボール箱［現在の要素番号］を整数変換
        最小ボール数＝段ボール箱［最小値要素番号］を整数変換
        もし、最小ボール数＞現在ボール数ならば
            最小値要素番号＝現在の要素番号
        ここまで
        現在の要素番号＝現在の要素番号＋１
    ここまで
    最小値要素番号で戻る。

```

では、トランスコンパイルしてみます。コマンドラインはあっているかは不明。
```ps
PS C:\developments\vscode\gonako> gonako gengo selectsort.nako
[字句解析エラー]selectsort.nako(26行目): 未知の語句: －１...

PS C:\developments\vscode\gonako> 
```
だめでした:joy:。バージョン番号からいってなでしこ３相当と思われますので、なでしこ１のソースは無謀だったかもしれません。

### helloworld
こちらもなでしこ１ではコンパイル・実行できていたソースで、少し短いです。

```nako:helloworld.nako

countとは整数
countMaxとは整数

count=0
countMax=0
コマンドライン[0]を表示する
コマンドライン[1]を表示する
もし コマンドラインの配列要素数 < 2 ならば
　　countMax=0
違えば
   エラー監視
　    countMax=コマンドライン[1]を整数変換
　　エラーならば
 　　 countMax=0
    ここまで
ここまで
countMaxを表示する
開始日時は、システム時間

（count < countMax）の間
　　「Hello World!」を表示する
	count = count + 1
ここまで

終了日時は、システム時間
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する
```
こちらもだめでした:joy::joy:。なでしこ１と３ではけっこう文法が違いそうですね。

```ps
PS C:\developments\vscode\gonako> gonako gengo helloworld.nako
[文法エラー]helloworld.nako(2行目): ローカル変数『count』の定義エラー

PS C:\developments\vscode\gonako> 
```
# おわりに

なでしこ３で書いたことがあったのかなかったのか、だいぶ忘れていますので、次回なでしこ３ソースでリトライしてみます。
