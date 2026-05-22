# Rutgers-LAQM-Strain-Setup
Documentation On Straining Setup

<img width="737" height="600" alt="image" src="https://github.com/user-attachments/assets/f803e9c0-7bec-48bd-a185-4abd19861b2a" />


## Overview Of Strain Cell Setup

The goal of this setup is to be able to apply force onto a conductive crystal while measuring electrical characteristics of the sample of interest. The equipment used in this setup are:


1. QD PPMS Model 6000 and EverCool II and connected desktop
2. FC100 Strain Cell
3. RP100 Power Supply
4. Keithley 2182A Nanovoltmeter and 6221 Current Source combo
5. Keysight E4980AL LCR meter
6. Remote data desktop computer

The entire experiment is controlled through a python script run on the data computer. Connection between the two computers is enabled through the MultiPyVu library and the two devices must be connected to the LAN. The RP100 power supply is used to control the force applied to the sample on the FC100 strain cell. The force applied to the sample is readback through capacitance which is collected through the E4980AL LCR meter. Electrical transport is done using the Keithley 2182A nanovoltmeter and 6221 current source combo. The EverCool II chamber houses the FC100 during operation and is used to adjust temperature and to apply magnetic field. 

**
This setup can be implemented using only the PPMS desktop, though we ran into some issues with mulitple GPIB connections not being recognized which drove us to use a two computer setup. Using this setup will require only very slight changes in the main code file - specifically an initial line to initialize the client and then after the initial host initialization. More information can be found in the [MultiPyVu] (https://pypi.org/project/MultiPyVu/) module used in the python script.

**
## Software Requirments

They scripts requires at least python version 3.7 or higher as per the module requirements. 

The **required modules** that need to be installed are:

1. [csv] (https://docs.python.org/3/library/csv.html)
2. [time] (https://docs.python.org/3/library/time.html)
3. [PyVISA] (https://pyvisa.readthedocs.io/en/latest/index.html)
4. [MultiPyVu] (https://pypi.org/project/MultiPyVu/)

**
Quantum design recommends an Anaconda distribution though installation of just the basic Cpython implementation is enough.
**

**A VISA Implementation must be installed.**
The PPMS desktop most likely already has a VISA implementaion installed (likely NI-VISA) though 

