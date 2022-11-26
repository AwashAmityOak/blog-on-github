# 音ゲーにコンボの仕組みを入れたい

作成日時: 2022年11月25日, 最終更新: 2022年11月26日

***

**To readers who don't speak Japanese:**
+ This page that I wrote for my friend is written with Japanese. Sorry.

**※注意**

私が書いたこの記事は間違っている箇所があるかもしれません。また、最終更新日時が一年以上立っている場合には、この記事の信憑性を疑うようにしてください。誤字、脱字、コードのエラー箇所などは、IssuesやPull requestで教えてくれるとありがたいです。

***

## この記事を書いた理由

何日か前に、友達（プログラミング仲間）が、[プロセカ](https://pjsekai.sega.jp/)みたいな音ゲーを見せてくれました。そのゲームには、コンボの機能がなかったので、教えるために書いてみようと思ったわけです。
[はてなブログ](https://hatenablog.com/)とか[Zenn](https://zenn.dev/)とかに投稿しようかな〜とも検討したのですが、アカウント作るの面倒くさいし、Githubにmarkdownを載せちゃおうかと考え、今ここに書いています。

## 想定読者

+ 私に音ゲーを見せてくれた友達
+ 上記の友達以外の私の知り合い
+ [Python](https://www.python.org/)の[Pygame](https://www.pygame.org/news)でプログラミングをしたことがある方
+ ポイント制のゲームにて、ミスをせずに、ポイントが入る行動を連続ですると、一回で得られるポイントが高くなる仕組み（いわばコンボです）の作り方を知りたい方

(※私のGithubアカウントはまだ出来立てなので、私の知っている人以外見ないと思いますが…)

## 動作確認
+ macOS Catalina 10.15.7
+ python 3.7.3
+ pygame 2.1.2

## 編集前のコード

このコードを友達が見せてくれました。（[このGithubリポジトリにもあげておきます。](src/02_tidied/music_game_nomal.py)）

<details><summary>コード</summary>

```python
import sys
import random
import pyxel
import time

import pygame as pg

pg.init()

WIDTH = 1000
HEIGHT = 500

screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
timer = 0
score = 0
time = 0

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 100)

font_score = pg.font.Font(None,20)

def bar_pos(index_x, y, h):
	return ((WIDTH // 4) * index_x + 5, y, (WIDTH // 4) - 10, h)

class Note():
	def __init__(self,index_x,y):
		self.index_x = index_x
		self.y = y
	def move_y_direction(self):
		# ノーツの第二(1)の速さの制御
		self.y += 10
	def draw(self):
		# 青い四角形の絵画
		pg.draw.rect(screen,BLUE,bar_pos(self.index_x,self.y,25)) 

notes = []

def spawn_notes(timer):
	# %の次の値を変えることで、ノーツの数を変えられる。
	if timer % 40 == 0:
		notes.append(Note(random.randint(0,3), -50))

def update_notes():
	for i in range(len(notes)):
		notes[i].move_y_direction()

def delete_notes(keys):
	global score
	indexes = []
	for i in range(len(notes)):
		if HEIGHT < notes[i].y:
			indexes.append(i)
		#if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 440 + 20:
		if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 441:   
			indexes.append(i)
			score += 1
		elif keys[notes[i].index_x] and 441 <= notes[i].y + 25 and notes[i].y < 450:
			indexes.append(i)
			score += 1000
		elif keys[notes[i].index_x] and 450 <= notes[i].y + 25 and notes[i].y < 455:
			indexes.append(i)
			score += 4000
		elif keys[notes[i].index_x] and 455 <= notes[i].y + 25 and notes[i].y < 465:
			indexes.append(i)
			score += 5000
		elif keys[notes[i].index_x] and 465 <= notes[i].y + 25 and notes[i].y < 470:
			indexes.append(i)
			score += 4000
		elif keys[notes[i].index_x] and 470 <= notes[i].y + 25 and notes[i].y < 475:
			indexes.append(i)
			score += 1000
		elif keys[notes[i].index_x] and 475 <= notes[i].y + 25 and notes[i].y < 480:
			indexes.append(i)
			score += 100
	for value in indexes:
		notes.pop(value)

def draw_notes():
	for i in range(len(notes)):
		notes[i].draw()

keys = [False,False,False,False]
def get_keys():
	pg.event.pump()
	pressed = pg.key.get_pressed()
	keys[0] = pressed[pg.K_d]
	keys[1] = pressed[pg.K_f]
	keys[2] = pressed[pg.K_j]
	keys[3] = pressed[pg.K_k]

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	get_keys()
	spawn_notes(timer)
	update_notes()
	delete_notes(keys)
	
	screen.fill(BLACK)
	for i in range(4):
		pg.draw.rect(screen, RED, bar_pos(i,440,20))
	draw_notes()
	text_score = font_score.render("score: "+str(score),True,WHITE)
	screen.blit(text_score,(0, 0))
	pg.display.update()

	timer += 1

	# 全体の速さの制御
	clock.tick(100)

```

</details>

## まず整形

上記のコードには、ちょっと気になるところがあったので、整形していきます。早くコンボのやり方が知りたいよーって人は、[本題](#本題)に飛んでください。

### 不要なモジュール

[Pyxel](https://github.com/kitao/pyxel/)やtimeモジュールは、このプログラムでは使われていません。余計にインポートの時間がかかり、コードを読む人を混乱させる恐れがあるため削除します。
個人的には、`import pygame as pg`を、`import pygame`にして、変数名を極端に短くするのは避けます。

<details><summary>コード</summary>

before

```python
# Line 1

import sys
import random
import pyxel
import time

import pygame as pg
```

after

```python
# Line 1

import sys
import random

import pygame as pg
# import pygame
```

</details>

### 定数・変数・初期化！

下記のbeforeコードでは、定数の定義、変数の宣言、pygameの初期化処理がごちゃごちゃに書かれています。
普通は

1. 定数の定義
2. 変数の定義
3. 初期化処理

の順番で書いた方がわかりやすいと思います。

また、変数`time`は使われていないので消します。（それから、もともとインポートしていた`time`モジュールを上書きするようなことはしちゃダメです。）

<details><summary>コード</summary>

before

```python
# Line 8

pg.init()

WIDTH = 1000
HEIGHT = 500

screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
timer = 0
score = 0
time = 0

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 100)

font_score = pg.font.Font(None,20)
```
after

```python
# Line 7

WIDTH = 1000
HEIGHT = 500

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 100)

timer = 0
score = 0

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
font_score = pg.font.Font(None,20)
```

</details>

### 整形完了！

よし！

<details><summary>全体のコード</summary>

```python
import sys
import random

import pygame as pg
# import pygame

WIDTH = 1000
HEIGHT = 500

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 100)

timer = 0
score = 0

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
font_score = pg.font.Font(None,20)

def bar_pos(index_x, y, h):
	return ((WIDTH // 4) * index_x + 5, y, (WIDTH // 4) - 10, h)

class Note():
	def __init__(self,index_x,y):
		self.index_x = index_x
		self.y = y
	def move_y_direction(self):
		# ノーツの第二(1)の速さの制御
		self.y += 10
	def draw(self):
		# 青い四角形の絵画
		pg.draw.rect(screen,BLUE,bar_pos(self.index_x,self.y,25)) 

notes = []

def spawn_notes(timer):
	# %の次の値を変えることで、ノーツの数を変えられる。
	if timer % 40 == 0:
		notes.append(Note(random.randint(0,3), -50))

def update_notes():
	for i in range(len(notes)):
		notes[i].move_y_direction()

def delete_notes(keys):
	global score
	indexes = []
	for i in range(len(notes)):
		if HEIGHT < notes[i].y:
			indexes.append(i)
		#if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 440 + 20:
		if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 441:   
			indexes.append(i)
			score += 1
		elif keys[notes[i].index_x] and 441 <= notes[i].y + 25 and notes[i].y < 450:
			indexes.append(i)
			score += 1000
		elif keys[notes[i].index_x] and 450 <= notes[i].y + 25 and notes[i].y < 455:
			indexes.append(i)
			score += 4000
		elif keys[notes[i].index_x] and 455 <= notes[i].y + 25 and notes[i].y < 465:
			indexes.append(i)
			score += 5000
		elif keys[notes[i].index_x] and 465 <= notes[i].y + 25 and notes[i].y < 470:
			indexes.append(i)
			score += 4000
		elif keys[notes[i].index_x] and 470 <= notes[i].y + 25 and notes[i].y < 475:
			indexes.append(i)
			score += 1000
		elif keys[notes[i].index_x] and 475 <= notes[i].y + 25 and notes[i].y < 480:
			indexes.append(i)
			score += 100
	for value in indexes:
		notes.pop(value)

def draw_notes():
	for i in range(len(notes)):
		notes[i].draw()

keys = [False,False,False,False]
def get_keys():
	pg.event.pump()
	pressed = pg.key.get_pressed()
	keys[0] = pressed[pg.K_d]
	keys[1] = pressed[pg.K_f]
	keys[2] = pressed[pg.K_j]
	keys[3] = pressed[pg.K_k]

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	get_keys()
	spawn_notes(timer)
	update_notes()
	delete_notes(keys)
	
	screen.fill(BLACK)
	for i in range(4):
		pg.draw.rect(screen, RED, bar_pos(i,440,20))
	draw_notes()
	text_score = font_score.render("score: "+str(score),True,WHITE)
	screen.blit(text_score,(0, 0))
	pg.display.update()

	timer += 1

	# 全体の速さの制御
	clock.tick(100)
```

</details>

[Githubにも載せておきますね。](src/02_tidied/music_game_nomal.py)

## 本題

やっと本題です。

### 1. コンボカウント用の変数

最初の変数定義のところに、カウント用の変数を追記します。

```python
timer = 0
score = 0
# コンボ用の変数追加
combo = 0
```

### 2. コンボ数追加処理

このプログラムでは、`delete_notes`関数でノーツを消す処理を行なっているのでそこにコンボ数を増やす処理を入れます。
また、ノーツを叩けなかったとき（ノーツが画面下まで行ってしまったとき）には、コンボ数をリセットします。

```python
def delete_notes(keys):
	# グローバル変数宣言追加忘れずに！
	global score, combo
	indexes = []
	for i in range(len(notes)):
		if HEIGHT < notes[i].y:
			indexes.append(i)
			# コンボ数のリセット
			combo = 0
		#if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 440 + 20:
		if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 441:   
			indexes.append(i)
			score += 1
			# コンボ数の追加（以下同様に）
			combo += 1
		elif keys[notes[i].index_x] and 441 <= notes[i].y + 25 and notes[i].y < 450:
			indexes.append(i)
			score += 1000
			combo += 1
		elif keys[notes[i].index_x] and 450 <= notes[i].y + 25 and notes[i].y < 455:
			indexes.append(i)
			score += 4000
			combo += 1
		elif keys[notes[i].index_x] and 455 <= notes[i].y + 25 and notes[i].y < 465:
			indexes.append(i)
			score += 5000
			combo += 1
		elif keys[notes[i].index_x] and 465 <= notes[i].y + 25 and notes[i].y < 470:
			indexes.append(i)
			score += 4000
			combo += 1
		elif keys[notes[i].index_x] and 470 <= notes[i].y + 25 and notes[i].y < 475:
			indexes.append(i)
			score += 1000
			combo += 1
		elif keys[notes[i].index_x] and 475 <= notes[i].y + 25 and notes[i].y < 480:
			indexes.append(i)
			score += 100
			combo += 1
	for value in indexes:
		notes.pop(value)
```

### 3. コンボ数表示処理

`while`ループの中で、表示処理を作ります。すでにスコアを表示する処理があるので、それを参考に。

```python
while True:

	# フレーム更新処理省略

	screen.fill(BLACK)
	for i in range(4):
		pg.draw.rect(screen, RED, bar_pos(i,440,20))
	draw_notes()
	text_score = font_score.render("score: "+str(score),True,WHITE)
	screen.blit(text_score,(0, 0))

	# ここでコンボの描画をします。

	text_combo = font_score.render("combo: "+str(combo),True,WHITE)
	screen.blit(text_combo,(0, 20))

	pg.display.update()

	timer += 1

	# 全体の速さの制御
	clock.tick(100)
```

あとは、お好きに演出を追加してください。

### 音ゲー以外を作る人へ: 一度に入る点数をあげるには

こんな風に自分で計算式を考えて、スコアを追加する処理を作ってください。

```python
score += int(100 * (combo / 10))
```

### 完成品

<details><summary>コード</summary>

```python
import sys
import random

import pygame as pg
# import pygame

WIDTH = 1000
HEIGHT = 500

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 100)

timer = 0
score = 0
# コンボ用の変数追加
combo = 0

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
font_score = pg.font.Font(None,20)

def bar_pos(index_x, y, h):
	return ((WIDTH // 4) * index_x + 5, y, (WIDTH // 4) - 10, h)

class Note():
	def __init__(self,index_x,y):
		self.index_x = index_x
		self.y = y
	def move_y_direction(self):
		# ノーツの第二(1)の速さの制御
		self.y += 10
	def draw(self):
		# 青い四角形の絵画
		pg.draw.rect(screen,BLUE,bar_pos(self.index_x,self.y,25)) 

notes = []

def spawn_notes(timer):
	# %の次の値を変えることで、ノーツの数を変えられる。
	if timer % 40 == 0:
		notes.append(Note(random.randint(0,3), -50))

def update_notes():
	for i in range(len(notes)):
		notes[i].move_y_direction()

def delete_notes(keys):
	global score, combo
	indexes = []
	for i in range(len(notes)):
		if HEIGHT < notes[i].y:
			indexes.append(i)
			combo = 0
		#if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 440 + 20:
		if keys[notes[i].index_x] and 440 <= notes[i].y + 25 and notes[i].y < 441:   
			indexes.append(i)
			score += 1
			combo += 1
		elif keys[notes[i].index_x] and 441 <= notes[i].y + 25 and notes[i].y < 450:
			indexes.append(i)
			score += 1000
			combo += 1
		elif keys[notes[i].index_x] and 450 <= notes[i].y + 25 and notes[i].y < 455:
			indexes.append(i)
			score += 4000
			combo += 1
		elif keys[notes[i].index_x] and 455 <= notes[i].y + 25 and notes[i].y < 465:
			indexes.append(i)
			score += 5000
			combo += 1
		elif keys[notes[i].index_x] and 465 <= notes[i].y + 25 and notes[i].y < 470:
			indexes.append(i)
			score += 4000
			combo += 1
		elif keys[notes[i].index_x] and 470 <= notes[i].y + 25 and notes[i].y < 475:
			indexes.append(i)
			score += 1000
			combo += 1
		elif keys[notes[i].index_x] and 475 <= notes[i].y + 25 and notes[i].y < 480:
			indexes.append(i)
			score += 100
			combo += 1
	for value in indexes:
		notes.pop(value)

def draw_notes():
	for i in range(len(notes)):
		notes[i].draw()

keys = [False,False,False,False]
def get_keys():
	pg.event.pump()
	pressed = pg.key.get_pressed()
	keys[0] = pressed[pg.K_d]
	keys[1] = pressed[pg.K_f]
	keys[2] = pressed[pg.K_j]
	keys[3] = pressed[pg.K_k]

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	get_keys()
	spawn_notes(timer)
	update_notes()
	delete_notes(keys)
	
	screen.fill(BLACK)
	for i in range(4):
		pg.draw.rect(screen, RED, bar_pos(i,440,20))
	draw_notes()
	text_score = font_score.render("score: "+str(score),True,WHITE)
	screen.blit(text_score,(0, 0))

	text_combo = font_score.render("combo: "+str(combo),True,WHITE)
	screen.blit(text_combo,(0, 20))

	pg.display.update()

	timer += 1

	# 全体の速さの制御
	clock.tick(100)
```

</details>

[こちら](src/03_finished/music_game_nomal.py)からも。

## 終わりに

初めてこのようなプログラミングの技術ブログ（のようなもの）を書いてみましたが、難しいですね。私の説明はわかりにくいと思うので、元の音ゲーを見せてくれた友達以外は、多分この記事の内容がわからないと思います（ｽﾐﾏｾﾝ）。もしかしたら、友達に頼まれて、またこんな日記を書くかもしれませんが、現時点ではないと思います。（もしこのまま増えていったとしたら、黒歴史として残しておこうかな…）

では、さようなら。
