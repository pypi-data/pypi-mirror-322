[![PyPI Downloads](https://static.pepy.tech/badge/typehandler)](https://pepy.tech/projects/typehandler)

# typehandler

`typehandler` は、タイピングゲーム用のPythonモジュールです。このモジュールは、ひらがなをローマ字に変換し、タイピングゲームの入力パターンを生成します。また、pygameやtkinterなどでキーイベントを検知し、入力されたキーを渡すことで、正誤判定などができます。これにより、タイピングゲームに必要な処理を行うことができます。

## インストール

```sh
pip install typehandler
```

## 使用方法

### 基本的な使い方

まず、`typehandler` モジュールをインポートし、`Process` クラスを使用します。Processクラスは、お題とそのフリガナの辞書を受け取ります。

```python
import typehandler

# お題とフリガナの辞書
words = {
    "西瓜": "すいか",
    "いちご": "いちご",
    "バナナ": "ばなな"
}

# Processクラスのインスタンスを作成
game_process = typehandler.Process(words)
```
辞書を設定するためのメソッドもあるので、必ずしもインスタンス作成のタイミングで辞書を渡す必要はありません。

#### 1. 新しい文章の設定

新しい文章を設定するには、`set_new_sentence` メソッドを使用します。このメソッドが呼び出されると、辞書からランダムに文章を選び、正誤判定に必要な準備まで行います。このメソッドを呼び出す以外に、文章の更新に必要な手順はありません。文章を打ち終わったときや、制限時間を過ぎたときに呼び出すことを想定しています。

```python
game_process.set_new_sentence()
```
通常は引数を受け取らずに使用することを想定しています。しかし、このメソッドは辞書を受け取ることができ、その場合、一度だけその辞書から文章を選びます。このモジュールでは完全ランダム以外に文章を選ぶ機能は実装していない関係で、一部のプロジェクトには使用できない場合があり、それを解決するための機能です。自分で文章を選んだあと、このメソッドに要素が1つの辞書を渡すことで、疑似的に文章を選ぶ機能を入れ替えることができます。

#### 2. 別の辞書を設定

別の辞書を設定するには、`set_new_words` メソッドを使用します。このメソッドを呼び出すと、`set_new_sentence`が呼び出され、次に表示する文章を選ぶところまで実行します。

```python
new_words = {
    "林檎": "りんご",
    "ぶどう": "ぶどう",
    "レモン": "れもん"
}
game_process.set_new_words(new_words)
```

#### 3. 入力の判定

入力が正しいかどうかを判定するには、`check_correct_input` メソッドを使用します。このメソッドは引数にキーの名前を受け取り、`True`か`False`を返します。基本的に`if`文の条件に使うことを想定しています。

```python
key = 'k'
is_correct = game_process.check_correct_input(key)
print(is_correct)  # True または False
```

以下のように、第二引数に`True`を渡すと、内部で、文字をシフトが押された状態のものに置き換えます。たとえば、この例では、入力を'K'として判定を行います。pygameなどでは、`event.unicode`を使う事で、あらかじめシフトが押されている場合の文字を取得できるので、こちらは利用する必要はありません。引数を渡さない場合はデフォルトで`False`になるので、第二引数を渡さずに使えばOKです。

```python
key = 'k'
is_correct = game_process.check_correct_input(key, True)
print(is_correct)  # True または False
```


#### 4. ひらがなの完了判定
ひらがなが完了したかどうかを判定するには`check_chunk_completion`メソッドを使用します。`check_correct_input`が`True`を返した後の`if`文の条件に使う事を想定しています。
```python
is_completed = game_process.check_chunk_completion()
print(is_completed)  #True または False
```

#### 5. 文章の完了判定

文章が完了したかどうかを判定するには、`check_sentence_completion` メソッドを使用します。`check_chunk_completion`が`True`を返した後の`if`文の条件に使うことを想定しています。

```python
is_completed = game_process.check_sentence_completion()
print(is_completed)  # True または False
```

#### 6. 画面に表示するローマ字の更新

　このモジュールでは、画面に描画するための、入力パターンの一例として`show_roman`というものを用意しています。直接このインスタンス変数にアクセスしていただくだけで利用できますが、あくまで一例を表示するだけなので、適宜更新しないとずれが生じてきます。
　画面に表示するローマ字を更新するには、`update_show_roman` メソッドを使用します。リアルタイムに反映させるために、ゲームループの中で、適切に更新することが求められます。毎フレーム呼び出すか、入力を検知するたびに呼び出すか、都合の良い方を選んで使ってください。このメソッドは、戻り値に入力パターンの一例を返しますが、必ずしも受け取る必要はありません。

```python
show_roman = game_process.update_show_roman()
print(show_roman)
```

#### 7. 全てこれで完結
上記の正誤判定から文章の更新までのメソッドを全てまとめた`main`というメソッドを用意してあります。これはキーの名前を受け取り、正誤判定から、文章の更新までの全てを行います。音声などの処理をそれぞれ追加する需要に応えるため、上記のメソッドを用意しています。しかし、音声も何もいらないという人は、これだけを呼び出せば、ゲームシステムは完成します。
アップデートで0~3のいずれかの数字を返すように機能を追加しました。これによって、mainの結果次第で、処理の追加を行うことができるようになりました。数字か以下のクラス変数名のいずれかを使って判定していただけます。※文章の入力完了時に、辞書を切り替えたりするような場合は、この方法では対応しきれないので、旧バージョンの方法を引き続きご利用ください。
```python
if result == game_process.MISS:                 #ミスタイプ時の処理を追加したい時(== 0)
if result == game_process.CORRECT:              #正しい入力時の処理を追加したい時(== 1)
if result == game_process.CHUNK_COMPLETE:       #ひらがなが完了した時の処理を追加したい時(== 2)
if result == game_process.SENTENCE_COMPLETE:    #文章が完了した時の処理を追加したい時(== 3)
```

おすすめの使用例
```python
key = 'k'
result = game_process.main(key)
if result:
    #正しい入力時の処理
    if result == 3:
        #文章が完了した時の処理
else:
    #ミスタイプ時の処理
```

こちらも第二引数に`True`を渡すと、内部で、文字をシフトが押された状態のものに置き換えます。たとえば、この例では、入力を'K'として判定を行います。

```python
key = 'k'
game_process.main(key, True)
```
#### 8. その他のメソッド
入力として有効なキーの名前の一覧を出力します
```python
game_process.show_key_names()
```

キーの名前を受け取って、シフトが押されている場合のキーの名前を返します。内部で行っている置換の処理もこれなので、キーが正しく入力されているかどうか`print`デバッグで確かめる際に使うと良いと思います。
```python
key = 'k'
new_key = game_process.shift_filter(key)
print(new_key)    #K
```

入力として有効なキーに含まれているかどうかを判定します。無効なキーが入力され、無視するべき場合に`True`を返します。Falseが帰ってきたときだけ正誤判定の処理を走らせる等の利用を想定しています。シフトを押さないと入力できない文字がお題に含まれているなら、多くの場合このメソッドが必要になります。そうでないとシフトを押した際に、ミスタイプ判定が行われます。また、音量の変更などをキー操作でした場合にも、このメソッドがあれば無視してくれます。

```python
key = 'k'
if not game_process.check_ignore(key):
    game_process.main(key)
```

#### 9.利用可能なインスタンス変数
画面に描画するための文字列など、自由にご使用いただけます。（描画機能自体はこのモジュールには実装していません。）
```python
self.input              #入力済みのローマ字
self.show_roman         #入力パターンの一例
self.sentence           #現在の文章
self.words              #文章のフリガナの辞書
self.next               #次の文章
```

#### 10.ローマ字の生成だけ使いたい場合
メインの使用方法からは逸れますが、ひらがなからローマ字の生成を行う部分だけを使いたい人もいると思うので、`divide`というメソッドを用意しておきました。
```python
game_process.divide('あいうえお')
```

## サンプルコード
pygameのテンプレに毛が生えた程度のコードで、本格的なタイピングゲームを実装できます。このコードでは日本語、記号、英数字が含まれている文章に対応しています。さらに、日本語については複数パターンの入力に対応しています。例）sha、sya、silyaなど

```python
import pygame, sys
from typehandler import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('example')
clock = pygame.time.Clock()
font = pygame.font.SysFont('MS Gothic', 32)

words = {'りんご食べたい':'りんごたべたい',
         'for i in range(0, 10):':'for i in range(0, 10):',
         '1+1=2':'1+1=2',
         'print("AはBと言った")':'print("AはBといった")',
         'I want to eat salmon.':'I want to eat salmon.'}

def main():
    process = Process(words)
    while True:
        process.update_show_roman()    #これ必須
        screen.fill((255, 255, 255))
        text_roman = font.render(process.show_roman, True, (192, 192, 192))    #入力例
        text_input = font.render(process.input, True, (0, 0, 0))               #現在の入力
        text_sentence = font.render(process.sentence, True, (0, 0, 0))         #お題の文章
        text_next = font.render('next=>'+process.next, True, (192, 192, 192))  #次の文章
        pygame.draw.line(screen, (0, 128, 255), (0, 50), (600, 50), 5)         #青い線を描画
        pygame.draw.line(screen, (255, 128, 0), (0, 150), (600, 150), 5)       #オレンジの線を描画
        screen.blit(text_roman, (30,60))
        screen.blit(text_input, (30,60))
        screen.blit(text_sentence, (30, 100))
        screen.blit(text_next, (180, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_name = event.unicode                  #これを使えばシフト入力も対応できるから楽
                if not process.check_ignore(key_name):    #シフトとかファンクションキーとかは正誤判定しない
                    process.main(key_name)                #この一文で正誤判定から文章の切り替えまで全部やってくれる！
        pygame.display.update()
        clock.tick(50)    #fpsは50くらいがおすすめ

if __name__ == '__main__':
    main()
```

もう数行増えますが、mainを使わずに、メソッドを組み合わせて処理部分を実装することで、入力時や、ミスタイプを検知した際の処理を自由にカスタマイズすることができます。これにより、音声の実装や、タイピングの結果と連動した、ゲーム画面の処理が行えます。

```python
import pygame, sys
from typehandler import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('example')
clock = pygame.time.Clock()
font = pygame.font.SysFont('MS Gothic', 32)

words = {'りんご食べたい':'りんごたべたい',
         'for i in range(0, 10):':'for i in range(0, 10):',
         '1+1=2':'1+1=2',
         'print("AはBと言った")':'print("AはBといった")',
         'I want to eat salmon.':'I want to eat salmon.'}

def main():
    process = Process(words)
    while True:
        process.update_show_roman()    #これ必須
        screen.fill((255, 255, 255))
        text_roman = font.render(process.show_roman, True, (192, 192, 192))    #入力例
        text_input = font.render(process.input, True, (0, 0, 0))               #現在の入力
        text_sentence = font.render(process.sentence, True, (0, 0, 0))         #お題の文章
        pygame.draw.line(screen, (0, 128, 255), (0, 50), (600, 50), 5)         #青い線を描画
        pygame.draw.line(screen, (255, 128, 0), (0, 150), (600, 150), 5)       #オレンジの線を描画
        screen.blit(text_roman, (30,60))
        screen.blit(text_input, (30,60))
        screen.blit(text_sentence, (30, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_name = event.unicode                  #これを使えばシフト入力も対応できるから楽
                if process.check_ignore(key_name):    #シフトとかファンクションキーとかは正誤判定しない
                    continue
                if correct_input:
                    #正しい入力がされた時の処理をここに追加
                    chunk_completed = self.check_chunk_completion()    #文章の打ち終わりを判定
                    if chunk_completed:
                        #ひらがなが打ち終わったときの処理をここに追加
                        sentence_completed = self.check_sentence_completion()
                        if sentence_completed:
                            #文章が打ち終わった時の処理をここに追加
                            self.sentence, self.hurigana, self.divided_roman = self.__create_sentence()    #新しい文章を用意
                else:
                    #ミスタイプ時の処理をここに追加
                    pass
        pygame.display.update()
        clock.tick(50)    #fpsは50くらいがおすすめ

if __name__ == '__main__':
    main()
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は`LICENSE`ファイルを参照してください。