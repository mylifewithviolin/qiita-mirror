# はじめに
[実質的な前回記事](https://qiita.com/mylifewithviolin/items/37d0af60ef8dc0b8a8a1)「Mind8のランタイムディスパッチャC実装の代替実装をC#で行う（zzNotif）」へMind開発者の@killyさんより重要な情報共有がございまして、[こちらの記事](https://qiita.com/mylifewithviolin/items/40772e39e4b44cd27a22)にてMind8のCランタイムディスパッチャ起動検証用Consoleでリビルドした中間コードをリビルドしました。本記事ではそちらの中間コードを使ってのC#代替実装リブートとなります。

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
[こちらの記事](https://qiita.com/mylifewithviolin/items/40772e39e4b44cd27a22)をご参照ください。Mind8のCランタイムディスパッチャ起動検証用Consoleでリビルドした中間コードのため、お題の「Hello by mind8」のコンソール出力までのmcode処理ステップ数は649から7までに削減されました:joy:

# お題のC#ソースコード
## Mind8Dispatcherクラス Main 暫定メイン
コンソールアプリのホストクラスのMainです。まだ引数からのファイル名には非対応です。このためディスパッチャ起動検証用Consoleでリビルドした中間コードのファイル名に書き換えます:sweat_smile:

```cs:Mind8Dispatch.cs
namespace Mind8Kernel
{
    /// <summary>Mind8ディスパッチャ</summary>
    public partial class Mind8Dispatcher
    {
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static int Main(string[] args)
        {
            string mcodefilename="hellodummy.mco";
            Dispatcher dispatcher =new();
            return dispatcher.Main(mcodefilename);
    
        }       
    }
}
```
## Dispatcherクラス（C#関数配列）
### C#の関数配列
Mindランタイムのスタートアップの初期化処理が大幅にバイパスされたため、文字列定数関連の関数がほぼいきなり呼ばれました。今回、実際に突入するのは下のZzSliteralEven()の方です。
```cs:CsFunctionsCompword.cs
namespace Mind8Kernel
{
    public partial class Dispatcher
    {

        /*--------------------- 文字列定数  ----------------------------*/
        private void ZzSliteralOdd(){       /* ;WORD $$SLITERAL_ODD */
                /* Mコード=0x00A4 */
            // tMcode  length = FETCH_MCODE;
            // PUSH_A( McodePointer.b );                       /* push address */
            // PUSH_C( length );                               /* push length  */
            // SKIP_MCODE( length + 1 );
            ushort length=mp.FetchMcode();
            dtp.PushUl(mp.GetMcodeIndex());
            dtp.PushUl(length);
            mp.MoveMcodeIndexByByte(length + 1);
        }
        private void ZzSliteralEven(){      /* ;WORD $$SLITERAL_EVEN */
                /* Mコード=0x00A5 */
            // tMcode length = FETCH_MCODE;
            // PUSH_A( McodePointer.b );                       /* push address */
            // PUSH_C( length );                               /* push length  */
            // SKIP_MCODE( length );
            ushort length=mp.FetchMcode();
            dtp.PushUl(mp.GetMcodeIndex());
            dtp.PushUl(length);
            mp.MoveMcodeIndexByByte(length);
        }
    }
}
```

## MCodePointerクラス
Mcode領域アクセスクラスです。Cのマクロに対応して少しメソッドを書き足しています。MoveMcodeIndexByByteとか、けっこう重要な操作でした。前回記事でのMoveMcodeIndexと同時に実装していました。

```cs:MCodePointer.cs   
namespace Mind8Kernel
{
    /// <summary>MCode領域アクセスポインタ</summary>
    public class MCodePointer{
        private readonly uint mcodeSize=2;
        private uint mcodeIndex;
        private byte[] mcodeArray =[];
        public void SetupMcodeArray(byte[] McodeBase){
            mcodeArray=McodeBase;
        }
        public void ResetMcodeIndex(uint index){
            mcodeIndex=index;
        }
        public void MoveMcodeIndexByByte(int point){
            mcodeIndex=(uint)(mcodeIndex + point);//byte配列インデックス単位で移動
        }
        public void MoveMcodeIndex(int point){
            mcodeIndex=(uint)(mcodeIndex + point*mcodeSize);//byte配列インデックス=アドレスポインタ変数の値*2
        }
        public uint GetMcodeIndex(){
            return mcodeIndex;
        }
        public ushort ReadMcode(){
            byte[] int16Byte = new byte[mcodeSize];
            for (ulong i = 0; i < mcodeSize; i++) int16Byte[i] = mcodeArray[mcodeIndex + i];
            return BitConverter.ToUInt16(int16Byte, 0);
        }
         public short ReadMcodeShort(){
            byte[] int16Byte = new byte[mcodeSize];
            for (ulong i = 0; i < mcodeSize; i++) int16Byte[i] = mcodeArray[mcodeIndex + i];
            return BitConverter.ToInt16(int16Byte, 0);
        }       
        public ushort FetchMcode(){
            byte[] int16Byte = new byte[mcodeSize];
            for (ulong i = 0; i < mcodeSize; i++) int16Byte[i] = mcodeArray[mcodeIndex + i];
            mcodeIndex +=2;
            return BitConverter.ToUInt16(int16Byte, 0);
        }

        //～略～
    }
}        

```
# デバッグ実行の結果
現状のディスパッチャのmcode到達状況です。00A5=zzSliteralEvenは正常通過して、次のmcodeの00C1が未実装のため関数配列のNull参照例外で落ちています。

```
   1 8019  32793   1024        0        0        0        0        0        0   1024        0        0
   2 002F     47   1024        0        0        0        0        0        0   1023      114        0
   3 00A5    165   1024        0        0        0        0        0        0   1023      114        0
   4 00C1    193   1022       14        0        0        0        0        0   1023      114        0
   例外がスローされました: 'System.NullReferenceException' (mind8dispatch.dll の中)
```
左端から1列目がディスパッチャが処理したステップ数、2列目が16進数表記のmcode、3列目が10進数表記のmcode、4列目がデータスタックのbyte配列インデックス値などとなっています。

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえずディスパッチャ起動検証用Consoleでリビルドした中間コードの完走をめざします。まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。
