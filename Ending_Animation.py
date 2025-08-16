#!/usr/bin/env python
#
#
#
#

import pygame
import os
import sys
import math


class Ending_Animation:

    def __init__(self):

        self.end_counter = 0

        self.end_pan = (-90, 90)

        self.stall_x = 240

        self.stall_y = 220

        self.channel = pygame.mixer.Channel(1)

        self.ending_music = pygame.mixer.Sound("Audio\\Misc\\ending.wav")

        self.end_image = pygame.image.load("images\\sheets\\imagecrown.png").convert()

    # --- [FIX] flyer 존재 체크 유틸 ---
    def _has_flyer(self, level):
        return hasattr(level, "flyer") and (level.flyer is not None)

    def update(self, level, king, babe):

        king_command = None
        babe_command = None

        if self.move_screen(level, king, babe):
            if self.end_counter < 50:

                pass

            elif self.end_counter == 50:

                babe_command = "Crouch"

            elif self.end_counter < 60:

                pass

            elif self.end_counter == 60:

                babe_command = "Jump"

            elif self.end_counter <= 120:

                pass

            elif self.end_counter <= 150:

                babe_command = "WalkLeft"

            elif self.end_counter <= 175:

                babe_command = "Kiss"

            elif self.end_counter <= 190:
                # --- [FIX] flyer 가드 ---
                if self._has_flyer(level):
                    level.flyer.active = True

            elif self.end_counter <= 205:

                king_command = "LookUp"
                # babe_command = "WalkRight"

            elif self.end_counter <= 1000:
                king_command = "jump"
                # sys.exit()


                return True

            self.end_counter += 1

        king.update(king_command)

        babe.update(king, babe_command)

    def scroll_screen(self, level, king):

        if king.rect_x > self.stall_x:

            rel_x = self.stall_x - king.rect_x

            king.rect_x += rel_x

            if level.midground:
                level.midground.x += rel_x

            if level.props:
                for prop in level.props:
                    prop.x += rel_x

            if level.npc:
                level.npc.x += rel_x

            if level.foreground:
                level.foreground.x += rel_x

            if level.platforms:
                for platform in level.platforms:
                    platform.x += rel_x

        if king.rect_y > self.stall_y:

            rel_y = self.stall_y - king.rect_y

            if self.stall_y > level.screen.get_height() / 2:

                self.stall_y -= 2

            king.rect_y += rel_y

            if level.midground:
                level.midground.y -= math.sqrt(abs(rel_y))

            if level.props:
                for prop in level.props:
                    prop.y -= math.sqrt(abs(rel_y))

            if level.npc:
                level.npc.y -= math.sqrt(abs(rel_y))

            if level.foreground:
                level.foreground.y -= math.sqrt(abs(rel_y))

            if level.platforms:
                for platform in level.platforms:
                    platform.y -= math.sqrt(abs(rel_y))


    def move_screen(self, level, king, babe):
        # print("bye")
        return True

    def update_audio(self):

        try:

            if not self.channel.get_busy():

                self.channel.play(self.ending_music)

        except Exception as e:

            print("ENDINGUPDATEAUDIO ERROR: ", e)

    def blitme(self, screen):

        screen.blit(self.end_image, (0, 0))
