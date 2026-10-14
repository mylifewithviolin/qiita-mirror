# はじめに
[前回](https://qiita.com/mylifewithviolin/items/b4653bd49b1eb2b5e417)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序二段として、type unionで実装されているMCodeポインタの代替実装を行ってみました。

お題のMCodeファイルは実行開始位置0x0070から8Byteは下記のようなMCodeが格納されていることがわかっていて
```
16進　10進
8019 32793
828D 33421
801A 32794
0020 32
```
この範囲のMCodeのディスパッチャの読み取りはC版と同じような動きをするところまでいきました。

今回はその次にあるコード、Mind8のLocation表、通称Locテーブルのアドレスポインタに適切な値をセットして次のMCodeを取得してMCodeポインタにセットして、さらに次のMCodeを取得するといったあたりを実装します。

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

## class LocTablePointer　LocTableポインタ
MCode領域と同じくByte配列で読み込んでいるLocテーブルにアクセスするクラスとメンバ関数を実装してみます。

```cs:Mind8Dispatcher.cs
   private class LocTablePointer{
        private byte[] locArray =[];
        public void SetupLocArray(byte[] locTable){
            locArray=locTable;
        }
        public int GetSl(ulong locIndex){/* for signed long access   */
            locIndex*=4;
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = locArray[locIndex + i];
            return BitConverter.ToInt32(int32Byte, 0);
        }
        
    }
```
同じくByte配列として確保しているデータ領域をアクセスするクラスと共通化するため、refを指定していましたが、MCode領域とLocテーブルは読み込みOnlyかもしれませんので、今回の関数にはrefつけないでいます。またインデックスの型がulongなのは大きすぎるかもしれませんが、とりあえず将来的な余裕を見ておきます。

## Main 暫定メイン
暫定メインがまた少し書き換わります。前回記事のMCodeポインタの初期化に加えて、今回のLocテーブルポインタの初期化が加わります。従来のGeneralPointerのAccessPointerは引き続き未使用です。
```cs:Mind8Dispatcher.cs
    private static Stack<ulong> DataStack = new();
    private static Stack<ulong> RetnStack = new();
    private static  byte[] McodeBase =[];//MCode領域
    private static byte[] WordOffsetTable=[];//LOCテーブル
    private static byte[] DataBase =[];//データ領域
    private static GeneralPointer McodePointer =new();
    private static GeneralPointer AccessPointer =new(); /* メモリアクセス用ポインタ */
    private static MCodePointer mp=new();
    private static LocTablePointer lp=new();

    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        String mcodefilename="hello.mco";
        McodeInfoStruct mcodeInfo =new();

        /* ディスパッチャを準備する */
        bool ret=SetupForDispatch(ref mcodeInfo,mcodefilename);
        if(!ret){
            return;
        }
        //resetDataStackPointer();	
        //resetRetnStackPointer();
        MonitorMcode(McodeBase);
        DataStack = new();//DstackPointer = DataStackBase[RestartEnvCount];
        RetnStack = new();//RstackPointer = RetnStackBase;
        mp =new();
        lp=new();
        mp.SetupMcodeArray(ref McodeBase);
        lp.SetupLocArray(WordOffsetTable);
        //McodePointer.b = (UCHAR *)McodeBase + 0x70;	/* 0x70=実行開始地点 */
        mp.ResetMcodeIndex(0x70);
        /* C#の関数を準備する */
        Action[] csFuncs=[]; //C#の関数を格納する配列
        /* C#の関数配列を準備する */
        SetupCsFunctions(ref csFuncs);
        /* ディスパッチャ開始 */
        Dispatcher(ref mcodeInfo,ref csFuncs);

    }
```

## Dispatcher ディスパッチャ
そしてディスパッチャのループ内のMind単語側のCのマクロ
```cs:
    SET_MCODE_POINTER_BY_WORDNO( mcode & 0x7fff );
```
の１文をC#の実装に置きかるのが本記事のお題中のお題です。上記マクロの下のコメントはマクロの実行内容のコメントです。
Locテーブルのアドレスポインタ配列のインデックスにmcode & 0x7fffの結果を渡し、LocテーブルからMCodeポインタの値を取得してMCodeポインタにセットします。

```cs:Mind8Dispatcher.cs
    /// <summary>ディスパッチャ</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void Dispatcher(ref McodeInfoStruct McodeInfo,
              ref Action[] csFuncs){
        
        ushort   mcode;

        int retcode=0;//setjmp( RESTARTENV );		/* ←ディスパッチャ再 */
        if ( retcode != 2 )			/* 強制脱出の検査 */
        {
            for(;;)
            {
                mcode = mp.GetMCodeCurrentIndex();
                if ( (mcode & 0x8000)==0 )
                {
                    /* C#関数 */
                    csFuncs[mcode]();
                }
                else
                {
                    /* Mind単語 */
                    //#define  PUSH_R(addr) *(--RstackPointer)=(ULONG)(addr)
                    RetnStack.Push(mp.GetUl());//現在のMCodeポインタをリターンスタックにプッシュする
                    //SET_MCODE_POINTER_BY_WORDNO( mcode & 0x7fff );
                    //McodePointer.b = (UCHAR *)(WordOffsetTable[wordNo])
                    mp.ResetMcodeIndex((ulong)lp.GetSl((ulong)(mcode & 0x7fff)));
                }
            }
        }
        return;
    }

```


# デバッグ実行の結果
ディスパッチャ内のループのMind単語側のLocテーブルからのMcodeポインタの取得はC版ランタイムと同じ動きをして、無事に2回目のループ先頭に進行し、今度はC＃関数側に同じmcodeの値で進行し、C版ランタイムのC関数配列と同じインデックスのC＃関数配列に進行しました:tada::tada:

これはかなり小さな一歩ですが私の中では無限大に近い大きな一歩です:joy:

進行したのは下記の関数でした。mcode=0x002F
```cs:Mind8Dispatcher.cs

    private static void ZzJmpIndexed(){
             /* Mコード=0x002F */
        //SET_MCODE_POINTER_BY_WORDNO( READ_MCODE );
        //#define  READ_MCODE	    (*McodePointer.w)
        //McodePointer.b = (UCHAR *)(WordOffsetTable[wordNo])
        mp.ResetMcodeIndex((ulong)lp.GetSl((ulong)(mp.GetMCodeCurrentIndex())));   
    }
```

この関数内では下記のCで書かれたマクロが実行されていました。
```cs:
    SET_MCODE_POINTER_BY_WORDNO( READ_MCODE );
```
これは先ほどのディスパッチャ内のMind単語側の分岐で実行したマクロと同じで、引数がREAD_MCODEというマクロで読み込まれるMCode領域の値です。

ここは下記のように定義されているので、ほんとは符号なしShortが正解だったかも。
```cs:
#define  READ_MCODE	    (*McodePointer.w)
```
昨晩はここを当初符号付きShortの読み取りにしていたので、この後のMCodeポインタの指す位置がずれてしまってC版ランタイムと異なる動きとなったのを確認したところで寝落ちしました。現在は符号なしShortなのでC版と同じ動きとなっています。


# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達して、序二段とかなという感じです。まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。

