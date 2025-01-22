# Rigol DG1022 Python Driver

This package provides a Python driver for controlling the Rigol DG1022 Function Generator via USB.

## Installation
Download the `.whl` file from the **Releases** page and install it using: `pip install <filename>.whl`

## Usage

```python
from rigol_dg1022 import RigolDG1022

# Connect to the device
dg = RigolDG1022()

# Set a sine wave on Channel 1
dg.set_waveform(channel=1, waveform="SIN", frequency=1000, amplitude=1, offset=0)

# Turn on the output for Channel 1
dg.set_output(channel=1, state=True)

# Get the current frequency of Channel 1
freq = dg.get_frequency(channel=1)
print(f"Current frequency: {freq} Hz")

# Turn off the output
dg.set_output(channel=1, state=False)
```

## Build package
To build the .whl, navigate to `rigol_dg1022` dir and execute `py -m build`

## Installation
Download the `.whl` file from the **Releases** page and install it using: `pip install <filename>.whl`
