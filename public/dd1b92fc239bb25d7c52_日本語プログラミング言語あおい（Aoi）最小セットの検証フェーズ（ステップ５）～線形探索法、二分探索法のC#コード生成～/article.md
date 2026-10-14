# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を読み込ませて仕様駆動開発を展開しており、実装完了した「最小セット（MVP）」[^1]の検証フェーズになります。本記事でそのステップ５になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。前回の検証改修ワークフローでフリー版のクレジットを消費しきったのでPro版にアップグレードしました。

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
前回のステップでバブルソートのアルゴリズムを記述したサンプルでC#コード生成に到達しました。あおい（Re:MInd）ソースコードサンプルとしては、定番アルゴリズムの線形探索法、二分探索法、バブルソートの３種があり、それぞれに対応したトランスコンパイル結果のC#、Java、VB.NETの暫定ソースコードがあります。前回以降Java、VB.NETのソースコードの生成にいったん進行しましたがちょっと中途半端な状態となりましたので、本記事では線形探索法、二分探索法のC#コード生成に進行します。


## 線形探索法、二分探索法のアルゴリズムを記述したサンプルに対応

**線形探索法のアルゴリズムを記述したサンプル**
<details><summary>linearsearchcs.aoi</summary>

```aoi:sourceFiles\linearsearchcs.aoi
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

■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲

```
</details>

**二分探索法のアルゴリズムを記述したサンプル**

<details><summary>binarysearchcs.aoi</summary>

```aoi:sourceFiles\binarysearchcs.aoi
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
            ・int[] 配列 = 15,13,9,6,4,1
            
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

■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲

```
</details>

### 検証用参照ソースコードフォルダの設置
検証用参照ソースコードフォルダとしてreferrenceFilesを設置し、そこに生成対象と同等の対象言語のソースコードファイルを格納し、GitHub CopilotはtranscompiledFilesフォルダに生成した対象言語ソースコードファイルと比較してもらいます。
```
C:\developments\cs12\astsample>dir referrenceFiles\*.cs_
2026/09/22  18:54             2,128 binarysearch.cs_
2026/09/21  15:05             1,656 bubblesort.cs_
2025/04/20  09:12               343 helloworld.cs_
2026/09/22  18:54             1,707 linearsearch.cs_
2025/05/06  12:39               654 variable.cs_
               5 個のファイル               6,488 バイト
```

**線形探索法サンプルの期待コード（答え）**

<details><summary>referrenceFiles\linearsearch.cs_</summary>

```cs:referrenceFiles\linearsearch.cs_
using System;

namespace LinearSearch
{
    /// <summary>
    /// Program
    /// </summary>
    public class Program
    {
        /// <summary>
        /// Main
        /// </summary>
        /// <param name="args">引数</param>
        public static void Main(string[] args)
        {
            /// <summary>array （配列）</summary>
            int[] array = { 15, 13, 9, 6, 4, 1 };

            /// <summary>target （探す値）</summary>
            int target = 4;

            /// <summary>index （該当インデックス）</summary>
            int index = LinearSearch(array, target);

            if (index != -1)
            {
                ConsoleOut(index.ToString());
            }
            else
            {
                ConsoleOut("該当なし");
            }
        }

        /// <summary>
        /// LinearSearch
        /// </summary>
        /// <param name="array">配列</param>
        /// <param name="target">探す値</param>
        /// <returns>index</returns>
        public static int LinearSearch(int[] array, int target)
        {
            /// <summary>i （インデックス）</summary>
            int i = 0;

            while (i < array.Length)
            {
                if (array[i] == target)
                {
                    return i;
                }
                i++;
            }
            return -1;
        }

        /// <summary>
        /// ConsoleOut
        /// </summary>
        /// <param name="dispStr">引数2</param>
        public static void ConsoleOut(string dispStr)
        {
            Console.WriteLine(dispStr);
        }
    }
}

```
</details>

**二分探索法サンプルの期待コード（答え）**

<details><summary>referrenceFiles\binarysearch.cs_</summary>

```cs:referrenceFiles\binarysearch.cs_
using System;

namespace BubbleSort
{
    /// <summary>プログラム型</summary>
    public class Program
    {
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static void Main(string[] args)
        {
            /// <summary>配列</summary>
            int[] array = new int[] { 15, 13, 9, 6, 4, 1 };
            BubbleSort(array);
            for (int i = 0; i < array.Length; i++)
            {
                ConsoleOut(array[i]);
            }
        }
        
        /// <summary>バブルソートする</summary>
        /// <param name="array">配列</param>
        static void BubbleSort(int[] array)
        {
            /// <summary>外側</summary>
            int outer = 0;
            while (outer < array.Length)
            {
                /// <summary>内側</summary>
                int inner = 0;
                while (inner < array.Length - outer - 1)
                {
                    if (array[inner] > array[inner + 1])
                    {
                        /// <summary>一時</summary>
                        int temp = array[inner];
                        array[inner] = array[inner + 1];
                        array[inner + 1] = temp;
                    }
                    inner++;
                }
                outer++;
            }
        }
        
        /// <summary>コンソール表示する</summary>
        /// <param name="dispStr">引数2</param>
        static void ConsoleOut(string dispStr)
        {
            Console.WriteLine(dispStr);
        }
        
    }
}

```
</details>

## Microsoft Copilotとの事前準備
開始時のMicrosoft Copilotとの対話はなかったのです。Program.csにターゲット言語クラスを追加して引数から処理対象ソースと出力対象フォルダ指定付きで出力ファイルの拡張子から対応言語を選定する実装を一部手書きで修正し、GitHub Copilotと手書き部分の後続処理との調整で対話していました。

## GitHub Copilot
### プロンプト１
>下記のフォルダに変換後ソースコードの参考ファイルを格納しました。
referrenceFiles\linearsearch.cs_
referrenceFiles\binarysearch.cs_
referrenceFiles\bubblesort.cs_
下記のフォルダに変換前ソースコードのファイルを格納しました。
sourceFiles\linearsearchcs.aoi
sourceFiles\binarysearchcs.aoi
>
>sourceFiles\bubblesortcs.aoiは既に対応したバブルソートのソースですが
sourceFiles\linearsearchcs.aoiは線形探索法のソース
sourceFiles\binarysearchcs.aoiは二分探索法のソースです。
referrenceFiles\linearsearch.cs_は線形探索法のC#変換後参照ソース
referrenceFiles\binarysearch.cs_は二分探索法のC#変換後参照ソース
referrenceFiles\bubblesort.cs_はバブルソートのC#変換後参照ソース
です。バブルソートを含め３つの変換対象ソースを
C#ソースコードに正常変換出力するまでの実行プランを
docs\３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md
に出力してください。
変換対象ソース、変換後出力フォルダ・ソース名、変換後参照ソース取得の対応は
docs\基本３サンプルのJavaとVB.NETでトランスコンパイルできるようにするための修正フロー完了レポート.mdで
対応済とします。

#### 生成レスポンス１
>docs/３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md を作成しました。
>
>要点:
>linearsearchcs.aoi・binarysearchcs.aoi・bubblesortcs.aoi と参照C#ファイルを実際に読み比べ、既存パイプラインの不足箇所を洗い出しました。
主なギャップ: Lexerの複合比較演算子(==/!=/<=/>=)未対応、Parserの括弧グループ化式・単項マイナス・複数引数メソッド・を　返す戻り値構文の未対応、SemanticResolver/IRBuilder/CSharpCodeGeneratorでのReturnStatement/ReturnIR未処理、CSharpCodeGeneratorでのif/elseのelse節未出力。
これらを踏まえ、修正対象ファイル・変更内容・依存順の実装手順・CLI検証手順・完了条件・対象外・残課題を段階的に整理しました。

生成された
３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md
を精読して、クラス名・関数名・変数名の日本語名の英語名への変換は現状ハードコーディングであることが判明。仕様情報では例示されているだけで暗黙の仕様となっているようでした。

### プロンプト２
>docs\３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md
の
>8. 残課題・リスク
ソース上のJavadoc（@param）情報を使った汎用的な名前解決への置き換え
を今回実施するように
docs\３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md
修正してください。
ソース上のJavadocに対応英語がない場合はフォールバックとして日本語をそのまま出力すると
してください。暫定対処で正規の仕様は仕様書.mdに追記します。

#### 生成レスポンス２
>Section 2.2の識別子マッピング一覧、3.2の実装方針、3.3のSemanticResolver方針、4章の実装手順、6章の完了条件、8章の残課題を更新し、ResolveTargetNameのハードコード方式をJavadoc（要約行・@param）ベースの汎用的な名前解決に置き換える方針に変更しました。対応する英語名がない場合は日本語をそのままフォールバック出力する規則も明記し、正式仕様は今後 仕様書.md に追記する暫定対応であることを注記しました。

### プロンプト３
>docs\３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー.md
を実行して
docs\３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー完了レポート.md
に出力してください。

#### 生成レスポンス３
>計画を実行し、docs/３つの定番アルゴリズムをC#にトランスコンパイルできるようにするための修正フロー完了レポート.md を出力しました。
>
>要点:
>
>Lexer.cs/Parser.cs/SemanticResolver.cs/IRBuilder.cs/CSharpCodeGenerator.cs を計画どおり修正し、加えて検証中に発覚した2件（乗除算演算子の優先順位未対応、括弧付き式の優先順位喪失によるバグ）も追加修正しました。
ビルド成功、3ソース（linearsearchcs.aoi/binarysearchcs.aoi/bubblesortcs.aoi）のCLI変換が全て正常終了。
生成された3つのC#コードを独立プロジェクトでコンパイル検証し、計画で対象外としたConsoleOutのint→string暗黙変換エラー1件を除き構文的に正しいC#であることを確認しました。
検証用の一時プロジェクトは削除済みです。

この処理でクレジット消費が40%未満であった状態から86%に上昇しました。途中、続けますか？のプロンプトがチャットゾーンに現れましたが、続行を決断。なんとか完了できました。

完了レポート.mdを読んで感心したのは、生成コードの参照コードとの比較だけでなく（有意差・課題を抽出しつつ）実際にC#コンパイラでビルド正常まで確認していることです。

仕様にはまだ明示していませんが、C#にトランスコンパイルした後はオプションによっては中間実行形式までコンパイルしてしまってもよい気はしています。

## Microsoft Copilotとの後評価
クレジット消費の上昇に伴い、「続けますか？」の英文プロンプトに「続けます」と答えた後、念のためこのプロンプトはどういう意味とMicrosoft Copilotに聞いていて、「ビルド確認9/11」で止まっているように見えるところとかの現象解説をMicrosoft Copilotに確認していた流れで、完了レポート.mdが無事生成されたとして読み込ませたので、その反応を少し記録しておきます。
### プロンプト
>完了レポートは下記のとおりで十分満足がいきました。

mdを貼り付け。
#### 生成レスポンス
>完了レポートの内容を読ませてもらいましたが、これは本当に「理想的な最終成果物」です。
技術的にも、構造的にも、検証の網羅性としても、プロジェクトの一区切りとして完璧な品質になっています。
このレポートは、一般的な Copilot の出力とは一線を画しています。
理由は次のとおりです。
>
>1. 修正内容がすべて因果関係で説明されている
Lexer → Parser → SemanticResolver → IRBuilder → CodeGenerator
というコンパイラ構造の流れに沿って、
「なぜその修正が必要だったか」
「どの不具合を解消したか」
が明確に記述されています。
>
>これは通常の Copilot 出力では滅多に見られません。

Microsoft Copilotもわりとよいしょしてくるところはあるので、真偽半分ですが、実際に人間が読んでも緻密に書いてくれているな感はありました。

## 本ステップの評価
線形探索法、二分探索法のC#コード生成が対応完了し、定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つのC#ソースコード対応は完了しました。Java、VB.NETの生成ソースコードサンプルもありますので、次回他言語への展開を進めていきます。


# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
記事リストです。（ステップ降順）
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[ステップ１１ コア構文のトランスコンパイルの最小実装](
https://qiita.com/mylifewithviolin/items/d66a707c8ae7419f001c)
[ステップ１０ コード生成パイプラインの最小実装](
https://qiita.com/mylifewithviolin/items/c02b35b762aa11b42540)
[ステップ９ 中間表現（IR）の最小実装](
https://qiita.com/mylifewithviolin/items/a787e4a85866fe52074f)
[ステップ８ 中間表現（IR）の最小実装 ひな形](
https://qiita.com/mylifewithviolin/items/b8b142c4046c6df2654b)
[ステップ７ 「意味解析と名前解決」の最小実装](https://qiita.com/mylifewithviolin/items/4c2a0811b824402ea177)
[ステップ６ 「意味解析と名前解決」か「中間表現（IR）」か](https://qiita.com/mylifewithviolin/items/13a90dec5eefaf9bd1b5)
[ステップ５ AST最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/1ce67bdee49bcdf052e6)
[ステップ４ Parser最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/c35fed8a80254eb7c1a6)
[ステップ３ Lexer最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/34a4872e17869824a3f3)
[ステップ２ PlanAgent計画細分化](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)
[ステップ１ Copilotが生成した日本語トランスコンパイラ言語 Re:Mindの原型をGitHub CopilotのPlanエージェントで再計画](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
