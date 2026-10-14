# はじめに
[前回](https://qiita.com/mylifewithviolin/items/54c80d6f1360d0115971)はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望の序二段のあたりとして、Mind8のLocテーブルのアドレスポインタ、データ領域のAccessポインタを実装しました。

これにより、ディスパッチャループが少しづつ回るようになりました。今回はリターンスタックを実装します。

前回記事まではC#のスタックコレクションを使う想定でしたが、Cの関数配列に対応したC#の関数配列をいくつか実装しているうち、リターンスタックのアドレスポインタを再セットしているように読み取れるマクロに遭遇したので、そちらの書き換えのためスタッククラスを独自に実装してみます。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
C# 12 
dotnet-sdk-8.0.204-win-x64

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

C/C++のデバッガは直接使わないのですが、Cで実装されているMind8kernelの動作をデバッグ実行で探るために使用します。[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境となります。

# お題のMind8の中間コードファイル
[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)をご参照ください。

下記はC版ディスパッチャのループ内のモニタを調整して出力したシーケンスNo順のmcodeの16進数表記のリストです。長くなるので下記は10までサンプル出力したものです。その下に全出力を掲示しています。
```
SqNo mcode
   1 8019
   2 002F
   3 0036
   4 0080
   5 0036
   6 0070
   7 803A
   8 002F
   9 813E
  10 0012
```

詳細展開で確認できます。お題の「Hello by mind8」のコンソール出力までは649のmcodeを処理しなければならないことがわかります。

<details><summary>SeqNo.11以降から終了までのmcode</summary>

```
  11 0036
  12 0071
  13 8046
  14 8045
  15 0012
  16 0036
  17 0074
  18 0020
  19 0020
  20 80BA
  21 0036
  22 0012
  23 016E
  24 0020
  25 80A6
  26 0097
  27 0065
  28 0020
  29 80D7
  30 0261
  31 8053
  32 8052
  33 001A
  34 006B
  35 0055
  36 008F
  37 00ED
  38 0055
  39 0012
  40 00A2
  41 00BF
  42 0095
  43 01D7
  44 006B
  45 0055
  46 00ED
  47 0055
  48 0055
  49 0103
  50 00BF
  51 0055
  52 0055
  53 0107
  54 0022
  55 0122
  56 0020
  57 0012
  58 0165
  59 80D6
  60 002F
  61 0264
  62 0104
  63 0065
  64 0012
  65 0036
  66 0071
  67 0020
  68 0036
  69 0074
  70 0264
  71 0104
  72 00EE
  73 0020
  74 80E8
  75 80E6
  76 80E2
  77 0268
  78 0020
  79 0020
  80 0020
  81 813C
  82 0095
  83 0296
  84 0298
  85 0096
  86 0296
  87 0298
  88 0097
  89 0296
  90 0298
  91 0020
  92 0020
  93 801F
  94 002F
  95 0052
  96 8175
  97 8170
  98 001D
  99 006E
 100 0058
 101 0097
 102 01D5
 103 00A5
 104 01DD
 105 00EC
 106 0058
 107 006E
 108 0042
 109 0070
 110 0058
 111 015F
 112 00EC
 113 003E
 114 01A5
 115 00A0
 116 00A0
 117 0119
 118 00EC
 119 0042
 120 0078
 121 002E
 122 0058
 123 015F
 124 00EC
 125 003E
 126 01A5
 127 00A0
 128 00A0
 129 0119
 130 00EC
 131 0042
 132 0078
 133 002E
 134 0058
 135 015F
 136 00EC
 137 003E
 138 01A5
 139 00A0
 140 00A0
 141 0119
 142 00EC
 143 0042
 144 0078
 145 002E
 146 0058
 147 015F
 148 00EC
 149 003E
 150 01A5
 151 00A0
 152 00A0
 153 0119
 154 00EC
 155 0042
 156 0078
 157 002E
 158 0058
 159 015F
 160 00EC
 161 003E
 162 01A5
 163 00A0
 164 00A0
 165 0119
 166 00EC
 167 0042
 168 0078
 169 002E
 170 0058
 171 015F
 172 00EC
 173 003E
 174 01A5
 175 00A0
 176 00A0
 177 0119
 178 00EC
 179 0042
 180 0078
 181 002E
 182 0058
 183 015F
 184 00EC
 185 003E
 186 01A5
 187 00A0
 188 00A0
 189 0119
 190 00EC
 191 0042
 192 0078
 193 002E
 194 0058
 195 015F
 196 00EC
 197 003E
 198 01A5
 199 00A0
 200 00A0
 201 0119
 202 00EC
 203 0042
 204 0078
 205 002E
 206 0058
 207 015F
 208 00EC
 209 003E
 210 01A5
 211 00A0
 212 00A0
 213 0119
 214 00EC
 215 0042
 216 0078
 217 002E
 218 0058
 219 015F
 220 00EC
 221 003E
 222 01A5
 223 00A0
 224 00A0
 225 0119
 226 00EC
 227 0042
 228 0078
 229 002E
 230 0058
 231 015F
 232 00EC
 233 003E
 234 01A5
 235 00A0
 236 00A0
 237 0119
 238 00EC
 239 0042
 240 0078
 241 002E
 242 0058
 243 015F
 244 00EC
 245 003E
 246 01A5
 247 00A0
 248 00A0
 249 0119
 250 00EC
 251 0042
 252 0078
 253 002E
 254 0058
 255 015F
 256 00EC
 257 002E
 258 0054
 259 003A
 260 01B7
 261 0058
 262 816D
 263 001C
 264 006E
 265 0058
 266 01D2
 267 00A0
 268 0114
 269 00ED
 270 0058
 271 0024
 272 011E
 273 0025
 274 0123
 275 0020
 276 8178
 277 8171
 278 001D
 279 006E
 280 0058
 281 006E
 282 0042
 283 0070
 284 0058
 285 015F
 286 00EC
 287 003E
 288 01A5
 289 006A
 290 0054
 291 00A0
 292 00A0
 293 0119
 294 00EC
 295 0054
 296 00A0
 297 0114
 298 00EC
 299 0042
 300 0078
 301 002E
 302 0058
 303 015F
 304 00EC
 305 003E
 306 01A5
 307 006A
 308 0054
 309 00A0
 310 00A0
 311 0119
 312 00EC
 313 0054
 314 00A0
 315 0114
 316 00EC
 317 0042
 318 0078
 319 002E
 320 0058
 321 015F
 322 00EC
 323 003E
 324 01A5
 325 006A
 326 0054
 327 00A0
 328 00A0
 329 0119
 330 00EC
 331 0054
 332 00A0
 333 0114
 334 00EC
 335 0042
 336 0078
 337 002E
 338 0058
 339 015F
 340 00EC
 341 003E
 342 01A5
 343 006A
 344 0054
 345 00A0
 346 00A0
 347 0119
 348 00EC
 349 0054
 350 00A0
 351 0114
 352 00EC
 353 0058
 354 015F
 355 0058
 356 8163
 357 00A4
 358 0020
 359 01DD
 360 00FE
 361 00EC
 362 0096
 363 002E
 364 00EC
 365 0058
 366 0054
 367 003A
 368 01B7
 369 002E
 370 0025
 371 0122
 372 0020
 373 0012
 374 0165
 375 0012
 376 0052
 377 8174
 378 8170
 379 001D
 380 006E
 381 0058
 382 0097
 383 01D5
 384 00A5
 385 01DD
 386 00EC
 387 0058
 388 006E
 389 0042
 390 0070
 391 0058
 392 015F
 393 00EC
 394 003E
 395 01A5
 396 00A0
 397 00A0
 398 0119
 399 00EC
 400 0042
 401 0078
 402 002E
 403 0058
 404 015F
 405 00EC
 406 003E
 407 01A5
 408 00A0
 409 00A0
 410 0119
 411 00EC
 412 0042
 413 0078
 414 002E
 415 0058
 416 015F
 417 00EC
 418 003E
 419 01A5
 420 00A0
 421 00A0
 422 0119
 423 00EC
 424 0042
 425 0078
 426 002E
 427 0058
 428 015F
 429 00EC
 430 003E
 431 01A5
 432 00A0
 433 00A0
 434 0119
 435 00EC
 436 0042
 437 0078
 438 002E
 439 0058
 440 015F
 441 00EC
 442 003E
 443 01A5
 444 00A0
 445 00A0
 446 0119
 447 00EC
 448 0042
 449 0078
 450 002E
 451 0058
 452 015F
 453 00EC
 454 003E
 455 01A5
 456 00A0
 457 00A0
 458 0119
 459 00EC
 460 0042
 461 0078
 462 002E
 463 0058
 464 015F
 465 00EC
 466 003E
 467 01A5
 468 00A0
 469 00A0
 470 0119
 471 00EC
 472 0042
 473 0078
 474 002E
 475 0058
 476 015F
 477 00EC
 478 003E
 479 01A5
 480 00A0
 481 00A0
 482 0119
 483 00EC
 484 0042
 485 0078
 486 002E
 487 0058
 488 015F
 489 00EC
 490 003E
 491 01A5
 492 00A0
 493 00A0
 494 0119
 495 00EC
 496 0042
 497 0078
 498 002E
 499 0058
 500 015F
 501 00EC
 502 003E
 503 01A5
 504 00A0
 505 00A0
 506 0119
 507 00EC
 508 0042
 509 0078
 510 002E
 511 0058
 512 015F
 513 00EC
 514 003E
 515 01A5
 516 00A0
 517 00A0
 518 0119
 519 00EC
 520 0042
 521 0078
 522 002E
 523 0058
 524 015F
 525 00EC
 526 003E
 527 01A5
 528 00A0
 529 00A0
 530 0119
 531 00EC
 532 0042
 533 0078
 534 002E
 535 0058
 536 015F
 537 00EC
 538 002E
 539 0054
 540 003A
 541 01B7
 542 0058
 543 816D
 544 001C
 545 006E
 546 0058
 547 01D2
 548 00A0
 549 0114
 550 00ED
 551 0058
 552 0024
 553 011E
 554 0025
 555 0122
 556 0020
 557 0165
 558 81A4
 559 0012
 560 0036
 561 0070
 562 0020
 563 8149
 564 002F
 565 0012
 566 0036
 567 0071
 568 0020
 569 0012
 570 0038
 571 0075
 572 0038
 573 0095
 574 01EC
 575 0012
 576 0068
 577 8150
 578 002F
 579 8252
 580 001C
 581 004E
 582 006B
 583 0012
 584 0036
 585 0071
 586 0055
 587 00EE
 588 00A5
 589 803C
 590 002F
 591 001A
 592 006E
 593 0015
 594 00ED
 595 0022
 596 004E
 597 0012
 598 0065
 599 0012
 600 0036
 601 0081
 602 0024
 603 0020
 604 8152
 605 002F
 606 821E
 607 0036
 608 0071
 609 0020
 610 0020
 611 02CD
 612 0020
 613 8021
 614 0020
 615 802A
 616 0020
 617 802C
 618 0020
 619 004D
 620 00EC
 621 0012
 622 0036
 623 0070
 624 802E
 625 0020
 626 8030
 627 0020
 628 8032
 629 0020
 630 8034
 631 0020
 632 0020
 633 00A5
 634 803C
 635 002F
 636 001A
 637 006E
 638 0015
 639 00ED
 640 0022
 641 0020
 642 828D
 643 00A5
 644 809A
 645 0012
 646 004E
 647 00EC
 648 0096
 649 026D
Hello by mind8
 650 0020
 651 0020
 652 801A
 653 002F
 654 801B
 655 002F
 656 0012
 657 0036
 658 0070
 659 0036
 660 0080
 661 803B
 662 002F
 663 8035
 664 0020
 665 8033
 666 0020
 667 8031
 668 0020
 669 802F
 670 0020
 671 0012
 672 004D
 673 00EC
 674 0012
 675 0036
 676 0070
 677 802D
 678 0020
 679 802B
 680 0020
 681 8022
 682 0020
 683 8020
 684 002F
 685 8151
 686 0020
 687 0020
 688 813F
 689 0020
 690 0020
 691 0020
 692 0012
 693 004E
 694 0014
```
</details>


# お題のC#ソースコード
## CsFunctions C#の関数配列
クラス構成は変えていないのですがソースファイルを分割するためクラスはpartialにしました。ソースファイル名をCsFuctions.csとしました。

```cs:CsFuctions.cs
public partial class Mind8Dispatcher
{
    private static readonly int maxCountCsFunctions = 1 + 0x0261;
    /// <summary>C#の関数配列を準備する</summary>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void SetupCsFunctions(ref Action[] csFuncs){
        csFuncs=new Action[maxCountCsFunctions];
    /*--------------------- 実行  -----------------------------------*/
            //～略～
    /*---------------------  局所変数の直接書き込み  ----------------*/
        csFuncs[0x0069]=ZzWriteBvarLocal;
        csFuncs[0x006A]=ZzWriteWvarLocal;
        csFuncs[0x006B]=ZzWriteDvarLocal;
        csFuncs[0x006C]=ZzWriteLvarLocal;
        csFuncs[0x006D]=ZzWriteQvarLocal;
        csFuncs[0x006E]=ZzWriteSvarLocal;
    /*---------------------  変数のクリア  --------------------------*/
            //～略～
        csFuncs[0x0261]=CmcodeFullFilename;//
    }           
            //～略～           
    /*---------------------  局所変数の直接書き込み  --------------------*/
    private static void ZzWriteBvarLocal(){ /* ;WORD $$WRITE_BVAR_LOCAL */
            /* Mコード=0x0069 */
        // UCHAR  *varAddr;   
        // varAddr = (UCHAR *)RstackPointer + FETCH_MCODE;
        // *varAddr = POP_B_OF_Q;
        
        // #define  DROP_L               DstackPointer++
        // #define  DROP_F               DROP_L
        // #define  POP_L                (*DstackPointer++)
        // #define  POP_F                POP_L
        // #define  POP_B_OF_Q           (DROP_F,(UCHAR)POP_L)
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        DataStack.Pop();//≒DROP Dataスタックから取り出して捨てる
        rtp.PushUb((byte)DataStack.Pop());
    }
    private static void ZzWriteWvarLocal(){  /* ;WORD $$WRITE_WVAR_LOCAL */
            /* Mコード=0x006A */
        // USHORT *varAddr;
        // varAddr = (USHORT *)((UCHAR *)RstackPointer + FETCH_MCODE);
        // *varAddr = POP_W_OF_Q;

        // #define  DROP_L               DstackPointer++
        // #define  DROP_F               DROP_L
        // #define  POP_L                (*DstackPointer++)
        // #define  POP_F                POP_L
        // #define  POP_W_OF_Q           (DROP_F,(USHORT)POP_L)
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        DataStack.Pop();//≒DROP Dataスタックから取り出して捨てる
        rtp.PushUs((ushort)DataStack.Pop());
    }
    private static void ZzWriteDvarLocal(){ /* ;WORD $$WRITE_DVAR_LOCAL */
            /* Mコード=0x006B */
        // LONG  	*varAddr;
        // varAddr = (LONG *)((UCHAR *)RstackPointer + FETCH_MCODE);
        // *varAddr = POP_L_OF_Q;

        // #define  POP_L_OF_Q           (DROP_F,POP_L)
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        DataStack.Pop();//≒DROP Dataスタックから取り出して捨てる
        rtp.PushSl((int)DataStack.Pop());
    }
    private static void ZzWriteLvarLocal(){ /* ;WORD $$WRITE_LVAR_LOCAL */
            /* Mコード=0x006C */
        // ULONG  	*varAddr;
        // varAddr = (ULONG *)((UCHAR *)RstackPointer + FETCH_MCODE);
        // varAddr[1] = POP_L;
        // varAddr[0] = POP_L;
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        uint var0=DataStack.Pop();//varAddr[0]用をデータスタックよりPOPしておく
        rtp.SetUl2var(DataStack.Pop(),var0);
    }
    private static void ZzWriteQvarLocal(){ /* ;WORD $$WRITE_QVAR_LOCAL */
            /* Mコード=0x006D */
        // ULONG  	*varAddr;
        // varAddr = (ULONG *)((UCHAR *)RstackPointer + FETCH_MCODE);
        // varAddr[0] = POP_L;
        // varAddr[1] = POP_L;
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        rtp.SetUl2var(DataStack.Pop(),DataStack.Pop());
    }
    private static void ZzWriteSvarLocal(){ /* ;WORD $$WRITE_SVAR_LOCAL */
            /* Mコード=0x006E */
        // ULONG  *varAddr;
        // varAddr = (ULONG *)((UCHAR *)RstackPointer + FETCH_MCODE);
        // varAddr[0] = POP_C;
        // varAddr[1] = (ULONG)POP_A;

        // #define  POP_A                ((UCHAR *)(*DstackPointer++))
        // #define  POP_C                POP_U
        rtp.ResetStackIndex(mp.GetMCodeCurrentIndex());//returnスタックのインデックスをMCode領域の値で移動
        rtp.SetUl2var(DataStack.Pop(),(byte)DataStack.Pop());
    }
}
```
上記のコメント部分はオリジナル版のCマクロ定義によるコードで、マクロはステップインしなかったので、マクロの定義部分もその下に引用しています。

ここが極めて重要で、このレベルでオリジナルのC版とコンパチブルな動作をしないと、Mind中間コードの処理結果が異なっていってしまいますね。

今回、リターンスタックの実装を変更したのは、上記の関数のオリジナルコードにいわゆるスタック操作とは異なるアドレスポインタへの操作が読み取れたためです。


データスタックはまだC#のスタック型のままですが、この動作の互換性も足らない可能性が今回の実装状態でも出てきていますが、この記事を書く前の状態からとしては、リターンスタックを書き換えて、上記のマクロが書き換えるように独自のアドレスポインタを実装しています。

## class StackPointer　スタックポインタ
こちらが独自実装のリターンスタック操作用のスタック操作クラスです。スタックっぽいPush、Popも実装していますが、型に応じて入出力できるように少し独自っぽい実装となっています。上記のアドレス（この実装ではbyte配列インデックス）を操作して、type unionのアドレスポインタ操作クラスと似たような実装も追加してあります。

```cs:Mind8Dispatcher.cs
    /// <summary>スタックポインタ</summary>
    private class StackPointer{
        private uint stackSize;
        private uint stackIndex;
        private byte[] dataArray =[];
        public void SetupStackArray(uint size){
            stackSize=size;
            dataArray =new byte[stackSize];
            stackIndex=0;
        }
        public void ResetStackIndex(uint index){
            stackIndex=index*4;//byte配列インデックス=アドレスポインタ変数の値*4
        }
        public byte PopUb(){    /* for unsigned byte access */
            if(stackIndex - 4 < 0)throw new Exception("stack user flow");
            stackIndex -=4;
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[stackIndex + i];
            return (byte)BitConverter.ToUInt32(int32Byte, 0);
        }
        public void PushUb(byte b){    /* for unsigned byte access */
            if(stackIndex + 4 > stackSize--)throw new Exception("stack over flow");
            byte[] int32Byte = new byte[4];
            int32Byte[3] =b;
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i]=int32Byte[i];
            stackIndex +=4;
        }

        public ushort PopUs(){    /* for unsigned byte access */
            if(stackIndex - 4 < 0)throw new Exception("stack under flow");
            stackIndex -=4;
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[stackIndex + i];
            return BitConverter.ToUInt16(int32Byte, 0);
        }
        public void PushUs(ushort us){    /* for unsigned byte access */
            if(stackIndex + 4 > stackSize--)throw new Exception("stack over flow");
            byte[] int32Byte =BitConverter.GetBytes(us);
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i]=int32Byte[i];
            stackIndex +=4;
        }
        public uint PopUl(){/* for unsigned long(int32) access   */
            if(stackIndex - 4 < 0)throw new Exception("stack under flow");
            stackIndex -=4;
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[stackIndex + i];
            return BitConverter.ToUInt32(int32Byte, 0);
        }
        public void PushUl(uint ul){/* for unsigned long(int32) access  */
            if(stackIndex + 4 > stackSize--)throw new Exception("stack over flow");
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i]=int32Byte[i];
            stackIndex +=4;
        }
        public void PushSl(int sl){/* for signed long(int32) access  */
            if(stackIndex + 4 > stackSize--)throw new Exception("stack over flow");
            byte[] int32Byte =BitConverter.GetBytes(sl);
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i]=int32Byte[i];
            stackIndex +=4;
        }
        public void SetUl2var(uint ul,uint ul2){/* for unsigned long access (for 1set of 2variable)  */
            //アドレス指定で直接セットしている元コードのためポインタインデックスの自動増加はなし
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i]=int32Byte[i];
            int32Byte =BitConverter.GetBytes(ul2);
            for (ulong i = 0; i < 4; i++) dataArray[stackIndex + i + 4]=int32Byte[i];
        }
    }
```


## Main 暫定メイン
暫定メインがまた少し書き換わります。リターンスタックはスタックポインタの実装に変わります。従来のC#スタックのコレクション型のRetnStackは削除されました。データスタックは現状まだC#スタックのコレクション型のままです。


```cs:Mind8Dispatcher.cs
    private static Stack<uint> DataStack = new();//データスタック
    private static byte[] McodeBase =[];//MCode領域
    private static byte[] WordOffsetTable=[];//LOCテーブル
    private static byte[] DataBase =[];//データ領域
    private static byte[] RetnStack =[];//リターンスタック
    private static MCodePointer mp=new();//MCode領域用ポインタ
    private static LocTablePointer lp=new();//LOCテーブル用ポインタ
    private static AccessPointer ap =new(); //データ領域用ポインタ
    private static StackPointer rtp =new(); //リターンスタック用ポインタ

    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        String mcodefilename="hello.mco";
        McodeInfoStruct mcodeInfo =new();

        /* ディスパッチャを準備する */
        bool ret=SetupForDispatch(ref mcodeInfo,mcodefilename);
        if(!ret){
            return;
        }

        MonitorMcode(McodeBase);
        DataStack = new();//resetDataStackPointer();//DstackPointer = DataStackBase[RestartEnvCount];
        mp =new();
        lp =new();
        ap =new();
        rtp=new();
        mp.SetupMcodeArray(McodeBase);
        lp.SetupLocArray(WordOffsetTable);
        ap.SetupDataArray(ref DataBase);
        rtp.SetupStackArray((ushort)mcodeInfo.minfoRstackSize);//resetRetnStackPointer();//RstackPointer = RetnStackBase;
        //McodePointer.b = (UCHAR *)McodeBase + 0x70;	/* 0x70=実行開始地点 */
        mp.ResetMcodeIndex(0x70);
        /* C#の関数を準備する */
        Action[] csFuncs=[]; //C#の関数を格納する配列
        /* C#の関数配列を準備する */
        SetupCsFunctions(ref csFuncs);
        /* ディスパッチャ開始 */
        Dispatcher(ref mcodeInfo,ref csFuncs);

    }
```

## Dispatcher ディスパッチャ
リターンスタックの最初のPushが書き換わっています。
また、お題の中間コードの節でも説明しました、オリジナルのC版ディスパッチャが処理しているmcodeリストと同等のものを出力するようにしました。こちらは10進数表記も出力しています。
```cs:Mind8Dispatcher.cs
    /// <summary>ディスパッチャ</summary>
    /// <param name="McodeInfo">MCode情報構造体の参照</param>
    /// <param name="csFunc">C#関数配列の参照</param>
    private static void Dispatcher(ref McodeInfoStruct McodeInfo,
              ref Action[] csFuncs){
        
        ushort   mcode;

        int retcode=0;//setjmp( RESTARTENV );		/* ←ディスパッチャ再 */
        if ( retcode != 2 )			/* 強制脱出の検査 */
        {
            int i=0;
            for(;;)
            {
                mcode = mp.GetMCodeCurrentIndex();
                Console.WriteLine("{0,4:d} {1,4:X4} {2,6:d}",++i,mcode,mcode);
                if ( (mcode & 0x8000)==0 )
                {
                    /* C#関数 */
                    csFuncs[mcode]();
                }
                else
                {
                    /* Mind単語 */
                    //PUSH_R( McodePointer.l );
                    //#define  PUSH_R(addr) *(--RstackPointer)=(ULONG)(addr)
                    rtp.PushUl((uint)mp.GetMcodeIndex());//現在のMCodeポインタの値をリターンスタックにプッシュする
                    //SET_MCODE_POINTER_BY_WORDNO( mcode & 0x7fff );
                    //McodePointer.b = (UCHAR *)(WordOffsetTable[wordNo])
                    mp.ResetMcodeIndex((ulong)lp.GetSl((ulong)(mcode & 0x7fff)));
                }
            }
        }
        return;
    }

```
# デバッグ実行の結果
ディスパッチャ内のループのMcodeポインタによるMCode領域からのmcode取得は34回までC版ランタイムと同じ動きをして、34回目のC#側関数mcode=006B ZzWriteDvarLocal内で
```
SqNo mcode mcode(dec)
   1 8019  32793
   2 002F     47
   3 0036     54
   4 0080    128
   5 0036     54
   6 0070    112
   7 803A  32826
   8 002F     47
   9 813E  33086
  10 0012     18
  11 0036     54
  12 0071    113
  13 8046  32838
  14 8045  32837
  15 0012     18
  16 0036     54
  17 0074    116
  18 0020     32
  19 0020     32
  20 80BA  32954
  21 0036     54
  22 0012     18
  23 016E    366
  24 0020     32
  25 80A6  32934
  26 0097    151
  27 0065    101
  28 0020     32
  29 80D7  32983
  30 0261    609
  31 8053  32851
  32 8052  32850
  33 001A     26
  34 006B    107
例外がスローされました: 'System.InvalidOperationException' (System.Collections.dll の中)
プログラム '[10784] mind8dispatch.dll' がコード -1 (0xffffffff) で終了しました。
```
下記のコードが'Stack empty.'で不正操作例外をスローしました。
```
DataStack.Pop();//≒DROP Dataスタックから取り出して捨てる
```
下記のマクロPOP_L_OF_Qを
```
// *varAddr = POP_L_OF_Q;
// #define  POP_L_OF_Q           (DROP_F,POP_L)
```
下記の定義から最初にデータスタックポインタを１つ動かすと解釈して、単にデータスタックからポップして捨てるで代替実装したのですが、そこがよくなかったのかも。あるいは手前の処理でスタック積み上げに不適合があったのかもしれませんね。
```
        // #define  DROP_L               DstackPointer++
        // #define  DROP_F               DROP_L
```

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードをざっと書くところまで到達して、序二段とかなという感じです。まだまだ課題山積ですが、次回以降でもこのソースコードを肉付けして実際に動く範囲をステップバイステップで広げてまいります。

## 補足

[こちらの記事](https://qiita.com/mylifewithviolin/items/922d72d13716bfae0d49)へのMind開発者@killyさんのコメントで気になっていた点が解明しましたのを受けて、今回記事ではソース長いので説明しませんでしたが、Accessクラスのフェッチっぽい動作は通常の読み取り動作に修正してあります。

## class AccessePointer　データ領域Accesseポインタ

<details><summary>訂正版ソースコード</summary>
```cs:Mind8Dispatcher.cs
    /// <summary>データ領域アクセスポインタ</summary>
    private class AccessPointer{
        private ulong dataIndex;
        private byte[] dataArray =[];
        public void SetupDataArray(ref byte[] DataBase){
            dataArray=DataBase;
        }
        public void ResetDataIndex(ulong index){
            dataIndex=index;
        }
        public byte GetUb(){    /* for unsigned byte access */
            return dataArray[dataIndex];
        }
        public void SetUb(byte b){    /* for unsigned byte access */
            dataArray[dataIndex] =b;
        }
        public void SetUb4Msi(byte b,uint length){  /* for unsigned byte access (for mind strings instance)*/
            for (ulong i = 0; i < length; i++) dataArray[dataIndex + i]= b;
        }
        public ushort GetUs(){/* for unsigned short access  */
            byte[] int16Byte = new byte[2];
            for (ulong i = 0; i < 2; i++) int16Byte[i] = dataArray[dataIndex + i];
            return BitConverter.ToUInt16(int16Byte, 0);
        }
         public void SetUs(ushort us){/* for unsigned short access  */
            byte[] int16Byte =BitConverter.GetBytes(us);
            for (ulong i = 0; i < 2; i++) dataArray[dataIndex + i]=int16Byte[i];
         }
        public short GetSs(){/* for signed short access  */
            byte[] int16Byte = new byte[2];
            for (ulong i = 0; i < 2; i++) int16Byte[i] = dataArray[dataIndex + i];
            return BitConverter.ToInt16(int16Byte, 0);
        }
        public void SetSs(short ss){/* for signed short access  */
            byte[] int16Byte =BitConverter.GetBytes(ss);
            for (ulong i = 0; i < 2; i++) dataArray[dataIndex + i]=int16Byte[i];
         }
        public int GetSl(){/* for signed long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[dataIndex + i];
            return BitConverter.ToInt32(int32Byte, 0);
        }
        public void SetSl(int sl){/* for signed long access  */
            byte[] int32Byte =BitConverter.GetBytes(sl);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i]=int32Byte[i];
        }
        public uint GetUl(){/* for unsigned long access   */
            byte[] int32Byte = new byte[4];
            for (ulong i = 0; i < 4; i++) int32Byte[i] = dataArray[dataIndex + i];

            return BitConverter.ToUInt32(int32Byte, 0);
        }
        public void SetUl(uint ul){/* for unsigned long access  */
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i]=int32Byte[i];
        }
        public void SetUl4Ms(uint ul,uint ul2){/* for unsigned long access (for mind string)  */
            byte[] int32Byte =BitConverter.GetBytes(ul);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i]=int32Byte[i];
            int32Byte =BitConverter.GetBytes(ul2);
            for (ulong i = 0; i < 4; i++) dataArray[dataIndex + i + 4]=int32Byte[i];
        }
        public long GetSll(){/* for signed long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = dataArray[dataIndex + i];
            return BitConverter.ToInt64(int64Byte, 0);
        }
        public void SetSll(long sll){/* for signed long access  */
            byte[] int64Byte =BitConverter.GetBytes(sll);
            for (ulong i = 0; i < 8; i++) dataArray[dataIndex + i]=int64Byte[i];
        }
        public ulong GetUll(){/* for signed long long access   */
            byte[] int64Byte = new byte[8];
            for (ulong i = 0; i < 8; i++) int64Byte[i] = dataArray[dataIndex + i];
            return BitConverter.ToUInt64(int64Byte, 0);
        }
        public void SetUll(ulong ull){/* for unsigned long access  */
            byte[] int64Byte =BitConverter.GetBytes(ull);
            for (ulong i = 0; i < 8; i++) dataArray[dataIndex + i]=int64Byte[i];
        }
    }
```
</details>


## 補足2
データスタックのPop例外は手前のmcode=0261のC#関数CmcodeFullFilenameの中身がまだ実装されていあないことによる原因でした。自ファイル名のアドレスをどうやってプッシュするか悩んで保留していたのが敗因でした。 
