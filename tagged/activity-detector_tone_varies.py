"""Similar to activity-detector.py in this folder, but plays different tones depending on the measured signal amplitude. Only measures on a single frequency.
Might do more -- I don't remember.
"""

import datetime
import time
from pcdr.flow import OsmoSingleFreqReceiver
import os
from playsound import playsound

tgt = float(input("What frequency are you targeting (in MHz expressed as [freq]e6)? "))   # targeted frequency input
rec = OsmoSingleFreqReceiver("hackrf=0", tgt)
rec.start()
avg = 0
count = 0
soundcount = 0
print("Starting Tone Variable script...")
print("Writing file if it has not been created...")
fn = "activity.csv"
if os.path.exists(fn):
    newfile = False
else:
    newfile = True

with open(fn, "a", encoding="utf-8") as f:
    if newfile:
        f.write("date,time,unix_timestamp,strength,avg_strength\n")
    while True:
        soundcount += 1
        stren = rec.get_strength()    # Strength and Average defined
        avg = 0.99*avg + 0.01*stren

        rec.set_center_freq(tgt)   # target freq actions  LOW
        if (stren - avg) <= 0.02:
            print(f"{dt} Activity on {tgt}. Current signal is measured as LOW.")
            soundcount >= 25
            playsound("kick.wav")
            soundcount = 0
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.05)

        if 0.02 <= (stren - avg) < 0.05:    # target freq actions  MEDIUM
            print(f"{dt} Activity on {tgt}. Current signal is measured as MEDIUM.")
            soundcount >= 25
            playsound("bass.wav")
            soundcount = 0
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.05)
    
        if 0.05 <= (stren - avg):    # target freq actions  HIGH
            print(f"{dt} Activity on {tgt}. Current signal is measured as HIGH.")
            soundcount >= 25
            playsound("DTMF.wav")
            soundcount = 0
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.05)

        count += 1
        if count == 100:  # Record every hundredth
            count = 0
            nowtime = time.time()
            dt = datetime.datetime.fromtimestamp(nowtime)
            print(f"{dt}  Activity. Recording to file.")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            f.flush()
