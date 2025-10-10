## Step 1:
##  DONE: Use a drawing program to make some arbitrary image.
## Step 2:
##  Convert that into something transmittable.
##  2a: Load image in Python
import numpy as np
import PIL.Image
from PIL.PngImagePlugin import PngImageFile
import matplotlib.pyplot as plt



def loadGrayscale(fn: str) -> np.ndarray:
    """Load an image; convert to grayscale; `np.array()`"""
    img: PngImageFile = PIL.Image.open(fn)
    grayscale = img.convert("L")
    return np.array(grayscale)



## 2b: Convert the data to the time domain
## 2b1: Let's try just one row.
print("IT IS IN THE MARIMO NOTEBOOK time_and_freq_...")
print("Todo - maybe jupytext or something to capture the idea flow.")

## 2c: Save the file as raw IQ


## Step 3:
##  Profit?  (meme reference)
## Step 4:
##  Transmit it!


## Other useful things:

if False:
    arr = loadGrayscale("verysmall1.png")


def fromnp(arr: np.ndarray):
    pimg = PIL.Image.fromarray(arr)
    pimg.save("multicol1_mod.png")
