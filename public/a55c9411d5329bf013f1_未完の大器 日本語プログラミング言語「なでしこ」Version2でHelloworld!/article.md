# はじめに
未完の大器 日本語プログラミング言語「なでしこ」Version2でHelloworld!してみます。昨年実行時間検証用に記述した「なでしこ」v1のコードは　「[ERROR] インデントレベルが間違っています。」と怒られてしまったので、とりあえず一番シンプルコードで実行してみました。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
nadesiko2 2014/04/22リリース版(β版)
C# 12 ※直接関係ないかもしれませんが入っているので
dotnet-sdk-8.0.206-win-x64 ※直接関係ないかもしれませんが入っているので monoは入れてないです。

# 日本語プログラミング言語「なでしこ」Version2とは

いろいろな情報を総合すると.NETCore統合前のmono版.NETのCLR中間コードにコンパイルするバージョンのようです。実装言語は2014年ごろのC#

https://nadesi.com/dev/wiki/index.php?%E3%81%AA%E3%81%A7%E3%81%97%E3%81%932.0

現時点では開発中断しているバージョンです。開発リポジトリ上の最終マージは2018年11月ごろ。今回実行しているバージョンは上記サイトに掲示されている 2014/04/22リリース版(β版)です。

# プロジェクトフォルダ構成
```cmd:
C:\nadesiko2\vscode>tree /F
C:.
│  callfunc.nako
│  count.nako
│  count3.nako
│  helloworld.nako
│  helloworld3.nako
│
└─bin
    │  cnako-sh.bat
    │  cnako.sh
    │  cnako2.exe
    │  edit.nako
    │  Libnako.dll
    │  NakoPlugin.dll
    │  ReadMe.txt
    │
    └─plug-ins
            fastJSON.dll
            HtmlAgilityPack.dll
            Interop.ADODB.dll
            Libnako.dll
            ...略
```

# 実行

無事に実行成功しました。まだよくわかっていないので、試行錯誤中です。cnako-sh.batのとおりにフォルダ構成していませんので、直接コマンド実行しています。

![nadesiko21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7e4180e2-c44a-2995-9b31-92c361280815.png)

「[ERROR] インデントレベルが間違っています。」と怒られたのはこちらの記事にあるコードなのですが、冒頭の実行モード指定文とかが対応していないような気もしてきましたので、機会があれば検証してみます。

https://qiita.com/mylifewithviolin/items/74b55ba0104889f7a93f

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
