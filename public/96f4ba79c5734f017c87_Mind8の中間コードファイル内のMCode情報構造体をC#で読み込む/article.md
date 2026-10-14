# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)でVSCodeでMind 8 for Windowsのkernelをデバッグ実行できる環境をつくり、[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)でC#とMind8を混在ビルドする環境をVSCodeで構築しました。

今回はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序の口として、Mind8の中間コードファイル内のMCode情報構造体をC#で読み込んでみます。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
C# 12 
dotnet-sdk-8.0.204-win-x64

このテーマでは処理単語の追加はなく、既存単語のMCode（の一部）を解釈実行する部分をCからC#に書き換えるというお題のため、辞書再構築ツールは使用しないので、Mind7ライセンスは不要です。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

C/C++のデバッガは直接使わないのですが、Cで実装されているMind8kernelの動作をデバッグ実行で探るために使用します。[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境となります。

# お題のMind8の中間コードファイル
本記事のテーマとなっているMind8の中間コードファイルは下記のファイルです。
```
c:\developments\vscode\mind8dispatch>dir hello.mco

2024/04/18  20:53            43,544 hello.mco
               1 個のファイル              43,544 バイト
```

これは正規のMind8ランタイムでは下記のように実行されます。詳しくは[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)をご参照ください。
```
c:\developments\vscode\mind8dispatch>hello
Hello by mind8
```

# お題のMCode情報構造体の確認
上記のファイル内のMCode情報構造体の値をまず確認します。そのため、Mind8Kernelのデバッグ環境へ上記のファイルを下記のようにコピーします。詳しくは[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)をご参照ください。
```
C:\developments\vscode\mind8dispatch>copy hello.mco c:\developments\vscode\mind8\kernel\mindexec.mco
c:\developments\vscode\mind8\kernel\mindexec.mco を上書きしますか? (Yes/No/All): Y
        1 個のファイルをコピーしました。
```

## 確認結果
MCode情報構造体のメンバの一部をVSCodeのC/C++デバッガのウォッチ式の値のコピーで採取した結果です。全部ではありませんが、雰囲気は感じ取っていただけるかと思います。
```
{minfoMark1=77 'M' minfoMark2=67 'C' minfoMark3=0 '\0' ...}
```

# お題のC#ソースコード
今回のC#ソースコードの全体雰囲気（Main）は下記のとおりです。ファイル名はリテラルコーディングの手抜きです。将来的には引数で渡せるようにしますが、当面はこの"hello.mco"一択との格闘になります。
```cs:
    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        McodeInfoStruct mcodeInfo =new();
        using FileStream fs = new("hello.mco", FileMode.Open);
        fs.Seek(0-sizeOfMcodoInfo, SeekOrigin.End);
        byte[] mcodeInf = new byte[sizeOfMcodoInfo];
        int ret=fs.Read(mcodeInf, 0, sizeOfMcodoInfo);
        if(ret<32){
            Console.WriteLine("Can't read Mcode-info({0}).", ret);
            return;
        }
        SetMcodeInfo(ref mcodeInfo,mcodeInf);
        MonitorMcodeInfo(ref mcodeInfo);

        fs.Seek(0, SeekOrigin.Begin);
        byte[] mcode = new byte[4];

        while (fs.Read(mcode, 0, 4) > 0)
        {
            Console.WriteLine(BitConverter.ToString(mcode));
        }
    }
```
当初のんきにMCode情報構造体が中間コードファイルの冒頭にあるもんだという思い込みで読み込んでいましたが、読み込み結果が異なっていたので実はMCode情報構造体はファイル末尾に配置されていることをKernelのソースよく読んで気づきました。

下記の関数はストリームから読み取ったバイト配列からMCode情報構造体をセットします。

Cで書かれたKernelではMCode情報構造体の参照アドレスにサイズ分バイトストリームを直接流し込んでいる感じですが、C#だとそんなアンマネージドなことはできません的な雰囲気があるので、マメにMCode情報構造体の各メンバの型に読み込んだバイト配列をキャストして代入しています。

```cs:
    /// <summary>バイト配列からMCode情報構造体をセットする</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
    /// <param name="mcodeInf">MCode情報構造体相当のバイト配列</param>
     private static void SetMcodeInfo(ref McodeInfoStruct McodeInfo,byte[] mcodeInf){
        McodeInfo.minfoMark1= (char)mcodeInf[0];//1
        McodeInfo.minfoMark2= (char)mcodeInf[1];//2
        McodeInfo.minfoMark3= mcodeInf[2];//3
        McodeInfo.minfoMark4= mcodeInf[3];//4
        byte[] int16Byte = new byte[2];
        int i=0;
        for(i=0;i<2;i++)int16Byte[i]=mcodeInf[i+4];
        McodeInfo.minfoMainExist= BitConverter.ToUInt16(int16Byte, 0);//5-6
        for(i=0;i<2;i++)int16Byte[i]=mcodeInf[i+6];
        McodeInfo.minfoLimitD= BitConverter.ToUInt16(int16Byte, 0);//7-8
        byte[] int32Byte = new byte[4];
        for(i=0;i<4;i++)int32Byte[i]=mcodeInf[i+8];
        McodeInfo.minfoMcodeSize= BitConverter.ToUInt32(int32Byte, 0);//9-12
        for(i=0;i<4;i++)int32Byte[i]=mcodeInf[i+12];
        McodeInfo.minfoLoctableSize= BitConverter.ToUInt32(int32Byte, 0);	//13-16
        for(i=0;i<4;i++)int32Byte[i]=mcodeInf[i+16];
        McodeInfo.minfoDataSize= BitConverter.ToUInt32(int32Byte, 0);	//17-20
        McodeInfo.minfoRuntimeNo= mcodeInf[20];//21
        McodeInfo.minfoDummy21= (char)mcodeInf[21];//22
        for(i=0;i<2;i++)int16Byte[i]=mcodeInf[i+22];
        McodeInfo.minfoSerialNo= BitConverter.ToUInt16(int16Byte, 0);//23-24
        for(i=0;i<4;i++)int32Byte[i]=mcodeInf[i+24];
        McodeInfo.minfoDstackSize= BitConverter.ToUInt32(int32Byte, 0);//25-28
        for(i=0;i<4;i++)int32Byte[i]=mcodeInf[i+28];
        McodeInfo.minfoRstackSize= BitConverter.ToUInt32(int32Byte, 0);//29-32
     }
```
一部のメンバは数値として見やすいようにchar型ではなくbyte型にしています。

下記の関数は読み込まれたMCode情報構造体のメンバの値をコンソール出力します。
```cs:
    /// <summary>MCode情報構造体をモニタする</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
     private static void MonitorMcodeInfo(ref McodeInfoStruct McodeInfo){
        Console.WriteLine("McodeInfo.minfoMark1({0}).",McodeInfo.minfoMark1);
        Console.WriteLine("McodeInfo.minfoMark2({0}).",McodeInfo.minfoMark2);
        Console.WriteLine("McodeInfo.minfoMark3({0}).",McodeInfo.minfoMark3);
        Console.WriteLine("McodeInfo.minfoMark4({0}).",McodeInfo.minfoMark4);
        Console.WriteLine("McodeInfo.minfoLoctableSize({0}).",McodeInfo.minfoLoctableSize);
        Console.WriteLine("McodeInfo.minfoMainExist({0}).",McodeInfo.minfoMainExist);
        Console.WriteLine("McodeInfo.minfoMcodeSize({0}).",McodeInfo.minfoMcodeSize);
        Console.WriteLine("McodeInfo.minfoRuntimeNo({0}).",McodeInfo.minfoRuntimeNo);
        Console.WriteLine("McodeInfo.minfoSerialNo({0}).",McodeInfo.minfoSerialNo);
        Console.WriteLine("McodeInfo.minfoDstackSize({0}).",McodeInfo.minfoDstackSize);
        Console.WriteLine("McodeInfo.minfoRstackSize({0}).",McodeInfo.minfoRstackSize);
     }
```

## 実行結果
では実行してみます。最初のメンバーの値がM、Cとなっているあたりで正常に読み取れている雰囲気を感じ取っていただけるかと思います。
```
McodeInfo.minfoMark1(M).
McodeInfo.minfoMark2(C).
McodeInfo.minfoMark3(0).
McodeInfo.minfoMark4(128).
McodeInfo.minfoLoctableSize(2616).
McodeInfo.minfoMainExist(1).
McodeInfo.minfoMcodeSize(36352).
McodeInfo.minfoRuntimeNo(10).
McodeInfo.minfoSerialNo(42).
McodeInfo.minfoDstackSize(4096).
McodeInfo.minfoRstackSize(4096).
```

下記はその後のコードの中間コードファイルを先頭から読みだして、4バイトづつ16進数形式で出力した結果です。

MindのMCodeは2バイトですので、下記のバイト列ばMCodeの場合は2づつセットで出力されているイメージとなります。印象としてはけっこう数が多いなという感じ。この中身の解釈が次回以降のお題となります。
```
20-00-58-00
04-00-54-00
14-00-66-80
20-00-40-00
74-00-42-00
14-00-70-00
58-00-04-00
D0-01-60-80
...略
```


# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりが始まりました。いつ終わるかは不明ですが、次は地道にステップバイステップでMCode領域とLOCテーブルの読み出しとかかも（かなり序の口の範囲ですね）。

# 参考情報
MCode情報構造体とは何ぞやと興味をお持ちになった方は、下記の記事のコメントでMind開発者の@killyさんに詳しく解説いただいていますので、よろしかったらご参照ください。

VSCodeでMind 8 for Windowsのkernelをデバッグ実行（mcodeinfo構造体の謎に迫る？）　Qiita
https://qiita.com/mylifewithviolin/items/96168b67c59ff03bf236

