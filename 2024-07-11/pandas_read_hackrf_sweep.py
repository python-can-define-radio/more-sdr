import fileinput
from io import BytesIO
import subprocess
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound



BEGIN_COLS = ["date", "time", "hzlow", "hzhigh", "binwidth", "samples"]


def make_db_columns(first_row_size: int, begincols: List[str]) -> List[str]:
    """Generate indexed dB columns."""
    dbcols = []
    n = first_row_size - len(begincols)
    for x in range(n):
        dbcols.append(f"dB{x}")
    return dbcols

## Unit test:
assert make_db_columns(5, ["date", "time"]) == ["dB0", "dB1", "dB2"]


def read_hackrf_sweep(filepath_or_buffer) -> pd.DataFrame:
    """Read a hackrf_sweep csv file and generate headers."""
    firstrow = pd.read_csv(filepath_or_buffer, header=None, nrows=1)
    dbcols = make_db_columns(firstrow.size, BEGIN_COLS)
    allcols = BEGIN_COLS + dbcols
    df = pd.read_csv(filepath_or_buffer, names=allcols)
    assert df.shape[1] == len(allcols)
    return df


def x_axis(df: pd.DataFrame, number_of_means: int) -> np.ndarray:
    """Generate x values based on the dataframe's hzlow and hzhigh."""
    if min(df["hzlow"]) != max(df["hzlow"]):
        raise ValueError("hzlow must be the same value throughout the dataframe")
    if min(df["hzhigh"]) != max(df["hzhigh"]):
        raise ValueError("hzhigh must be the same value throughout the dataframe")

    ## Any arbitrary row will work since we've verified
    ## that they are the same throughout.
    hzlow = df["hzlow"].iat[0]
    hzhigh = df["hzhigh"].iat[0]
    return np.linspace(hzlow, hzhigh, number_of_means, endpoint=False)
    

def read_lines(line_chunk_size: int) -> str:
    """Read from std input. This function is not yet finished."""
    line_group = ""
    for idx, line in zip(range(line_chunk_size), fileinput.input()):
        line_group += line
    return line_group


def get_hackrf_sweep_proc(*, prootloc, rootfsloc, freqlowMHz, freqhighMHz, widthHz):
    return subprocess.Popen([
        prootloc,
        "-S",
        rootfsloc,
        "hackrf_sweep",
        "-f", f"{freqlowMHz}:{freqhighMHz}",
        "-w", f"{widthHz}",
        ],
        stdout=subprocess.PIPE)


def getDataframe(*, csvfile: str = "", proc = None) -> pd.DataFrame:
    if proc and csvfile:
        raise ValueError("Cannot read from file and live simultaneously")
    elif proc:
        # arbitrary; will eventually allow user to input this
        number_of_lines_to_avg = 100
        lineProducer = proc.stdout.readline

        ## this is just for testing
        # lineProducer = lambda: bytes(input("type something: ") + "\n", "utf")

        ## TODO: read back over this another time to make sure it makes sense
        firstline = lineProducer()
        biofirstline = BytesIO()
        biofirstline.write(firstline)
        biofirstline.seek(0)
        firstrow = pd.read_csv(biofirstline, header=None, nrows=1)
        biofirstline.close()
        dbcols = make_db_columns(firstrow.size, BEGIN_COLS)
        allcols = BEGIN_COLS + dbcols

        bio = BytesIO()
        bio.write(firstline)
        for count in range(number_of_lines_to_avg):
            bio.write(lineProducer())
        bio.seek(0)
        df = pd.read_csv(bio, names=allcols)
        bio.close()
        return df
    
    elif csvfile:
        return read_hackrf_sweep(csvfile)
    else:
        raise ValueError("Must specify")


def find_idx_nearest(xv: np.ndarray, wanted: float):
    return abs(xv - wanted).argmin()


proc = get_hackrf_sweep_proc(
    prootloc="../../../Downloads/proot",
    rootfsloc="../../../Downloads/jammy_rootfs_1",
    freqlowMHz=433,
    freqhighMHz=453,
    widthHz=20000,
)
while True:
    df_orig = getDataframe(proc=proc)
    desired_start_freq = 433_000_000
    desired_check_freq = 433_920_000
    df_specific_start = df_orig[df_orig["hzlow"] == desired_start_freq]
    dbMeans = df_specific_start.filter(like="dB").mean()
    xvals = x_axis(df_specific_start, dbMeans.size)
    idx_desired = find_idx_nearest(xvals, desired_check_freq)
    meas_freq_db = dbMeans[idx_desired]
    if meas_freq_db > -73:
        print(f"Activity on {desired_check_freq}")
        playsound("drum_cowbell.wav", block=False)        
    else:
        print("All quiet")

# yvals = np.array(dbMeans)
# plt.plot(xvals, yvals, "o-")
# plt.show()

