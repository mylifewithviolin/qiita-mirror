# はじめに
VSCodeでMind 8 for WindowsのKernelを[デバッグ実行できました](https://qiita.com/mylifewithviolin/items/83d95970c19ea0b2f2a8)ので、今回も引き続きそのデバッグ途中のご様子のレポートです。※注 デバッグの言い回しですが、もちろんデバッグが目的ではなく、学習目的でステップ実行しているだけです。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

# デバッグ実行の前提条件
Mind開発者の@killyさんからの前回記事コメントでのさらなる情報共有で、今回デバッグ対象のmindexec.exeはランタイムのローンチャに過ぎないことが判明。（以前からさんざん聞いていたような:sweat_smile:）
前回はターゲットのMコードファイルないかなということで、無謀にもとっさにMindコンパイラ自体のmind.mcoを使ってしまいましたので、今回はkillyさんお勧めのシンプルサンプルのhello.mcoをリネームしてみることとします。（そこから思いもよらない発見をすることになります！）

```
C:\developments\vscode\mind8\kernel>dir mindexec.*

 C:\developments\vscode\mind8\kernel のディレクトリ

2023/01/22  16:36             2,130 mindexec.c
2024/02/17  10:12           169,472 mindexec.exe
2024/02/17  10:12           747,528 mindexec.ilk
2023/07/23  09:31            43,562 mindexec.mco
2024/02/17  10:12            34,727 mindexec.obj
2024/02/17  10:12         1,272,832 mindexec.pdb
               6 個のファイル           2,378,143 バイト
```
mindexec.mcoがほんとはhello.mcoだったやつです。

# デバッグ実行中のご様子
最初から下図の状態までいったわけではありませんが、無事に正常実行されまして「こんにちは、Ｍｉｎｄです。」がコンソール出力されていることがわかります。

![vscodec15.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/992ac2ba-02b7-5fca-2f4c-ba0476a1976e.png)

賢明な本記事読者のみなさまはお気づきかと存じますが、前回のmind.mcoの場合と異なる状態となっています。

それはランタイムのファイル名です。前回のmind.mcoの場合はmrunt060.exeだったのですが、今回のhello.mcoの場合はmrunt010.exeとなったのでした。

 したがって上図の状態ではmrunt010.exeもkernelフォルダに置かせていただきます。mrunt010.exeのがmrunt060.exeより若干でかいことがわかります。
```
C:\developments\vscode\mind8\kernel>dir mrunt*.exe

 C:\developments\vscode\mind8\kernel のディレクトリ
 
2023/01/22  16:36           291,840 mrunt010.exe
2023/01/22  16:36           181,760 mrunt060.exe
               1 個のファイル             181,760 バイト
```

# デバッグ実行中のご様子2
どこでこのバージョン番号が変わったのか、なんどか注意深くステップ実行してみますと次のことがわかりました。

mindex.cが	make_runtname_and_cmdline();を実行すると、その関数内で
	strcat( RuntimeProgname, VersionDigits );
でVersionDigits("010")をランタイム名にセットしていて、そのVersionDigitsの値がどこでセットされているかというと
mindex.cのdecide_version_no()という関数がその手前で呼ばれて


![vscodec17.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d3147d35-3ad1-4c3f-61c1-9d9d2f87716e.png)

その関数内でmindex_readmcode.cのreadMcodeInfoTableという関数を実行し、Mコードファイルの先頭固定32バイトを読みだしてMcodeInfo構造体に値をセットして、McodeInfo構造体メンバのminfoRuntimeNoに10がセットされ、それがVersionDigitsに連携されるという流れでした。

![vscodec16.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c840c641-f26a-d003-8ee0-115e09bf611a.png)

# おわりに
ちょっとタイムアウトしてしまいました。McodeInfo構造体の存在に気づいたのは収穫ですがぜんぜん謎には迫れていませんので、続きは次回ということで。また、mrunt0NN.exeにどのソースファイルが該当するのかはmakefileやその他のbatを見ても読み取れていません。
