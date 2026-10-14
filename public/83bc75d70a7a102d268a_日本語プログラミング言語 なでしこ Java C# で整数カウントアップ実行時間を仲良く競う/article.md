# はじめに
日本語プログラミング言語 なでしこ とJava C# とで整数カウントアップの反復実行時間を仲良く競い合わせてみます。コンソール出力は意外と重い処理なので、いったん素の処理でどんなものなのか検証します。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
nadesiko version 1.588 for Windows
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz

## この記事内容の保証
※この記事の実行結果は参考情報です。実行環境に大きく依存します。

# お題のソースコード
#### Java
```Java:main.java
import java.lang.System;
/**
* プログラム型
*/
class Program
{
    /**
    * メイン
    * @param args 引数
    */
    public static void main(String[] args) throws Exception
    {
        int countMax=0;
        int count=0;
        if (args.length != 1) {
            countMax=0;
        }
        try
        {
            countMax=Integer.parseInt(args[0]);
        }
        catch (Exception e)
        {
            countMax=0;
        }
        //開始時間（ナノ秒）
        long startTime = System.nanoTime();

        while(count < countMax){

            count+=1;
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

    }
}
```
#### C#
```cs:main.cs
using System;

/// <summary>プログラム型</summary>
class Program
{

    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        int countMax=0;
        int count=0;
        if (args.Length != 1) {
            countMax=0;
        }else{
            try
            {
                countMax=int.Parse(args[0]);
            }
            catch (FormatException)
            {
                countMax=0;
            }
        }
 
        //開始時間（ミリ秒）
        DateTime startTime= new DateTime();
        DateTime stopTime = new DateTime();
        startTime = DateTime.Now;

        while(count < countMax){

            count+=1;
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
}
```

#### なでしこ
```mind:count.nako
※【なでしこ実行モード】cnako

countとは整数
countMaxとは整数

count=0
countMax=0

もし コマンドラインの配列要素数 < 2 ならば
　　countMax=0
違えば
   エラー監視
　    countMax=コマンドライン[1]を整数変換
　　エラーならば
 　　 countMax=0
    ここまで
ここまで

開始日時は、システム時間

（count < countMax）の間

	count = count + 1
ここまで

終了日時は、システム時間
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する
    
```
※なでしこ(v1)のコンソールアプリケーション[^1]

# 実行結果
#### Java
```:
C:\developments\java20>java -cp . Program 4000000
処理回数: 4000000回
処理時間: 3ミリ秒

C:\developments\java20>
```

#### C#

```:
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Count.exe 4000000
処理回数: 4000000回
処理時間: 23.1618ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```

#### なでしこ
```:
C:\nadesiko\sample1>count.exe 4000000
処理回数：4000000回
処理時間：8695ミリ秒

C:\nadesiko\sample1>
```

# 実行結果まとめ
表2　整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | なでしこ |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 7  | 16  |
| 40,000  | 0  | 6  | 78  |
| 400,000  | 3  | 7  | 843  |
| 4,000,000  | 3  | 23  | 8,695  |
| 40,000,000  | 3  | 139  | 83,129 |
| 400,000,000  | 3  | 1,341  | 827,183  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。

Javaは回数の桁数の増加の影響をほぼ受けないという結果で、他の言語が40万回を超えると線形に処理時間が増えていくのと対照的でした。


[^1]: なでしこ(v1)の上記のソースコードにウィンドウ版とコンソール版の違いはなく、なでしこパッドで一度コンソールアプリケーションの実行モードで実行してから、実行ファイルを作成するとコンソールアプリケーションとなりました。今回は「現在の実行モードをカーソル位置に挿入」を最初の行で行っています。
