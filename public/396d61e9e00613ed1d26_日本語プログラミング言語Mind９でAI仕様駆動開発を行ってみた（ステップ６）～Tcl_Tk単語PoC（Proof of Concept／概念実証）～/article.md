# はじめに
日本語プログラミング言語Mindのバージョン９でAI仕様駆動開発（っぽいこと）を行っています。本記事はその第６ステップで、AIがMind９の内蔵するTcl/Tkインタプリタ機能を使ってグラフィック機能を自動生成するという内容です。

本記事での実装仕様は難度が高く、AIも苦戦していていったんステップ５が完了した後、本要件対応するにはPoC（Proof of Concept／概念実証）からやらせてくれはAIのご提案です。

# 使用AI
## GitHub Copilot
GitHub CopilotのPro+版。あおい実装[^1]と検証の主担当。
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。GitHub Copilotの使い方スーパバイザとして利用し続けています。モードは「無料プラン」のsmart。

# 本記事のステップ
## Microsoft Copilotとの事前準備
本ステップではとくにございません。
## GitHub Copilot
本ステップでのやりとりは非常に長ステップにわたり、従来のような具体的なやりとりの記事化が困難であるため、要所を要約して俯瞰します。

## 本記事の課題
firework修正方針.mdの最初のバージョンに記載された下記の機能要件を実装することです。

```md:docs\firework修正方針.md
# firework.src 修正方針
### 2.3 文字花火

`FireworkTextEffect` は、次の処理を行う。

1. 1600 x 220 のBitmapを作成する。
2. Bitmapへフォントで文字列を描画する。
3. 2ピクセル間隔で全画素を走査する。
4. アルファ値が20より大きい画素を粒子へ変換する。
5. 粒子を更新し、横速度の摩擦、重力、寿命、透明度を適用する。
6. 粒子を円として描画し、透明度が高ければ残光を描画する。

これは通常花火とは別の機能であり、通常花火の粒子生成処理だけでは代替できない。
```
下記は修正方針v2.mdですが、v2以降は一貫して本機能対象外としてきました。
```md:docs\firework修正方針v2.md
### 6.6 第6段階: 文字花火は別機能として判定

文字花火は通常花火の粒子生成へ混ぜない。
```

前回記事のステップ５は基本的に上記規定を継承しているfirework修正方針v4.mdの状態でした。記事のステップNoと修正方針書のバージョンNoは非同期です。

ステップ５（修正方針v4状態の完成）でいったん花火の体は実現しましたので、わたしの中では次のステップの修正方針バージョンの策定に進行していました。

そして、修正方針v5でPoCが提案されました。わたしの方ではPoCやってとはプロンプトで特に触れてはおりませんでした。

```md:docs\firework修正方針v5.md
# firework修正方針 v5
## 4. 最初に実装するPoC単語
### 4.1 対象

最初の追加候補は、既存図形を作り直さず色を変更する次のGUI単語とする。
//```text
canvas図形の塗り色を更新
//```

```
このPoCの試作は不完全な状態となり（わたしがしびれを切らして未完了状態で中断とし）ましたが、

（中間的な完了レポートは数も多くひとつあたり長文すぎて詳しくはのせられませんが、なんか非常に優秀な技術者報告という感じ）

なんとなくGitHub CopilotはTcl/Tkプログラミングに慣れてきた感がございましたので、「ちょっと文字花火やってみない」ということで文字花火PoCをやってみる（いただく）ことにしました。

```md:docs\firework修正方針v5文字花火PoC単語実装プラン完了レポート.md
# firework修正方針 v5 文字花火PoC単語実装プラン完了レポート
Phase 4: 完了判定と後続判断
判定: 文字花火の点群化境界PoCとして合格。通常花火への統合や性能改善の合格を意味しない。

日本語を含む固定入力から、再現可能なCanvasローカル座標点群を取得・表示できた。
```

このPoCの試作は完全な状態となり、firework修正方針v6.mdとして本体への統合可否を検討しましたところ、中断状態の方の既存図形を作り直さず色を変更するPoC（下記では固定図形poolと表記）も加味した上で判定してくれたようでした。

```md:docs\firework修正方針v6完了レポート.md
# firework修正方針 v6 — 文字花火の統合境界と受入計画
## Phase 4: 通常花火との統合可否判断

**判定: 固定図形poolは性能採用候補にならず、通常花火への統合を見送る。
文字花火の検証成果だけを独立PoCとして保持する。**
```

GitHub Copilotも本件ではだいぶデグレにナーバスになっている（？とわたし的に解釈される）雰囲気を考慮して、本体ソースは別として実装してねといたしました。

### プロンプト１
>docs\firework修正方針v6完了レポート.md
を受けて
文字花火をfireworkに適用したfirework2.srcを作成する
docs\firework2修正方針.md
に出力してください。
花火化する文字列の内容は
cs\FireWorkForm.cs
の
private readonly string releaseMessage
と同じとしてください。

#### 生成レスポンス１

そして生成されたのがfirework2修正方針.mdです。

```md:docs\firework2修正方針.md
# firework2 修正方針 — 通常花火への文字花火追加
## 1. 結論

`firework.src` を基に別プログラム `firework2.src` を作成し、通常花火と同じ
1200×600 Canvas上に文字花火を追加する。

採用するのは、**文字点群を起動時に生成・保持し、活動中の文字粒子を毎フレーム
描き直す方式**である。固定図形poolは通常花火・文字花火とも有効化しない。

v6の「統合見送り」は、性能ゲートを通過しなかった固定図形poolについての判断
として引き継ぐ。本書はpool再評価ではなく、通常花火の既存clear・再描画経路に、
同じく再描画する文字花火を追加する別の実装計画である。性能改善を前提にせず、
全文表示・通常花火の維持・寿命終了時の消失・正常終了を新たに検証する。
```

## 生成されたソースコード　一部抜粋

### firework.src
サブソース作ったのかなと思い、メインソースの「コンパイルする」を確認。新規作成はない模様。canvas_color_control.srcになにか追加したのかなと思いきや、こちらも変更はありませんでした。
```mind:firework.src
"snowdrops\\randomtcl.src"を　コンパイル。
"canvas_color_control.src"を　コンパイル。
```
では、メインソースになにかべた書きで評価する系でなにか追加したのかなと追いかけていきますと…
```mind:firework.src
メインとは
        "source" "-encoding" "utf-8" "firework2_text.tcl"　４個で　複数語を評価した値を　捨
        ０を　診断花火番号に　入れ
        ０を　診断段階に　入れ
        ０を　比較フレーム番号に　入れ
        診断ログを開始する
        "APP_READY"を　診断を記録する
        性能比較モードが　１に　等しい　ならば
                "source" "poc/firework_bench_fixture.tcl"　２個で　複数語を評価した値を　捨
                固定図形プール有効が　１に　等しい　ならば
                        "firework_bench_init" "pool"　２個で　複数語を評価した値を　捨
                さもなければ
                        "firework_bench_init" "baseline"　２個で　複数語を評価した値を　捨
                つぎに
        つぎに
        メインウィンドウと　キャンバス幅と　キャンバス高と　黒色で
                キャンバスを立て　キャンバスに　入れ
        キャンバスを　ＩＤからパス名を得て　PoCパスに　入れ
        "::firework2::call" "init" PoCパス
        "祝！日本語プログラミング言語Mindバージョン９リリース！"
        ４個で　複数語を評価した値を　捨
        性能比較モードが　１に　等しい　ならば
                キャンバスを　ＩＤからパス名を得て　PoCパスに　入れ
                "firework_bench_set_canvas" PoCパス　１個で　
                複数語を評価した値を　捨
        つぎに
        花火群を初期化する
        固定図形プール有効が　１に　等しい　ならば
                固定図形プールを初期化する
        つぎに
        花火を再描画する
        "INITIALIZATION_COMPLETE"を　診断を記録する
        次の花火処理を予約する。

メインウィンドウクローズ処理とは　本定義　（・　→　・）
        "NORMAL_SHUTDOWN"を　診断を記録する
        "::firework2::shutdown"　１個で　複数語を評価した値を　捨。
```
「複数語を評価した値」という単語に"firework2_text.tcl"というTclスクリプトをセットしている箇所を発見！:scream::joy::joy:（メインが最初というわけではないのですが、とりあえずお話を単純化しております。:joy:）

### firework2_text.tcl
<details><summary>firework2_text.tcl AIによるTCLスクリプト自動生成</summary>

```tcl:firework2_text.tcl
namespace eval ::firework2 {
    variable points {}
    variable particles {}
    variable generation 0
    variable pending {}
    variable active 0
    variable stopping 0
    variable timer ""
    variable canvas ""
    variable log_channel ""
    variable enabled 1
    variable capacity 2400
    variable deaths 0
    variable triggers 0
    variable skipped 0
    variable prepared 0
    variable rng 12345
    variable scheduled_before {}
    variable dir [file dirname [info script]]
}

proc ::firework2::log {message} {
    variable log_channel
    if {$log_channel eq ""} {
        puts stderr $message
    } else {
        puts $log_channel $message
        flush $log_channel
    }
}

proc ::firework2::validate_points {cloud capacity} {
    if {![string is integer -strict $capacity] || $capacity < 1 || $capacity > 2400} {
        error "CAPACITY_INVALID $capacity"
    }
    set count [llength $cloud]
    if {$count < 1 || $count > 2400} {
        error "POINT_COUNT_INVALID $count"
    }
    if {$count > $capacity} {
        error "SLOT_SHORTAGE need=$count capacity=$capacity"
    }
    foreach point $cloud {
        if {[llength $point] != 2} {
            error "POINT_INVALID $point"
        }
        lassign $point x y
        if {![string is integer -strict $x] || ![string is integer -strict $y] ||
            $x < 0 || $x >= 1200 || $y < 0 || $y >= 600} {
            error "COORDINATE_INVALID $point"
        }
    }
}

proc ::firework2::prepare {text} {
    variable points
    variable prepared
    if {[string length $text] < 1 || [string length $text] > 32 ||
        [string trim $text] eq ""} {
        error "TEXT_LENGTH_INVALID"
    }
    set img_dir [file join [file dirname [info library]] tk8.6 Img1.4.16]
    if {[lsearch -exact $::auto_path $img_dir] < 0} {
        lappend ::auto_path $img_dir
    }
    package require img::window
    if {[lsearch -exact [font families] "Yu Gothic UI"] < 0} {
        error "FONT_UNAVAILABLE Yu Gothic UI"
    }
    if {[winfo exists .fw2raster]} {
        error "RASTER_ALREADY_EXISTS"
    }
    set photo ""
    set font_name ""
    try {
        for {set size 32} {$size >= 18} {incr size -1} {
            set descriptor [list "Yu Gothic UI" $size bold]
            set measured [font measure $descriptor $text]
            if {$measured <= 1092} { break }
        }
        if {$size < 18} {
            error "TEXT_TOO_WIDE"
        }
        set font_name [font create -family "Yu Gothic UI" -size $size -weight bold]
        set width [expr {$measured + 24}]
        set height [expr {[font metrics $font_name -linespace] + 24}]
        toplevel .fw2raster
        wm title .fw2raster "Firework2 text initialization"
        wm geometry .fw2raster ${width}x${height}+20+20
        canvas .fw2raster.c -width $width -height $height -background black \
            -borderwidth 0 -highlightthickness 0
        pack .fw2raster.c
        wm attributes .fw2raster -topmost 1
        raise .fw2raster
        set item [.fw2raster.c create text 12 12 -anchor nw -text $text \
            -fill #606060 -font $font_name]
        update
        after 100
        update
        lassign [.fw2raster.c bbox $item] x1 y1 x2 y2
        if {$x1 < 0 || $y1 < 0 || $x2 >= $width || $y2 >= $height} {
            error "RASTER_CLIPPED bbox=$x1,$y1,$x2,$y2 size=$width,$height"
        }
        set photo [image create photo -format window -data .fw2raster.c]
        set dw [expr {[image width $photo] - [winfo width .fw2raster.c]}]
        set dh [expr {[image height $photo] - [winfo height .fw2raster.c]}]
        if {$dw < 0 || $dh < 0 || $dw > 4 || $dh > 4 || $dw % 2 || $dh % 2} {
            error "CAPTURE_SIZE_INVALID delta=$dw,$dh"
        }
        set ox [expr {$dw / 2}]
        set oy [expr {$dh / 2}]
        set cloud {}
        for {set y 0} {$y < $height} {incr y 4} {
            for {set x 0} {$x < $width} {incr x 4} {
                lassign [$photo get [expr {$x + $ox}] [expr {$y + $oy}]] r g b
                if {$r > 32 || $g > 32 || $b > 32} {
                    lappend cloud [list $x $y]
                }
            }
        }
        validate_points $cloud 2400
        set points $cloud
        set prepared 1
        log "PREPARE_OK text=$text length=[string length $text] count=[llength $cloud] font=[font actual $font_name] raster=${width}x${height} capture_offset=$ox,$oy bbox=$x1,$y1,$x2,$y2"
        return $cloud
    } finally {
        if {$photo ne ""} { image delete $photo }
        if {[winfo exists .fw2raster]} { destroy .fw2raster }
        if {$font_name ne ""} { font delete $font_name }
    }
}

proc ::firework2::random {} {
    variable rng
    set rng [expr {(1103515245 * $rng + 12345) & 0x7fffffff}]
    return $rng
}

proc ::firework2::build {cloud burst_y seed capacity generation} {
    validate_points $cloud $capacity
    foreach value [list $burst_y $seed $generation] {
        if {![string is integer -strict $value]} {
            error "PARTICLE_INITIALIZER_INVALID $value"
        }
    }
    set xs {}
    set ys {}
    foreach point $cloud {
        lassign $point x y
        lappend xs $x
        lappend ys $y
    }
    set xs [lsort -integer $xs]
    set ys [lsort -integer $ys]
    set min_x [lindex $xs 0]
    set min_y [lindex $ys 0]
    set cloud_width [expr {[lindex $xs end] - $min_x}]
    set cloud_height [expr {[lindex $ys end] - $min_y}]
    if {$cloud_width > 1100 || $cloud_height > 490} {
        error "PARTICLE_BOUNDS_INVALID"
    }
    set left [expr {600 - int(round($cloud_width / 2.0))}]
    set top [expr {max(50, min(547 - $cloud_height, $burst_y - 80))}]
    variable rng
    set rng $seed
    set result {}
    set slot 0
    foreach point $cloud {
        lassign $point x y
        set vx [expr {[random] % 9 - 4}]
        set vy [expr {[random] % 6 + 2}]
        set size [expr {[random] % 3 + 1}]
        set color [lindex {#ffd700 #dc143c #ff8c00 #00bfff} [expr {[random] % 4}]]
        set life [expr {[random] % 8 + 16}]
        lappend result [dict create slot $slot x [expr {$left + $x - $min_x}] \
            y [expr {$top + $y - $min_y}] vx $vx vy $vy size $size \
            color $color life $life active 1 generation $generation]
        incr slot
    }
    return $result
}

proc ::firework2::init {canvas_path text} {
    variable canvas
    variable enabled
    variable log_channel
    variable stopping
    set canvas $canvas_path
    if {![winfo exists $canvas] || [winfo class $canvas] ne "Canvas"} {
        error "DISPLAY_CANVAS_INVALID $canvas"
    }
    variable dir
    set path [file join $dir firework2_text.log]
    if {[info exists ::env(FW2_RUN)]} {
        set path [file join $dir poc "firework2_$::env(FW2_RUN)_text.log"]
    }
    set log_channel [open $path w]
    fconfigure $log_channel -encoding utf-8
    set stopping 0
    if {[info exists ::env(FW2_TEXT)]} {
        if {$::env(FW2_TEXT) ni {0 1}} { error "TEXT_MODE_INVALID" }
        set enabled $::env(FW2_TEXT)
    }
    log "INIT Tcl=[info patchlevel] Tk=[package provide Tk] enabled=$enabled"
    if {$enabled} { prepare $text }
    wm protocol . WM_DELETE_WINDOW ::firework2::shutdown
    return 1
}

proc ::firework2::begin {} {
    variable pending
    variable stopping
    variable canvas
    if {$stopping || ![winfo exists $canvas]} { error "CANVAS_CLOSED" }
    set pending {}
}

proc ::firework2::event {slot x y} {
    variable pending
    variable enabled
    variable skipped
    if {!$enabled} { return }
    foreach value [list $slot $x $y] {
        if {![string is integer -strict $value]} { error "EVENT_INVALID" }
    }
    if {$slot < 1 || $slot > 4 || $x < 0 || $x > 1200 || $y < 0 || $y > 600} {
        error "EVENT_BOUNDS_INVALID $slot,$x,$y"
    }
    if {$pending eq ""} {
        set pending [list $slot $x $y]
    } else {
        incr skipped
        log "EVENT_SKIP reason=same_tick slot=$slot"
    }
}

proc ::firework2::advance {snapshot} {
    set result {}
    foreach particle $snapshot {
        if {[dict get $particle active]} {
            dict incr particle x [dict get $particle vx]
            dict incr particle y [dict get $particle vy]
            dict incr particle vy
            dict incr particle life -1
            if {[dict get $particle life] <= 0} {
                dict set particle active 0
            }
        }
        lappend result $particle
    }
    return $result
}

proc ::firework2::step {} {
    variable active
    variable particles
    variable points
    variable generation
    variable pending
    variable capacity
    variable triggers
    variable skipped
    variable deaths
    if {$active} {
        set particles [advance $particles]
        set active 0
        foreach particle $particles {
            if {[dict get $particle active]} { set active 1; break }
        }
        if {!$active} {
            incr deaths [llength $particles]
            log "EXPIRED generation=$generation slots=[llength $particles]"
        }
    }
    if {$pending ne ""} {
        lassign $pending slot x y
        if {$active} {
            incr skipped
            log "EVENT_SKIP reason=active slot=$slot"
        } else {
            set next [expr {$generation + 1}]
            set snapshot [build $points $y [expr {12345 + 1009 * $next}] $capacity $next]
            set particles $snapshot
            set generation $next
            set active 1
            incr triggers
            log "TRIGGER generation=$generation slot=$slot burst=$x,$y count=[llength $particles]"
        }
        set pending {}
    }
}

proc ::firework2::render {canvas_path snapshot} {
    if {![winfo exists $canvas_path]} { error "CANVAS_CLOSED" }
    try {
        foreach particle $snapshot {
            if {![dict get $particle active]} { continue }
            set x [dict get $particle x]
            set y [dict get $particle y]
            set size [dict get $particle size]
            set color [dict get $particle color]
            $canvas_path create oval $x $y [expr {$x + $size}] [expr {$y + $size}] \
                -fill $color -outline $color -state normal \
                -tags [list fw2text fw2slot-[dict get $particle slot]]
        }
    } on error {message options} {
        $canvas_path delete fw2text
        return -options $options $message
    }
}

proc ::firework2::draw {} {
    variable canvas
    variable particles
    variable active
    if {$active} { render $canvas $particles }
}

proc ::firework2::call {command args} {
    try {
        return [::firework2::$command {*}$args]
    } on error {message options} {
        variable active
        variable particles
        variable canvas
        set active 0
        set particles {}
        if {$canvas ne "" && [winfo exists $canvas]} { $canvas delete fw2text }
        log "ERROR command=$command message=$message\n[dict get $options -errorinfo]"
        if {[info exists ::env(FW2_RUN)]} {
            variable dir
            set out [open [file join $dir poc "firework2_$::env(FW2_RUN)_error.log"] w]
            puts $out "$message\n[dict get $options -errorinfo]"
            close $out
        } else {
            tk_messageBox -icon error -type ok -title Firework2 -message $message
        }
        shutdown 1
    }
}

proc ::firework2::cancel_callbacks {} {
    variable stopping
    variable timer
    set stopping 1
    if {$timer ne ""} { after cancel $timer; set timer "" }
}

proc ::firework2::before_schedule {} {
    variable timer
    variable stopping
    variable scheduled_before
    if {$stopping || $timer ne ""} { error "CALLBACK_STATE_INVALID" }
    set scheduled_before [after info]
}

proc ::firework2::claim_timer {} {
    variable timer
    variable scheduled_before
    set added {}
    foreach id [after info] {
        if {[lsearch -exact $scheduled_before $id] < 0} { lappend added $id }
    }
    if {[llength $added] != 1} { error "CALLBACK_RESERVATION_INVALID $added" }
    set timer [lindex $added 0]
}

proc ::firework2::callback_enter {} {
    variable timer
    variable stopping
    if {$stopping} { error "CALLBACK_AFTER_STOP" }
    set timer ""
}

proc ::firework2::shutdown {{code 0}} {
    variable stopping
    variable particles
    variable active
    variable log_channel
    cancel_callbacks
    set particles {}
    set active 0
    if {[winfo exists .fw2raster]} { destroy .fw2raster }
    log "SHUTDOWN code=$code"
    if {$log_channel ne ""} { close $log_channel; set log_channel "" }
    if {[winfo exists .]} { destroy . }
    exit $code
}

```
</details>

Mind7でファイルとしてのTclスクリプトを読み込んでいるところを見たことがあるようなないような、このような作り方もMind９でできたんですね:joy:

「複数語を評価した値」という単語を使うとできる模様。

## 実行のご様子

粗削りながらAIが自動生成したソースによる実行状態です。

![firework2-2.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/b44811dc-e7ac-414d-9dd1-8d7651738bf6.gif)


文字花火が爆発するまでのインターバルがちょっと調整できていないので、文言がよみとりづらい感じです:joy:なんて文字だかわからないひとは、前記ソースのメイン定義部分を参照してください:joy::joy:



# おわりに
いかがでしたでしょうか？同じことをしようとしている方々の参考になれば幸いです。


興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/download/download.html#download-base)にアクセスすると、Mindコンパイラをダウンロードできますよ。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:

https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita

