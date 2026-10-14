# はじめに
いまとなってはそこそこの前ですが、node.jsのexpressを実装したときに初めてVSCodeを使いました。
その後.NETはやっぱりVisualStudioで、Javaはeclipseでという使い分けでしたが、昨年ごろからC#もJavaもTypeScriptも一つのシステム内で機能分担ということから、みんなVSCodeで編集デバッグビルドを行って仕事してます。

そんなことから日本語プログラミング言語MindのソースもVSCodeで編集ビルドしてみたくなった。デバッグはExtensionがないのでたぶんできない。でも、雰囲気は味わってみたい。てな感じです。

## この記事内容の作業目的
[トランスコンパイラの作り方 Ｃ言語を日本語プログラミング言語Mindにトランスコンパイルしてみる（四則演算版）](https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c)で出力させたMindのソースコードをコンパイル検証したい、その検証環境を構築した。
## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu 22.04.1 LTS）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
Mind 8 for Linux　mind-for-linux-8.0.08.tgz
### Mindコンパイラの前提状態
[Ubuntu 22.04.1 LTS でMindコンパイラ 8.0.08 のカーネルをmakeする（したい）](https://qiita.com/mylifewithviolin/items/367d98edc057765387b3)という記事に記載のbash上でのmindexecの起動確認が済んだ状態。
## この記事内容の保証
※この記事には環境構築の手順的な情報が含まれます。本記事に書かれた手順の妥当性は保証されません。とくにbashdbgつかったローンチはあくまでイメージ、ファンタジーです。

# 文字コード、環境変数
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
homeのユーザー名とmindのインストールフォルダpmindの位置関係です。
VSCodeは/home/puremindをワークフォルダとして開いてるとします。
pmindフォルダの下のsrc/qccにソースファイルを格納します。
```
$ tree /home/puremind -d
/home/puremind
|-- gcc11
`-- pmind
    |-- bin
    |-- kernel
    |-- lib
    |-- src
    |   `-- qcc
```
## VSCodeの文字コード変更
まず、VSCodeの文字コードをeucJPにします。
設定でリモート[WSL:Ubuntu]のFiles:Encodingを[Japanese (EUC-JP)]に変更します。
これはマストです。既定のUTF-8の場合、Mindコンパイラは正しく日本語ソースを認識しません。

統合ターミナルのエンコーディングの設定は未発見です。設定の検索機能でEncodingを指定しても、上記ファイルエディタのエンコーディングしか該当しませんでした。
## .profileの修正
続いてUbuntuの文字コードを変更し、Mindの環境変数を追加します。
VSCodeのフォルダエクスプローラーで/home/puremindにある.profileを開きます。

下記の４行をファイルの末尾に追加して保存します。
```bash:.profile
export LANG=ja_JP.eucJP
export JLESSCHARSET=japanese
export PATH="$PATH:/home/puremind/pmind/bin"
export MLIBPATH="/home/puremind/pmind/lib
```
# tasks.jsonの編集
VSCodeのフォルダエクスプローラーでワークフォルダルート配下にある.vscodeフォルダ（これは隠しフォルダのためtreeでは出力されていません）の下にtasks.jsonというファイルを作成します。
```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "process",
            "command": "./mind",
            "args": [
                "${workspaceFolder}/pmind/src/qcc/main.src",
                "file"
            ]
        },       
        {
            "label": "run",
            "type": "process",
            "command": "${workspaceFolder}/pmind/src/qcc/main",
              "args": [],
              "options": {
                "cwd": "${workspaceFolder}/pmind/bin"
            },
        }
    ]
}
```
"label": "build"がMindコンパイラによるコンパイルタスクを指定しており、
"label": "run"が生成コードの実行を指定しています。

このタスクはメニュー:ターミナルのタスクの実行から、"build"、"run"でそれぞれリストから選択して実行できるようになります。

# タスクの実行
それでは、[トランスコンパイラの作り方 Ｃ言語を日本語プログラミング言語Mindにトランスコンパイルしてみる（四則演算版）](https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c)で出力させた下記のソースコードをVSCodeのエディタから、コンパイルとコンパイル結果の実行を行ってみます。

```:5 * ( 9 - 6 )
メインとは
  5
  9
  6
  引き
  掛け
  数値表示する
```
元の記事を読まれていない方のため簡単に説明しますと、これは　5 * ( 9 - 6 )という計算をMindの該当計算コードに機械的に変換したものです。「数値表示する」という結果の出力機能はオリジナルのCコンパイラのアセンブラ出力コードにはないのですが、計算結果をコンソールに出力させて結果をわかりやすくするため追加しています。
縦に改行して並んでいるのもオリジナルのアセンブラソースとの関係の影響です。

このソースコードをVSCodeのエディタに貼り付け、pmind/src/qcc/main.srcとして保存します。

## タスク"build"の実行

VSCodeのメニュー:ターミナルのタスクの実行から、実行するタスクの選択で"build"を選択します。するとタスクの出力のスキャンをどうするかの選択しが表示されますので[タスクの出力をスキャンせずに続行する]を選択します。これで実行されます。
下記はその結果のターミナルの出力です、

```
 *  実行するタスク: ./mind /home/puremind/pmind/src/qcc/main.src file 


���ܸ�ץ�����ߥ󥰸��� �ͣ��� Version 8.07 for UNIX
          Copyright(C) 1985 Scripts Lab. Inc.
����ѥ����� .. ��λ
Coping.. /home/puremind/pmind/bin/mindex --> /home/puremind/pmind/src/qcc/main
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 

```
VSCodeが出力する日本語は正常ですがMindコンパイラのエコーの日本語が化けているという謎状態ですが、コンパイルは成功したっぽいです。

```bash:
~/pmind/src/qcc$ ls -l
total 92
-rwxr-xr-x 1 puremind puremind 12862 Jan 29 01:27 main
-rw-r--r-- 1 puremind puremind    79 Jan 29 01:27 main.his
-rwxr-xr-x 1 puremind puremind 39444 Jan 29 01:27 main.mco
-rw-r--r-- 1 puremind puremind    54 Jan 28 20:55 main.src
-rw-r--r-- 1 puremind puremind 28516 Jan 29 01:27 main.sym
```
成功です！
では続いて実行タスクを実行してみます。

## タスク"run"の実行

VSCodeのメニュー:ターミナルのタスクの実行から、実行するタスクの選択で"run"を選択します。あとは"build"と同じです。
下記はその結果のターミナルの出力です、

```
 *  実行するタスク: /home/puremind/pmind/src/qcc/main  

15 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
成功です！
ちょっとわかりにくいかもですが、15 というのが結果です。
Mindのコンソール出力関数「数値表示」は改行は別途実行のタイプのようです。たしか、「改行する」とか？

9 - 6 は 3 で、それ掛ける 5は 15であってますね。

# デバッグ実行を疑似体験する

ここまでくるとC#やJavaのようにデバッグ実行してみたくなります。
コンパイルと実行はタスクに依存関係を設定して、"run"を実行する前に"build"を実行させるとかもできますが、ここはやはりlaunch.jsonを編集してみたくなります。

## launch.jsonを編集

下記は日本語プログラミング言語MindのソースコードをVSCodeエディタでデバッグしているかのような雰囲気を味わうためのものです。
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "mindc",
            "type": "bashdb",
            "request": "launch",
            "preLaunchTask": "build",
            "postDebugTask": "run",
            "program": "${workspaceFolder}/pmind/src/qcc/main.src",
            "args": [],
            "cwd": "${workspaceFolder}/pmind/src/qcc/",

        }
    ]
}
```
ポイントはダミーのデバッガextensionとしてVS Code Bash Debugを設定したことです。
設定オプションもコンソールアプリとして少な目で、実際にMindのソースを読み込んでも、ちゃんとステップ実行できてハングしてとまったりはしなかったです。

"preLaunchTask": "build" で、デバッグ開始前にコンパイル、 
"postDebugTask": "run" でデバッグ後にコンパイルコード実行としています。

## デバッグ実行開始

VSCodeのメニュー:実行から、デバッグの開始を選んでもよいですが、ここは左側のアイコンメニューから△を選んで、実行とデバッグにmindcと表示されていることを味わいたい。


![vscedemind.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7c41827e-bd68-921e-c037-11a0df94d5fb.png)

この状態はbash debugにMindのソースを読み込ませているだけですが、想像以上に感動的でした。
下図はデバッグ終了して、事後タスクの実行がターミナルに出力だれている状態です。
![vscedemind2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/aa3960bf-8c0f-6fa3-e101-97acdedbacac.png)

# 最後に
VSCodeのExtension界隈はかなり盛り上がっている感じですね。
VSCodeExtensionの実装も覚えておきたい気分はあります。

# 参考リンク

https://qiita.com/__cooper/items/9517addaaf1e77215848

https://qiita.com/smileyFace/items/0e4c2a47809c84f45cbf

https://qiita.com/killy/items/e4c7e491a077a6aedb67

https://qiita.com/mylifewithviolin/items/367d98edc057765387b3
