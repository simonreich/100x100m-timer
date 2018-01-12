# -*- coding: utf-8 -*-
"""
This file is part of 100x100m Timer.
    100x100m Timer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    100x100m Timer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with 100x100m Timer.  If not, see <http://www.gnu.org/licenses/>.
"""

# (c) Simon Reich 2018

######################################################



# Time before counter starts in seconds
timePrecounter = 30

# Time for one lap in seconds
timeLap = 120

# Number of laps
nrLap = 100

# Break before this laps
# For example nrBreak = [10, 20], means that a break will be inserted between lap 9-10 and lap lap 19-20
# Leave empty for no breaks nrBreak = []
nrBreak = [26, 51, 76]

# Length of break in seconds
timeBreak = 300

# Pitch of start tunes
tunePitch = [440, 440, 440]



######################################################
## No Configuration after this
######################################################



import pygame
from pygame.mixer import Sound, get_init, pre_init
from array import array


pre_init(44100, -16, 1, 1024)
pygame.init()
screen = pygame.display.set_mode((1920, 1020))
clock = pygame.time.Clock()

counter, text = timePrecounter, str(timePrecounter).rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 600)



## https://gist.github.com/ohsqueezy/6540433
# Generate a 440 Hz square waveform in Pygame by building an array of samples and play
# it for 5 seconds.  Change the hard-coded 440 to another value to generate a different
# pitch.
class Note(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples



# The window always shows two texts:
textTop = ""
textBottom = ""

# Phase of the program
# phase = 1 Countdown before Timer
# phase = 2 Timer, running nrLap times
# phase = 3 Swimming break
# phase = 4 Done 
phase = 1

# Countdown
cTimePrecounter = timePrecounter
m, s = divmod(timePrecounter, 60)

# Timer
cTimeLap = timeLap
cNrLap = 1

# Break
cTimeBreak = timeBreak
cNrBreak = nrBreak



# This is the main loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.USEREVENT: 
            # Phase 1 is Countdown before timer
            if phase == 1:
                # Substract Counter and update text
                cTimePrecounter -= 1
                m, s = divmod(cTimePrecounter, 60)
                textTop = "Los!"
                textBottom = str(m).rjust(2) + ":" + str(s).rjust(2) + " s"

                # Play sounds
                if cTimePrecounter == 2:
                    Note(tunePitch[0]).play(100)
                if cTimePrecounter == 1:
                    Note(tunePitch[1]).play(100)
                if cTimePrecounter <= 0:
                    Note(tunePitch[2]).play(100)
                    phase = 2

            # Phase 2 is Timer
            if phase == 2:
                # Substract Counter and update text
                cTimeLap -= 1
                m, s = divmod(cTimeLap, 60)
                textTop = "Lap: " + str(cNrLap).ljust(3)
                textBottom = str(m).rjust(1) + ":" + str(s).ljust(2) + " m"

                # Play sounds
                if cTimeLap == 2 and sound == "on":
                    Note(tunePitch[0]).play(100)
                if cTimeLap == 1 and sound == "on":
                    Note(tunePitch[1]).play(100)
                if cTimeLap <= 0 and sound == "on":
                    Note(tunePitch[2]).play(100)

                # Is lap finished
                if cTimeLap <= 0:
                    cNrLap += 1
                    cTimeLap = timeLap

                # Is a break comming up
                if cNrLap in nrBreak:
                    cTimeBreak = timeBreak
                    cNrBreak.remove(cNrLap)
                    phase = 3

                # Is series finished
                if cNrLap > nrLap:
                    phase= 4

                # do not play sounds before break or end
                if cNrLap+1 in nrBreak or cNrLap+1 > nrLap:
                    sound = "off"
                else:
                    sound = "on"

            # Phase 3 is break
            if phase == 3:
                # Substract Counter and update text
                cTimeBreak -= 1
                m, s = divmod(cTimeBreak, 60)
                textTop = "Pause"
                textBottom = str(m).rjust(1) + ":" + str(s).ljust(2) + " s"

                # Play sounds
                if cTimeBreak == 2:
                    Note(tunePitch[0]).play(100)
                if cTimeBreak == 1:
                    Note(tunePitch[1]).play(100)
                if cTimeBreak <= 0:
                    Note(tunePitch[2]).play(100)
                    cTimeLap = timeLap
                    phase = 2

            # Phase 4 is done
            if phase == 4:
                textTop = "Lap: " + str(cNrLap).ljust(3) + " Fertig"
                textBottom = "Herzlichen Glückwunsch!"
        if e.type == pygame.QUIT: break
    else:
        screen.fill((255, 255, 255))
        screen.blit(font.render(textTop, True, (0, 0, 0)), (120, 24))
        screen.blit(font.render(textBottom, True, (0, 0, 0)), (32, 500))
        pygame.display.flip()
        clock.tick(60)
        continue
    break

