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


## Software Requirments

