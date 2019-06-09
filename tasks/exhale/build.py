#!/usr/bin/env python3

import os

letters = {
    "U": "01:04.00",
    "G": "00:08.80",
    "R": "04:42.80",
    "A": "01:16.56",
    "J": "00:00.60",
    "S": "00:05.72",
    "H": "01:07.40",
    "W": "01:20.40",
    "T": "01:34.40",
    "E": "06:45.90",
    "B": "06:05.00",
    "O": "07:44.60",
    "F": "07:49.00",
    "I": "08:46.80",
    "_": "13:20.72"
}

os.system("rm -f seg*.mp4 segments.txt trump.mp4")

# get the video at https://americanrhetoric.com/speeches/donaldjtrumpbodersecurityplan.htm

for n, i in enumerate("UGRA_JOSHUA_THE_BOI_WITH_HIS_RABBIT_WIFE"):
    os.system("ffmpeg -fflags +genpts -ss %s -t 00:00.28 -i donaldjtrumpimmigrationcompromise.mp4 -map 0 -b:v 4096k -b:a 128k seg%02d.mp4" % (letters[i], n))

os.system("(echo ffconcat version 1.0; ls seg*.mp4 | sed -E 's/^/file /') > segments.txt")
os.system("ffmpeg -i segments.txt -f concat -map 0 -b:v 4096k -b:a 128k -f mp4 trump.mp4")
