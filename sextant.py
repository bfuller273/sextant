import pyperclip
import re
import pyautogui as pg
import keyboard
import time
from numpy import random

pg.MINIMUM_DURATION = 0.01
pg.MINIMUM_SLEEP = 0.01

class SexBot:

	def __init__(self):
		self.mods = self.read_mods()
		#locations
		self.watchstone = 0,0
		self.sextantstash = 0,0
		self.compass = 0,0
		self.topleftinv = 0,0
		self.count = 0
		self.rolls = 50

	def read_mods(self):
		file = open("mods.txt")
		return file.read()

	def set_locations(self):
		print("mouse over watchstone and press f3")
		keyboard.wait('f3')
		self.watchstone = pg.position()

		print("mouse over sextant stash and press f3")
		keyboard.wait('f3')
		self.sextantstash = pg.position()

		print("mouse over top left inv and press f3")
		keyboard.wait('f3')
		self.topleftinv = pg.position()

		print("mouse over compass stash and press f3")
		keyboard.wait('f3')
		self.compass = pg.position()

		print("setup done ready to cook")

	def scan_sextant(self):
		pg.keyDown('ctrl')
		pg.press('c')
		pg.keyUp('ctrl')

		s=pyperclip.paste()
		match = re.search(self.mods, s, re.IGNORECASE)

		if match:
			return True
		else:
			return False

	def roll_sextant(self):

		paused = self.check_pause()
		if paused:
			return (True, False)

		#move to 
		pg.moveTo(self.sextantstash[0], self.sextantstash[1], random.uniform(0.15,0.25), pg.easeInOutQuad)
		pg.rightClick()
		pg.moveTo(self.watchstone[0], self.watchstone[1], random.uniform(0.15,0.25), pg.easeInOutQuad)		
		pg.keyDown('shift')

		while self.count < self.rolls:
			pg.leftClick()
			self.count = self.count + 1

			match = self.scan_sextant()
			if match:
				#print("match found")
				pg.keyUp('shift')
				return (False, False)
			else:
				#print("no match")
				time.sleep(random.uniform(0.4,0.7))
				paused = self.check_pause()
				if paused:
					return (True, False)

		pg.keyUp('shift')
		return (False, True)

	def compass_sextant(self):

		paused = self.check_pause()
		if paused:
			return True

		#move to compass
		pg.moveTo(self.compass[0], self.compass[1], random.uniform(0.15,0.25), pg.easeInOutQuad)
		pg.rightClick()
		#move to watchstone
		pg.moveTo(self.watchstone[0], self.watchstone[1], random.uniform(0.15,0.25), pg.easeInOutQuad)
		pg.leftClick()	
		#move to inv	
		pg.moveTo(self.topleftinv[0], self.topleftinv[1], random.uniform(0.15,0.25), pg.easeInOutQuad)
		pg.leftClick()
		#stash it
		pg.press('right')
		pg.keyDown('ctrl')
		pg.leftClick()
		pg.keyUp('ctrl')
		pg.press('left')		

		return False

	def check_pause(self):
		if keyboard.is_pressed('f2'):
			return True
		else:
			return False

	def pause(self):
		pg.keyUp('shift')

		print("Paused, press f3 to continue")
		keyboard.wait('f3')

		print("mouse over watchstone and press f3")
		keyboard.wait('f3')
		self.watchstone = pg.position()

class ChanceBot:

	def __init__(self):	
		self.count = 0
		self.rolls = 50
		#locations		
		self.chance = 0,0
		self.scour = 0,0
		self.item = 0,0

	def set_locations(self):
		print("mouse over chance and press f3")
		keyboard.wait('f3')
		self.chance = pg.position()

		print("mouse over scour stash and press f3")
		keyboard.wait('f3')
		self.scour = pg.position()

		print("mouse over item and press f3")
		keyboard.wait('f3')
		self.item = pg.position()

		print("setup done ready to cook")

	def chance_item(self):

		paused = self.check_pause()
		if paused:
			return True

		#move to scour
		pg.moveTo(self.scour[0], self.scour[1], random.uniform(0.1,0.15), pg.easeInOutQuad)
		pg.rightClick()
		#move to item
		pg.moveTo(self.item[0], self.item[1], random.uniform(0.1,0.15), pg.easeInOutQuad)
		pg.leftClick()	

		#move to chance
		pg.moveTo(self.chance[0], self.chance[1], random.uniform(0.1,0.15), pg.easeInOutQuad)
		pg.rightClick()
		#move to item
		pg.moveTo(self.item[0], self.item[1], random.uniform(0.1,0.15), pg.easeInOutQuad)
		pg.leftClick()

		self.count = self.count + 1

		return False

	def check_pause(self):

		if keyboard.is_pressed('f2'):
			return True
		else:
			return False

	def pause(self):

		print("Paused, press f3 to continue")
		keyboard.wait('f3')



bot = SexBot()
chancebot = ChanceBot()
print("F1: start\tF2: set sex locations\tF3: set rolls\tF4: set chance location\tF6: chance\tQ: quit")

while True:
	event = keyboard.read_event()

	if event.event_type == keyboard.KEY_DOWN and event.name == 'f1':
		bot.count = 0;
		print("rolling for", bot.rolls, "sextants, hold f2 to pause")
		while bot.count < bot.rolls:
			paused, finished = bot.roll_sextant()			
			if paused:
				bot.pause()
				continue
			if finished:
				break

			paused = bot.compass_sextant()
			if paused:
				bot.pause()
				continue
		print("Run Finished")
		print("F1: start\tF2: set locations\tF3: set rolls\tQ: quit")
		

	if event.event_type == keyboard.KEY_DOWN and event.name == 'f2':
		bot.set_locations()

	if event.event_type == keyboard.KEY_DOWN and event.name == 'f3':
		rolls = int(input("Input number of rolls: "))
		bot.rolls = rolls
		chancebot.rolls = rolls
		print("Number of rolls set to", bot.rolls)

	if event.event_type == keyboard.KEY_DOWN and event.name == 'f4':
		chancebot.set_locations()

	if event.event_type == keyboard.KEY_DOWN and event.name == 'f6':
		chancebot.count = 0
		print("rolling for", chancebot.rolls, "chances, hold f2 to pause")
		while chancebot.count < chancebot.rolls:
			paused = chancebot.chance_item()			
			if paused:
				chancebot.pause()
				continue
		print("Run Finished")

	if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
		print("QUITTING")
		break

