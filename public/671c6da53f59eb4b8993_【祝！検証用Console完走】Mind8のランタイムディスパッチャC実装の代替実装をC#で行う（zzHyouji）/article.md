# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/40772e39e4b44cd27a22)にてMind開発者の@killyさんより情報共有いただいたMind8のCランタイムディスパッチャ起動検証用Consoleでリビルドした中間コードをリビルドし[前回記事](https://qiita.com/mylifewithviolin/items/7183d7b86b1309a8ef43)ではそちらの中間コードを使ってのC#代替実装をリブートしました。本記事はその続きとなります。

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

C/C++のデバッガはCで実装されているMind8kernelの動作をデバッグ実行で探るために使用します。[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境となります。

# お題のMind8の中間コードファイル
[こちらの記事](https://qiita.com/mylifewithviolin/items/40772e39e4b44cd27a22)をご参照ください。Mind8のCランタイムディスパッチャ起動検証用Consoleでリビルドした中間コードのため、お題の「Hello by mind8」のコンソール出力までのmcode処理ステップ数は649から7までに削減されました:joy:

# お題のC#ソースコード
## Dispatcherクラス（C#関数配列）

### C#の関数配列
今回実装するのは前回記事で未実装であったために落ちていたmcode=0x00C1の「＄＄表示」です。
C版オリジナルではdispword.cに実装されていますので分割クラスファイルのCsFunctionsDispword.csに実装しました。

```cs:CsFunctionsDispword.cs
using System.Text;
namespace Mind8Kernel
{
    public partial class Dispatcher
    {
        /*--------------------- 表示系  --------------------------------*/
        private void ZzHyouji()                	/* ;WORD ＄＄表示 */
        {
                /* Mコード=0x00C1 */
            // ULONG	count;
            // UCHAR  *addr;
            // count = POP_C;
            // addr  = POP_A;
            // #define  POP_U                ((ULONG)(*DstackPointer++))
            // #define  POP_A                ((UCHAR *)(*DstackPointer++))
            // #define  POP_C                POP_U
            // printStrinf( addr, count );
            uint count=dtp.PopUl();
            uint index=dtp.PopUl();
            byte[] chars=mp.GetUb(index,count);
            string text = Encoding.GetEncoding("shift_jis").GetString(chars);
            Console.Write(text);   
    }
}
```
SetupCsFunctions内で.NETCoreでSHIFT-JISエンコードを使うためのおまじない実行を追加しました。
```cs:CsFunctions.cs
using System.Text;
using System.Dynamic;
using System.Runtime.InteropServices;

namespace Mind8Kernel
{
    public partial class Dispatcher
    {
        private readonly int maxCountCsFunctions = 1 + 0x0261;
        /// <summary>C#の関数配列を準備する</summary>
        /// <param name="csFunc">C#関数配列の参照</param>
        private void SetupCsFunctions(ref Action[] csFuncs){
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            csFuncs=new Action[maxCountCsFunctions];
        //～略～
        /*--------------------- 文字列定数  ----------------------------*/
            csFuncs[0x00A4]=ZzSliteralOdd;//
            csFuncs[0x00A5]=ZzSliteralEven;//
        /*--------------------- 文字列情報分解・合成  -------------------*/
            csFuncs[0x00BE]=MojiretuJyouhouBunkai;//
            csFuncs[0x00BF]=MojiretuJyouhouGousei;//
        /*--------------------- 表示系  --------------------------------*/
            csFuncs[0x00C1]=ZzHyouji;//
            
        /*--------------------- ならば～つぎに  -------------------------*/
            csFuncs[0x00EC]=zzif;//
            csFuncs[0x00ED]=zzNotif;//
            //～略～
        }

    }
}
```
今回追加したのはZzHyoujiだけです。

## MCodePointerクラス
Mcode領域アクセスクラスに今回のZzHyoujiの実装のため、指定インデックスで指定バイト数（配列数）のbyte配列を返すメソッドを追加しました。

```cs:MCodePointer.cs
namespace Mind8Kernel
{
    /// <summary>MCode領域アクセスポインタ</summary>
    public class MCodePointer{
        //～略～
        public byte[] GetUb(uint index,uint count){
            byte[] chars = new byte[count];
            for (uint i = 0; i < count; i++) chars[i] = mcodeArray[index + i];
            return chars;
        }        
        //～略～
    }
}
```
前回記事で実装しましたmcode=0x00A5のZzSliteralEvenでは、MCode領域の文字列定数の開始インデックスとバイト数がデータスタックに積まれましたので、mcode=0x00C1のZzHyoujiでは、データスタックからMCode領域の開始インデックスとカウントをポップして、その値からMCode領域から文字列文のbyte配列を取得します。

# デバッグ実行の結果
現状のディスパッチャのmcode到達状況です。
```
   1 8019  32793   1024        0        0        0        0        0        0   1024        0        0
   2 002F     47   1024        0        0        0        0        0        0   1023      114        0
   3 00A5    165   1024        0        0        0        0        0        0   1023      114        0
   4 00C1    193   1022       14        0        0        0        0        0   1023      114        0
$$COLD_FORTH
   5 0020     32   1024        0      132       14        0        0        0   1023      114        0
   6 8029  32809   1024        0      132       14        0        0        0   1024        0      114
   7 00A5    165   1024        0      132       14        0        0        0   1023      116        0
   8 00C1    193   1022       14        0        0        0        0        0   1023      116        0
Hello by mind8   9 0020     32   1024        0      628       14        0        0        0   1023      116        0
  10 801A  32794   1024        0      628       14        0        0        0   1024        0      116
  11 002F     47   1024        0      628       14        0        0        0   1023      118        0
  12 00A5    165   1024        0      628       14        0        0        0   1023      118        0
  13 00C1    193   1022       10        0        0        0        0        0   1023      118        0
実行終り
  14 801B  32795   1024        0      180       10        0        0        0   1023      118        0
  15 002F     47   1024        0      180       10        0        0        0   1022      194        0
  16 00A5    165   1024        0      180       10        0        0        0   1022      194        0
  17 00C1    193   1022       18        0        0        0        0        0   1022      194        0
実行終り時の処理
  18 0020     32   1024        0      154       18        0        0        0   1022      194        0
  19 004D     77   1024        0      154       18        0        0        0   1023      118      194
  20 0014     20   1022        0        0        0        0        0        0   1023      118      194
例外がスローされました: 'Mind8Kernel.Dispatcher.ExitModule' (mind8dispatch.dll の中)
プログラム '[11720] mind8dispatch.dll' がコード 0 (0x0) で終了しました。
```

最後が例外スローされていますが、これはmcode=0014の「プロセス終り０」で意図的にスローさせたアプリケーション例外でした。
```cs:CsFunctionsCompword.cs
        //～略～
        private void ProcessOwari(){ /* ;WORD プロセス終り０ */
                /* Mコード=0x0014 */
            // LONG retCode;
            // retCode = POP_L_OF_Q;
            // exit_program( retCode );

            // #define  POP_L_OF_Q           (DROP_F,POP_L)
            dtp.PopUl();
            int retCode =(int)dtp.PopUl();
            throw new ExitModule(retCode);
        }
        //～略～
```
とりあえず終了動作としては意図したものですので、無事に完走したようでした！:tada::tada:


# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえずディスパッチャ起動検証用Consoleでリビルドした中間コードの完走をめざしましたが、意外とあっさり完走しました。:joy::joy:
まだまだ課題山積ですが、気を良くしたのでとりあえずディスパッチャ（の一部）をCからC#に書き換えてみるという野望の現状認識を「幕下」に昇格としてみます。次回以降でも実際に動く範囲をステップバイステップで広げてまいります。
