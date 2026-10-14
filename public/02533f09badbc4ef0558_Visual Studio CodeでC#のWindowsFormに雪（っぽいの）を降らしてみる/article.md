# はじめに

C#のWindowsFormアプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。[前回の記事](https://qiita.com/mylifewithviolin/items/b526928ce01df7d2104d)でとりあえずデバッグ開始できたので、今回はWindowsFormに雪（っぽいの）を降らしてみます。


VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.86.1
C# 12 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# C# Windowsフォームアプリケーションプロジェクトの作成
たいへんお手数ですが、[前回の記事](https://qiita.com/mylifewithviolin/items/b526928ce01df7d2104d)をご参照ください。

# どうやって降らせるの？

とりあえず乱数をつかって雪片（っぽい白い円）の直径と座標と下降位置差分を計算して、Windowsフォームに描画してみます。これはこちらの記事のロジックの原型としたものです。

https://qiita.com/mylifewithviolin/items/565e61987a0fbaaa6abe

# お題のソースコード
## Snowflake.cs
雪片クラスを下記のように追加します。

```cs:Snowflake.cs
public class Snowflake
{
    public int X { get; set; }
    public int Y { get; set; }
    public int Speed { get; set; }
    public int Size { get; set; }
    private static Random random = new Random();

    public Snowflake(int width)
    {
        X = random.Next(width);
        Y = random.Next(-50, -10);
        Speed = random.Next(1, 5);
        Size = random.Next(2, 6);
    }

    public void Update(int height)
    {
        Y += Speed;
        if (Y > height)
        {
            Y = random.Next(-50, -10);
            Speed = random.Next(1, 5);
            Size = random.Next(2, 6);
        }
    }
}

```
ここで使っているrandom.nextの詳細です。

https://learn.microsoft.com/ja-jp/dotnet/api/system.random.next?view=net-8.0

## WinForm.cs
とりあえず前回の記事では空のフォームであったのを雪が降るフォームにします。
### 修正前
```cs:WinForm.cs
using System;
using System.Windows.Forms;
using Microsoft.VisualBasic;

namespace WinFormsApp
{
    public class WinForm : Form
    {
        public WinForm()
        {
        }
    }
}
```

### 修正後
```cs:WinForm.cs
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;


namespace WinFormsApp
{
    public class WinForm : Form
    {

        private System.Windows.Forms.Timer timer;
        private List<Snowflake> snowflakes;
        private int numberOfSnowflakes = 100;
        public WinForm()
        {
            this.DoubleBuffered = true;
            this.ClientSize = new Size(1200, 600);
            this.Text = "Snowfall";
            this.BackColor =Color.Black;
    
            snowflakes = new List<Snowflake>();
            for (int i = 0; i < numberOfSnowflakes; i++)
            {
                snowflakes.Add(new Snowflake(this.ClientSize.Width));
            }
    
            timer = new System.Windows.Forms.Timer();
            timer.Interval = 30;
            timer.Tick += new EventHandler(OnTimerTick);
            timer.Start();
        }

        private void OnTimerTick(object? sender, EventArgs e)
        {
            foreach (var snowflake in snowflakes)
            {
                snowflake.Update(this.ClientSize.Height);
            }
            this.Invalidate();
        }
    
        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Graphics g = e.Graphics;
            foreach (var snowflake in snowflakes)
            {
                g.FillEllipse(Brushes.White, snowflake.X, snowflake.Y, snowflake.Size, snowflake.Size);
            }
        }
    }
}
```
タイマー割込みで雪片の座標を書き換え、ペイントイベントのオーバーライドで雪片の円を描画という感じでしょうか。

https://learn.microsoft.com/ja-jp/dotnet/desktop/winforms/controls/overriding-the-onpaint-method?view=netframeworkdesktop-4.8&viewFallbackFrom=netdesktop-9.0

# 実行イメージ

実行時の様子は下記の感じです。

![CsWinForm2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7bcba1d7-17e2-e32e-dd92-38fffaf26600.png)


![CsWinForm3.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/243a894a-f654-9e88-5c1d-3cb2d01f3237.gif)


# おわりに
いかがでしたでしょうか？なにかの役にたてば幸いです。
