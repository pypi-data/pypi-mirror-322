# Introduction

**`qbd` (/kjuːbd/) can create FITS-file data cubes which are larger than your machine's RAM.**

Want to get going right now? Start here: [Installation](./installation.md)

## Context
The modern radio interferometer facilities, such as MeerKAT, ngVLA, LOFAR,
ASKAP, uGMRT, and the forthcoming SKA, generate an unprecedented amount of astronomical
data. Processing, reducing, viewing, analyzing, and storing this data are
hard challenges that will continue to pose difficulties in the field.

One common problem encountered by researchers is producing multi-channel (and
often full Stokes) data cubes. To address this issue, `qbd` (pronounced
/kju:bd/) creates a large empty data cube on disk first and then fills it with
data, channel by channel. By doing so, only the necessary RAM to hold a single
channel is required at maximum.

This strategy allows to efficiently process large-scale astronomical datasets
using regular High Performance Computing (HPC) hardware. Producing 20,000 x
20,000 pixels, full Stokes, cubes with hundreds of channels can be done in
minutes to hours.
