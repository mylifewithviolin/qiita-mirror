# はじめに
日本語プログラミング言語Mindのバージョン９でAI仕様駆動開発とVibeコーディングのハイブリッド（っぽいこと）を行ってみます。

本記事はその後編で、[前編](https://qiita.com/mylifewithviolin/items/8065894b892ab9f69798)でAIが提案したMind９GUIミニゲームアプリの企画構想の３つの案のうちの１つのソースコード完成（正常実行）までです。いったんAIが実行する内容をスキル化するとかは仕様駆動開発っぽい要素を取り入れています。

# 使用AI
GitHub CopilotのPro+版。[^1]

## プロンプト（Mind９のGUIアプリを自己診断して完成させる）
>C:\developments\vscode\mind9-ai
こちらの
firework.src
を参考にして
flashgrid_diagnostic.logを
出力するようにして
読み取り判断することはできますか？
現在は起動はしますがエラーがでるようです。
エラーの内容を自力で診断できるようにできますか？

### 生成レスポンス
>まず、firework.src と現在の flashgrid.src の起動・エラー処理を比較し、診断ログの出力先や既存のログ形式も確認します。

・・・・

>対応しました。
firework.src を参考に、flashgrid.src に診断ログを追加しました。起動・ウィジェット作成／有効化／配置・ゲーム開始・タイマー・クリック・終了を記録し、検出可能な Mind エラーはエラー文字列と一緒に記録します。ログは起動時に作り直し、各記録をすぐファイルへ反映します。
>
>起動エラーの原因も確認できました。ラベルやボタンを有効化する前に格子配置していたため、「有効化されていないウィジェットを格子配置しようとしました」というエラーになっていました。有効化してから配置する順に修正しています。
>
>flashgrid_diagnostic.log に APP_READY、ゲーム開始、タイマー、クリック、終了まで記録されることを確認しました。診断ログの読み方はガイドにまとめています。

### 完了レポート

```md:
# 光るマスをねらえ 実装プラン完了レポート

## 実施結果

- `flashgrid.src`に3 x 3のボタン盤面、開始ボタン、得点表示、残り時間表示を実装。
- 開始後30秒間、正解セルを固定順で移動し、正解クリックで得点を加算する。
- 誤クリックでは得点・目標を変更せず、時間切れ後はセル操作を無効にする。
- タイマーは遅延実行で更新し、ゲーム状態が終了なら更新を継続しない。
- セル番号をイベント引数として渡し、共通のセル押下処理で判定する。

## 修正したコンパイルエラー

初回の`flashgrid.inf`は59行目で、`セル番号列`と`引数個数`が未定義として報告していた。イベント引数を受け取る行を宣言済みローカル変数の`＿セル番号列`と`＿引数個数`に修正した。

## 検証結果

- `flashgrid.src`のエラーチェック: 問題なし。
- Mind9で再ビルド後、`flashgrid.exe`が生成され、以前のコンパイルエラー記録`flashgrid.inf`はなくなった。
- `flashgrid.exe`の起動コマンドを実行した。
- VS Codeの統合端末が利用できず、画面上での盤面表示・クリック操作・30秒経過の手動確認はできていない。
```

# 修正されたソースコード
診断ログ出力機能が残った状態です。このデバッグ用のログ機能を手書きで埋め込んで後で消すというのを手作業でやると、うっかりよけいなことをやってしまいそうですね。今回はそのようにしていませんが、完動が確認されたら診断機能は消してくださいというのも手順としてはよいかもです。

```mind:flashgrid.src
セルボタン数は　定数　９個。
セルボタン群は　セルボタン数の　ＩＤ。
セル番号文字列は　文字列定数配列
	"1"　"2"　"3"
	"4"　"5"　"6"
	"7"　"8"　"9"
	。

ゲーム中は　変数。
目標セルは　変数。
得点は　変数。
残り秒は　変数。

スコアラベル記憶は　ＩＤ。
時間ラベル記憶は　ＩＤ。
開始ボタン記憶は　ＩＤ。
得点表示文は　文字列実体　長さ　２００桁。
時間表示文は　文字列実体　長さ　６０桁。
診断ログは　ファイル。
診断ログ有効は　変数。

診断を記録するとは　（文字列　→　・）
        記録文は　文字列
        記録文に　入れる
        診断ログ有効が　１に　等しい？
                ならば
                        記録文を　診断ログに　一行書き込み
                        診断ログの　ファイルポインタを末尾に設定し
                        エラー？
                                ならば
                                        ０を　診断ログ有効に　入れ
                                        "DIAGNOSTIC_LOG_WRITE_FAILED"を　一行表示し
                                        エラー文字列を　一行表示し
                                        エラークリアし
                                つぎに
                つぎに。

診断エラーを記録するとは　（文字列　→　・）
        診断エラー文は　文字列
        処理名は　文字列
        処理名に　入れる
        エラー？
                ならば
                        エラー文字列を　診断エラー文に　入れ
                        エラークリアし
                        "ERROR: "と　処理名を　合成し　診断を記録し
                        診断エラー文を　診断を記録する
                つぎに。

診断ログを開始するとは
        １を　診断ログ有効に　入れ
        エラークリアし
        "flashgrid_diagnostic.log"で　診断ログを　新規オープンする
        エラー？
                ならば
                        ０を　診断ログ有効に　入れ
                        "DIAGNOSTIC_LOG_OPEN_FAILED"を　一行表示し
                        エラー文字列を　一行表示し
                        エラークリアし
                さもなければ
                        "APP_START"を　診断を記録する
                つぎに。

目標セルを表示とは　（・　→　・）
		＿セルは　ＩＤ
		＿回数は　変数
	　　セルボタン数を
	回数指定し
		回数を　＿回数に　入れ
		セルボタン群（＿回数）を　＿セルに　入れ
		"#d0d0d0"を　＿セルに　背景色を設定し
		＿セルを　変更を反映し
		繰り返し
	セルボタン群（目標セル）を　＿セルに　入れ
	"#ffe66d"を　＿セルに　背景色を設定し
	＿セルを　変更を反映する。

ゲーム終了とは　（・　→　・）
	"GAME_OVER"を　診断を記録する
	０を　ゲーム中に　入れ
	"TIME UP!"を　時間ラベル記憶に　テキストを設定し
	時間ラベル記憶を　変更を反映する。

時計更新とは　（引数１、引数２、・・、引数個数　→　・）
	イベント引数を捨て
	"TIMER_TICK"を　診断を記録する
	ゲーム中が　ゼロ以外
		ならば
			残り秒を　一つ減少し
			時間表示文を　一文字右側削除し
			残り秒が　ゼロ？
				ならば　ゲーム終了し
			さもなければ
				時間表示文を　時間ラベル記憶に　テキストを設定し
				時間ラベル記憶を　変更を反映し
				"TIME_LABEL_UPDATE"を　診断エラーを記録する
				１０００ミリと　時計更新の　実行情報と　空列で　遅延実行を予約する
			つぎに
		つぎに
	。

セル押下処理とは　（セル番号列、引数個数　→　・）
		＿セル番号列は　文字列
		＿引数個数は　変数
		＿セル番号は　変数
	＿セル番号列と　＿引数個数に　入れ
	ゲーム中が　ゼロ？
		ならば　終り
		つぎに
	＿セル番号列を　数値変換＋し　＿セル番号に　入れ
	"CELL_CLICK:"と　＿セル番号列を　合成し　診断を記録する
	＿セル番号が　目標セルに　等しい？
		ならば
			得点を　一つ増加し
			"*"を　得点表示文に　一文字追加し
			得点表示文を　スコアラベル記憶に　テキストを設定し
			スコアラベル記憶を　変更を反映し
			"SCORE_LABEL_UPDATE"を　診断エラーを記録する
			目標セルが　セルボタン数に　等しい？
				ならば　１を　目標セルに　入れ
			さもなければ
				目標セルを　一つ増加し
			つぎに
			目標セルを表示し
			"TARGET_CELL_UPDATE"を　診断エラーを記録する
		つぎに
	。

開始処理とは　（引数１、引数２、・・、引数個数　→　・）
	イベント引数を捨て
	ゲーム中が　ゼロ以外
		ならば　終り
		つぎに
	１を　ゲーム中に　入れ
	"GAME_START"を　診断を記録する
	１を　目標セルに　入れ
	０を　得点に　入れ
	３０を　残り秒に　入れ
	"SCORE: "を　得点表示文に　入れ
	"TIME: ##############################"を　時間表示文に　入れ
	得点表示文を　スコアラベル記憶に　テキストを設定し
	スコアラベル記憶を　変更を反映し
	時間表示文を　時間ラベル記憶に　テキストを設定し
	時間ラベル記憶を　変更を反映し
	目標セルを表示し
	"GAME_START_UI_UPDATE"を　診断エラーを記録する
	１０００ミリと　時計更新の　実行情報と　空列で　遅延実行を予約する
	"TIMER_SCHEDULE"を　診断エラーを記録する
	。

メインとは
		＿得点ラベルは　ＩＤ
		＿時間ラベルは　ＩＤ
		＿開始ボタンは　ＩＤ
		＿セルは　ＩＤ
		＿行は　変数
		＿列は　変数
		＿番号は　変数
	診断ログを開始する
	
	"SCORE_LABEL_CREATE_BEGIN"を　診断を記録する
	メインウィンドウで　ラベルのＩＤを取得し　＿得点ラベルに　入れ
	"SCORE_LABEL_CREATE"を　診断エラーを記録する
	"SCORE_LABEL_CREATED"を　診断を記録する
	"SCORE: "を　＿得点ラベルに　テキストを設定し
	＿得点ラベルを　スコアラベル記憶に　入れ
	"SCORE_LABEL_ENABLE_BEGIN"を　診断を記録する
	＿得点ラベルを　有効化し
	"SCORE_LABEL_ENABLED"を　診断エラーを記録する
	＿得点ラベルを　格子配置を準備し
	４と　１を　＿得点ラベルに　ウィジェットの位置を設定し
	"SCORE_LABEL_GRID_BEGIN"を　診断を記録する
	＿得点ラベルを　格子配置し
	"SCORE_LABEL_CONFIGURED"を　診断エラーを記録する

	"TIME_LABEL_CREATE_BEGIN"を　診断を記録する
	メインウィンドウで　ラベルのＩＤを取得し　＿時間ラベルに　入れ
	"TIME_LABEL_CREATE"を　診断エラーを記録する
	"TIME_LABEL_CREATED"を　診断を記録する
	"TIME: ##############################"を　＿時間ラベルに　テキストを設定し
	＿時間ラベルを　時間ラベル記憶に　入れ
	"TIME_LABEL_ENABLE_BEGIN"を　診断を記録する
	＿時間ラベルを　有効化し
	"TIME_LABEL_ENABLED"を　診断エラーを記録する
	＿時間ラベルを　格子配置を準備し
	４と　２を　＿時間ラベルに　ウィジェットの位置を設定し
	"TIME_LABEL_GRID_BEGIN"を　診断を記録する
	＿時間ラベルを　格子配置し
	"TIME_LABEL_CONFIGURED"を　診断エラーを記録する

	"GRID_BUTTONS_CREATE_BEGIN"を　診断を記録する
	メインウィンドウと　セルボタン数で　ボタンのＩＤを複数取得し
	セルボタン群に　複数のＩＤを配列に格納し
	"GRID_BUTTONS_CREATED"を　診断エラーを記録する
	"GRID_BUTTONS_READY"を　診断を記録する
	
	＿番号を　クリアし
	３行を
	回数指定し
		回数を　＿行に　入れ
		３列を
		回数指定し
			回数を　＿列に　入れ
			＿番号を　一つ増加し
			"CELL_WIDGET_SETUP_BEGIN"を　診断を記録する
			セルボタン群（＿番号）を　＿セルに　入れ
			" "を　＿セルに　テキストを設定し
			"#d0d0d0"を　＿セルに　背景色を設定し
			セル押下処理の　実行情報を　＿セルに　イベント処理を登録し
			セル番号文字列（＿番号）を　＿セルに　イベント引数を設定し
			"CELL_WIDGET_ENABLE_BEGIN"を　診断を記録する
			＿セルを　有効化し
			"CELL_WIDGET_ENABLED"を　診断エラーを記録する
			＿セルを　格子配置を準備し
			＿行と　＿列を　＿セルに　ウィジェットの位置を設定し
			"CELL_GRID_BEGIN"を　診断を記録する
			＿セルを　格子配置し
			"CELL_WIDGET_CONFIGURED"を　診断エラーを記録する
			繰り返し
		繰り返し

	"START_BUTTON_CREATE_BEGIN"を　診断を記録する
	メインウィンドウで　ボタンのＩＤを取得し　＿開始ボタンに　入れ
	"START_BUTTON_CREATE"を　診断エラーを記録する
	"START_BUTTON_CREATED"を　診断を記録する
	"START"を　＿開始ボタンに　テキストを設定し
	開始処理の　実行情報を　＿開始ボタンに　イベント処理を登録し
	"START_BUTTON_ENABLE_BEGIN"を　診断を記録する
	＿開始ボタンを　有効化し
	"START_BUTTON_ENABLED"を　診断エラーを記録する
	＿開始ボタンを　格子配置を準備し
	５と　２を　＿開始ボタンに　ウィジェットの位置を設定し
	"START_BUTTON_GRID_BEGIN"を　診断を記録する
	＿開始ボタンを　格子配置する
	"START_BUTTON_CONFIGURED"を　診断エラーを記録する
	"APP_READY"を　診断を記録する
	。
```
## 診断ログ
私が動かしてみたときの診断ログです。

```txt:flashgrid_diagnostic.log
APP_START
SCORE_LABEL_ENABLE_BEGIN
SCORE_LABEL_GRID_BEGIN
TIME_LABEL_ENABLE_BEGIN
TIME_LABEL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
CELL_WIDGET_ENABLE_BEGIN
CELL_GRID_BEGIN
START_BUTTON_ENABLE_BEGIN
START_BUTTON_GRID_BEGIN
APP_READY
GAME_START
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
CELL_CLICK:4
TIMER_TICK
TIMER_TICK
CELL_CLICK:5
TIMER_TICK
TIMER_TICK
CELL_CLICK:6
TIMER_TICK
CELL_CLICK:9
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
TIMER_TICK
CELL_CLICK:4
TIMER_TICK
CELL_CLICK:8
TIMER_TICK
CELL_CLICK:5
TIMER_TICK
CELL_CLICK:2
TIMER_TICK
TIMER_TICK
CELL_CLICK:3
TIMER_TICK
CELL_CLICK:6
TIMER_TICK
CELL_CLICK:9
TIMER_TICK
CELL_CLICK:7
TIMER_TICK
GAME_OVER
```
## 実行時のご様子

![flashgrid.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/1e7ad42f-bac9-415c-a4a8-e7f66c1ebc9c.gif)

まだ粗削りですが、１行も手書きせずに動くGUIアプリが生成できたのは驚愕でした:tada:この状態からであれば、ここをあーしてこーしてのVibeコーディングできそうな予感ですね。

# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/download/download.html#download-base)にアクセスすると、Mindコンパイラをダウンロードできますよ。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:

https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71


## 2026/10/03 追記　CopilotはGUIアプリの実行時エラーダイアログの内容をどのように認識したか
Mind言語開発者の@killyさんより、コメントにてGithub Copilotは下記の実行時エラーをどのように認識したのか？というご質問をいただきましたので、Github Copilotに問い合わせてみました。
>「有効化されていないウィジェットを格子配置しようとしました」というエラーになっていました。　Github Copilotチャット応答より

わたしも興味があったので後学のため詳しいレポートにまとめてもらいました。

## プロンプト
>「有効化されていないウィジェットを格子配置しようとしました」というエラーの
文言の内容をどのように採取したのか詳しく教えてください。
docs\光るマスをねらえ実装プラン完了レポートエラー確認のしくみ.md
に出力してください。

### 生成レスポンス
>指定のドキュメントを作成しました。
>光るマスをねらえ実装プラン完了レポートエラー確認のしくみ.md
>
>当時の作業記録を確認したところ、エラー文言は診断ログからではなく、「重大エラー」ダイアロ>グを画像保存し、その画像を読み取って採取していました。

**光るマスをねらえ実装プラン完了レポートエラー確認のしくみ.md　抜粋**
```md:
# 光るマスをねらえ：起動エラー確認のしくみ

## 1. 結論：文言は診断ログではなく、エラーダイアログの画像から読み取った

前回のチャットで報告した、
> 有効化されていないウィジェットを格子配置しようとしました
という文言は、**Mind ランタイムが表示した「重大エラー」ダイアログを画像として保存し、その画像を表示して読み取ったもの**です。

## 2. 実際の採取手順
### 2.1 Mind の環境を設定して起動した
### 2.2 ゲームの実行を担うランタイムを特定した
起動用の `flashgrid.exe` だけを調べるのではなく、Mind の実行コードを動かしている `mrunt102.exe` を調べました。
### 2.3 UI Automation による文字列取得では本文を採取できなかった
### 2.4 Windows API でダイアログだけを画像保存した

次に、PowerShell の `Add-Type` で小さな C# の補助クラスを定義し、`user32.dll` の以下の API を呼び出しました。
```

仕事で使っているAmazonKiroも一時的なC#アプリやPythonアプリを実装して保存してPowerShellで(Kiro-cliをVSCodeターミナルから起動している場合)それを呼び出して必要な課題を達成して一時的なアプリは削除するという動きをみていましたがGithub Copilotも同じようなことをやってくれるようですね:joy:

### 結論：
文言は診断ログではなく、エラーダイアログの画像から読み取った。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
