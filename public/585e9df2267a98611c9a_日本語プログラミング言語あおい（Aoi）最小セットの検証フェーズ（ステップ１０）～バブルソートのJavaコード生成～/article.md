# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の検証フェーズのステップ１０になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態でGitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro+版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

# 本記事のステップ
## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。下記の実装タスクから構成され実行完了しました。
　Phase 1. Lexer タスク
　Phase 2. Parser タスク
　Phase 3. AST タスク
　Phase 4. 意味解析と名前解決 タスク
　Phase 5. 中間表現（IR） タスク
　Phase 6. コード生成パイプライン タスク
　Phase 7. コア構文のトランスコンパイル実装
　Phase 8. Program.cs からの実行フロー統合の実装

### Phase 9: 検証と品質改善
前回は基礎サンプルのJavaソースコード生成対応が完了しました。本記事ではバブルソートのアルゴリズムを記述したサンプルでのJavaコード生成に進行します。

## バブルソートのアルゴリズムを記述したサンプルに対応
### あおいのソースコードサンプル
ターゲット言語がJavaの場合のあおいのソースコードサンプルでは、現状カバーする範囲の構文ではインポート文のみ異なる形となります。

**バブルソートのアルゴリズムを記述したサンプル**
**sourceFiles\bubblesortjv.aoi**
<details open><summary>sourceFilesbubblesortjv.aoi</summary>

```aoi:sourceFiles\bubblesortjv.aoi
▽名前空間 BubbleSort
    /**
    * Program
    */
    ▽public クラス プログラム型

        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            /** array */
            ・int[] 配列 = 15,13,9,6,4,1
           
            /** index */
            □バブルソートする(配列)

            〇int i=0,i<配列.Length,i++ 繰り返す
            　□コンソール表示する(配列[i])
            〇ここまで
        △
            
        /** BubbleSort
         * @param 配列 array
         */
        ▽public void バブルソートする(int[] 配列)
          /** i */
          ・int 外側 = 0
          〇外側 < 配列.Length の間は繰り返す
            /** j */
            ・int 内側 = 0
            〇内側 < 配列.Length - 外側 - 1 の間は繰り返す
              ◇配列[内側] > 配列[内側 + 1] の場合
                /** temp */
                ・int 一時 = 配列[内側]
                □配列[内側] = 配列[内側 + 1]
                □配列[内側 + 1] = 一時
              ◇ここまで
              □内側++
            〇ここまで
            □外側++
          〇ここまで
        △

        /**
        * ConsoleOut
        * @param 引数2 dispStr
        */
        ▽static void コンソール表示する(string 引数2)
            □コンソール.一行表示する(引数2)
        △
    △
△

■インポートする java.lang.System
▼public class コンソール PrintStream System.out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲
```
</details>

インポート文がJavaのパッケージを指定する形となります。インポート文は将来的にはあおいのターゲット言語別ライブラリリソースとなります。

またJavaの場合クラス名とファイル名が同一という制約もありますので、生成ファイル名はフォルダ別に出力します。

**sourceFiles\bubblesortcs.aoi**
C#/VB.NET向けは[こちらの記事](
https://qiita.com/mylifewithviolin/items/91857ad240e382a9ed54)を参照してください。
「■インポートする」の違いに注目してください。

## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでMicrosoft Copilotとのやりとりはなかったです。
## GitHub Copilot
### プロンプト１
>sourceFiles\bubblesortjv.aoiはバブルソートのソースです。
Javaソースコードにトランスコンパイルして
transcompiledFiles\java\bubblesort\Program.java_
上記生成コードがJavacでコンパイルが正常か検証するフローを
docs\バブルソートをJavaでトランスコンパイルできるようにするための修正フロー.md
に出力してください。
#### 生成レスポンス１
docs\バブルソートをJavaでトランスコンパイルできるようにするための修正フロー.md
が出力されました。
### プロンプト２
>docs\バブルソートをJavaでトランスコンパイルできるようにするための修正フロー.md
を実行して
docs\バブルソートをJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
に出力してください。
#### 生成レスポンス２
Javaソースコードが生成され
docs\バブルソートをJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
が出力されました。


### トランスコンパイル後のJavaソースコード
Javaコンパイラによるコンパイル検証済コードとなります。
**transcompiledFiles\java\bubblesort\Program.java**

```java:transcompiledFiles\java\bubblesort\Program.java
package bubblesort;

import java.lang.System;

/**
 * プログラム型
 */
public class Program
{
    /**
     * メイン
     * @param args 引数
     */
    public static void main(String[] args)
    {
        /**
         * 配列
         */
        int[] array = new int[] { 15, 13, 9, 6, 4, 1 };
        bubbleSort(array);
        for (int i = 0; i < array.length; i++)
        {
            System.out.println(array[i]);
        }
    }
    
    /**
     * バブルソートする
     * @param array 配列
     */
    public static void bubbleSort(int[] array)
    {
        /**
         * 外側
         */
        int i = 0;
        while (i < array.length)
        {
            /**
             * 内側
             */
            int j = 0;
            while (j < array.length - i - 1)
            {
                if (array[j] > array[j + 1])
                {
                    /**
                     * 一時
                     */
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
                j++;
            }
            i++;
        }
    }
    
    /**
     * コンソール表示する
     * @param dispStr 引数2
     */
    public static void consoleOut(String dispStr)
    {
        System.out.println(dispStr);
    }
    
}
```

## 本ステップの評価
定番アルゴリズムのバブルソートのJavaの生成ソースコード対応が完了しました。比較的複雑なソースコードとして定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つがあり、そのひとつが完了した形となりましたが、次回は線形探索法、二分探索法を変換します。この時点ではMVPの検証フェーズは終わりに近づいていると思っていました。

# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
