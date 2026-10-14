# はじめに
VSCodeでMind 8 for WindowsのKernelを[デバッグ実行できました](https://qiita.com/mylifewithviolin/items/96168b67c59ff03bf236)ので、今回も引き続きそのデバッグ途中のご様子のレポートです。※注 デバッグの言い回しですが、もちろんデバッグが目的ではなく、学習目的でステップ実行しているだけです。

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
[前回記事](https://qiita.com/mylifewithviolin/items/381d842d81f9fc280244)と同じです。launch.jsonとmakefileの修正が[前々回](https://qiita.com/mylifewithviolin/items/96168b67c59ff03bf236)の状態に対してありますのでご確認の上、本記事お読みください。
前々回まで mindexec.exeのデバッグ実行
前回以降　kernel.exeのデバッグ実行

# 前々回までのまとめ
・mindexec.exeはMindコンパイラによりMindソースファイル、例えばhello.srcがコンパイルされて、MCodeファイル（Mindの中間コードファイル）hello.mcoが生成されると同時にhello.exeにリネームされる。

・mindexec.exeのソースmindexec.cをVSCodeのmscデバッガに認識させるため、hello.mcoをmindexec.mcoにリネームしてmindexec.exeのデバッグローンチに成功。

・mindexec.cがインクルードするmindex.cのint main()関数内からmindex_readmcode.cのdecide_version_no()関数を実行してMCodeファイル（hello.mco=mindexec.mco）の先頭32バイトを読み取りmcodeinfo構造体のメンバに値をセットする。

・mindコンパイラ以外のmindアプリケーションはMcodeInfo構造体メンバのminfoRuntimeNoに10がセットされて、kernel.exeがリメームされたmrunt010.exeをmindex.cのint main()関数内でspawnvによりローンチされる。

# 前回までのまとめ
・mrunt010.exeのソースkernel.cをVSCodeのmscデバッガに認識させるため、hello.mcoをmindexec.mcoにリネームしたままlaunch.jsonで起動ファイル名をkernel.exeとして引数にmindexec.mcoを与えてデバッグローンチに成功。

・kernel.cがkerbody.cをインクルードしてkerbody.cがkermain.cをインクルードする入れ子構造となっていて、kermain.cのexecute_main_wordという関数内で、同じくkermain.cのsetupForDispatchという関数でMCodeファイルが読み込まれ、同じくexecute_main_word関数内からdispatch.c内のdispatcher()という関数が実行されます。

# kermain.c内のexecute_main_word()
dispatch.c内のdispatcher()に進む前に、前々回の記事に対するコメントでMind開発者の@killyさんが強調されていた、execute_main_word()の中でsetupForDispatchの少し後に出現する下記のヶ所に注目します。

>　McodePointer.b = (UCHAR *)McodeBase + 0x70;
>という 0x70 番地が最初に実行するＭコードのロケーションです。これはどのようなユーザプログラムでも固定です。

それがここです。

![vscodec20.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/412c34ab-7194-36ed-edc0-68644d42abed.png)

左側のウォッチ式にMcodePointerを追加していますので、McodePointerにはbメンバの他にもいくつかメンバが構成されているようでした。これらのメンバには上図より少し進むと値がセットされます。

以下にkillyさんのコメントを引用させていただきます。私はまだよく意味がわかっておりません。
>本来「メイン」はもっと後ろにあるのですが、仮定義／本定義の形でとりあえず70番地をスタートして、そこからジャンプするようになっています。
「メイン」に限り、
>　メインとは　本定義
>と書かなくて済むようにコンパイラで工夫をしています。

逆のことを言っているかもしれませんが、ほんとうはメインも仮定義で手前のアドレスにエントリポイントがあるのだけれど、この処理によって本定義による後方のエントリポイントの確定を書かなくてもよくしているような？感じ？めちゃくちゃアバウトですみません。

# dispatch.c内のdispatcher()

さて、いよいよ本記事のお題です。
dispatcher()の中身はざっくり書くと下記のような感じになっているようです。
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
本日は上記のC関数の方に分岐した場合の
```
C_Words_Addr[mcode]();
```
に注目します。

私のMindコンパイラ用語ボキャブラリの不足から自力では説明できないのですが、この関数ポインタの配列みたいなのが、MindのC定義単語の順番変えちゃよろしくないです的なKillyさんの過去説明が思い浮かぶところです。

ここをデバッグ実行して、ループが回ってmcodeにいろいろな値が入って（基本はこんにちはMind一行表示にまつわるMCode）ビット論理積がC関数側に成立して、C_Words_Addr関数配列が実行されると、

![vscodec21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/27572db3-f56b-18bb-7950-947805089cbd.png)

mcodeがインデックスになって、kerbody.cに定義されている
```
void    (*C_Words_Addr[])(void)= {
    //ダミー略
    #include    "c_words.tbl"		/* アプリ用(console) */
        NULL                        /* 調整用のダミー(','調整)  */
};    
```
を介してテーブルを参照して所定の対応関数を呼び出しているようでした。

# おわりに
タイムアウトしてしまいました。ちょっとおなかいっぱいです。次回はMind単語の方に挑戦してみます。
