1. Download Proot: https://proot-me.github.io/
2. Get a rootfs: https://images.linuxcontainers.org/images
    - pick ubuntu/jammy/amd64/default
    - pick newest date
    - download rootfs.tar.xz
    - Extract
3. Run `proot -S path_to_the_rootfs`
4. (Optional) Inside the proot, run `bash`
5. Run `apt install hackrf`
6. `hackrf_sweep`
7. If you get an error about firmware:
    - `hackrf_info` to verify that firmware is old
    - Download latest release from here: https://github.com/greatscottgadgets/hackrf/releases (not the source code)
    - Extract
    - `cd` to the extracted folder
    - `cd` to `firmware-bin`
    - `hackrf_spiflash -w hackrf_one_usb.bin`
    - Press "reset" button on the HackRF box
    - `hackrf_info` to verify that firmware is updated
 9. Verify `hackrf_sweep` works now
 10. Interpret `hackrf_sweep` results
