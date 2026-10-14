# はじめに
Windows11上のVSCode統合のUbuntuターミナル(bash)でEucJPネイティブアプリの文字出力を確認したいため、統合ターミナルの構成方法を調査しました。応急処置として[VSCode [WSL2:Ubuntu] をTeraTermで接続できるよう構成する](https://qiita.com/mylifewithviolin/items/8b6bb4b6b64fda6d3f19)により、EucJPネイティブアプリの文字出力を確認できています。

## この記事内容の作業目的
VSCode [WSL2:Ubuntu] のterminal.integrated.profiles.linuxを構成する。
EucJPネイティブアプリの文字出力をVSCode [WSL2:Ubuntu] で確認するため。

## この記事内容の作業環境
Windows11
Windows11WSL2（Ubuntu 22.04.1 LTS）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2

## この記事内容の保証
※この記事には環境構築の手順的な情報が含まれます。本記事に書かれた手順の妥当性は保証されません

# settings.json
実行環境はVSCode [WSL2:Ubuntu] です。
設定情報のsettings.jsonは下記のパスに保存されます。

/home/{user}/.vscode-server/data/Machine/settings.json

## terminal.integrated.profiles.linux

このあたりの情報を参考にして
[Terminal Profiles in Visual Studio Code](https://code.visualstudio.com/docs/terminal/profiles)
settings.jsonを編集して下記の状態としますと、いちおうVSCode統合のUbuntuターミナル(bash)は起動成功します。

```json:settings.json
{
    "files.encoding": "eucjp",
    "terminal.integrated.profiles.linux": {
        "bash": {
            "path": "bash",
            "icon": "terminal-bash",
            "encoding": "eucjp",
            "args": [],
            "env": {},
            },
    },
    "terminal.integrated.env.linux": {
        "JLESSCHARSET": "japanese",
        "LANG": "ja_JP.eucJP",
    },
}

```
認識されない変なオプションを指定するとターミナルが起動失敗するようになりますから、この構成を認識しているのは確かです。

"files.encoding": "eucjp"は、ユーザー設定のUIからコードエディタの文字コードを変更した際に、出力された行です。当初はこの一行だけでした、

"terminal.integrated.env.linux"はこちらの記事
[VSCodeのターミナル/プロファイルの設定の詳細](https://qiita.com/take_me/items/47f192a126d75a9264a9)　
を参考にして.profileに記載した環境変数を追記してあります。

"terminal.integrated.profiles.linux"内の"env"に当初指定していましたが、こちらより適用されるスコープが広いようであるため、"terminal.integrated.env.linux"だけの設定としています。

# ターミナル起動
統合のUbuntuターミナル(bash)を追加起動してみます。
しかし、コマンドでEucJPネイティブアプリの文字出力を確認すると化けてます。

```bash:
$ ./main
EUC-JP���ܸ��VSCode����Bash�����ߥʥ뤫��ɽ�����Ƥߤ�
```

Tera Termで接続して実行した結果です。
```bash:
$ ./main
EUC-JP日本語をVSCode統合Bashターミナルから表示してみる
```

windows版の統合ターミナルのパワーシェルの場合は、起動オプションの引数argsに文字コード指定があり、それにより変更できるようですが、bashの場合その上にかぶさっている統合機能の文字コード構成方法が不明です。

# タスクの実行
タスクの実行で起動されたターミナルには下図のようなVSCode独自の日本語メッセージが出力されます。

```bash:
 *  実行するタスク: /home/puremind/pmind/src/qcc/main  

EUC-JP���ܸ��VSCode����Bash�����ߥʥ뤫��ɽ�����Ƥߤ�
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

このメッセージのエンコードは既定ではLanguage pack extension for Japaneseのエンコードに従っていると推察され、そっちのオプションの日本語の中になにか選択子はないか、確認してみましたが、UI上はConfigure Display Languageの日本語選択子はjaの一択でした。

下記はだめもとでEnglish(en)に戻した場合のエコーです。
```bash:
���ܸ�ץ�����ߥ󥰸��� �ͣ��� Version 8.07 for UNIX
          Copyright(C) 1985 Scripts Lab. Inc.
����ѥ����� .. ��λ
Coping.. /home/puremind/pmind/bin/mindex --> /home/puremind/pmind/src/qcc/main
 *  Terminal will be reused by tasks, press any key to close it. 
```


下記の記事にこのタスクの内容を書いてあります。
[VSCode [WSL:Ubuntu] で日本語プログラミング言語Mindのソースをビルドしてみた](https://qiita.com/mylifewithviolin/items/366d1e3b0fea9485acdb)

# 参考リンク

https://qiita.com/take_me/items/47f192a126d75a9264a9

https://qiita.com/tt4q/items/8a0e4c31f13279db0d65
