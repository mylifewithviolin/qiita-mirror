# はじめに
日本語プログラミング言語Mindのバージョン９のVSCode用言語サーバー(LSP)を実装してみます。本記事はその最初のステップで、この記事でLSPができているわけではありません。

## 採用工法
工法は日本語プログラミング言語あおいコンパイラの開発と同様AIドリブンな感じでいきます。自力では完全には実装できないのでAIだのみではありますが、大枠の適切な進め方は理解しているという前提です。(VSCode拡張でシンタックスハイライトやスニペットは自力で実装可能でその自スキルを背景にAIで拡張していきます。）

https://qiita.com/mylifewithviolin/items/66632e23fa7394e669bc

# ステップ１　日本語プログラミング言語Mind９の言語ヘルプをmarkdownにしておく
markdown形式は人間が読むときはhtmlほど美麗に体裁が整うわけではないので、そっちを期待するとこんなのやとなりますが、今日のAI伴奏開発では必須といえるファイル形式です。というわけで、最初のステップはEUCエンコードで記述されたhtmlをUTF-8のmdに変換します。
```cmd
C:\developments\vscode\mind9languagespec\doc>dir *.html

2026/08/02  17:59             2,952 00-Cover.html
2026/08/02  17:59             9,338 00-Introduction.html
2026/08/02  17:59            19,464 01-Mechanism.html
2026/08/02  17:59            55,895 02-Program-Hyoki.html
2026/08/02  17:59            50,682 03-Control-syntax.html
2026/08/02  17:59            50,376 04-Data-and_variable.html
2026/08/02  17:59            17,814 05-Array.html
～略～
2026/08/02  17:59            27,296 indexBase.html
2026/08/02  17:59            72,638 indexGUI.html
2026/08/02  17:59            10,852 indexOperation.html
2026/08/02  17:59             4,183 operation-0-Welcome.html
2026/08/02  17:59             2,210 operation-1-Install-windows.html
2026/08/02  17:59             4,875 operation-2-Directory.html
2026/08/02  17:59            71,414 operation-3-Introduction.html
2026/08/02  17:59            19,493 operation-4-OtherTools.html
2026/08/02  17:59            15,836 operation-4-Tools.html
2026/08/02  17:59            10,861 operation-5-package-userprogs.html
2026/08/02  17:59            15,234 operation-6-SamplePrograms.html
              48 個のファイル           1,600,253 バイト
```

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができて結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

## Microsoft Copilotとの事前準備
### プロンプト
>数が多いのでフォルダを指定するとそのフォルダ内のeucのhtmlを同名のmdに連続変換するskillを作成したいです。文字コードがeucのhtmlをutf-8のmarkdownに変換します。

#### 生成レスポンス
>Node.js Skill を “最小クレジット消費で CodeAgent に実行させるための最適プロンプト” は、以下の 1 本で完成します。

>以下の Node.js スクリプトを Copilot Skill として登録し、
フォルダ内の EUC-JP HTML を UTF-8 Markdown に連続変換できるようにしてください。
>
>--- Skill 名 ---
convert-euc-html-to-md
>
>--- Skill コード ---
```typescript
import fs from "fs";
import path from "path";
import iconv from "iconv-lite";
import TurndownService from "turndown";

export async function convertFolderEucHtmlToMd(folderPath) {
    const turndown = new TurndownService();
    const files = fs.readdirSync(folderPath);

    for (const file of files) {
        if (!file.toLowerCase().endsWith(".html")) continue;

        const fullPath = path.join(folderPath, file);
        const eucData = fs.readFileSync(fullPath);
        const utf8Html = iconv.decode(eucData, "EUC-JP");
        const md = turndown.turndown(utf8Html);

        const outPath = path.join(
            folderPath,
            file.replace(/\.html$/i, ".md")
        );

        fs.writeFileSync(outPath, md, "utf8");
    }

    return "すべての HTML を Markdown に変換しました。";
}
```
>
>--- 依存ライブラリ ---
npm install iconv-lite turndown
>
>--- 実行 ---
```typescript
/skill convert-euc-html-to-md
{
  "folderPath": "C:/work/euc_html"
}
```
>
>既存コードは保持し、差分生成を使って最小のクレジット消費で処理してください。
Skill 登録 → 依存インストール → 実行までを 1 セッション内で行ってください。

フォルダパスは前記環境にあわせて下記のように書き換えます。
```typescript
  "folderPath": "C:\developments\vscode\mind9languagespec\doc"
```

## GitHub Copilot
Microsoft Copilotが生成したGitHub Copilotへのプロンプトを実行した結果、下記のmdファイルが生成されました。
```cmd
C:\developments\vscode\mind9languagespec\doc>dir *.md

2026/09/19  09:06             2,359 00-Cover.md
2026/09/19  09:25            10,883 00-Introduction.md
2026/09/19  09:25            17,113 01-Mechanism.md
2026/09/19  09:25            49,696 02-Program-Hyoki.md
2026/09/19  09:25            46,421 03-Control-syntax.md
2026/09/19  09:25            44,144 04-Data-and_variable.md
2026/09/19  09:25            14,196 05-Array.md
～略～
2026/09/19  09:18            16,196 indexBase.md
2026/09/19  09:18            39,498 indexGUI.md
2026/09/19  09:18             5,317 indexOperation.md
2026/09/19  09:25             3,661 operation-0-Welcome.md
2026/09/19  09:25               679 operation-1-Install-windows.md
2026/09/19  09:25             3,612 operation-2-Directory.md
2026/09/19  09:25            69,168 operation-3-Introduction.md
2026/09/19  09:25            18,029 operation-4-OtherTools.md
2026/09/19  09:25            13,591 operation-4-Tools.md
2026/09/19  09:25             9,956 operation-5-package-userprogs.md
2026/09/19  09:25            13,195 operation-6-SamplePrograms.md
              48 個のファイル           1,290,173 バイト
```

## Microsoft Copilotとの事前準備２
### プロンプト
>mdへの変換が完了しました。クレジット消費は２％でした。リンクの拡張子がhtmlのままなのでhtmlが開いてしまいます。生成されたすべてのmdのリンクファイルの拡張子をmdに変換させるクレジット最小のプロンプトをおしえてください。

#### 生成レスポンス
>新しい Skill を作らず、既存 Skill に “リンク拡張子置換専用の軽量処理” を追加実行するだけが最も軽いです。
>
>フォルダ内のすべての .md ファイルを対象に、
Markdown 内のリンクの拡張子 .html を .md に置換してください。
>
>既存の Skill やコードは変更せず、追加の軽量処理として実行してください。
>
>対象フォルダ:
C:/developments/vscode/mind9languagespec/doc/euc_html_md
>
>処理内容:
>- .md ファイルを読み込む
>- 正規表現でリンクの .html を .md に置換する
>- 同じファイル名で上書き保存する
>- 正規表現でリンク部分の .html を .md に置換する
>  例: [[索引へ](image/foo.png)](indexGUI.html#chapter_34)
>      → [[索引へ](image/foo.png)](indexGUI.md#chapter_34)
>- 同じファイル名で上書き保存する
>
>クレジット消費を最小にするため、Skill の再登録や npm install は行わず、
>既存環境での追加実行のみを行ってください。

## GitHub Copilot
Microsoft Copilotが生成したGitHub Copilotへのプロンプトを実行した結果、無事にすべてのリンクはmdへつながるようになりました。

![mindhelpmd.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/0c6e0f6e-40d6-4d3e-b59a-5a0a26a56b65.jpeg)


## 本ステップの評価
とりあえずMind9の言語仕様情報をmarkdownに変換できました。OKです。

# おわりに
もともとAIがオンラインの情報だけから日本語プログラミング言語のソースコードを生成すると、どの日本語プログラミング言語のソースコードであるかもよくわからない疑似言語状態を生成してくるハルシネーションがひどい印象でした。そこでGitHub Copilotのようなローカルの参照情報を確実に指定できる昨今のエージェントならば各日本語プログラミング言語の言語仕様に沿ったコード生成ができそうな気がしましたので、まずはMindの言語仕様をmarkdown化してなにか生成してみようと思っていたのですが、この過程でLSPもできますよとMicrosoft Copilotが提案してきたので、それにのっかってみることにしました。次回ステップは未定です。

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[^3]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
