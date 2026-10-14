# はじめに
「日本語トランスコンパイラ言語 Re:Mind（リマインド）」はオープンな実装言語仕様で、どなたでもどの実装言語でもコンパイラ・トランスコンパイラを実装することができます。本記事は仕様策定者の筆者がC#で実装しているステップバイステップな備忘録記事です。

# 本試作の実装言語
・C#
コンソールアプリケーションとして実装します。本試作範囲は策定仕様のごくごく一部です。ターゲット言語は一部のみ対応、言語の対応ソース構文も超限定的です。

## 本試作のターゲット言語
本試作のターゲット言語としては下記の4言語を想定しております、本記事はそのうちのVB.NETに該当する内容です。
・C#
・Java
・**VB.NET**　←本記事の対象言語
・Mind

・想定稼働OS Windows
※VB.NETは.NETCore対応以降のバージョンは非Windows環境でも動作する範囲がありますが、検証パワー不足のため動作環境をWindows限定とさせていただいております。

## 本試作のターゲット言語の対応仕様範囲
"Hellow World!"がコンソール出力されるソースコードをファイル読み込みして、ターゲット言語のソースコードをファイル出力する。（どの言語向けソースを出力するかは起動パラメータにする。）

### お題のターゲット言語出力ソースコード
#### VB.NET
```vb:targetSourceFiles\helloworld.vb
    Imports System

    Namespace HelloWorld

        ''' <summary>プログラム型</summary>
        Module Program
            ''' <summary>メイン</summary>
            ''' <param name="args">引数</param>
            Sub Main(args As String())
                Console.WriteLine("Hello World!")
            End Sub
        End Module
    End Namespace
```

### お題のトランスコンパイラ言語 Re:Mind入力ソースコード(ターゲット言語一部依存)
#### VB.NET
既存ライブラリを引用する記述は毎回書く必要をなくす想定ですが、まだライブラリのサンプルコードは皆無のため、本試作ではライブラリ引用ソースコードも明確に書いてもらう想定です。Systemは既定のImports文として明示不要であっても既定でない今後のImports文のため、出力するとしています。

```mind:sourceFiles\helloworldvb.remind
▽名前空間 HelloWorld
    /**
    * Program
    */
    ▽モジュール プログラム型
        /**
        * Main
        * @param 引数 args
        */
        ▽void メイン(string[] 引数)
            □コンソール.一行表示する("Hello World!")
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

### トランスコンパイラの内部構造

たいへんお手数ですがこちらの記事をご参照ください。

https://qiita.com/mylifewithviolin/items/b3d921383aab4211dc84

日本語ロジック仕様記述言語 Re:Mind（リマインド）は[オープンな設計言語仕様](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)で、どなたでもこの記法を使いロジックを記述することができます。


### トランスコンパイラの言語仕様

たいへんお手数ですがこちらの記事をご参照ください。本試作が実装しているのは全体仕様の一部です。

https://qiita.com/mylifewithviolin/items/c3aff020a6831e6ae848

# 実行結果

## 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.86.1
C# 12 
dotnet-sdk-8.0.206-win-x64

### VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

## トランスコンパイラの出力コード
C#で実装されたソースをコンパイル実行します。ビルド（コンパイル）はVSCodeのタスクで実行しました。ターゲット言語のソースコードは実行時にファイルから読み込みます。

実行環境はWindows11上のVSCodeのターミナルです。
デバッグ用に最終トランスコンパイルソースコードの他、中間状態の分析結果も出力しています。実際はソースコードオリジナル出力というのが冒頭に出力されるのですが、そちらは記載を割愛しています。

ターゲット言語のトランスコンパイル後のソースコードはファイルでも出力されます。

#### VB.NET
```mind:vb.net
************ソースコードノード判定出力*********************
名前空間 HelloWorld                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Program                              ND_JDC_MIDLE//JavaDoc備考途中
*/                              ND_JDC_END JavaDoc備考終了
モジュール プログラム型                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Main                              ND_JDC_MIDLE//JavaDoc備考途中
* @param 引数 args                              ND_JDC_PARAM//JavaDoc備考変数
*/                              ND_JDC_END JavaDoc備考終了
void メイン(string[] 引数)                              ND_DEF_BEGIN//定義開始
コンソール.一行表示する("Hello World!")                              ND_EXE_BEGIN//実行開始
                              ND_DEF_END//定義終了
                              ND_DEF_END//定義終了
                              ND_DEF_END//定義終了
                              インポートする System                              ND_QAT_BEGIN//引用開始
public static class コンソール Console                              ND_QAD_BEGIN//引用定義開始
public static 一行表示する(string? value)                              ND_QAD_BEGIN//引用定義開始
WriteLine (string? value)                              ND_QAD_MIDLE//引用定義中
                              ND_QAD_END//引用定義終了
                              ND_QAD_END//引用定義終了

************nameDictionary出力***************************
Key:名前空間 Value:Namespace
Key:クラス Value:Class
Key:モジュール Value:Module
Key:インポートする Value:Imports
Key:void Value:Sub
Key:プログラム型 Value:Program
Key:引数 Value:args
Key:メイン Value:Main
Key:コンソール Value:Console
Key:一行表示する Value:WriteLine

No matching parameters found.
No matching parameters found.
Extracted Parameters: string[] args
Parameters:string[] args

************トランスコンパイル後ソースコード出力************
Imports System
Namespace HelloWorld

    ''' <summary>プログラム型</summary>
    Module Program


        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Sub Main(ByVal args As String())


            Console.WriteLine("Hello World!")
        End Sub

    End Module

End Namespace

プログラム '[11936] remind.dll' がコード 0 (0x0) で終了しました。
```
# 実行結果の実行結果

#### VB.NET
VB.NETの出力コードの実行結果はVSCodeのコンパイル環境でビルド・実行しました。デバッグコンソールに「Hello World!」出力されています。
```:
Hello World!
プログラム '[10784] HelloWorld.dll' がコード 0 (0x0) で終了しました。
```


# ソースコード
GitHub [Commit 0a63fb1](https://github.com/mylifewithviolin/remind/commit/0a63fb1b7fb9846315d9e5f76403b7ce3adc7eee)

#### target\vb\TargetVb.cs
VB言語の場合、定義の終端が「End 〇〇〇」のように定義のタイプによって変化しますので、定義文の解析段階でスタックに終端種類を積むようにしています。
また、引数の変数名と型名の語順が他のターゲット言語と異なっているため変換するようにしました。

```cs:target\vb\TargetVb.cs
namespace remind.target.vb
{
    public  partial  class TargetVb
    {
        // /////他のターゲット言語と共通部分は略しています。/////
        
        // ターゲットソース行の終端種類
        private class TargetSourceEndKind{
            public const string NameSpace ="Namespace";
            public const string Module ="Module";
            public const string Class ="Class";
            public const string SubRoutine ="Sub";
            public const string Function ="Function";
        }
        // ターゲットソース行の引数型種類
        private class ParameterInfo
        {
            public string? Name { get; set; }
            public string? Type { get; set; }
            public string? Modifier { get; set; } //ref, out, none
        }
    }
}
```

#### target\vb\Transcompile.cs
定義開始文の変換段階でスタックに終端種類を積むようにして、定義終了文の変換時にスタック情報から終端の文を変換しています。
また、引数の変数名と型名の語順が他のターゲット言語と異なっている点の変換も定義開始文の変換段階で対応するようにしました。

```cs:target\vb\Transcompile.cs
using System.Text.RegularExpressions;

namespace remind.target.vb;

public partial class TargetVb
{
    
        /// <summary>トランスコンパイルする</summary>
        /// <param name="soruce">ソース</param>
        /// <param name="sourcesLineList">ソースライン型リスト</param>
        /// <param name="nameDictionary">名称辞書</param>
        private static int transcompile(List<SourceLines> sourcesLineList,List<TargetSourceLines> targetSourcesLineList,
                                            Dictionary<string, string> nameDictionary){
            int ret=1;//初期値 1:失敗
            int targetSouceLineNumber=0;
            var endKindStack = new Stack<string>(); // VBの場合はスタックで終端のタイプを追跡
            var typeNameDictionary = initTypeNameDictionary();//変数型名辞書の初期化

            for(int i=0;i<sourcesLineList.Count;i++){
                SourceLines sourceLines =sourcesLineList.ElementAt(i);
                var nodeKind =sourceLines.nodeKind;
                
                switch(nodeKind){
                case NodeKind.ND_DEF_BEGIN://定義開始
                    ret=generateTargetSouceLine(sourceLines,targetSourcesLineList,nodeKind,nameDictionary,typeNameDictionary,endKindStack,ref targetSouceLineNumber);
                    break;
                    
            // /////他のターゲット言語と共通部分は略しています。/////
            
                    //行レベルカテゴライズ済のため例外は生じない
                }
            }
            ret=0;//ここまで進行したら成功
            return ret;
        }


        /// <summary>ターゲットソース行を生成する</summary>
        /// <param name="sourceLines">ソースライン型変数</param>
        /// <param name="nameDictionary">名称辞書</param>
        /// <param name="typeNameDictionary">変数型名辞書</param>
        /// <param name="endKindStack">終端種類</param>
        /// <param name="targetSouceLineNumber">ターゲットソース行番号</param>
        private static int generateTargetSouceLine(SourceLines sourceLines,List<TargetSourceLines> targetSourcesLineList,NodeKind nodeKind,
        Dictionary<string, string> nameDictionary,Dictionary<string, string> typeNameDictionary,Stack<string> endKindStack,ref int targetSouceLineNumber){
            int ret=1;//初期値 1:失敗
            var targetSourceLines =new TargetSourceLines();
            var sourceLineString=sourceLines.lineStrings ?? "";
            switch(nodeKind){
            case NodeKind.ND_DEF_BEGIN://定義開始
                targetSouceLineNumber+=1;
                targetSourceLines.sourceLineNumber=sourceLines.sourceLineNumber;
                var targetSourceCode=nameDictionaryReplase(nameDictionary,sourceLineString);//名称辞書で置換する
                targetSourceCode=generateParameterList(targetSourceCode,typeNameDictionary);
                targetSourceLines.targetLineStrings=targetSourceCode;
                targetSourceLines.targetSourceLineNumber=targetSouceLineNumber;
                targetSourcesLineList.Add(targetSourceLines);
                JugdeEndKind(targetSourceLines.targetLineStrings,endKindStack);

                targetSouceLineNumber+=1;
                targetSourceLines =new TargetSourceLines();
                targetSourceLines.sourceLineNumber=sourceLines.sourceLineNumber;
                targetSourceLines.targetLineStrings=TargetSourceLineNodeKind.DefBeginNote+Environment.NewLine;//定義開始 中かっこ{を追加　VBはなし
                targetSourceLines.targetSourceLineNumber=targetSouceLineNumber;
                targetSourcesLineList.Add(targetSourceLines);
                break;
            case NodeKind.ND_DEF_END://定義終了
                targetSouceLineNumber+=1;
                var endKind = " ";
                if(endKindStack!=null) endKind+= endKindStack.Pop();
                targetSourceLines.sourceLineNumber=sourceLines.sourceLineNumber;
                targetSourceLines.targetLineStrings=TargetSourceLineNodeKind.DefEndNote + endKind;//定義終了 中かっこ}を追加
                targetSourceLines.targetLineStrings+=Environment.NewLine;//定義終了 中かっこ}を追加
                targetSourceLines.targetSourceLineNumber=targetSouceLineNumber;
                targetSourcesLineList.Add(targetSourceLines);
                break;

            // /////他のターゲット言語と共通部分は略しています。/////
            }

            ret=0;//ここまで進行したら成功
            return ret;
        } 
        /// <summary>終端種類を判定する</summary>
        /// <param name="targetLineString">ターゲットライン文字列</param>
        /// <param name="endKindStack">終端種類</param>
        private static void JugdeEndKind(string targetLineString,Stack<string> endKindStack){
            if(targetLineString.IndexOf(TargetSourceEndKind.NameSpace)>=0){
                endKindStack.Push(TargetSourceEndKind.NameSpace);
            }else if(targetLineString.IndexOf(TargetSourceEndKind.Module)>=0){
                endKindStack.Push(TargetSourceEndKind.Module);
            }else if(targetLineString.IndexOf(TargetSourceEndKind.Class)>=0){
                endKindStack.Push(TargetSourceEndKind.Class);
            }else if(targetLineString.IndexOf(TargetSourceEndKind.Function)>=0){
                endKindStack.Push(TargetSourceEndKind.Function);
            }else if(targetLineString.IndexOf(TargetSourceEndKind.SubRoutine)>=0){
                endKindStack.Push(TargetSourceEndKind.SubRoutine);
            }
            return;
        }
        
        private static string generateParameterList(string sourceCode , Dictionary<string, string> typeNameDictionary){
            // 関数定義の引数部分を抽出する正規表現
            string pattern = @"\(([^)]*)\)"; // 括弧内の内容をキャプチャ
            Match match = Regex.Match(sourceCode, pattern);

            if (match.Success)
            {
                string parameterList = match.Groups[1].Value; // 括弧内の文字列
                Console.WriteLine("Extracted Parameters: " + parameterList);

                // 各引数を分割して配列にする
                var parameters = parameterList.Split(',');
                Console.Write("Parameters:");
                var parameterInfo=new List<ParameterInfo>();
                foreach (string parameter in parameters)
                {
                    Console.WriteLine(parameter.Trim()); // 空白を取り除く
                    var parames = parameter.Split(' ');
                    var paramInfo = new ParameterInfo(){
                        Name=parames.Length==2 ?parames[1]:parames[2],
                        Type=parames.Length==2 ?parames[0]:parames[1],
                        Modifier=parames.Length==2 ? "":parames[0],
                    };
                    parameterInfo.Add(paramInfo);
                }
                var newParameterList=convertParameterList(parameterInfo, typeNameDictionary);
                return sourceCode.Replace(parameterList,newParameterList);

            }
            else
            {
                Console.WriteLine("No matching parameters found.");
            }
            return sourceCode;
        }
        private static string convertParameterList(List<ParameterInfo> parameters, Dictionary<string, string> typeNameDictionary)
        {
            return string.Join(", ", parameters.Select(param =>
            {
                var vbType = param.Type!=null ? typeNameDictionary.ContainsKey(param.Type) ? typeNameDictionary[param.Type] : param.Type : "";
                var modifier = param.Modifier == "ref" || param.Modifier == "out" ? "ByRef" : "ByVal";
                return $"{modifier} {param.Name} As {vbType}";
            }));
        }
}
```
# おわりに
いかがでしたでしょうか？たいしたことはできていないのですが、ソースコード量が意外とちょっと多いです。もうちょいで各言語の制御構文に対応できそうな気もしていますが、完成までは自転車でアルファケンタウリや観測可能な宇宙の範囲の淵まで移動しようとしている気分です:joy:　とりあえずステップバイステップで進みます。:alarm_clock:
