"""
A rudimentary proof-of-concept for an RF activity detector using a HackRF.
Writes activity to a file.
Cycles between center frequencies.
Plays a sound if the activity exceeds a threshold.
Maybe more -- I don't remember from when we wrote it.
"""


import datetime
import time
from pcdr.flow import OsmoSingleFreqReceiver
import os
from playsound import playsound


rec = OsmoSingleFreqReceiver("hackrf=0", 104.1e6)
rec.start()
avg = 0
count = 0
freq1 = 104.3e6    # add or delete freqs as needed for target set
freq2 = 150e6
freq3 = 462e6
freq4 = 465e6

fn = "activity.csv"
if os.path.exists(fn):
    newfile = False
else:
    newfile = True

with open(fn, "a", encoding="utf-8") as f:
    if newfile:
        f.write("date,time,unix_timestamp,strength,avg_strength\n")
    while True:
        
        stren = rec.get_strength()    # Strength and Average defined
        avg = 0.99*avg + 0.01*stren

        rec.set_center_freq(freq1)   # FREQ 1 
        if stren >= avg:
            print(f"{dt} Activity on {freq1}. Recording to file.")
            playsound("cowbell.wav")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.1)

        rec.set_center_freq(freq2)    # FREQ 2
        if stren >= avg:
            print(f"{dt} Activity on {freq2}. Recording to file.")
            playsound("cowbell.wav")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.1)

        rec.set_center_freq(freq3)    # FREQ 3
        if stren >= avg:
            print(f"{dt} Activity on {freq3}. Recording to file.")
            playsound("cowbell.wav")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.1)

        rec.set_center_freq(freq4)    # FREQ 4
        if stren >= avg:
            print(f"{dt} Activity on {freq4}. Recording to file.")
            playsound("cowbell.wav")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            time.sleep(0.1)    

        count += 1
        if count == 100:  # Record every hundredth
            count = 0
            nowtime = time.time()
            dt = datetime.datetime.fromtimestamp(nowtime)
            print(f"{dt}  Activity. Recording to file.")
            f.write(f"{dt.date()},{dt.time()},{nowtime},{stren},{avg}\n")
            f.flush()
