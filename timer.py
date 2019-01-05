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

# (c) Simon Reich 2018 - 2019

######################################################


# Use fixed time (system clock) to start first lap or use countdown (set in seconds below)
#precounter = "countdown"
#precounter = "time"
precounter = "time"

# If precounter is set to "time", the below starting times are used in format "HH:mm:ss" (e.g. "16:45:00" to start at quarter to five o'clock)
timePrecounterTime120 = "14:40:00"
timePrecounterTime135 = "14:15:00"

# If precounter is set to "countdown", the below time is the time before counter starts in seconds
timePrecounterCountdown = 30

# Number of laps
nrLap = 100

# Break before this laps
# For example nrBreak = [10, 20], means that a break will be inserted between lap 9-10 and lap lap 19-20
# Leave empty for no breaks nrBreak = []
nrBreak = [31, 61, 81]

# Length of break in seconds
timeBreak = 300

# Turn sound on or off
#soundState = "on"
#soundState = "off"
soundState = "on"



######################################################
## No Configuration after this
######################################################



import pygame
from pygame.mixer import Sound, get_init, pre_init
from datetime import datetime
import time
from array import array
import sys
from copy import deepcopy



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


class Timer():
    def __init__(self, _precounter, _timePrecounterCountdown, _timePrecounterTime, _timeLap, _nrLap, _nrBreak, _timeBreak, _soundState, _soundPitch):
        # Start timer at fixed system time or use countdown
        self.precounter = deepcopy(_precounter)

        # Time before counter starts in seconds
        self.timePrecounterCountdown = deepcopy(_timePrecounterCountdown)

        # System time to start counter
        self.timePrecounterTime = deepcopy(_timePrecounterTime)

        # Compute countdown in seconds.
        if self.precounter == "time":
            time = _timePrecounterTime.split(":")
            d1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(time[0]), int(time[1]), int(time[2]))
            d2 = datetime.now()
            diff = d1 - d2
            diff_in_seconds = diff.days*24*60*60 + diff.seconds
            print( "Start " + str(diff_in_seconds))
            self.timePrecounterCountdown = diff_in_seconds

        # Time for one lap in seconds
        self.timeLap = deepcopy(_timeLap)

        # Number of laps
        self.nrLap = deepcopy(_nrLap)

        # Break before this laps
        # For example nrBreak = [10, 20], means that a break will be inserted between lap 9-10 and lap lap 19-20
        # Leave empty for no breaks nrBreak = []
        self.nrBreak = deepcopy(_nrBreak)

        # Length of break in seconds
        self.timeBreak = deepcopy(_timeBreak)

        # The window always shows two texts:
        self.textTop = ""
        self.textBottom = ""

        # Phase of the program
        # phase = 1 Countdown before Timer
        # phase = 2 Timer, running nrLap times
        # phase = 3 Swimming break
        # phase = 4 Done 
        self.phase = 1

        # Countdown
        self.cTimePrecounter = deepcopy(self.timePrecounterCountdown)
        self.m, self.s = divmod(self.timePrecounterCountdown, 60)

        # Timer
        self.cTimeLap = deepcopy(self.timeLap)
        self.cNrLap = 1

        # Break
        self.cTimeBreak = deepcopy(self.timeBreak)
        self.cNrBreak = deepcopy(self.nrBreak)

        # Sound
        # Turn sound on/off
        self.soundState = deepcopy(_soundState)

        # Sound
        # Used internally such that no sound before breaks are played
        self.sound = "on"

        # Pitch of start tunes
        self.tunePitch = deepcopy(_soundPitch)

        # Sound test
        for _pitch in self.tunePitch:
            Note(_pitch).play(100)

    def update(self):
        # Phase 1 is Countdown before timer
        if self.phase == 1:
            # Substract Counter and update text
            self.cTimePrecounter -= 1
            self.m, self.s = divmod(self.cTimePrecounter, 60)
            self.textTop = "Los!"
            self.textBottom = str(self.m).rjust(2) + ":" + str(self.s).zfill(2) + " m"

            # Play sounds
            if self.cTimePrecounter == 2:
                if (self.soundState == "on"):
                    Note(self.tunePitch[0]).play(100)
            if self.cTimePrecounter == 1:
                if (self.soundState == "on"):
                    Note(self.tunePitch[1]).play(100)
            if self.cTimePrecounter <= 0:
                if (self.soundState == "on"):
                    Note(self.tunePitch[2]).play(100)
                self.phase = 2

        # Phase 2 is Timer
        if self.phase == 2:
            # Substract Counter and update text
            self.cTimeLap -= 1
            self.m, self.s = divmod(self.cTimeLap, 60)
            self.textTop = "# " + str(self.cNrLap).ljust(3)
            self.textBottom = str(self.m).rjust(1) + ":" + str(self.s).zfill(2) + " m"

            # Play sounds
            if self.cTimeLap == 2 and self.sound == "on":
                if (self.soundState == "on"):
                    Note(self.tunePitch[0]).play(100)
            if self.cTimeLap == 1 and self.sound == "on":
                if (self.soundState == "on"):
                    Note(self.tunePitch[1]).play(100)
            if self.cTimeLap <= 0 and self.sound == "on":
                if (self.soundState == "on"):
                    Note(self.tunePitch[2]).play(100)

            # Is lap finished
            if self.cTimeLap <= 0:
                self.cNrLap += 1
                self.cTimeLap = self.timeLap

            # Is a break comming up
            if self.cNrLap in self.cNrBreak:
                self.cTimeBreak = self.timeBreak
                self.cNrBreak.remove(self.cNrLap)
                self.phase = 3

            # Is series finished
            if self.cNrLap > self.nrLap:
                self.phase= 4

            # do not play sounds before break or end
            if self.cNrLap+1 in self.nrBreak or self.cNrLap+1 > self.nrLap:
                self.sound = "off"
            else:
                self.sound = "on"

        # Phase 3 is break
        if self.phase == 3:
            # Substract Counter and update text
            self.cTimeBreak -= 1
            self.m, self.s = divmod(self.cTimeBreak, 60)
            self.textTop = "Pause"
            self.textBottom = str(self.m).rjust(1) + ":" + str(self.s).zfill(2) + " m"

            # Play sounds
            if self.cTimeBreak == 2:
                if (self.soundState == "on"):
                    Note(self.tunePitch[0]).play(100)
            if self.cTimeBreak == 1:
                if (self.soundState == "on"):
                    Note(self.tunePitch[1]).play(100)
            if self.cTimeBreak <= 0:
                if (self.soundState == "on"):
                    Note(self.tunePitch[2]).play(100)
                self.cTimeLap = self.timeLap
                self.phase = 2

        # Phase 4 is done
        if self.phase == 4:
            self.textTop = "# " + str(self.cNrLap-1).ljust(3)
            self.textBottom = "Fertig!"

    def getText(self):
        return self.textTop, self.textBottom

def main(argv=None):
    """ main function
        argv: possible arguments, will be replaced by sys.argv if none are 
              given.
    """
    if argv is None:
        argv = sys.argv

    # Pygame initialization
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 140)

    # Class 1: 120s
    pitch = [440, 440, 440]
    timer120 = Timer(precounter, timePrecounterCountdown, timePrecounterTime120, 120, nrLap, nrBreak, timeBreak, soundState, pitch)

    # Class 2: 135s
    pitch = [380, 380, 380]
    timer135 = Timer(precounter, timePrecounterCountdown, timePrecounterTime135, 135, nrLap, nrBreak, timeBreak, soundState, pitch)

    # This is the main loop
    while True:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT: 
                timer120.update()
                timer135.update()
            if e.type == pygame.QUIT: break
        else:
            textTop120, textBottom120 = timer120.getText()
            textTop135, textBottom135 = timer135.getText()

            screen.fill((255, 255, 255))
            yoffset = 50
            xoffset = 300
            screen.blit(font.render(textTop120, True, (0, 0, 0)), (10, yoffset))
            screen.blit(font.render(textBottom120, True, (0, 0, 0)), (300, yoffset))

            screen.blit(font.render(textTop135, True, (0, 0, 0)), (10, (480/2)+yoffset))
            screen.blit(font.render(textBottom135, True, (0, 0, 0)), (300, (480/2)+yoffset))
            pygame.display.flip()
            clock.tick(60)
            continue
        break


if __name__ == "__main__":
    main()
