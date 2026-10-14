# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の検証フェーズのステップ１１になります。

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
前回のステップでバブルソートのアルゴリズムを記述したサンプルでJavaのコード生成を行いました。本記事では線形探索法、二分探索法のJavaコード生成に進行します。

## 線形探索法、二分探索法のアルゴリズムを記述したサンプルに対応
### あおいのソースコードサンプル
ターゲット言語がJavaの場合のあおいのソースコードサンプルでは、現状カバーする範囲の構文ではインポート文のみ異なる形となります。

インポート文がJavaのパッケージを指定する形となります。インポート文は将来的にはあおいのターゲット言語別ライブラリリソースとなります。

またJavaの場合クラス名とファイル名が同一という制約もありますので、生成ファイル名はフォルダ別に出力します。

**線形探索法のアルゴリズムを記述したサンプル**
**sourceFiles\linearsearchjv.aoi**
<details open><summary>sourceFiles\linearsearchjv.aoi</summary>

```aoi:sourceFiles\linearsearchjv.aoi
▽名前空間 LinearSearch
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
            
            /** target */
            ・int 探す値 = 4
            
            /** index */
            ・int 該当インデックス = 線形探索する(配列, 探す値)
            ◇該当インデックス != -1 の場合
            　 □コンソール表示する(該当インデックス)
            ◇他に
            　 □コンソール表示する("該当なし")
            ◇ここまで
        △
        
        /** LinearSearch
         * @param 配列 array
         * @param 探す値 target
         */
        ▽public int 線形探索する(int[] 配列, int 探す値)
          /** i */
          ・int インデックス = 0
          〇インデックス < 配列.Length の間は繰り返す
            ◇配列[インデックス] == 探す値 の場合
              □インデックスを　返す
            ◇ここまで
            □インデックス++
          〇ここまで
          □-1を　返す
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

**sourceFiles\linearsearchcs.aoi**
C#/VB.NET向けは[こちらの記事](
https://qiita.com/mylifewithviolin/items/5acf86b12bd538caca30)を参照してください。
「■インポートする」の違いに注目してください。

**二分探索法のアルゴリズムを記述したサンプル**
**sourceFiles\binarysearchjv.aoi**
<details open><summary>sourceFiles\binarysearchjv.aoi</summary>

```aoi:sourceFiles\binarysearchjv.aoi
▽名前空間 BinarySearch
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
            ・int[] 配列 = 1,4,6,9,13,15
            
            /** target */
            ・int 探す値 = 4
            
            /** index */
            ・int 該当インデックス = 二分探索する(配列, 探す値)
            ◇該当インデックス != -1 の場合
            　 □コンソール表示する(該当インデックス)
            ◇他に
            　 □コンソール表示する("該当なし")
            ◇ここまで
        △
            
         /** BinarySearch
         * @param 配列 array
         * @param 探す値 target
         */
        ▽public int 二分探索する(int[] 配列, int 探す値)
          /** left */
          ・int 左端 = 0
          /** right */
          ・int 右端 = 配列.Length - 1
          〇左端 <= 右端 の間は繰り返す
            /** mid */
            ・int 中央 = (左端 + 右端) / 2
            ◇配列[中央] == 探す値 の場合
              □中央を　返す
            ◇ここまで
            ◇配列[中央] < 探す値 の場合
              □左端 = 中央 + 1
            ◇他に
              □右端 = 中央 - 1
            ◇ここまで
          〇ここまで
          □-1を　返す
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

**sourceFiles\binarysearchcs.aoi**
C#/VB.NET向けは[こちらの記事](
https://qiita.com/mylifewithviolin/items/5acf86b12bd538caca30)を参照してください。


## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでMicrosoft Copilotとのやりとりはなかったです。
## GitHub Copilot
### プロンプト１
>sourceFiles\linearsearchjv.aoiは線形探索法のソース
sourceFiles\binarysearchjv.aoiは二分探索法のソースです。
Javaソースコードにトランスコンパイルして
transcompiledFiles\java\linearsearch\Program.java_
transcompiledFiles\java\binarysearch\Program.java_
Javacでコンパイルが正常か検証するフローを
docs\線形探索法と二分探索法をJavaでトランスコンパイルできるようにするための修正フロー.md
に出力してください。

#### 生成レスポンス１
docs\線形探索法と二分探索法をJavaでトランスコンパイルできるようにするための修正フロー.md
が出力されました。
### プロンプト２
>docs\線形探索法と二分探索法をJavaでトランスコンパイルできるようにするための修正フロー.md
を実行して
docs\線形探索法と二分探索法をJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
に出力してください。
#### 生成レスポンス２
Javaソースコードが生成され
docs\線形探索法と二分探索法をJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
が出力されました。

以下は完了レポート.mdからの抜粋です。

```md
## 7. 最終判定

線形探索法と二分探索法について、以下をすべて確認した。

- AOIソースからJavaソースを生成できる
- Javaのpackage名が小文字で出力される
- Javaエントリポイントが `main` で出力される
- 探索関数の戻り値が `return` として出力される
- 条件分岐の `else` ブロックが出力される
- UTF-8指定の固定 `javac` でコンパイルできる
- 2ファイルとも `javac` 終了コード `0` を確認できる
- 2ファイルともpackage階層下に `Program.class` が生成される

以上により、線形探索法と二分探索法のJavaトランスコンパイル
および `javac` コンパイル検証は完了とする。
```

### トランスコンパイル後のJavaソースコード
Javaコンパイラ(Eclipse Adoptiumのjdk-20.0.2.9)によるコンパイル検証済コードとなります。
**transcompiledFiles\java\linearsearch\Program.java**

```java:transcompiledFiles\java\linearsearch\Program.java
package linearsearch;

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
        /**
         * 探す値
         */
        int target = 4;
        /**
         * 該当インデックス
         */
        int index = linearSearch(array, target);
        if (index != -1)
        {
            System.out.println(index);
        }
        else
        {
            System.out.println("該当なし");
        }
    }
    
    /**
     * 線形探索する
     * @param array 配列
     * @param target 探す値
     */
    public static int linearSearch(int[] array, int target)
    {
        /**
         * インデックス
         */
        int i = 0;
        while (i < array.length)
        {
            if (array[i] == target)
            {
                return i;
            }
            i++;
        }
        return -1;
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
**transcompiledFiles\java\binarysearch\Program.java**

```java:transcompiledFiles\java\binarysearch\Program.java
package binarysearch;

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
        int[] array = new int[] { 1, 4, 6, 9, 13, 15 };
        /**
         * 探す値
         */
        int target = 4;
        /**
         * 該当インデックス
         */
        int index = binarySearch(array, target);
        if (index != -1)
        {
            System.out.println(index);
        }
        else
        {
            System.out.println("該当なし");
        }
    }
    
    /**
     * 二分探索する
     * @param array 配列
     * @param target 探す値
     */
    public static int binarySearch(int[] array, int target)
    {
        /**
         * 左端
         */
        int left = 0;
        /**
         * 右端
         */
        int right = array.length - 1;
        while (left <= right)
        {
            /**
             * 中央
             */
            int mid = left + right / 2;
            if (array[mid] == target)
            {
                return mid;
            }
            if (array[mid] < target)
            {
                left = mid + 1;
            }
            else
            {
                right = mid - 1;
            }
        }
        return -1;
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
定番アルゴリズムの線形探索法、二分探索法のJavaの生成ソースコード対応が完了しました。次回は「最小セット（MVP）」の３言語対応状況を評価します。まだ先は遠いですがだいぶ形になってきました。

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
