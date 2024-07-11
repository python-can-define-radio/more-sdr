1. Download Proot as described [here](https://proot-me.github.io/). Steps:
    1. Open a terminal
    2. `cd` to wherever you want to download proot
    3. Download proot: `curl -LO https://proot.gitlab.io/proot/bin/proot`
    4. Make it executable: `chmod +x ./proot`
    5. See if it worked: `./proot -h`
2. Download a rootfs as described on the same page. Here are two possible examples:
    - <details><summary>Option 1: How to download DragonOS:</summary>
            
        1. Go to the [list of DragonOS files](https://sourceforge.net/projects/dragonos-focal/files/)
        2. Click "Download Latest Version", which is currently "DragonOS_FocalX_R36.iso" as of 2024 July
        3. ... (unfinished) ...

      </details>

    - <details><summary>Option 2: How to download a version of Ubuntu:</summary>
        
        1. In a browser, https://images.linuxcontainers.org/images
        2. pick ubuntu/jammy/amd64/default
        3. pick newest date
        4. download rootfs.tar.xz
        5. Extract

      </details>
4. Run `./proot -S path_to_the_rootfs`
5. (Optional) Inside the proot, run `bash`
6. Run `apt install hackrf`
7. Run `hackrf_sweep`
8. If you get an error about firmware:
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
