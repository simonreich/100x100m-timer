# 100x100m Timer

## Anwendung

Dieses Pythonscript ist als Timer und Counter für die Mutter aller Ausdauerübungen, den 100x100m GA1 Schwimmen gedacht.

Es kann natürlich für beliebige Sportarten neben Schwimmen mit beliebigen Serienwiederholungen benutzt werden.

## Features

Es können folgende Optionen eingestellt werden:
 * Countdown vor der eigentlichen Serie
 * Zeit für eine einzelne Strecke, zum Beispiel 2:00 Minuten oder 2:30 Minuten.
 * Länge der Gesamtserie, zum Beispiel 100 mal.
 * Pausen beliebiger Länge während des Sets, zum Beispiel nach 25,50,75 Laps.

Die Anzeige ist zur besseren Lesbarkeit aus dem Wasser bewusst schlicht im schwarz/weiß Modus gehalten.

## Installation

Optional: Eine lokale Virtual Environment für Python installieren. Die einzige Abhängigkeit ist pygame.

```bash
virtualenv -p python3 100x1000-timer
cd 100x1000-timer
source bin/activate
pip install pygame
```

Clone timer & have fun!

```bash
git clone https://github.com/simonreich/100x100m-timer.git
cd 100x100m-timer
python ./timer.py
```

## TODO

 * Sound does not always work. Sometimes ALSA throws an error message at program start and there is no sound. Restarting the program fixes the issue. Todo: Find a more reliable way to play sounds.
 * Allow for timer start at specific time. E.g. start timer at exactly 8:00:00pm or start timer next at x:xx:00 o'clock - meaning at the full minute. This way the timer can be easily synchonized with clocks running in the same room.
