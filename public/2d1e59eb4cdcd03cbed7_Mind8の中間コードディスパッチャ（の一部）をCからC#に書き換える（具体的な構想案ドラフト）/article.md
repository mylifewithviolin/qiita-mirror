# はじめに
[前回](https://qiita.com/mylifewithviolin/items/551d7cfdd62b46b8d29c)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序の口として、Mind8の中間コードファイル内のMCode情報構造体、MCode領域とLocation表をそれぞれC#で読み込んでみましたので、今回はディスパッチャの基本構造としていま想定しているイメージをソースコードにしてみます。

このコードは構想段階のものであり未検証、ビルドエラーはないですが正常実行しないことを確認しているもので、あくまで構想を検討するためのコードです。実際のコードは既にもう少し書き換わっていますが、構想の説明用には前回記事の状態と整合性のある状態を維持しています。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
C# 12 
dotnet-sdk-8.0.204-win-x64

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

C/C++のデバッガは直接使わないのですが、Cで実装されているMind8kernelの動作をデバッグ実行で探るために使用します。[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境となります。

# お題のMind8の中間コードファイル
[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)をご参照ください。

# お題のC#ソースコード
## Main 暫定メイン
本記事から読まれている場合はお手数ですが、[前回記事](https://qiita.com/mylifewithviolin/items/551d7cfdd62b46b8d29c)をご確認ください。
## McodePointer　MCodeポインタ
同じく前回記事もご参照ください。

オリジナルのC版カーネルではCの共用体unionで実装されていますところを、クラス内に共通変数を設けてgetter/setter風の関数を介して操作するという想定です。

スタックにいろいろな型のデータがのるということからのちのバージョンではgetter/setter風の関数の引数型を個々の変数型にしてキャストしながら入出力するという構想ですが、この記事でのソースコードではまだそのあたり未記述です。


今回のC#ソースコードの主な内容は下記のとおりです。ビルドエラーがないだけで動作はしません。あくまで構想段階のソースコードです。

## Dispatcher ディスパッチャ
なるべくグローバル（クラス内プライベート）のスコープを避けるため、重要インスタンスが前回記事のMain内のローカル変数としていて、この関数は参照を渡すことで操作していますが、後で説明する関数配列内からも操作されるため、最新版ではクラス内プライベートスタティックに変更されていることをご容赦ください。
```cs:Mind8Dispatcher.cs

    /// <summary>ディスパッチャ</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
    /// <param name="McodeBase">MCode領域の参照</param>
    /// <param name="WordOffsetTable">LOCテーブルの参照</param>
    /// <param name="DataBase">データ領域の参照</param>
    /// <param name="McodeInfo">データスタックの参照</param>
    ///  <param name="McodeInfo">リターンスタックの参照</param>
    /// <param name="mcodefilename">MCodeポインタの参照</param>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void Dispatcher(ref McodeInfoStruct McodeInfo,
            ref byte[] McodeBase,ref byte[] WordOffsetTable,ref byte[] DataBase,
            ref Stack<ulong> DataStack,ref Stack<ulong>RetnStack,
            ref GeneralPointer McodePointer,ref Action[] csFuncs){
        
        short   mcode;

        int retcode=0;//setjmp( RESTARTENV );		/* ←ディスパッチャ再 */
        if ( retcode != 2 )			/* 強制脱出の検査 */
        {
            for(;;)
            {
                mcode = (short)McodePointer.GetUw();
                if ( (mcode & 0x8000)==0 )
                {
                    /* C#関数 */
                    csFuncs[mcode]();
                }
                else
                {
                    /* Mind単語 */
                    RetnStack.Push(McodePointer.GetUl());//現在のMCodeポインタをリターンスタックにプッシュする
                    McodePointer.SetUb(WordOffsetTable[mcode & 0x7fff]);
                }
            }
        }
        return;
    }
```

## SetupCsFunctions C#の関数配列を準備する
オリジナルのC版カーネルではディスパッチャからC定義関数を実行する際に、関数の配列が使われています。ここはまさにMindのランタイムを実装言語から浮かせた疎の関係で構築するまさにまさにキモの部分ですが、C#でも同じように実装します。下記の記事を参考にさせていただきました。

デリゲートを利用して配列に関数を格納する C# Qiita
https://qiita.com/papyrustaro/items/a6420caec8ac8dabca60

```cs:Mind8Dispatcher.cs

    /// <summary>C#の関数配列を準備する</summary>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void SetupCsFunctions(ref Action[] csFuncs){
        csFuncs=new Action[maxCountCsFunctions];
        csFuncs[0x0010]=DummyFunc0;
        csFuncs[0x0011]=DummyFunc1;
        csFuncs[0x0012]=DummyFunc2;
        csFuncs[0x0013]=DummyFunc3;
        csFuncs[0x0014]=DummyFunc4;
    }
    private static void DummyFunc0(){
    }
    private static void DummyFunc1(){
    }
    private static void DummyFunc2(){
    }
    private static void DummyFunc3(){
    }
    private static void DummyFunc4(){
    }
```
Mindの基礎的な単語に紐づくこれらの関数の中身は本記事ではまだまったく未実装です。（本記事下書き後、少し実装しはじめてスタックやスタックポインタのスコープが本記事のままではよろしくないことに気づきました。追って更新版を展開いたします。）

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達して、序の口は抜けたかなという感じです。（まだ動きません。現状は中間コードファイルの中身を３つの領域でbyte配列の読み込むところまでが動作している範囲です。）
次回以降で、このソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。



# 参考情報
Mindのランタイムを実装言語から浮かせた疎の関係で構築するまさにまさにキモの部分についてもっと詳しく知りたいと興味をお持ちになった方は、下記の記事のコメントでMind開発者の@killyさんに詳しく解説いただいていますので、よろしかったらご参照ください。

VSCodeでMind 8 for Windowsのkernelをデバッグ実行（dispatch->C_Words_Addr[mcode]）Qiita
https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c
