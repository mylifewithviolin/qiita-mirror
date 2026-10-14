# はじめに
[前回](https://qiita.com/mylifewithviolin/items/922d72d13716bfae0d49)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序二段のあたりとして、Mind8のLocation表、通称Locテーブルのアドレスポインタを実装しました。
これにより、ディスパッチャループ内のMind単語側が動作するようになってループが一巡するようになりましたので、今回はデータ領域のAccessポインタを実装します。


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

## class AccessePointer　データ領域Accesseポインタ
MCode領域と同じくByte配列で獲得したデータ領域にアクセスするクラスとメンバ関数を実装してみます。C版オリジナルランタイムではCのtype unionのアドレスポインタ共用体で実装されているところで、MCodeポインタとAccessポインタは同じ共用体型で宣言されています。

C#版ではByte配列のインデックスのSet関数と、Byte配列の変数型に応じたサイズの配列を変数型にキャストして入出力する関数から実装します。Mcodeポインタとしては先行して参照系のみで別に実装していますが、本記事ではそちらに更新系を追記して同じ型とすることはまだしておりません。

後の構成の再整理の際に、MCodeポインタの実装範囲（参照系の関数）のクラスをAccessポインタのクラス（更新系の関数のみにして）が継承するように調整する可能性が高いです。

```cs:Mind8Dispatcher.cs
private class AccessPointer{
        private ulong dataIndex;
        private byte[] dataArray =[];
        public void SetupDataArray(ref byte[] DataBase){
            dataArray=DataBase;
        }
        public void ResetdataIndex(ulong index){
            dataIndex=index;;
        }
        public byte GetUb(){    /* for unsigned byte access */
            dataIndex +=1;
            return dataArray[dataIndex];
        }
        public void SetUb(byte b){    /* for unsigned byte access */
            dataArray[dataIndex] =b;
        }
        public ushort GetUs(){/* for unsigned short access  */
            byte[] int16Byte = new byte[2];
            for (ulong i = 0; i < 2; i++) int16Byte[i] = dataArray[dataIndex + i];
            dataIndex +=2;
            return BitConverter.ToUInt16(int16Byte, 0);
        }
         public void SetUs(ushort us){/* for unsigned short access  */
            byte[] int16Byte =BitConverter.GetBytes(us);
            for (ulong i = 0; i < 2; i++) dataArray[dataIndex + i]=int16Byte[i];
         }
        public short GetSs(){/* for signed short access  */
            byte[] int16Byte = new byte[2];
            for (ulong i = 0; i < 2; i++) int16Byte[i] = dataArray[dataIndex + i];
            dataIndex +=2;
            return BitConverter.ToInt16(int16Byte, 0);
        }
        public void SetSs(short ss){/* for signed short access  */
            byte[] int16Byte =BitConverter.GetBytes(ss);
            for (ulong i = 0; i < 2; i++) dataArray[dataIndex + i]=int16Byte[i];
         }
        public int GetSl(){/* for signed long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[dataIndex + i];
            dataIndex +=4;
            return BitConverter.ToInt32(int32Byte, 0);
        }
        public void SetSl(int sl){/* for signed long access  */
            byte[] int32Byte =BitConverter.GetBytes(sl);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i]=int32Byte[i];
        }
        public uint GetUl(){/* for unsigned long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[dataIndex + i];
            dataIndex +=4;
            return BitConverter.ToUInt32(int32Byte, 0);
        }
        public void Setul(uint ul){/* for unsigned long access  */
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i]=int32Byte[i];
        }
        public long GetSll(){/* for signed long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = dataArray[dataIndex + i];
            dataIndex +=8;
            return BitConverter.ToInt64(int64Byte, 0);
        }
        public void SetSll(long sll){/* for signed long access  */
            byte[] int64Byte =BitConverter.GetBytes(sll);
            for (ulong i = 0; i < 8; i++) dataArray[dataIndex + i]=int64Byte[i];
        }
        public ulong GetUll(){/* for signed long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = dataArray[dataIndex + i];
            dataIndex +=8;
            return BitConverter.ToUInt64(int64Byte, 0);
        }
        public void SetUll(ulong ull){/* for unsigned long access  */
            byte[] int64Byte =BitConverter.GetBytes(ull);
            for (ulong i = 0; i < 8; i++) dataArray[dataIndex + i]=int64Byte[i];
        }
    }
```


## Main 暫定メイン
暫定メインがまた少し書き換わります。前回までのMCodeポインタの初期化、Locテーブルポインタの初期化に加えて、Accessポインタの初期化が加わります。従来のGeneralPointer（コンセプトコード状態）のAccessPointerは削除されました。

本記事ではとりあえずMCodeポインタは参照系の一部、Accessポインタは参照系更新系両方、別々に定義しています。（当初は同じクラスにする想定でしたのでMCodeポインタの実装のByte配列渡すヶ所にもrefをつけてましたが今回やめました。）

```cs:Mind8Dispatcher.cs
    private static Stack<ulong> DataStack = new();//データスタック
    private static Stack<ulong> RetnStack = new();//リターンスタック
    private static  byte[] McodeBase =[];//MCode領域
    private static byte[] WordOffsetTable=[];//LOCテーブル
    private static byte[] DataBase =[];//データ領域
    private static MCodePointer mp=new();//MCode領域用ポインタ
    private static LocTablePointer lp=new();//LOCテーブル用ポインタ
    private static AccessPointer ap =new(); //データ領域用ポインタ

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
        ap=new();
        mp.SetupMcodeArray(McodeBase);
        lp.SetupLocArray(WordOffsetTable);
        ap.SetupDataArray(ref DataBase);
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
ディスパッチャの実装は前回記事より変更ありません。[前回記事](https://qiita.com/mylifewithviolin/items/922d72d13716bfae0d49)をご参照ください。

ディスパッチャループが回るようになってくると、C版オリジナルではCの広域ジャンプで実装されているループ打ち切りの代替実装をどうするかが課題になってまいりますが、本記事ではまだ取り扱いません。

## SetupCsFunctions C#の関数配列を準備する
おなじく、ディスパッチャループが回ってくると、最終的にはこの関数配列に対応する関数（Mind8がもともと持っている機能関数）をどの程度実装していくかが長期課題になっていきます。当面はお題の中間コードが実行する順に実装してきます。

お題の中間コードで前回実装関数の次に実行されたのが下記のmcodeの２関数で、最初にAccessポインタが引用されました。
mcode=0x0036
mcode=0x0080
今回はこのmcodeに対応する２関数を実装して関数配列にセットします。
```cs:Mind8Dispatcher.cs
    /// <summary>C#の関数配列を準備する</summary>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void SetupCsFunctions(ref Action[] csFuncs){
        csFuncs=new Action[maxCountCsFunctions];
        csFuncs[0x0010]=ZzEndExecute;
        csFuncs[0x0011]=Jikkou;
        //～略～  
        csFuncs[0x002F]=ZzJmpIndexed; 
        //～略～
        csFuncs[0x0036]=ZzPointVarAddr;
        //～略～  
        csFuncs[0x0080]=ZzSetWvar;
        //～略～       
    }

    private static void ZzPointVarAddr(){   /* ;WORD $$POINT_VARADDR */
            /* Mコード=0x0036 */
            //AccessPointer.b = DataBase + FETCH_MCODE_LONG;
            //#define  FETCH_MCODE_LONG   (*McodePointer.l++)
            ap.ResetdataIndex(mp.GetUl());
    }
    
    private static void ZzSetWvar(){       /* ;WORD $$SET_WVAR */
            /* Mコード=0x0080 */
            //*AccessPointer.w = 1;
            //USHORT* w;      /* for unsigned word access */
            ap.SetUs(1);
    }
```

# デバッグ実行の様子
下図はオリジナルC版のディスパッチャがmcode=0x0036の関数でデータ領域のアドレスポインタをカレントのmcodeが示すmcode領域のロケーション相対アドレスをデータ領域の絶対番地にオフセット値として加算してセットして、mcode=0x0080の関数でその絶対アドレスから2byteに１を書き込んだところのデバッガの様子です。

![dispatch1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/864d50a4-be41-51a2-acc4-52865f0744d4.png)

下図はC#版のディスパッチャがmcode=0x0036の関数でデータ領域のアドレスポインタ(byte配列のインデックス)をカレントのmcodeが返すmcode領域のロケール相対アドレスをセットして、mcode=0x0080の関数でそのインデックスからの2byteに１を書き込んだところのデバッガの様子です。

![dispatch2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6cafa7f1-2e56-ab33-3c3c-a4739f3e6d2a.png)

Cのtype unionでメモリアドレスポインタが実装されている箇所をC#の代替実装
としてはbyte配列で実装した点について、だいぶ遅くなることは覚悟していたのですが、ロジック的にはメモリの絶対アドレスからはフリーになるので、Mind中間コード上のメモリロケーションとは相性がよいような気もしてきました。:grin:

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達して、序二段とかなという感じです。まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。

## 補足

[前回記事](https://qiita.com/mylifewithviolin/items/922d72d13716bfae0d49)へのMind開発者@killyさんのコメントで気になっていた点が解明しましたので次回訂正します。今回の実行範囲はアクセスポインタの参照後の２巡目がないので問題は潜在的な状態にとどまっています。
