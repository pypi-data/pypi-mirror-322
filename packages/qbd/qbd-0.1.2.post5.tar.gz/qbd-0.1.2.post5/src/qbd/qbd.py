#!/users/lennart/venv/bin/python3

import errno
import os
import click
import numpy as np
from glob import glob
from pathlib import Path
from astropy.io import fits
from rich.traceback import install
install(show_locals=True)


def get_and_add_custom_header(header, channels_filelist):
    with fits.open(channels_filelist[0], memmap=True) as hud:
        header = hud[0].header
        header['NAXIS3'] = len(channels_filelist)
    return header


def build_empty_cube(output: str, channels_filelist: list) -> None:
    """
    Generate an empty dummy fits data cube.
    The data cube dimensions are derived from the cube images.
    """
    firstc = channels_filelist[0]
    hdu_firstc = fits.open(firstc, memmap=True, mode="update")
    if len(np.squeeze(hdu_firstc[0].data).shape) == 2:
        ydim, xdim = np.squeeze(hdu_firstc[0].data).shape
        wdim = 1
    elif len(np.squeeze(hdu_firstc[0].data).shape) == 3:
        wdim, ydim, xdim = np.squeeze(hdu_firstc[0].data).shape
    zdim = len(channels_filelist)

    dims = tuple(np.squeeze([xdim, ydim, zdim, wdim]))

    # create header

    dummy_dims = tuple(1 for d in dims)
    dummy_data = np.zeros(dummy_dims, dtype=np.float32)
    hdu = fits.PrimaryHDU(data=dummy_data)

    header = hdu_firstc[0].header
    header = get_and_add_custom_header(header, channels_filelist)
    for ii, dim in enumerate(dims, 1):
        header["NAXIS%d" % ii] = dim
        #header["NAXIS"] = 4

    header.tofile(output, overwrite=True)

    # create full-sized zero image
    header_size = len(
        header.tostring()
    )  # Probably 2880. We don't pad the header any more; it's just the bare minimum
    data_size = np.prod(dims) * np.dtype(np.float32).itemsize
    # This is not documented in the example, but appears to be Astropy's default behaviour
    # Pad the total file size to a multiple of the header block size
    block_size = 2880
    data_size = block_size * (((data_size -1) // block_size) + 1)

    with open(output, "rb+") as f:
        f.seek(header_size + data_size - 1)
        f.write(b"\0")
    print("Creating empty cube:", output)


def update_fits_header_of_cube(filepathCube, headerDict):
    '''
    '''
    print(f"Updating header for file: File: {filepathCube}, Update: {headerDict}")
    with fits.open(filepathCube, memmap=True, ignore_missing_end=True, mode="update") as hud:
        header = hud[0].header
        for key, value in headerDict.items():
            header[key] = value


def fill_cube_with_data(output, channels_filelist):
    """
    Fills the empty data cube with fits data.
    """
    for ii, channel_file in enumerate(channels_filelist):
        if channel_file:
            print(f"Processing channel {ii+1}/{len(channels_filelist)}: {channel_file}")
            hud_input = fits.open(channel_file, memmap=True, ignore_missing_end=True, mode="update")
            data_input = hud_input[0].data

            hud_output = fits.open(output, memmap=True, ignore_missing_end=True, mode="update")
            data_output = hud_output[0].data

            if len(np.squeeze(data_input).shape) == 3:
                data_output[:, ii, :, :] = data_input[:, 0, :, :]
            else:
                data_output[ii, :, :] = data_input[:, :, :]
        else:
            print(f"Processing channel {ii+1}/{len(channels_filelist)}: Empty channel. Setting NaN.")
            if len(np.squeeze(data_input).shape) == 3:
                data_output[:, ii, :, :] = np.nan
            else:
                data_output[ii, :, :] = np.nan

    if len(np.squeeze(data_output).shape) == 3:
        del hud_output[0].header['NAXIS4']

    hud_input.close()
    hud_output.close()
    print("Cube filled:", output)


def call_create_demo_data():
    Path("channels").mkdir(parents=True, exist_ok=True)
    create_demo_fits_file("channels/demo-channel-001.fits")
    create_demo_fits_file("channels/demo-channel-002.fits")
    create_demo_fits_file("channels/demo-channel-003.fits")
    create_demo_fits_file("channels/demo-channel-006.fits")
    create_demo_fits_file("channels/demo-channel-007.fits")


def create_demo_fits_file(filename):
    mock_data = np.zeros((4, 1, 500, 500), dtype=np.float32)
    for ii in range(0, 4):
        random_data = np.random.random((500, 500))# * np.random.randint(10)
        mock_data[ii, :, :] = random_data
    hdu = fits.PrimaryHDU(data=mock_data)
    print("Writing file:", filename)
    hdu.writeto(filename, overwrite=True)


def get_channels(inpt):
    if os.path.isfile(inpt):
        with open(inpt, 'r') as f:
            return f.read().strip().split('\n')
    elif os.path.isdir(inpt):
        return sorted(glob(str(inpt)+"/*"))
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), inpt)


@click.command()
@click.argument('inpt', nargs=1, required=False)
@click.option('--create-demo-data', default=False, is_flag=True, help='Creates a "channels" directory with demo FITS-data.')
@click.option('--output', default="cube.fits", help='Filename of the output file.')
def main(inpt, create_demo_data, output):
    if create_demo_data:
        call_create_demo_data()
    if inpt:
        channels_filelist = get_channels(inpt)
        build_empty_cube(output, channels_filelist)
        fill_cube_with_data(output, channels_filelist)


if __name__ == "__main__":
    main()
