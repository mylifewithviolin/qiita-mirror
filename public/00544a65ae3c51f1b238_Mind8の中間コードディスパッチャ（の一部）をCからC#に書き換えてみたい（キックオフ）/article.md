# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)でVSCodeでMind 8 for Windowsのkernelをデバッグ実行できる環境をつくり、[前回記事](https://qiita.com/mylifewithviolin/items/923875a640768e3e993f)まで主に64bit整数変数の処理単語の習作をMind開発者の@killyさんのご支援をいただきつつ行って参りました。

今回はその処理単語追加の習作へと進行する分岐点となったMind8のkernelをデバッグ実行できる環境の記事に立ち戻り、その後の習作で学習した知見もまじえつつ、Mind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望に進行してみようと思います。今回はそのキックオフ的な記事で、当時の振り返りとこれまでのまとめです。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows

このテーマでは処理単語の追加はなく、既存単語のMCode（の一部）を解釈実行する部分をCからC#に書き換えるというお題のため、辞書再構築ツールは使用しないので、Mind7ライセンスは不要です。

C# 10 
dotnet-sdk-6.0.419-win-x64
dotnet-sdk-6.0.419-win-x86
Mind Version 7.5 for Windows

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

C/C++のデバッガはMind8のCカーネルアプリケーションをデバッグ実行するために使用しています。実装には使いませんが動作を確認するのに引き続き使用します。
.NETCoreバージョンは少し低めなので、どこかのタイミングで引き上げる見込みです。x86かx64か微妙ですが、いまのところx64で実装してなにか問題があればx86に切り替えるというスタンスで行きます。

# これまでのまとめ
・kernel.cがkerbody.cをインクルードしてkerbody.cがkermain.cをインクルードする入れ子構造となっていて、kermain.cのexecute_main_wordという関数内で、同じくkermain.cのsetupForDispatchという関数でMCodeファイルが読み込まれ、同じくexecute_main_word関数内からdispatch.c内のdispatcher()という関数が実行されます。

・dispatcher()の中身はざっくり書くと下記のような感じになっているようです。
細かい話ははしょってます。以下は疑似言語Re:Mindによる表記です。

```
〇ループする

　□mcode = フェッチする
 ◇mcodeと0x8000のビット論理積が偽の場合
   //C関数
   □C_Words_Addr[mcode]()
 ◇真の場合
   //Mind単語
   □PUSH_R( McodePointer.l )
   □SET_MCODE_POINTER_BY_WORDNO( mcode & 0x7fff )
 ◇ここまで

〇ここまで
```
当面の課題は上記のC関数の方に分岐した場合の
```
C_Words_Addr[mcode]();
```
をC#に書き換えることをめざします。

このあたりの実行イメージは、64bit整数変数の処理単語の追加習作の過程でだいぶつかんでいるとはいえ、MindのCランタイムが用意しているアプリケーションスタックやそのポインタの動きはまだ細かくは認識していません。いろいろな試行錯誤が想定されます。

このループが回ってmcodeにいろいろな値が入ってくるとビット論理積がC関数側に成立して、C_Words_Addr関数配列が実行されると、mcodeがインデックスになって、テーブルを参照して所定の対応関数を呼び出していく処理のあたりです。

これはものすごく画期的な処理構造と認識しました。mcodeは相当ランタイムフリーな実装と思われます。これによりほとんどの範囲の特定の実装言語で実装された処理を直接ファンクションコールすることを回避していることになります。ただし、ディスパッチャ自体はその実装言語で実装される必要はあり、ここが本記事のテーマです。


# なにがうれしいかのまとめ
本記事はキックオフということであまり中身がありませんが、最後にMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えれると、なにがうれしいのかまとめてみます。

Mind自体がmcodeというCPU実装やOSから切り離された環境で走行していますが、ランタイムがCで書かれているため、他の言語実装の機能を利用するためにはC言語のDLLにする必要があったり、Cで処理単語を追加する必要があります。

Mind8の中間コードディスパッチャがC#で書かれた処理単語を呼び出せるようになると.NETCoreや.NETFrameworkの資産をMind側のソースコードから簡単に呼び出せるようになる気がします。mcode上のデータフォーマットはC言語互換っぽいので、マネージドランタイム型へのマーシャリングとか問題になるかと思われますが、MindのDLLをC#から呼び出す際にちらっとやっているので、そのあたりがとっかかりにはなる想定です。

またC#のランタイムの.NETCoreは今日的にはいろいろなプラットフォームで動くのでそれらの環境でMindが走行できるようになるのも楽しいかもしれません。

# おわりに
しかし、実際の課題は山積で思うように進まないことも想定されますので、いろいろなテーマと並行してのんびりやっていこうかと考えております。Cで書かれているすべての処理単語を対応させるのは気の遠くなる作業なので、あくまで一部単語を動かして悦んでみたいという興味本位のテーマです。

# 追記
* その後の展開情報

https://qiita.com/mylifewithviolin/items/818de8aca51f6750da6c

https://qiita.com/mylifewithviolin/items/151517f7a57b5b8b97f5
