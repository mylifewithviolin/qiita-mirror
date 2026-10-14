# はじめに
[前回](https://qiita.com/mylifewithviolin/items/96f4ba79c5734f017c87)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序の口として、Mind8の中間コードファイル内のMCode情報構造体をC#で読み込んでみましたので、今回はMCode領域とLocation表を読み込みます。

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
本記事のテーマとなっているMind8の中間コードファイルは下記のファイルです。
```
c:\developments\vscode\mind8dispatch>dir hello.mco

2024/04/18  20:53            43,544 hello.mco
               1 個のファイル              43,544 バイト
```
詳しくは[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)をご参照ください。

# お題のC#ソースコード
今回のC#ソースコードの主な内容は下記のとおりです。
## SetupForDispatch ディスパッチャを準備する
前回はMainに直接書いていましたが、今回よりこの関数内に移設しました。

ファイル名は引き続きリテラルコーディングの手抜きですが、ディスパッチャの準備処理を関数化したんで、その関数への引数にはなっています。
```cs:Mind8Dispatcher.cs

    /// <summary>ディスパッチャを準備する</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
    /// <param name="McodeBase">MCode領域の参照</param>
    /// <param name="WordOffsetTable">LOCテーブルの参照</param>
    /// <param name="DataBase">データ領域の参照</param>
    /// <param name="mcodefilename">MCode中間コードファイル名</param>
    private static bool SetupForDispatch(
        ref McodeInfoStruct McodeInfo,
        ref byte[] McodeBase,ref byte[] WordOffsetTable,ref byte[] DataBase,
        String mcodefilename){

        using FileStream fs = new(mcodefilename, FileMode.Open);
        fs.Seek(0-sizeOfMcodoInfo, SeekOrigin.End);
        byte[] mcodeInf = new byte[sizeOfMcodoInfo];
        int ret=fs.Read(mcodeInf, 0, sizeOfMcodoInfo);
        if(ret < sizeOfMcodoInfo){
            Console.WriteLine("Can't read Mcode-info({0}).", ret);
            return false;
        }

        SetMcodeInfo(ref McodeInfo,mcodeInf);
        MonitorMcodeInfo(ref McodeInfo);
        if ( McodeInfo.minfoMark1 != 'M' || McodeInfo.minfoMark2 != 'C' )
        {
            Console.WriteLine("Illegal Mcode mark" );
            return false;
        }
       	if ( McodeInfo.minfoMainExist == 0 )
        {
            Console.WriteLine("kermain: MAIN is not defined" );
            return false;
        }
        //その他のmcodeInfoチェック当面割愛
        //checkNeedToBeSwapped();関連の処理は当面割愛
        fs.Seek(0, SeekOrigin.Begin);//rewindMcodeFileと同等
        //readMcode;
        uint size = McodeInfo.minfoMcodeSize;
        McodeBase = new byte[size];
        ret=fs.Read(McodeBase, 0, (int)size);//符号無サイズ読み取り不足の可能性あり
        if(ret<size){
            Console.WriteLine("kermain: Can't read M-code({0})", ret);
	       return false;
        }

        //readLoctable;
        size = McodeInfo.minfoLoctableSize;
        WordOffsetTable= new byte[size];
        ret=fs.Read(WordOffsetTable, 0, (int)size);//符号無サイズ読み取り不足の可能性あり
        if(ret<size){
            Console.WriteLine("kermain: Can't read Loc-table({0})", ret);
	       return false;
        }
        //adjustLoctable();
        //McodeBaseはバイト配列なのでこの処理成立しない
        // uint entryNo = McodeInfo.minfoLoctableSize / 4;
    	// for(int index=0; index<entryNo; index++ )
        // {
        //     WordOffsetTable[index] += (uint)McodeBase;
        // }
        //reserveDataArea();
        uint DataSize = McodeInfo.minfoDataSize;
        DataBase= new byte[DataSize];//データ領域をByte配列で確保
        //reserveStackArea();
       	/* スタックサイズの確定 */
        //ushort DataStackSize = (ushort)McodeInfo.minfoDstackSize;
        //ushort RetnStackSize = (ushort)McodeInfo.minfoRstackSize;
        //C#のStack<T>で実装
        return true;
    }
```
MCode情報構造体の読み込みの後、前回記事より若干構造体メンバ変数のチェック処理をオリジナルから一部移植してあります。

MCode領域、Locテーブルともにbyte配列で読み込んでいます。後で試行錯誤して修正する余地はあるのですが、とりあえずこの状態で読み込んでいます。

オリジナルのMind8カーネルにセットアップ処理では、checkNeedToBeSwapped();という関数の戻り値での分岐処理が実装されているのですが、今回の環境ではこの関連の処理はfalse判定されていますので、実装を割愛しています。

他にもいちおうオリジナルの処理と等価な実装を書いてコメントアウトしています。オリジナルのMind8カーネルのメモリアロケートしてアドレスポインタで操作するという実装ではなくなるため、そのままでは実装できないためです。

## Main 暫定メイン
MCode領域とLocation表を読み込んだ後の処理については、まだ正常動作していませんが、ビルドエラーがない程度にざっと書いてあります。本記事では長くなりますので、次回記事で構想を説明いたします。

```cs:Mind8Dispatcher.cs
    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        String mcodefilename="hello.mco";
        McodeInfoStruct mcodeInfo =new();
        byte[] McodeBase =[];//MCode領域
        byte[] WordOffsetTable=[];//LOCテーブル
        byte[] DataBase =[];//データ領域
        /* ディスパッチャを準備する */
        bool ret=SetupForDispatch(ref mcodeInfo,
                    ref McodeBase,ref WordOffsetTable,ref DataBase,mcodefilename);
        if(!ret){
            return;
        }
        //resetDataStackPointer();	
        //resetRetnStackPointer();
        Stack<ulong> DataStack = new();
        Stack<ulong> RetnStack = new();
        GeneralPointer McodePointer =new();
        //McodePointer.b = (UCHAR *)McodeBase + 0x70;	/* 0x70=実行開始地点 */
        /* C#の関数を準備する */
        Action[] csFuncs=[]; //C#の関数を格納する配列
        /*C#の関数配列を準備する */
        SetupCsFunctions(ref csFuncs);
        /* ディスパッチャ開始 */
        Dispatcher(ref mcodeInfo,
                    ref McodeBase,ref WordOffsetTable,ref DataBase,
                    ref DataStack,ref RetnStack,ref McodePointer,ref csFuncs);

    }
```
詳しくは次回記事で説明しますが、下記の点だけ説明しておきます。スタック操作はC#のStack<T>を使う構想で、スタックの型はとりあえず符号なし64bit整数を想定しています。ただし、これはデバッグしていくうちに変更するかもしれません。
```cs:Mind8Dispatcher.cs
        Stack<ulong> DataStack = new();
        Stack<ulong> RetnStack = new();
        GeneralPointer McodePointer =new();
```

## McodePointer　MCodeポインタ
オリジナルのMind8カーネルではMcodePointerはC言語の共用体のアドレスポインタで実装されていますが、本試作では下記のようなクラスで代替しようと考えています。
これもデバッグ時にキャストなどが追加される可能性があります。いまはざっと自分のイメージをソースコードにしているだけです。
```cs:Mind8Dispatcher.cs
    private class GeneralPointer{
   
        private ulong union;
        public void SetUb(ulong b){    /* for unsigned byte access */
            union =b;
        }
        public ulong GetUb(){    /* for unsigned byte access */
           return union;
        }
        public void SetUw(ulong w){  /* for unsigned word access */
        union =w;
        }
        public ulong GetUw(){  /* for unsigned word access */
           return union;
        } 
        public void SetSs(ulong s){ /* for signed short access  */
            union =s;
        }
        public ulong GetSs(){ /* for signed short access  */
           return union;
        } 
        
        public void SetSl(ulong l){ /* for signed long access   */
            union =l;
        }
        public ulong GetSl(){/* for signed long access   */
           return union;
        } 
        
        public void SetUl(ulong u){ /* for unsigned long access */
            union =u;
        }
        public ulong GetUl(){ /* for unsigned long access */
           return union;
        } 
        public void SetSq(ulong q){ /* for quad word accrss     */
            union =q;
        }
        public ulong GetSq(){ /* for quad word accrss     */
           return union;
        } 
        public void SetSll(ulong ll){ /* for long long access */
            union =ll;
        }
        public ulong GetSll(){ /* for long long access */
           return union;
        } 
        public void SetSf(ulong f){ /* for fraction access      */
            union =f;
        }
        public ulong GetSf(){ /* for fraction access      */
           return union;
        }       
    }
```
クラス内に共通変数を設けてgetter/setter風の関数を介して操作するという想定です。スタックにいろいろな型のデータがのるということからgetter/setter風の関数の引数型を個々の変数型にしてキャストしながら入出力することになりそうですが、この記事でのソースコードではまだそのあたり未記述です。

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達しました。次回はディスパッチャ本体の構想段階のソースコードを検討します。（まだ動きません。現状は中間コードファイルの中身を３つの領域でbyte配列の読み込むところまでが動作している範囲です。）

