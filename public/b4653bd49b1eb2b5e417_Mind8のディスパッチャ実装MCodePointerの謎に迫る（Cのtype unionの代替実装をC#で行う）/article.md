# はじめに
[前回](https://qiita.com/mylifewithviolin/items/2d1e59eb4cdcd03cbed7)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序の口を抜けて、ディスパッチャの基本構造としていま想定しているイメージをソースコードにしてみました。（序二段ともいうらしい。）

とりあえず関数配列のようなものができるということでC#イケるかもと踏んでいたのですが、踏み込んでみますとかなりC言語の実装に密着していることがジョジョに判明してきており、課題山積という状況ではあります。longJmpとかどうしようかなと悩みつつ、それよりもっと手前のtype unionの代替実装を引き続き行ってみます。

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

## class McodePointer　MCodeポインタ
前々回の記事のMCodeポインタの実装は、Cのtype unionの代替をC#で実装するとしたらこんな感じのコンセプトコードにしかすぎず、実際のC#の実装で読み込んだMCode領域のアクセスとは直接的には関係のないコードサンプルでした。今回は少し踏み込んで、Byte配列で読み込んでいるMCode領域にアクセスするクラスのメンバ関数を実装してみます。

```cs:Mind8Dispatcher.cs
    private class MCodePointer{
        private ulong mcodeIndex;
        private byte[] mcodeArray =[];
        public void SetupMcodeArray(ref byte[] McodeBase){
            mcodeArray=McodeBase;
        }
        public void ResetMcodeIndex(ulong index){
            mcodeIndex=index;;
        }
        public ushort GetMCodeCurrentIndex(){/* for signed short access  */
            byte[] int16Byte = new byte[2];
            for (ulong i = 0; i < 2; i++) int16Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=2;
            return BitConverter.ToUInt16(int16Byte, 0);
        }
        public int GetSl(){/* for signed long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=4;
            return BitConverter.ToInt32(int32Byte, 0);
        }
        public uint GetUl(){/* for unsigned long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=4;
            return BitConverter.ToUInt32(int32Byte, 0);
        }
        public long GetSll(){/* for signed long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=8;
            return BitConverter.ToInt64(int64Byte, 0);
        }
        public ulong GetUll(){/* for unsigned long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=8;
            return BitConverter.ToUInt64(int64Byte, 0);
        }
    }

```
Byte配列から指定の型（サイズ）で値を取得して、ポインタもサイズ分移動しておくようなつくりです。

とりあえず符号無しの16bit、符号有り無しの32bit、64bitの整数型で値を取得するメソッドを用意しています。符号無しの16bitの値取得はMCode所得と特別な関数名にしています。
また、Byte配列状態のMCode領域の配列インデックスを別途内部変数として保持しています。このインデックスの（リ）セット関数を用意しました。

## Main 暫定メイン
暫定メインも少し書き換わっています。従来のGeneralPointerのAccessPointerは現状未使用です。

```cs:Mind8Dispatcher.cs
    private static Stack<ulong> DataStack = new();
    private static Stack<ulong> RetnStack = new();
    private static  byte[] McodeBase =[];//MCode領域
    private static byte[] WordOffsetTable=[];//LOCテーブル
    private static byte[] DataBase =[];//データ領域
    private static MCodePointer mp=new();
    private static GeneralPointer AccessPointer =new(); /* メモリアクセス用ポインタ */

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
        mp.SetupMcodeArray(ref McodeBase);
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

下記のあたりで今回のMCodePointerを初期化しています。実は詳しくは理由を認識していないのですが、Mind開発者@killyさんの教えに従ってMCode領域の実行開始位置を0x0070オフセットとっています。Byte配列のインデックスが相対アドレスポインタ変数のような状態となっています。

```cs:Mind8Dispatcher.cs
        mp =new();
        mp.SetupMcodeArray(ref McodeBase);
        //McodePointer.b = (UCHAR *)McodeBase + 0x70;	/* 0x70=実行開始地点 */
        mp.ResetMcodeIndex(0x70);
```

## Dispatcher ディスパッチャ
MCode領域やその他のデータ領域をクラスのスタティックメンバにしたので、関数の引数からはなくしております。

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
                    //McodePointer.b = (UCHAR *)(WordOffsetTable[wordNo])
                    mp.ResetMcodeIndex(WordOffsetTable[mcode & 0x7fff]);

                }
            }
        }
        return;
    }
```

Mind単語側のMCodeポインタの扱い方はまだ確立しておらず、仮のコード状態です。
また、冒頭でも触れましたがsetJmp/longJmpの代替も未実装です。したがって現状無限ループです。（C#関数配列のデリゲートが未設定のインデックスにMCodeがはまって落ちる感じ）

## SetupCsFunctions C#の関数配列を準備する
C#関数側も関数配列の状態はまだほぼほぼダミー状態ですが、雰囲気はリアルっぽくしてきています。
MCodeインデックスが適合しているダミー関数配列内に進行することは確認済です。

```cs:Mind8Dispatcher.cs
    /// <summary>C#の関数配列を準備する</summary>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void SetupCsFunctions(ref Action[] csFuncs){
        csFuncs=new Action[maxCountCsFunctions];
        csFuncs[0x0010]=ZzEndExecute;
        csFuncs[0x0011]=Jikkou;
        csFuncs[0x0012]=Musyori;
        csFuncs[0x0013]=EmgcyExit;
        csFuncs[0x0014]=ProcessOwari;
        csFuncs[0x0015]=StackKensa0;
        csFuncs[0x0016]=StackReset;
        csFuncs[0x0017]=FinishDispatcher;
        csFuncs[0x0018]=C_stack_data_no;
        csFuncs[0x0019]=ZzReserve1L;
        csFuncs[0x001A]=ZzReserve2L;
        csFuncs[0x001B]=ZzReserve3L;
        csFuncs[0x001C]=ZzReserve4L;
        csFuncs[0x001D]=ZzReserve5L;
        csFuncs[0x001E]=ZzReserve6L; 
        csFuncs[0x001F]=ZzReserve; 

        csFuncs[0x0020]=ZzExit1L;
        csFuncs[0x0021]=ZzExit2L;
        csFuncs[0x0022]=ZzExit3L;
        csFuncs[0x0023]=ZzExit4L;
        csFuncs[0x0024]=ZzExit5L;
        csFuncs[0x0025]=ZzExit6L;
        csFuncs[0x0026]=ZzExit7L;
        csFuncs[0x0027]=ZzExit;
        csFuncs[0x0028]=ZzIfExit;
        csFuncs[0x0029]=ZzIf0Exit;
        csFuncs[0x002A]=ZzIf1Exit;
        csFuncs[0x002B]=ZzNotIfExit;
        csFuncs[0x002C]=ZzNotIf0Exit;
        csFuncs[0x002D]=ZzNotIf1Exit;
        csFuncs[0x002E]=ZzJmpRelative; 
        csFuncs[0x002F]=ZzJmpIndexed; 
        //～略～
    }
        
    private static void ZzEndExecute(){  /* ;WORD $$END_EXECUTE */
            /* Mコード=0x0010 */
    }
    private static void Jikkou(){       /* ;WORD 実行 */
            /* Mコード=0x0011 */
    }
    private static void Musyori(){      /* ;WORD 無処理 */
            /* Mコード=0x0012 */
    }
    private static void EmgcyExit(){
            /* Mコード=0x0013 */
    }
    private static void ProcessOwari(){
            /* Mコード=0x0014 */
    }
    //～略～
```
# デバッグ実行の様子
お題のMCodeファイルは実行開始位置0x0070から8Byteは下記のようなMCodeが格納されていることがわかっていて
```
16進　10進
8019 32793
828D 33421
801A 32794
0020 32
```
この範囲のMCodeのディスパッチャの読み取りはC版と同じような動きをしています。

ただし、C#版のWordOffsetTableは1Byteづつの配列となっているためC版とは下記のコードの動きがまだ異なっている可能性があります。
ですので、このコードを１回抜けた後の動きがまだC版とは異なっていると思われます。
```
        //McodePointer.b = (UCHAR *)(WordOffsetTable[wordNo])
        mp.ResetMcodeIndex(WordOffsetTable[mcode & 0x7fff]);
```

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達して、序の口は抜けたかなという感じです。まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。



