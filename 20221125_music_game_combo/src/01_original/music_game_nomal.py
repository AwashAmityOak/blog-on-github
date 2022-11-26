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
