# はじめに
日本語プログラミング言語 なでしこ３ とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。ついに、なでしこ３コンソールで「Hello World」にもどってきました。

https://qiita.com/advent-calendar/2023/nadesiko

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
nadesiko version 3.4.5 nadesiko3win32-3.4.5
Node.js v20.10.0.
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

#### なでしこ3
```mind:helloworld3.nako
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
　　「Hello World!」を表示する
	count = count + 1
ここまで

終了日時は、システム時間
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する
    
```
#### なでしこ(v3)のコンソールアプリケーション
なでしこ(v1)のソースコードとは若干の非互換があり調整しています。
起動引数のindexはNode.jsで2つ、なでしこで1つ使われるので3が正解でした。

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

#### なでしこ3

```:
C:\nadesiko\sample1>helloworld3.nako.bat 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数：40000回
処理時間：7267ミリ秒

C:\nadesiko\sample1>
```
# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | なでしこ3 |
|-:|-:|-:|-:|
|  40 |  8 | 16  | 15 |
| 400  | 72  | 57  | 120  |
| 4,000  | 563  | 468  | 899  |
| 40,000  | 4,565  | 4,206  | 7,267  |
| 400,000  | 42,618  | 40,075  | 67,793  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。

# 余談
余談ですが、ナデシコパッドでなでしこ３コンソールを実行させると、コマンドプロンプロが開いて生成されたbatが実行されるのですが、再現状況不明でnako.bakファイルが生成されずにbatが実行エラーになる場合がありました。
nako.bakファイルはソースのnakoファイルのコピーですが、このbatは直接nakoファイルを開かずnako.bakファイルをトランスパイラ本体に読み込ませているのですね。

<details><summary>エラー内容</summary>
C:\nadesiko\sample1>helloworld3.nako.bat
[cnako3のエラー] Error: ENOENT: no such file or directory, open 'C:\nadesiko\sample1\helloworld3.nako.bak'
    at Object.readFileSync (node:fs:453:20)
    at CNako3.execCommand (file:///C:/nadesiko/node_modules/nadesiko3/src/cnako3mod.mjs:154:24)
    at file:///C:/nadesiko/node_modules/nadesiko3/src/cnako3.mjs:10:22
    at file:///C:/nadesiko/node_modules/nadesiko3/src/cnako3.mjs:17:3
    at ModuleJob.run (node:internal/modules/esm/module_job:218:25)
    at async ModuleLoader.import (node:internal/modules/esm/loader:329:24)
    at async loadESM (node:internal/process/esm_loader:34:7)
    at async handleMainPromise (node:internal/modules/run_main:113:12) {
  errno: -4058,
  code: 'ENOENT',
  syscall: 'open',
  path: 'C:\\nadesiko\\sample1\\helloworld3.nako.bak'
}

C:\nadesiko\sample1>

</details>
