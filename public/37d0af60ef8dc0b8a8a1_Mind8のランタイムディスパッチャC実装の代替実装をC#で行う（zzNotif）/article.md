# はじめに
[前回](https://qiita.com/mylifewithviolin/items/818de8aca51f6750da6c)はMind8のランタイムの中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の現状認識を「三段目」とかってに判定して、構想段階のクラス図なんかをまとめてみました。（この番付の判定はてきとうです:joy:）

その後、お題の中間コードをディスパッチャが処理するステップ数をより一層進行させようと、基本的にはC版オリジナルのディスパッチャが処理するC定義単語の関数配列のC#代替実装の範囲を地道に広げていくという工程に入っております。

この個々の配列関数の定義内容がほんとうに妥当かということがステップ数の進行状況に影響を与えるようになってきており、ざっと仮実装しているようなところでオリジナルの動作と非互換な場合はその後に処理するMCodeへのジャンプ先が微妙に異なってしまうというような問題も起きています。

（この非互換は次のステップですぐに起きるというわけではなく、間に他のスタック操作を挟んだのちに発現するので特定の難度がやや高いという状況です。）

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
また、[前回記事](https://qiita.com/mylifewithviolin/items/c24cac3a0788cc2ad6f5)に実際のMCode領域内のMCodeをC版オリジナルがディスパッチしたリストを確認しています。お題の「Hello by mind8」のコンソール出力までは649（同一コード含む）のmcodeを処理します。

# とりあえずどんな状況か
前回記事は37ステップ目で未実装関数の出現でとまっていましたが、現状は下記のとおりです。
```
SqNo mcode mcode(dec)
   1 8019  32793  //2024/04/23
   2 002F     47  //2024/04/25
   3 0036     54
   4 0080    128  //2024/04/27
   5 0036     54
   6 0070    112
   7 803A  32826
   8 002F     47
   9 813E  33086
  10 0012     18
  11 0036     54
  12 0071    113
  13 8046  32838
  14 8045  32837
  15 0012     18
  16 0036     54
  17 0074    116
  18 0020     32
  19 0020     32
  20 80BA  32954
  21 0036     54
  22 0012     18
  23 016E    366
  24 0020     32
  25 80A6  32934
  26 0097    151
  27 0065    101
  28 0020     32
  29 80D7  32983
  30 0261    609
  31 8053  32851
  32 8052  32850
  33 001A     26
  34 006B    107  //2024/04/29
  35 0055     85
  36 008F    143
  37 00ED    237  //2024/05/03
　38 0055     85
  39 0012     18
  40 00A2    162
  41 00BF    191
  42 0095    149
  43 01D7    471
  44 006B    107
  45 0055     85
  46 00ED    237
  47 0055     85
  48 0055     85
  49 0103    259
  50 00BF    191
  51 0055     85
  52 0055     85
  53 0107    263
  54 0022     34  //2024/05/06
```
実際にはもう少しループしていますが、55ステップ以降のmcodeはC版オリジナルとは異なる値を読み込んでおり、64ステップまでループした後、未実装コードで例外により停止しています。

# お題のC#ソースコードのクラス構成
クラス構成に変更はないのですが、C#デリゲートによる関数配列の数が増えてきましたので、ソースコード内を縦スクロールするのがちょっとつらくなってきましたので、オリジナルとにた感じで分割しました。
## クラスの説明と対応ソースファイル構成
| クラス名 | 概要 | 対応ソースファイル |
|:-|:-|:-|
|Mind8Dispatcher|Windowsコンソールアプリのホストクラス|Mind8Dispatch.cs|
|Dispatcher|ディスパッチャ本体クラス|Dispatcher.cs|
||C#関数配列（配列初期化）|CsFunctions.cs|
||同実際の定義部分|CsFunctionsCompword.cs|
||同実際の定義部分|CsFunctions0ker.cs|
||同実際の定義部分|CsFunctions1ker.cs|
||同実際の定義部分|CsFunctions2ker2.cs|
||同実際の定義部分|CsFunctions3ker.cs|
||同実際の定義部分|CsFunctionsBunki.cs|
|McodeInfoStruct|Mcode情報構造体|Dispatcher.cs|
|LongJmp|広域ジャンプ用のアプリケーション例外|Dispatcher.cs|
|MCodePointer|Mcode領域アクセスクラス|MCodePointer.cs|
|LocTablePointer|Locテーブルアクセスクラス|LocTablePointer.cs|
|AccessPointer|データ領域アクセスクラス|AccessPointer.cs|
|StackPointer|スタッククラス|StackPointer.cs|

C関数配列の数は膨大で、オリジナルの実装数に対して数的にまともに実装してあるのはCsFunctionsCompword.csくらいで、内容的にはまだ妥当性不明状態のものが多数あります。その他の配列関数ファイルはお題の中間コード処理で出現したものから優先的に実装していますが、仮実装にとどもっているものを含みます。

# お題のC#ソースコード
## StackPointerクラス
スタックアクセスクラスです。前回記事でインデックスのPOP/PUSHの際の増減方向を変更してMind互換に変更しましたが、デバッガの配列の展開順が昇順なので末尾のインデックスから使用して逆順に成長させるとデバッグが若干しずらいため、配列のインデックス変数とは別にポインタ変数を導入してこちらはMind互換（最大値が初期値でPUSHすると減っていくPOPすると減っていく（最大値に近づく））として、Byte配列のインデックスは0から使用するに換算を挟みました。

```cs:StackPointer.cs
namespace Mind8Kernel
{ 
 /// <summary>スタックポインタ</summary>
    public class StackPointer{
        private readonly uint stackSize=4;
        private uint stackMaxSize;
        private uint stackIndex;
        private uint stackPointer;
        public byte[] dataArray =[];
        public void SetupStackArray(uint size){
            stackMaxSize=size;
            dataArray =new byte[stackMaxSize];
            stackPointer=stackMaxSize/stackSize;//stackPointerは1024が初期値
            stackIndex=0;//stackIndexは0が初期値
        }        
        public void ResetStackPointer(uint point){
            stackPointer=point;
            stackIndex=(stackMaxSize/stackSize-point)*stackSize;//byte配列インデックス=アドレスポインタ変数の値*4
        }
        public void MoveStackPointer(int point){
            stackPointer=(uint)(stackPointer+point);
            stackIndex=(uint)(stackIndex + point*stackSize);//byte配列インデックス=アドレスポインタ変数の値*4
        }
        public uint GetCurrentStackPointer(){
            return stackPointer;
        }
        public byte GetUb(){
            //アドレス指定で直接参照している元コードのためポインタインデックスの自動減少はなし
            byte[] int32Byte = new byte[stackSize];
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[stackIndex + i];
            return (byte)BitConverter.ToUInt32(int32Byte, 0);            
        }
        public uint GetUl(){
            //アドレス指定で直接参照している元コードのためポインタインデックスの自動減少はなし
            byte[] int32Byte = new byte[stackSize];
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[stackIndex + i];
            return BitConverter.ToUInt32(int32Byte, 0);            
        }
        public uint GetUlOffset(int offset){/* for unsigned long access  */
            //アドレス指定で直接セットしている元コードのためポインタインデックスの自動増加はなし
            byte[] int32Byte = new byte[stackSize];
            uint index=(uint)(stackIndex + offset*stackSize);
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[index + i];
            return BitConverter.ToUInt32(int32Byte, 0);      
        }
        public byte PopUb(){    /* for unsigned byte access */
            if(stackIndex - stackSize < 0)throw new Exception("stack under flow");
            byte[] int32Byte = new byte[stackSize];
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[stackIndex + i];
            stackPointer++;//POPはポインタ増加
            stackIndex-=stackSize;//POPはインデックス減少
            return (byte)BitConverter.ToUInt32(int32Byte, 0);
        }
        public ushort PopUs(){    /* for unsigned byte access */
            if(stackIndex - stackSize < 0)throw new Exception("stack under flow");
            byte[] int32Byte = new byte[stackSize];
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[stackIndex + i];
            stackPointer++;//POPはポインタ増加
            stackIndex-=stackSize;//POPはインデックス減少
            return BitConverter.ToUInt16(int32Byte, 0);
        }
        public uint PopUl(){/* for unsigned long(int32) access   */
            if(stackIndex - stackSize < 0)throw new Exception("stack under flow");
            byte[] int32Byte = new byte[stackSize];
            for (ulong i = 0; i < stackSize; i++) int32Byte[i] = dataArray[stackIndex + i];
            stackPointer++;//POPはポインタ増加
            stackIndex-=stackSize;//POPはインデックス減少
            return BitConverter.ToUInt32(int32Byte, 0);
        }
        
        public void PushUb(byte b){    /* for unsigned byte access */
            if(stackIndex + stackSize > stackMaxSize-1)throw new Exception("stack over flow");
            stackPointer--;//POPはポインタ減少
            stackIndex +=stackSize;//PUSHはインデックス増加
            byte[] int32Byte = new byte[stackSize];
            int32Byte[3] =b;
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
        }
        public void PushUs(ushort us){    /* for unsigned byte access */
            if(stackIndex + stackSize > stackMaxSize-1)throw new Exception("stack over flow");
            stackPointer--;//POPはポインタ減少
            stackIndex +=stackSize;//PUSHはインデックス増加
            byte[] int32Byte =BitConverter.GetBytes(us);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
        }
        public void PushUl(uint ul){/* for unsigned long(int32) access  */
            if(stackIndex + stackSize > stackMaxSize-1)throw new Exception("stack over flow");
            stackPointer--;//POPはポインタ減少
            stackIndex +=stackSize;//PUSHはインデックス増加           
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
        }
        public void PushSl(int sl){/* for signed long(int32) access  */
            if(stackIndex + stackSize > stackMaxSize-1)throw new Exception("stack over flow");
            stackPointer--;//POPはポインタ減少
            stackIndex +=stackSize;//PUSHはインデックス増加
            byte[] int32Byte =BitConverter.GetBytes(sl);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
        }
        public void SetUl(uint ul){/* for unsigned long access  */
            //アドレス指定で直接セットしている元コードのためポインタインデックスの自動増加はなし
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
        }
        public void SetUl2var(uint ul,uint ul2){/* for unsigned long access (for 1set of 2variable)  */
            //アドレス指定で直接セットしている元コードのためポインタインデックスの自動増加はなし
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i]=int32Byte[i];
            int32Byte =BitConverter.GetBytes(ul2);
            for (ulong i = 0; i < stackSize; i++) dataArray[stackIndex + i + 4]=int32Byte[i];
        }
        public void SetUlOffset(uint ul,int offset){/* for unsigned long access  */
            //アドレス指定で直接セットしている元コードのためポインタインデックスの自動増加はなし
            byte[] int32Byte =BitConverter.GetBytes(ul);
            uint index=(uint)(stackIndex - offset*stackSize);//+は減方向
            for (ulong i = 0; i < stackSize; i++) dataArray[index + i]=int32Byte[i];
        }
    }
}
```

</details>

## Dispatcherクラス（C#関数配列）
### C#の関数配列
前回記事で未実装のため該当mcodeの処理でとまっていた関数配列は下記のような感じで実装しています。オリジナルのCマクロの定義内容を実行文の前後に引用して全体をコメントアウトしているので読み取りづらくなってしますが、オリジナルのマウロの動きを忠実にC#で再現することがキモとも言えますので、いったんざっと書いた後、ほんとにあっているかどうかを再考する上でも、このコメント部に立ち返るようにしておりまして、わたしの中ではかなり重要です。

実際に突入するのは下のzzNotif()の方です。デバッグ用に中間変数を介しています。

```cs:CsFunctionsBunki.cs
namespace Mind8Kernel
{
    public partial class Dispatcher
    {

        /*--------------------- ならば～つぎに  -------------------------*/    
        private void zzif(){ /* ;WORD $$IF */
                /* Mコード=0x00EC */
            // #define  DROP_L               DstackPointer++
            // #define  DROP_F               DROP_L
            // #define  POP_L                (*DstackPointer++)
            // #define  POP_L_OF_Q           (DROP_F,POP_L)
            // if ( POP_L_OF_Q )
            // {
            //         SKIP_MCODE_1WORD;
            //#define  SKIP_MCODE_1WORD   McodePointer.w++
            // }
            // else
            // {
            //         SKIP_MCODE( READ_MCODE_SHORT );
            //#define  SKIP_MCODE(bytes)  McodePointer.b+=(bytes)
            //#define  READ_MCODE_SHORT   (*McodePointer.s)
            // }
            dtp.PopUl();//≒DROP Dataスタックから取り出して捨てる
            if(dtp.PopUl()>=1){
                mp.MoveMcodeIndex(1);
            }else{
                mp.MoveMcodeIndexByByte(mp.ReadMcodeShort());
            }
        }
        private void zzNotif(){ /* ;WORD $$-IF */
                /* Mコード=0x00ED */
            // if ( POP_L_OF_Q )
            // {
            //         SKIP_MCODE( READ_MCODE_SHORT );
            //#define  SKIP_MCODE(bytes)  McodePointer.b+=(bytes)
            //#define  READ_MCODE_SHORT   (*McodePointer.s)
            // }
            // else
            // {
            //         SKIP_MCODE_1WORD;
            // }
            dtp.PopUl();//≒DROP Dataスタックから取り出して捨てる
            if(dtp.PopUl()>=1){
                //mp.MoveMcodeIndexByByte(mp.ReadMcodeShort());
                short mc=mp.ReadMcodeShort();
                mp.MoveMcodeIndexByByte(mc);
            }else{
                mp.MoveMcodeIndex(1);
            }
        }
    }
}
```
これを実装した当初、分岐の結果がC版オリジナルと逆になってしまって、後続のmcodeがあさってになるという現象に遭遇したため、Mind開発者の@killyさんが注意喚起されていたPOP_L_OF_Q すなわち(DROP_F,POP_L)の実行順が逆なのではとも考えたのですが、実際のところは現状でもこの対応実装であっているようで、原因は少し手前のデータスタックへの値の積み具合の不具合でした。

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードの確度をざくっと引き上げて「三段目」とかかなという感じでしたが、最近は道の険しさにひるんでいます。（この番付の判定はてきとうです:joy:）まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。
