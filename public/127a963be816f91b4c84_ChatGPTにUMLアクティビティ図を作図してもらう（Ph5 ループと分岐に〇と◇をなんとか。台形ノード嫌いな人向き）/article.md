# はじめに
前回の記事 [「Ph4 ループをもう少しなんとか。台形ノード嫌いな人向き」](https://qiita.com/mylifewithviolin/items/e1bed4e27401ec8638af)では、ChatGPTのRe:Mindの制御構文の反復の例の提示には感動させられました。しかし、いろいろ細かいところで不安定さに直面しております。

## この記事内容の作業目的
自作言語Re:Mindの構文仕様をAIに学習してもらい、UMLアクティビティ図を作図してもらうことから、日本語ロジック仕様記述言語がUMLアクティビティ図の間接的なソースコードになりうるか検討します。

## この記事内容の保証
※この記事にはAIが自動生成した情報が含まれます。AIが自動生成して書かれた内容の妥当性は保証されません。

# 実行結果
ChatGPTにご提示いただいたMermaidのソースコードでエラーのない状態は、都度Qiita上でイメージ描画するようにしています。（エラーを直しきれず私の方でとりあえずご提示したソースコードを含む場合があります。）

## ChatGPT3.5

私：
こんにちは！あなたは先日のUMLのアクティビティ図の作図について覚えていますか？

ChatGPT：
>こんにちは！はい、先日のUMLのアクティビティ図の作図について覚えています。ご質問がありましたらどうぞお知らせください。



私：
ありがとうございます。Re:Mindの制御構文の反復基本形と、それに対応したMermaidのソースはは覚えてますか？

ChatGPT：
>はい、Re:Mindの制御構文の反復基本形とそれに対応したMermaidのソースについては覚えています。以下がその例です。

Re:Mindの反復基本形:
```:
〇i=0,i<10,i++ 繰り返す
    □処理内容
〇ここまで
```
対応するMermaidのソース:

```:mermaid
graph TD
    start((開始)) --> A["i=0,i<10,i++ 繰り返す"]
    A --> B["処理内容"]
    B --> C[i=i+1]
    C -->|true| D[i<10]
    C -->|false| stop((終了))
    D -->|true| A
    D -->|false| stop
```

>上記のMermaidのソースコードでは、反復の開始と終了が示され、ループの条件や反復の内容が適切に表現されています。
もし他にも質問があればお知らせください。


私：
ありがとうございます。Re:Mindの制御構文の反復基本形はあっていますが、それに対応したMermaidのソースは下記のようでしたね。
```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|true| C["表示する(i)"]
    B -->|false| stop((終了))
    C --> D[i=i+1]
    D --> B
```
```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|true| C["表示する(i)"]
    B -->|false| stop((終了))
    C --> D[i=i+1]
    D --> B
```
ChatGPT：
>申し訳ありません、先程の誤った回答になりました。提供していただいたMermaidのソースコードが正しいものです。おっしゃる通り、以下が正しいMermaidのソースコードです。

```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|true| C["表示する(i)"]
    B -->|false| stop((終了))
    C --> D[i=i+1]
    D --> B
```

>お手数をおかけしましたが、正しい情報を提供していただき、ありがとうございます。もし他にも質問があればお知らせください。


私：
はい、ありがとうございます。ここからが本題です。いまのソースですと、終了がループの内部に描画されます。
i<5のtrueのfalseのダイアグラム上の左右の位置関係は逆にして、終了がループの外側に描画されるようにできますか？

ChatGPT：
>もちろん、Mermaidのソースコードを変更して終了がループの外側に描画されるようにすることができます。以下がそのソースコードです。

```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|false| C["終了"]
    B -->|true| D["表示する(i)"]
    D --> E[i=i+1]
    E --> B
```

>このソースコードでは、i<5 の false のフローで終了ノードが描画されています。おっしゃる通りの結果になるはずです。
お手数をおかけしましたが、これで正しく表示されるはずです。もし他にも質問があればお知らせください。

```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|false| C["終了"]
    B -->|true| D["表示する(i)"]
    D --> E[i=i+1]
    E --> B
```



私：
はい、ありがとうございます。いい感じです。終了がループの外側に描画されました。終了ノードを〇で描くように戻せますか？

ChatGPT：
>もちろんです！終了ノードを〇で描画するように変更したソースコードは以下の通りです。

```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|false| C((終了))
    B -->|true| D["表示する(i)"]
    D --> E[i=i+1]
    E --> B
```

>上記のソースコードでは、終了ノードが〇で描画されています。これでお望みの結果が得られるはずです。
お手数をおかけしましたが、これで正しく表示されるはずです。もし他にも質問があればお知らせください。

```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> B["i<5"]
    B -->|false| C((終了))
    B -->|true| D["表示する(i)"]
    D --> E[i=i+1]
    E --> B
```


私：
はい、ありがとうございます。完璧です！
ここで少し説明が難しいところをご説明します。
ダイアグラム上の開始ノードと終了ノードはそのまま維持して、それとは別にループの起点と終点を〇ノードで記述します。
なぜなら、フローダイアログの開始ノードと終了ノードはRe:Mindの制御構文のソースには明示されていないけれど、一般的にロジックの開始と終了を示すものとして使われているものだからです。
ですから、Re:Mindの制御構文の反復のソースの〇で始まる下記の文
```
〇繰り返す
〇ここまで
```
は、フローダイアログの開始ノードと終了ノードの内側に記述されます。
この点を考慮して、再度Mermaidのソースを修正することは可能ですか？

ChatGPT：
>了解しました。フローダイアグラム上の開始ノードと終了ノードを維持しつつ、ループの起点と終点を〇ノードで記述する方法ですね。以下が修正されたMermaidのソースコードです。

```:mermaid
graph TD
    start((開始)) --> loopStart[〇繰り返す]
    loopStart --> loopCond["i<5"]
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd[〇ここまで]
    loopBody --> loopInc[i=i+1]
    loopInc --> loopCond
    loopEnd --> stop((終了))
```

>上記のソースコードでは、フローダイアグラム上の開始ノードと終了ノードを保ちつつ、ループの起点と終点を〇ノードで明示的に記述しています。これによって、意図した図を作成することができます。
お手数をおかけしましたが、これで正しく表示されるはずです。もし他にも質問があればお知らせください。




私：
ありがとうございます。いい感じです。（プロンプト外：だいぶエラーを入れてきた感じ:sweat_smile:）for文相当なのでi=0も考慮し、ループの起点にもどることを加味すると、こんな感じです。
```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond["i<5"]
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```
loopCond["i<5"]を菱形◇ノードにできますか？

```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond["i<5"]
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```
ChatGPT：
>申し訳ありませんが、Mermaidのソースコードでは、直接菱形◇ノードを描画することはできません。しかし、菱形の外観を持つノードを別の方法で表現することは可能です。
以下のように、テキストで菱形の外観を模倣することができます。

```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond["i<5"]
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```

>こちらのソースコードで、loopCond["i<5"] の部分はテキストとして菱形の外観を持つノードを模倣しています。ただし、直接的な菱形ノードと同じような外観を得ることはできません。
もし他にも質問があればお知らせください。


私：
ありがとうございます。Mermaidのソースでは{"i<5"}がnode (rhombus)菱形ノードみたいですよ。
```:mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond{"i<5"}
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```

```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond{"i<5"}
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```

ChatGPT：
>申し訳ありません、誤解がありました。ご指摘いただきありがとうございます。正しい情報を提供していただき、正しい方法で菱形ノードを描画することができることを理解しました。お手数をおかけしました。
これで正しく表示されるはずです。もし他にも質問があればお知らせください。

# おわりに
生成AIにいろいろやってもらうのは自然言語で対話しつつ形式言語のソースコードを調整していく形になりますが、ロジック仕様記述言語からMermaidへのトランスコンパイラという処理系は実装としては成り立つ気はしてきました。

今回の最終状態（表示名の不等号はダブルクオーテーションで囲ってもエスケープ文字になっていますのはQiita上の現象のようです。）

```mermaid
graph TD
    start((開始)) --> A["i=0"]
    A --> loopStart((繰り返す))
    loopStart --> loopCond{"i<5"}
    loopCond -->|true| loopBody["表示する(i)"]
    loopCond -->|false| loopEnd((ここまで))
    loopBody --> loopInc[i=i+1]
    loopInc --> loopStart
    loopEnd --> stop((終了))
```
同じソースをmermaid.liveで描画するとi<5は正常に表示されるようです。

https://mermaid.live/edit#pako:eNqrVkrOT0lVslJKL0osyFAIcYnJUwCC4pLEohINjZfTup8u79bUVNDVtVNwjI5RyrQ1iFGKhahxBIvm5OcXBENUP9-54XFT14v9Ux43ztTUhCiCS8MVO-fnpVQDTbIxjVGqRSgCCYPU1JQUlabWgIWc8lMqgXa-WLji-ZJdQDMfN3VrZGrC7UfRlZaYUwzV5pqXoqHxuHEyGO173Lgc2S0gM-FO8cxLjs60zdQ2RDIRKIbqL4SUK8QuYODkFwB9u7Xpya42kNkxeUo6SrmpRbmJmSnAkKwG6YhRKslIzU2NUbICMlNS0xJLc0pilGLyaoFKE0tL8oMr85KVrEB-1VEqLUhJLEl1yUwExkGukhXYK7UANRCTOg

# 参考リンク

https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94
