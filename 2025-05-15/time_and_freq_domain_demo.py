import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import PIL.Image
    from PIL.PngImagePlugin import PngImageFile
    import matplotlib.pyplot as plt
    import deal
    from typing import Callable
    return Callable, PIL, PngImageFile, deal, mo, np, plt


@app.cell
def __(freq, maxtime, plt, t, wav):
    plt.figure(figsize=(8, 2))
    plt.plot(t, wav, "o")
    plt.title(f"A {freq.value} Hz wave in the Time Domain")
    plt.gca(), freq, maxtime
    return


@app.cell
def __(fft, freq, freqs, plt):
    plt.figure(figsize=(8, 2))
    plt.plot(freqs, fft, "bo-")
    plt.title(f"The FFT of the above wave. In other words, the same wave in the Frequency Domain. Should have a spike at {freq.value} Hz.")
    plt.gca()
    return


@app.cell
def __(frq, mxtim, np, npoints):
    t = np.linspace(0, mxtim, npoints, endpoint=False)
    wav = np.cos(frq * 2 * np.pi * t)
    fft = np.fft.rfft(wav).real
    freqs = np.fft.rfftfreq(len(wav), mxtim/npoints)
    return fft, freqs, t, wav


@app.cell
def __(fft, np, plt, wav):
    wav_from_fft = np.fft.irfft(fft, len(wav))
    plt.figure(figsize=(8, 2))
    plt.plot(wav_from_fft, "bo")
    plt.gca()
    return (wav_from_fft,)


@app.cell
def __(freq):
    frq = freq.value
    return (frq,)


@app.cell
def __(maxtime):
    mxtim = maxtime.value
    return (mxtim,)


@app.cell
def __():
    npoints = 64
    return (npoints,)


@app.cell
def __(mo, mxtim, npoints):
    freq = mo.ui.slider(0, npoints/mxtim/2, label="freq", show_value=True)
    return (freq,)


@app.cell
def __(mo):
    maxtime = mo.ui.slider(1, 3, label="maxtime", show_value=True)
    return (maxtime,)


@app.cell
def __(deal, fft, np, plt):
    @deal.ensure(lambda _: len(_.result) == (len(_.row) - 1) * 2)
    def irfft_onerow(row: np.ndarray) -> np.ndarray:
        if len(row) % 2 != 1:
            raise ValueError("Only odd row lengths allowed")
        return np.fft.irfft(row)

    irffted = irfft_onerow(fft)
    plt.figure(figsize=(8, 2))
    plt.plot(irffted, "o")
    plt.show()
    return irfft_onerow, irffted


@app.cell
def __(np):
    def bizzare_row_operation(row: np.ndarray) -> np.ndarray:
        """not finished."""
        return np.array([row[0], row[-1], row[0] - row[-1]])

    bizzare_row_operation(np.array([3, 2, 6, 8]))
    return (bizzare_row_operation,)


@app.cell
def __(Callable, bizzare_row_operation, deal, np):
    @deal.pre(lambda _: len(_.arr.shape) == 2)
    @deal.post(lambda result: len(result.shape) == 1)
    def flat_op_by_row(op: Callable, arr: np.ndarray) -> np.ndarray:
        opped = np.array(list(map(op, arr)))
        return opped.flatten()
        
    flat_op_by_row(
        bizzare_row_operation,
        np.array([
            [3, 0, 0, 20],
            [2, 0, 1, 5]
        ])
    )
    return (flat_op_by_row,)


@app.cell
def __(flat_op_by_row, irfft_onerow, np, plt):
    def irfft_image(arr: np.ndarray) -> np.ndarray:
        """Given an 'image' (represented as a numpy array), convert by row to the time domain."""
        return flat_op_by_row(irfft_onerow, arr)

    _wav = irfft_image(np.array([
            [0, 3, 0,  0, 1] + [0]*20,
            [0, 0, 10, 0, 0] + [0]*20,
            [0, 0, 0,  4, 0] + [0]*20,
        ]))
    plt.plot(_wav)
    plt.gca()

    return (irfft_image,)


@app.cell
def __():
    def dostuff():
        return 3
    return (dostuff,)


if __name__ == "__main__":
    app.run()
