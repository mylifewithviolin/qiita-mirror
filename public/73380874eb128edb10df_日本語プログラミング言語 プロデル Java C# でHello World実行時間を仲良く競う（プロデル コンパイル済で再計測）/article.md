# はじめに
日本語プログラミング言語 プロデル とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。プロデルはコンパイル済中間コードでの実行を再計測してみます。


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
```mind:helloworld2.rdr
※コンソール
【count:整数】は、0
【countMax:整数】は、0
【引数:文字列】
コンソールから受け取って引数に入れる
引数をcountMaxに入れる

開始日時は、起動時間
count < countMaxの間、繰り返す
	「Hello World!」をコンソールへ表示して改行する
	count =count +1
繰り返し終わり
終了日時は、起動時間
経過時間＝終了日時-開始日時

「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
「処理時間：」＆ 経過時間＆ 「ミリ秒」をコンソールへ表示して改行する。
    
```
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（コンパイル済）」で行っています。

ランタイム環境で動作したソースは実行ファイル作成は通過しましたが、実行時にランタイム例外が発生しましたので、今回、以下のように書き換えています。

実行時間はOS起動経過時間（ミリ秒整数値）の除算に書き換えています。日付形式の式は動きませんでした。
他の言語と同様に文字列を数値変換した際の例外をキャッチする例外監視は動作しないのではずしました。
コマンドライン引数は読み込めなかったので、コンソールからの入力としています。

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

#### プロデル（コンパイル済版、処理回数はコンソール入力）

```:
C:\produire\sample2>helloworld2.exe
40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数：40000回
処理時間：5156ミリ秒

C:\produire\sample2>

C:\produire\sample>
```
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（ランタイム環境）」で行っています。2023/12/07追記

# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | プロデル |
|-:|-:|-:|-:|
|  40 |  8 | 16  | 0 |
| 400  | 72  | 57  | 46  |
| 4,000  | 563  | 468  | 515  |
| 40,000  | 4,565  | 4,206  | 5,156  |
| 400,000  | 42,618  | 40,075  | 46,421  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
Javaはさすがに物理I/Oが入るのでリアルにループしていると考えられます。細かい最適化は各言語あまり気にしていませんが、JavaとC#はいずれ時間があるときに再計測しておきたいです。
