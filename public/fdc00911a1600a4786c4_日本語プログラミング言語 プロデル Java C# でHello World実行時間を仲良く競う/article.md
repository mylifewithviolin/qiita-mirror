# はじめに
日本語プログラミング言語 プロデル とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。

https://qiita.com/advent-calendar/2023/produire

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Produire Version 2.0.1197 for Windows
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
            System.out.println("Hello World!");
            count+=1;
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

    }
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
            Console.WriteLine("Hello World!");
            count+=1;
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
```

#### プロデル
```mind:main.rdr
※コンソール
    【count:整数】は、0
    【countMax:整数】は、0
    
    もしプログラムのコマンドライン引数が無なら
    　　countMax=0
    そうでなければ
       例外監視
    　　  countMax=プログラムのコマンドライン引数(1)
    　　発生した場合
     　　 countMax=0
        監視終わり
    もし終わり
    
    開始日時は、今日
    count < countMaxの間、繰り返す
    　 「Hello World!」をコンソールへ表示して改行する
    	count =count +1
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する
    
```
# 実行結果
#### Java
```:
C:\developments\java20>java -cp . Program 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 4565ミリ秒

C:\developments\java20>
```

#### C#

```:
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Helloworld 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 4206.8631ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```

#### プロデル

```:
C:\produire\sample>helloworld 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数：40000回
処理時間：6646.3256ミリ秒

C:\produire\sample>
```
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（ランタイム環境）」で行っています。2023/12/07追記

# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | プロデル |
|-:|-:|-:|-:|
|  40 |  8 | 16  | 62 |
| 400  | 72  | 57  | 124  |
| 4,000  | 563  | 468  | 781  |
| 40,000  | 4,565  | 4,206  | 6,646  |
| 400,000  | 42,618  | 40,075  | 62,613  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。プロデルは.NET Framework 4.8のCLRで動いているのでC#との差異は.NET Core 6.0との差異なのかもしれません。スミレで要検証。
