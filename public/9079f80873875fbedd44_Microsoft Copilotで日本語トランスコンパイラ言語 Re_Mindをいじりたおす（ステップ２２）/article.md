# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思ったのですが、これがなかなか難儀でした。本記事はその第２２ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１８ステップの後にはサインアウトがあります。

# 第２２ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにしましたところ、比較的正常な結果が返るようになりました。第１９，２０，２１ステップの生成レスポンスで、Copilotが次のステップのご提案として「Re:Mind の AST（抽象構文木）風の構造化表示」ということを提案したので今回はそれをやってみることにします。

## プロンプト
ご提案いただいた Re:Mind の AST（抽象構文木）風の構造化表示　をやってみてください。

## 生成レスポンス
いいですね、それやりましょう。
まずは「バブルソート」の Re:Mind ソースを対象に、Re:Mind 向けの AST っぽい構造を一度きっちり形にしてみます。

方針
- 元の情報を落とさないことを優先
- 日本語名 / 英語名
- Javadoc コメント内容
- ローカル変数の元コメント（/** i */ など）
- 「トランスコンパイルにそのまま使える」ことを意識したノード構造
- ここでは JSON風構造 で表現します（実装言語はまだ決めない前提の中立フォーマット）

Re:Mind バブルソートの AST 風構造（JSON 風）
対象ソース：BubbleSort 名前空間のバブルソート版 Re:Mind。
```json:json
{
  "type": "CompilationUnit",
  "namespaces": [
    {
      "type": "NamespaceDeclaration",
      "name": "BubbleSort",
      "classes": [
        {
          "type": "ClassDeclaration",
          "javadoc": {
            "summary": "Program",
            "originalLanguage": "ja-en-mixed"
          },
          "modifiers": ["public"],
          "name": "プログラム型",
          "transpiledName": "ProgramType",
          "methods": [
            {
              "type": "MethodDeclaration",
              "javadoc": {
                "summary": "Main",
                "params": [
                  {
                    "nameJa": "引数",
                    "nameEn": "args",
                    "description": null
                  }
                ]
              },
              "modifiers": ["static"],
              "returnType": "void",
              "name": "メイン",
              "transpiledName": "main",
              "parameters": [
                {
                  "type": "string[]",
                  "name": "引数",
                  "transpiledName": "args"
                }
              ],
              "body": [
                {
                  "type": "LocalVariableDeclaration",
                  "javadoc": {
                    "summary": "array",
                    "nameJa": "配列"
                  },
                  "variableType": "int[]",
                  "name": "配列",
                  "transpiledName": "array",
                  "initializer": {
                    "type": "ArrayLiteral",
                    "elementType": "int",
                    "values": [15, 13, 9, 6, 4, 1]
                  }
                },
                {
                  "type": "ExpressionStatement",
                  "javadoc": {
                    "summary": "index",
                    "nameJa": "該当インデックス"
                  },
                  "expression": {
                    "type": "InvocationExpression",
                    "target": {
                      "type": "Identifier",
                      "name": "バブルソートする",
                      "transpiledName": "bubbleSort"
                    },
                    "arguments": [
                      {
                        "type": "Identifier",
                        "name": "配列",
                        "transpiledName": "array"
                      }
                    ]
                  }
                },
                {
                  "type": "ForStatement",
                  "initializer": {
                    "type": "LocalVariableDeclaration",
                    "variableType": "int",
                    "name": "i",
                    "transpiledName": "i",
                    "initializer": {
                      "type": "Literal",
                      "value": 0
                    }
                  },
                  "condition": {
                    "type": "BinaryExpression",
                    "operator": "<",
                    "left": {
                      "type": "Identifier",
                      "name": "i"
                    },
                    "right": {
                      "type": "MemberAccess",
                      "expression": {
                        "type": "Identifier",
                        "name": "配列",
                        "transpiledName": "array"
                      },
                      "memberName": "Length"
                    }
                  },
                  "iterator": {
                    "type": "UnaryExpression",
                    "operator": "++",
                    "operand": {
                      "type": "Identifier",
                      "name": "i"
                    }
                  },
                  "body": [
                    {
                      "type": "ExpressionStatement",
                      "expression": {
                        "type": "InvocationExpression",
                        "target": {
                          "type": "Identifier",
                          "name": "コンソール表示する",
                          "transpiledName": "consoleOut"
                        },
                        "arguments": [
                          {
                            "type": "ElementAccess",
                            "array": {
                              "type": "Identifier",
                              "name": "配列",
                              "transpiledName": "array"
                            },
                            "index": {
                              "type": "Identifier",
                              "name": "i"
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              ]
            },
            {
              "type": "MethodDeclaration",
              "javadoc": {
                "summary": "BubbleSort",
                "displayNameJa": "バブルソートする",
                "params": [
                  {
                    "nameJa": "配列",
                    "nameEn": "array"
                  }
                ]
              },
              "modifiers": ["public"],
              "returnType": "void",
              "name": "バブルソートする",
              "transpiledName": "bubbleSort",
              "parameters": [
                {
                  "type": "int[]",
                  "name": "配列",
                  "transpiledName": "array"
                }
              ],
              "body": [
                {
                  "type": "LocalVariableDeclaration",
                  "javadoc": {
                    "summary": "i",
                    "nameJa": "外側"
                  },
                  "variableType": "int",
                  "name": "外側",
                  "transpiledName": "outer",
                  "initializer": {
                    "type": "Literal",
                    "value": 0
                  }
                },
                {
                  "type": "WhileStatement",
                  "condition": {
                    "type": "BinaryExpression",
                    "operator": "<",
                    "left": {
                      "type": "Identifier",
                      "name": "外側",
                      "transpiledName": "outer"
                    },
                    "right": {
                      "type": "MemberAccess",
                      "expression": {
                        "type": "Identifier",
                        "name": "配列",
                        "transpiledName": "array"
                      },
                      "memberName": "Length"
                    }
                  },
                  "body": [
                    {
                      "type": "LocalVariableDeclaration",
                      "javadoc": {
                        "summary": "j",
                        "nameJa": "内側"
                      },
                      "variableType": "int",
                      "name": "内側",
                      "transpiledName": "inner",
                      "initializer": {
                        "type": "Literal",
                        "value": 0
                      }
                    },
                    {
                      "type": "WhileStatement",
                      "condition": {
                        "type": "BinaryExpression",
                        "operator": "<",
                        "left": {
                          "type": "Identifier",
                          "name": "内側",
                          "transpiledName": "inner"
                        },
                        "right": {
                          "type": "BinaryExpression",
                          "operator": "-",
                          "left": {
                            "type": "MemberAccess",
                            "expression": {
                              "type": "Identifier",
                              "name": "配列",
                              "transpiledName": "array"
                            },
                            "memberName": "Length"
                          },
                          "right": {
                            "type": "BinaryExpression",
                            "operator": "-",
                            "left": {
                              "type": "Identifier",
                              "name": "外側",
                              "transpiledName": "outer"
                            },
                            "right": {
                              "type": "Literal",
                              "value": 1
                            }
                          }
                        }
                      },
                      "body": [
                        {
                          "type": "IfStatement",
                          "condition": {
                            "type": "BinaryExpression",
                            "operator": ">",
                            "left": {
                              "type": "ElementAccess",
                              "array": {
                                "type": "Identifier",
                                "name": "配列",
                                "transpiledName": "array"
                              },
                              "index": {
                                "type": "Identifier",
                                "name": "内側",
                                "transpiledName": "inner"
                              }
                            },
                            "right": {
                              "type": "ElementAccess",
                              "array": {
                                "type": "Identifier",
                                "name": "配列",
                                "transpiledName": "array"
                              },
                              "index": {
                                "type": "BinaryExpression",
                                "operator": "+",
                                "left": {
                                  "type": "Identifier",
                                  "name": "内側",
                                  "transpiledName": "inner"
                                },
                                "right": {
                                  "type": "Literal",
                                  "value": 1
                                }
                              }
                            }
                          },
                          "thenBody": [
                            {
                              "type": "LocalVariableDeclaration",
                              "javadoc": {
                                "summary": "temp",
                                "nameJa": "一時"
                              },
                              "variableType": "int",
                              "name": "一時",
                              "transpiledName": "temp",
                              "initializer": {
                                "type": "ElementAccess",
                                "array": {
                                  "type": "Identifier",
                                  "name": "配列",
                                  "transpiledName": "array"
                                },
                                "index": {
                                  "type": "Identifier",
                                  "name": "内側",
                                  "transpiledName": "inner"
                                }
                              }
                            },
                            {
                              "type": "Assignment",
                              "left": {
                                "type": "ElementAccess",
                                "array": {
                                  "type": "Identifier",
                                  "name": "配列",
                                  "transpiledName": "array"
                                },
                                "index": {
                                  "type": "Identifier",
                                  "name": "内側",
                                  "transpiledName": "inner"
                                }
                              },
                              "right": {
                                "type": "ElementAccess",
                                "array": {
                                  "type": "Identifier",
                                  "name": "配列",
                                  "transpiledName": "array"
                                },
                                "index": {
                                  "type": "BinaryExpression",
                                  "operator": "+",
                                  "left": {
                                    "type": "Identifier",
                                    "name": "内側",
                                    "transpiledName": "inner"
                                  },
                                  "right": {
                                    "type": "Literal",
                                    "value": 1
                                  }
                                }
                              }
                            },
                            {
                              "type": "Assignment",
                              "left": {
                                "type": "ElementAccess",
                                "array": {
                                  "type": "Identifier",
                                  "name": "配列",
                                  "transpiledName": "array"
                                },
                                "index": {
                                  "type": "BinaryExpression",
                                  "operator": "+",
                                  "left": {
                                    "type": "Identifier",
                                    "name": "内側",
                                    "transpiledName": "inner"
                                  },
                                  "right": {
                                    "type": "Literal",
                                    "value": 1
                                  }
                                }
                              },
                              "right": {
                                "type": "Identifier",
                                "name": "一時",
                                "transpiledName": "temp"
                              }
                            }
                          ]
                        },
                        {
                          "type": "ExpressionStatement",
                          "expression": {
                            "type": "UnaryExpression",
                            "operator": "++",
                            "operand": {
                              "type": "Identifier",
                              "name": "内側",
                              "transpiledName": "inner"
                            }
                          }
                        }
                      ]
                    },
                    {
                      "type": "ExpressionStatement",
                      "expression": {
                        "type": "UnaryExpression",
                        "operator": "++",
                        "operand": {
                          "type": "Identifier",
                          "name": "外側",
                          "transpiledName": "outer"
                        }
                      }
                    }
                  ]
                }
              ]
            },
            {
              "type": "MethodDeclaration",
              "javadoc": {
                "summary": "ConsoleOut",
                "displayNameJa": "コンソール表示する",
                "params": [
                  {
                    "nameJa": "引数2",
                    "nameEn": "dispStr"
                  }
                ]
              },
              "modifiers": ["static"],
              "returnType": "void",
              "name": "コンソール表示する",
              "transpiledName": "consoleOut",
              "parameters": [
                {
                  "type": "string",
                  "name": "引数2",
                  "transpiledName": "dispStr"
                }
              ],
              "body": [
                {
                  "type": "ExpressionStatement",
                  "expression": {
                    "type": "InvocationExpression",
                    "target": {
                      "type": "MemberAccess",
                      "expression": {
                        "type": "Identifier",
                        "name": "コンソール",
                        "transpiledName": "Console"
                      },
                      "memberName": "一行表示する",
                      "transpiledMemberName": "WriteLine"
                    },
                    "arguments": [
                      {
                        "type": "Identifier",
                        "name": "引数2",
                        "transpiledName": "dispStr"
                      }
                    ]
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "imports": [
    {
      "type": "ImportDeclaration",
      "name": "System",
      "aliasClasses": [
        {
          "originalName": "コンソール",
          "transpiledName": "Console",
          "members": [
            {
              "originalName": "一行表示する",
              "transpiledName": "WriteLine",
              "parameters": [
                {
                  "type": "string?",
                  "name": "value"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

何が「おいしいポイント」か
この AST 風構造があると：
- 日本語 → 各言語のマッピング表をノード単位で保持できる
- name（日本語） / transpiledName（英語）
- コメントも nameJa / nameEn で保持
- 「線形探索・二分探索・バブルソート」を同じノード構造で並べて
- アルゴリズム差分だけを比較
- 「Re:Mind アルゴリズム図鑑」の骨格に出来る
- 将来的に
- Mermaid フローチャート
- UML クラス図
- 各言語へのコード生成
を全部この AST から起こせる

次にできること
この続きとして、例えば：
- 同じ AST 仕様で
- 線形探索 / 二分探索 の AST も並べてみる
- ノード型を固定して、
- 「Re:Mind AST 用のミニ仕様書」化する
- この AST から
- Java / C# / VB.NET コードを再生成する手順（マッピングルール）を明文化する
どこから深掘りしてみたいですか？
「まずは線形探索の AST も同じ形式で欲しい」など、次に見たいアルゴリズムを指定してくれれば、同じスタイルで並べていきます。

## 第２２ステップの評価
ＡＳＴのひとつの形が具現化できたのは思わぬ結果でした。現在のトランスコンパイラの実装はＡＳＴ化は行わずに変換対応していますが、いろいろな実装があってもよいと考えられます。

# おわりに
第２２ステップは以上です。アドベントカレンダーの枠としては完了しました。
## 目次
「Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす」の目次です。（ステップ降順）
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
