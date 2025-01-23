# Installation
 
``` bash
pip install qbd
```
# Running `qbd`

## 1. Create demo data
Run the `qbd` command with the `--create-demo-data` flag to create the directory
`channels` with FITS demo data.
```bash
qbd --create-demo-data
Writing file: channels/demo-channel-001.fits
Writing file: channels/demo-channel-002.fits
Writing file: channels/demo-channel-003.fits
Writing file: channels/demo-channel-006.fits
Writing file: channels/demo-channel-007.fits
```

## 2. Create input file list
Create a simple text file containing the filepaths to input the channel data.
```bash
find channels/*.fits > channel-list.txt
```

```bash
cat channel-list.txt
channels/demo-channel-001.fits
channels/demo-channel-002.fits
channels/demo-channel-003.fits
channels/demo-channel-006.fits
channels/demo-channel-007.fits
```

## 3. (Optional) Add empty channels
Add empty channels (filled with np.nan) by adding an empty lines in channel-list.txt:
```bash
cat channel-list.txt
channels/demo-channel-001.fits
channels/demo-channel-002.fits
channels/demo-channel-003.fits


channels/demo-channel-006.fits
channels/demo-channel-007.fits
```

## 4. Start cube creation
Start the data cube creation by calling the `channel-list.txt` with `qbd`.
```
qbd channel-list.txt
Creating empty cube: cube.fits
Processing channel 1/7: channels/demo-channel-001.fits
Processing channel 2/7: channels/demo-channel-002.fits
Processing channel 3/7: channels/demo-channel-003.fits
Processing channel 4/7: Empty channel. Setting NaN.
Processing channel 5/7: Empty channel. Setting NaN.
Processing channel 6/7: channels/demo-channel-006.fits
Processing channel 7/7: channels/demo-channel-007.fits
Cube filled: cube.fits
```
