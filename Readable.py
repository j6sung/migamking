import pygame
import os
import collections
import re
import inspect

class Readables:

	def __init__(self):
		self.font = pygame.font.Font("Fonts\\ttf_pixolde.ttf", 14)
		self.readable_0 = ((304, 278, 29, 27), """Let's jump to window 10 !!
					 							You can do it !""")
		self.readable_3 =  ((175, 57, 23, 23), """
												Let't jump to page table !
					  							First, PML4 TABLE
					  							Second, PDP TABLE
					  							Third, DIR
					  							Finally, PAGE TABLE !!!
					  							Tang! Tang! Tang! Tang!""")
		self.readable_7 = ((329, 239, 31, 33), """Lastly, Let's rescue the bread man
												Jump to the bob center !!!""")
		self.readables = collections.defaultdict()
		self._load_readables() 

	def _load_readables(self):
		self.readables[0] = Readable(self.readable_0[0], self.readable_0[1], self.font)
		self.readables[3] = Readable(self.readable_3[0], self.readable_3[1], self.font)
		self.readables[7] = Readable(self.readable_7[0], self.readable_7[1], self.font)

class Readable:

	def __init__(self, rect, quote, font):

		self.interval = 10

		self.pause_interval = 360

		self.pause = 0

		self.blit_counter = 0

		self.rect = pygame.Rect(rect)

		self.quote = quote

		self.font = font

		self.line = iter(inspect.cleandoc(quote))

		self.text = ""

		self.channel = pygame.mixer.Channel(9)

		self.channel_counter = 1

		self.audio = pygame.mixer.Sound("Audio\\Misc\\talking.wav")

	def update(self, king):
		# if문과 else문을 모두 삭제하고 try 구문만 남깁니다.
		try:
			if not self.blit_counter % self.interval:
				next_letter = next(self.line)
				if next_letter == "\n":
					self.blit_counter = str(self.blit_counter)
				else:
					self.text += next_letter
					if next_letter != " ":
						self.channel.play(self.audio)
			self.blit_counter += 1
		except TypeError:
			self.pause += 1
			if self.pause > self.pause_interval / 4:
				self.pause = 0
				self.blit_counter = int(self.blit_counter)
				self.text = ""
		except StopIteration:
			self.pause += 1
			if self.pause > self.pause_interval:
				self.reset()

	def reset(self):
		self.line = iter(inspect.cleandoc(self.quote))
		self.blit_counter = 0
		self.pause = 0
		self.text = ""

	def blitmetext(self, screen):
		if self.text:
			for index, line in enumerate(map(lambda x: x[0], re.findall(r"(([^ .,!?]+[ .,!?]*){0,4})", self.text)[::-1])):
				text = self.font.render(line, True, (255, 255, 255))
				text_x, text_y = self.rect.x - text.get_width(), self.rect.y - (index + 1) * text.get_height()
				if text_x < 0:
					text_x = self.rect.right				
				screen.blit(text, (text_x, text_y))