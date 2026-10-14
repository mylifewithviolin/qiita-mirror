# はじめに
日本語プログラミング言語 なでしこ３ とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。なでしこワンはレガシーかもしれませんのでなでしこ３の検証を急ぎましたので、関数呼び出しが最初の記事となります。

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
            count = countup(count);
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

    }
	
	/**
    * カウントアップ関数
    * @param c count
    */
	private int countup(int c){
		return c+=1;
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
            count = Countup(count);
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
    /// <summary>カウントアップ関数</summary>
    /// <param name="c">count</param>
    private static int Countup(int c){
		return c+=1;
	}
 }
```


#### なでしこ3
```mind:helloworld.nako
※【なでしこ実行モード】cnako3


count=0
countMax=0
sizeArgs=コマンドラインの配列要素数
もし (sizeArgs < 4) ならば
　　countMax=0
違えば
   エラー監視
　    countMax=コマンドライン[3] //を整数変換
　　エラーならば
 　　 countMax=0
    ここまで
ここまで

開始日時は、システム時間ミリ秒

（count < countMax）の間
	//countをカウントアップし、countに代入する
	count = カウントアップする(count)
ここまで

終了日時は、システム時間ミリ秒
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する


●カウントアップする(cを)
     c = c +1
     cで戻る
ここまで

```
#### なでしこ(v3)のコンソールアプリケーション
なでしこ(v1)のソースコードとは若干の非互換があり調整しています。「システム時間」は秒単位となったので「システム時間ミリ秒」としています。
起動引数のindexはNode.jsで2つ、なでしこで1つ使われるので3が正解でした。

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
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Count2.exe 4000000
処理回数: 4000000回
処理時間: 62.3866ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```


#### なでしこ3
```:
C:\nadesiko\sample1>callfunc3.nako.bat 40
処理回数：40回
処理時間：0ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 400
処理回数：400回
処理時間：0ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 4000
処理回数：4000回
処理時間：4ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 40000
処理回数：40000回
処理時間：11ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 400000
処理回数：400000回
処理時間：22ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 4000000
処理回数：4000000回
処理時間：156ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 40000000
処理回数：40000000回
処理時間：4886ミリ秒

C:\nadesiko\sample1>callfunc3.nako.bat 400000000
処理回数：400000000回
処理時間：50070ミリ秒
```
なでしこパッドからは「なでしこ実行モード:cnako3」で一度実行成功すると
上記callfunc3.nako.batが生成されました。コマンドライン引数を受け取れるよう下記のように少し調整しています。

「なでしこ実行モード:cnako3」でも「実行ファイルを生成する」を実行すると保存ダイアログが開いてcallfunc3.exeを保存しに行こうとしますが、開けませんでしたエラーが返りますので注意が必要です。
```bat
@ ECHO OFF
REM --- NADESIKO V3 ---
"C:\nadesiko\nodejs\node.exe" "C:\nadesiko\node_modules\nadesiko3\src\cnako3.mjs" "C:\nadesiko\sample1\callfunc3.nako.bak" %1
rem ECHO ---
rem pause
```

当初v1状態のソースでは引数がうまく拾えませんでしたの
cnako3.mjsのこのあたりと
```js:cnako3.mjs
// メイン
(async () => {
    const cnako3 = new CNako3();
    try {
        await cnako3.execCommand();
    }
```
cnako3mod.mjsのこのあたりに
```js:cnako3mod.mjs
        // ファイルを読んで実行する
        try {
            // コンパイルと実行を行うメソッド
            const g = await this.runAsync(src, opt.mainfile);
            return g;
        }
```
引数のコンソール出力を仕込んで確認しました。
```js
	    for(var i = 0;i < process.argv.length; i++){
		  console.log("argv[" + i + "] = " + process.argv[i]);
		}
```
```
C:\nadesiko\sample1>callfunc3.nako.bat 40
argv[0] = C:\nadesiko\nodejs\node.exe
argv[1] = C:\nadesiko\node_modules\nadesiko3\src\cnako3.mjs
argv[2] = C:\nadesiko\sample1\callfunc3.nako.bak
argv[3] = 40
argv[0] = C:\nadesiko\nodejs\node.exe
argv[1] = C:\nadesiko\node_modules\nadesiko3\src\cnako3.mjs
argv[2] = C:\nadesiko\sample1\callfunc3.nako.bak
argv[3] = 40
処理回数：40回
処理時間：0ミリ秒
```
起動引数のindexはNode.jsで2つ、なでしこで1つ使われるので3が正解でした。

# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# |なでしこ3 |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 4 |
| 40,000  | 0  | 6  | 11  |
| 400,000  | 2  | 11 | 22  |
| 4,000,000  | 3  | 62  | 156  |
| 40,000,000  | 5  | 538  | 4,886  |
| 400,000,000  | 6  | 5,304  | 50,070  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
