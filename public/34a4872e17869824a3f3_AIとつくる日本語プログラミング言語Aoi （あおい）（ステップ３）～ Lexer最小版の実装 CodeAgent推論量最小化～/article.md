# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）開発コード名（Re:Mind）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではLexerの最小版を実装します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。実装しなくなったSE向け用途を想定しています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[前回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の開始です。Lexerの最小版を実装します。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
### 1. Lexer タスク
- Re:Mind の予約記号を識別できるようにする
  - `・`、`□`、`◇`、`〇`、`▽`、`△`、`▲`、`■`、`▼`
- 文字列・数値・識別子・演算子をトークンとして分解できるようにする
- コメントと Javadoc 風コメントをトークン化できるようにする
- 文字列リテラルや改行・空白の扱いを定義する

## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 0-1,2,3 が完了しました。Phase 1（Lexer）の具体的な進め方をご提案してください。

#### 生成レスポンス１
>Re:Mind の Lexer は「日本語識別子」「□ ◇ 〇 などの記号構文」「独自の予約語」が混在するため、
一般的な言語より 設計が重要で、実装は小さく分割するのが最適です。
Step 1：TokenType を定義する（最初にやるべき）
　Lexer の最初の仕事は「どんなトークンを認識するか」を決めることです。
　✔ TokenType.cs を作成（小さな enum）
Step 2：Token クラスを作る（位置情報を持つ）
　Parser やエラー報告で必須になるため、
　Token は 行番号・列番号を持つ必要があります。
Step 3：Lexer の骨格を作る

上記のStep 3でCopilotが下記のLexer.csを生成したので、これはローカルに格納。
```cs:Lexer.cs
public class Lexer
{
    private readonly string _source;
    private int _index;
    private int _line = 1;
    private int _column = 1;

    public Lexer(string source)
    {
        _source = source;
    }

    public List<Token> Tokenize()
    {
        var tokens = new List<Token>();

        while (!IsEnd())
        {
            var token = NextToken();
            tokens.Add(token);
        }

        tokens.Add(new Token(TokenType.Eof, "", _line, _column));
        return tokens;
    }
}
```

>Step 4：NextToken() を「小さなタスク」に分割する（最重要）

### プロンプト２
>Step 3を完了しました。NextToken の各タスクを CodeAgent 用に最小化したプロンプトを作成してください。
#### 生成レスポンス２
NextToken の CodeAgent 用「最小タスク化プロンプト」完全版
>以下のテンプレートは、
Lexer.cs の NextToken() に差分追加するための CodeAgent 用プロンプトです。
>
>① 空白・改行のスキップ（最も軽いタスク）
以下は Lexer の仕様です。
NextToken() のうち「空白と改行をスキップする部分」だけを
既存の Lexer.cs に差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
② コメントのスキップ（// と / /）
NextToken() のうち「コメント（// と /* */）をスキップする部分」だけを
既存の Lexer.cs に差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。

AI的にはきっちり反復的にプロンプトを生成していますが、本記事的には以下同様で内容割愛しています。
>③ □ ◇ 〇 の判定（Re:Mind 特有記号）
④ 記号トークン（(){}[].,）の判定
⑤ 演算子（= + - * / %）の判定
⑥ 数値リテラルの読み取り
⑦ 文字列リテラルの読み取り（"..."）
⑧ 日本語識別子の読み取り（コンソール、一行表示する など
⑨ 英字識別子の読み取り（Console, WriteLine など）
⑩ 不明な文字のエラー処理
✔ CodeAgent を起動したら、この 10 個のタスクを順番に投げる
→ 起動コストを 1 回に抑えられる
→ 各タスクは非常に軽いのでクレジット消費が最小


## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 1　Step 4の各タスクの実行プロンプトを逐次実行した結果、下記のソースコードが生成されました。

```cs:Lexer.cs
// -----------------------------------------------------------------------------
// Re:Mind Language Lexer
// -----------------------------------------------------------------------------
// このファイルは Re:Mind 言語処理系の Phase 1（Lexer）に対応する実装です。
// ReMindSourceCode をトークン列へ変換する役割を持ち、
// 後続フェーズ（Parser → AST → IR → CodeGen）の基盤となります。
// 
// 主な構成:
//   - TokenType : Re:Mind の構文要素を表すトークン種別
//   - Token     : トークン本体（種別・文字列・行番号・列番号）
//   - Lexer     : 入力文字列を走査し、Token の列へ変換する字句解析器
//
// 特徴:
//   - 日本語識別子（例: コンソール, 一行表示する）をサポート
//   - Re:Mind 特有記号（□, ◇, 〇）を専用トークンとして扱う
//   - コメント（//, /* */）のスキップ処理
//   - 行番号・列番号を保持し、構文解析時のエラー報告に利用可能
//
// Phase 1 完了条件:
//   - ReMindSourceCode を Tokenize() に渡すと、正しいトークン列が得られる
//   - □コンソール.一行表示する(引数2) が適切なトークン列に分解される
//
// この Lexer は Phase 2（Parser）の入力として使用されます。
// -----------------------------------------------------------------------------

using System;
using System.Collections.Generic;

namespace ReMindParser
{
    public enum TokenType
    {
        Identifier,
        Number,
        String,
        Keyword,
        Symbol,
        Operator,
        Box,        // □
        Diamond,    // ◇
        Circle,     // 〇
        Comma,
        Dot,
        LParen,
        RParen,
        LBrace,
        RBrace,
        LBracket,
        RBracket,
        Assign,     // =
        Plus,
        Minus,
        Asterisk,
        Slash,
        Percent,
        Eof
    }

    public class Token
    {
        public TokenType Type { get; }
        public string Text { get; }
        public int Line { get; }
        public int Column { get; }

        public Token(TokenType type, string text, int line, int column)
        {
            Type = type;
            Text = text;
            Line = line;
            Column = column;
        }
    }

    public class Lexer
    {
        private readonly string _source;
        private int _index;
        private int _line = 1;
        private int _column = 1;

        public Lexer(string source)
        {
            _source = source;
        }

        public List<Token> Tokenize()
        {
            var tokens = new List<Token>();

            while (!IsEnd())
            {
                var token = NextToken();
                tokens.Add(token);
            }

            tokens.Add(new Token(TokenType.Eof, "", _line, _column));
            return tokens;
        }

        public Token NextToken()
        {
            while (!IsEnd())
            {
                var ch = Peek();

                if (ch == '/' && _index + 1 < _source.Length && _source[_index + 1] == '/')
                {
                    _index += 2;
                    _column += 2;
                    while (!IsEnd() && Peek() != '\n')
                    {
                        Advance();
                    }
                    continue;
                }

                if (ch == '/' && _index + 1 < _source.Length && _source[_index + 1] == '*')
                {
                    _index += 2;
                    _column += 2;
                    while (!IsEnd())
                    {
                        if (Peek() == '*' && _index + 1 < _source.Length && _source[_index + 1] == '/')
                        {
                            _index += 2;
                            _column += 2;
                            break;
                        }

                        Advance();
                    }
                    continue;
                }

                if (ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n')
                {
                    Advance();
                    continue;
                }

                break;
            }

            if (IsEnd())
            {
                return new Token(TokenType.Eof, "", _line, _column);
            }

            var currentChar = Peek();
            if (currentChar == '□')
            {
                Advance();
                return new Token(TokenType.Box, "□", _line, _column);
            }

            if (currentChar == '◇')
            {
                Advance();
                return new Token(TokenType.Diamond, "◇", _line, _column);
            }

            if (currentChar == '〇')
            {
                Advance();
                return new Token(TokenType.Circle, "〇", _line, _column);
            }

            if (currentChar == '(')
            {
                Advance();
                return new Token(TokenType.LParen, "(", _line, _column);
            }

            if (currentChar == ')')
            {
                Advance();
                return new Token(TokenType.RParen, ")", _line, _column);
            }

            if (currentChar == '{')
            {
                Advance();
                return new Token(TokenType.LBrace, "{", _line, _column);
            }

            if (currentChar == '}')
            {
                Advance();
                return new Token(TokenType.RBrace, "}", _line, _column);
            }

            if (currentChar == '[')
            {
                Advance();
                return new Token(TokenType.LBracket, "[", _line, _column);
            }

            if (currentChar == ']')
            {
                Advance();
                return new Token(TokenType.RBracket, "]", _line, _column);
            }

            if (currentChar == '.')
            {
                Advance();
                return new Token(TokenType.Dot, ".", _line, _column);
            }

            if (currentChar == ',')
            {
                Advance();
                return new Token(TokenType.Comma, ",", _line, _column);
            }

            if (currentChar == '=')
            {
                Advance();
                return new Token(TokenType.Assign, "=", _line, _column);
            }

            if (currentChar == '+')
            {
                Advance();
                return new Token(TokenType.Plus, "+", _line, _column);
            }

            if (currentChar == '-')
            {
                Advance();
                return new Token(TokenType.Minus, "-", _line, _column);
            }

            if (currentChar == '*')
            {
                Advance();
                return new Token(TokenType.Asterisk, "*", _line, _column);
            }

            if (currentChar == '/')
            {
                Advance();
                return new Token(TokenType.Slash, "/", _line, _column);
            }

            if (currentChar == '%')
            {
                Advance();
                return new Token(TokenType.Percent, "%", _line, _column);
            }

            if (char.IsDigit(currentChar))
            {
                var startLine = _line;
                var startColumn = _column;
                var numberText = string.Empty;

                while (!IsEnd() && char.IsDigit(Peek()))
                {
                    numberText += Peek();
                    Advance();
                }

                return new Token(TokenType.Number, numberText, startLine, startColumn);
            }

            if (currentChar == '"')
            {
                var startLine = _line;
                var startColumn = _column;
                var stringText = string.Empty;

                Advance();
                while (!IsEnd() && Peek() != '"')
                {
                    stringText += Peek();
                    Advance();
                }

                if (!IsEnd())
                {
                    Advance();
                }

                return new Token(TokenType.String, stringText, startLine, startColumn);
            }

            if (char.IsLetter(currentChar))
            {
                var startLine = _line;
                var startColumn = _column;
                var identifierText = string.Empty;

                while (!IsEnd() && char.IsLetter(Peek()))
                {
                    identifierText += Peek();
                    Advance();
                }

                return new Token(TokenType.Identifier, identifierText, startLine, startColumn);
            }

            throw new InvalidOperationException($"Unexpected character '{currentChar}' at line {_line}, column {_column}.");
        }

        private bool IsEnd()
        {
            return _index >= _source.Length;
        }

        private char Peek()
        {
            return _source[_index];
        }

        private void Advance()
        {
            if (IsEnd())
            {
                return;
            }

            if (_source[_index] == '\n')
            {
                _line++;
                _column = 1;
            }
            else
            {
                _column++;
            }

            _index++;
        }
    }
}
```
## 本ステップの評価
わるくないと評価しています。まだ当初の不具合解消にいたっておりませんが、急がば回れということで次回Parserの実装に進行します。

# おわりに
以上です。次回の方向性はParserの実装の実行からとなります。なるべくサンプルソースに対して実行できる状況づくりを急ぎます。

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
「Re:Mindをいじりたおす」の記事リストです。（ステップ降順）
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[ステップ２５ ターゲット言語C#へのASTからの生成処理](https://qiita.com/mylifewithviolin/items/13d78530f2b7d8895502)
[ステップ２４ ASTを生成するサンプル実装をC#で生成](https://qiita.com/mylifewithviolin/items/e9589fc28b077ab46fa5)
[ステップ２３ マッピングルール生成](https://qiita.com/mylifewithviolin/items/f446a20ee2f6a71b65c4)
[ステップ２２ AST（抽象構文木）風の構造化表示](https://qiita.com/mylifewithviolin/items/9079f80873875fbedd44)
[ステップ２１ バブルソート 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/94a8b69c9c467497e1e6)
[ステップ２０ 二分探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/2902026b161c10bfb6a3)
[ステップ１９ 線形探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/5d2466574f9d6fbbaa59)
[ステップ１８ バブルソート １案件づつやりなおし](
https://qiita.com/mylifewithviolin/items/d1e346f83d98381c3a9e)
[ステップ１７ 二分探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/baeb565cf8378106b5c2)
[ステップ１６ 線形探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/b503e16aacbdba6c59c4)
[ステップ１５ ３つの定番アルゴリズムソースの忘却原因調査](https://qiita.com/mylifewithviolin/items/2859b860bc96a5887f83)
[ステップ１４ バブルソートソースの忘却発生再確認](https://qiita.com/mylifewithviolin/items/4e0761c28d91ff66a507)
[ステップ１３ 二分探索法ソースの忘却発生](https://qiita.com/mylifewithviolin/items/11d9f898474eb895c049)
[ステップ１２ 線形探索法の６言語変換](https://qiita.com/mylifewithviolin/items/bff13bbeb71163fcf2d7)
[ステップ１１ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/2fb2909efbbfe9ee20f9)
[ステップ１０ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/3c5467b0b6b59e6d8c01)
[ステップ９ バージョン情報付きで３定番アルゴリズムソースの生成](
https://qiita.com/mylifewithviolin/items/55fdb18e72bac7e99c1d)
[ステップ８ バージョニングが可能か確認](
https://qiita.com/mylifewithviolin/items/fbc80e45d927000af85a)
[ステップ７ Re:Mindの詳しい言語仕様の学習結果をバブルソートで確認](https://qiita.com/mylifewithviolin/items/99b52bcba7a41b459d31)
[ステップ６ Re:Mindの詳しい言語仕様の学習結果を二分探索法で確認](https://qiita.com/mylifewithviolin/items/cf41523b54887e638363)
[ステップ５ Re:Mindの詳しい言語仕様の学習結果を線形探索法で確認](https://qiita.com/mylifewithviolin/items/c0e912c98375ab72f09e)
[ステップ４ Re:Mindの詳しい言語仕様の学習成果を保持するスコープを確認](https://qiita.com/mylifewithviolin/items/d17dbd2daff7486bc034)
[ステップ３ Re:Mindの詳しい言語仕様を学習できる方法を確認](https://qiita.com/mylifewithviolin/items/79c7be1247521f1a8eed)
[ステップ２ Re:Mindの言語仕様の認知度を確認](https://qiita.com/mylifewithviolin/items/edebd6042808892f50af)
[ステップ１ Re:Mindの認知度を確認](https://qiita.com/mylifewithviolin/items/68376e6375b63e361b51)
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
「Re:MindのASTパーサが動作するまで」の記事リストです。（ステップ降順）
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[ステップ１１](
https://qiita.com/mylifewithviolin/items/9c891cdcc8d2bd78f36f)
[ステップ１０ 生成済コードの伝達完了](
https://qiita.com/mylifewithviolin/items/a0b5747e40e7b545175a)
[ステップ９](
https://qiita.com/mylifewithviolin/items/f34548d50a974fb4420e)
[ステップ８](
https://qiita.com/mylifewithviolin/items/cb8f54f87329d7e62c9a)
[ステップ７](https://qiita.com/mylifewithviolin/items/1e05c80a0cad0580f073)
[ステップ６ 生成済コードの伝達開始](https://qiita.com/mylifewithviolin/items/31e8413e0789e5433705)
[ステップ５](https://qiita.com/mylifewithviolin/items/2af14676b1c267af22a2)
[ステップ４ Program.csが動作](https://qiita.com/mylifewithviolin/items/b037019608d6b5d068a7)
[ステップ３](https://qiita.com/mylifewithviolin/items/7c9568d238550b997e21)
[ステップ２](https://qiita.com/mylifewithviolin/items/076e1a792b8545fae7a6)
[ステップ１ 検証環境構築](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)
[^3]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
「Re:MindのC#コード生成が動作するまで」の記事リストです。（ステップ降順）
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
[ステップ３](https://qiita.com/mylifewithviolin/items/9f8082ae6629c9d8e35a)
[ステップ２](https://qiita.com/mylifewithviolin/items/bcb4b56688101463937c)
[ステップ１](https://qiita.com/mylifewithviolin/items/54e3c7cdd2757b694f79)
