# Rutgers-LAQM-Strain-Setup
Documentation On Straining Setup

<p align="center">
<img width="737" height="600" alt="image" src="https://github.com/user-attachments/assets/f803e9c0-7bec-48bd-a185-4abd19861b2a" />
</p>

***DISCLAIMER***
This is an on-going project and still requires more development and fine tuning. 

## Overview Of Strain Cell Setup

The goal of this setup is to be able to apply force onto a conductive crystal while measuring electrical characteristics of the sample of interest. The equipment used in this setup are:


1. QD PPMS Model 6000/EverCool II and connected desktop
2. [FC100 Strain Cell](https://razorbillinstruments.com/fc1x0-high-performance-cryogenic-stress-cell/)
3. [RP100 Power Supply](https://razorbillinstruments.com/rp100/)
4. [Keithley 2182A Nanovoltmeter and 6221 Current Source combo](https://www.tek.com/en/products/keithley/low-level-sensitive-and-specialty-instruments/series-6200-2182a)
5. [Keysight E4980AL LCR meter](https://www.keysight.com/us/en/product/E4980AL/precision-lcr-meter-20-hz-300-khz-500-khz-1-mhz.html)
6. Remote data desktop computer

The entire experiment is controlled through a python script run on the data computer. Connection between the two computers is enabled through the MultiPyVu library and the two devices must be connected to the LAN. The RP100 power supply is used to control the force applied to the sample on the FC100 strain cell. The force applied to the sample is readback through capacitance which is collected through the E4980AL LCR meter. Electrical transport is done using the Keithley 2182A nanovoltmeter and 6221 current source combo. The EverCool II chamber houses the FC100 during operation and is used to adjust temperature and to apply magnetic field. 

***This setup can be implemented using only the PPMS desktop, though we ran into some issues with mulitple GPIB connections not being recognized which drove us to use a two computer setup. Using this setup will require only slight changes in the main code file - specifically an initial line to initialize the host and then after the initial client initialization. More information can be found in the [MultiPyVu](https://pypi.org/project/MultiPyVu/) module used in the python script. The with-blocks were not used for client reinitialization.***

## Software Requirments

They scripts requires at least python version 3.7 or higher as per the module requirements. 

The **required modules** that need to be installed are:

1. [Csv](https://docs.python.org/3/library/csv.html)
2. [Time](https://docs.python.org/3/library/time.html)
3. [PyVISA](https://pyvisa.readthedocs.io/en/latest/index.html)
4. [MultiPyVu](https://pypi.org/project/MultiPyVu/)

***Quantum design recommends an Anaconda distribution though installation of just the basic Cpython implementation is enough.***

**A VISA Implementation must be installed.**
The PPMS desktop most likely already has a VISA implementaion installed (likely NI-VISA) though you will need to install an implementation on the remote data computer. Also install and setup drivers for any GPIB adaptors or cards that you will use.

Initial connection with the RP100 power supply should install drivers though it would be wise to check. 

## FC100 Strain Cell

The FC100 strain cell is a high force strain cell specifically designed to be used for millimeter sized samples in a 25mm bore cyrostat like the QD PPMS EverCool II or PPMS Dynacool. The cell has a full titanium construction and is safe to be used in a magnetic field. A WP100 wiring platform from Razorbill is used for electrical connections sample of interest. 

It is wise to review and be familiar with cell's documentation before use. 

***The FC100 is designed for operation inside a cryostat under vacuum, dry air, or low-pressure helium exchange gas. During epoxy curing, the maximum  process temperature is 100 °C, but the cell must not be mechanically operated at those elevated temperatures because the structural epoxies soften and insulation degrades.***

The FC100 is used for high force applications with a ±200 N force sensor. ***At room 300 K, the FC100 can apply approximately ±170 N at zero displacement and ±45 μm displacement at zero load. At 4 K, the available force decreases to approximately ±100 N and displacement to ±25 μm because the piezoelectric stroke decreases at low temperature.***

The cells are thermally compensated to match titanium thermal expansion, minimizing unintended strain during cooling. ***However, rapid cooling and heating needs to be avoided. Razorbill recommends limiting all temperature ramps to less than 10 K/min under all circumstances.***

***The cell's piezoelectric stacks that must always remain connected to discharge resistors during heating or cooling.*** Temperature changes generate pyroelectric charge in the stacks, and failure to discharge them can permanently damage the piezos. ***When the power supply is disconnected, each pair of drive wires should be shorted together through a resistor of a few kΩ.*** The  RP100 Power Supply includes integrated discharge resistors when its output is switched off.

***The FC100 has maximum ecommended voltage limits that depend on temperature. See the offical documentation for the numbers.***

The cell must never be cooled or operated if condensation is present. Humidity effects the capacitance and can require several days in vacuum to stabilize. ***Razorbill recommends pumping the cell under vacuum for at least a day before precision measurements.***

The FC100 uses toothed sample plates to transfer large forces into the sample. ***The plate spacing is adjustable in discrete 1/3 mm increments over approximately 0.3–2.5 mm gap spacing.*** Razorbill explains in their documentation different ways to mount the sample.

The force response from the cell is related to capacitance. To convert force to capacitance, the given formula from Razorbill is:

<p align="center">
<img width="358" height="118" alt="image" src="https://github.com/user-attachments/assets/2814450d-1cb1-4251-94d5-48cbb8227df5" />
</p>

For our strain cell, alpha is 1555 NpF, fo is 1368N, Cp is 0.0822 pF and C is read capacitance. Solving for f will give you your sample tension force in newtons. These parameters may not not the same across each manufactured cell. A compressive force will see the capacitance increase while a tensile force will see the capacitance decrease. 

***It is important to note that the zero force capacitance will decrease was the temperature decreases. Therefor, it a good idea make a claibration curve of zero force capacitance measurments across a temperature range. Razorbill includes information at the end of their [AP006](https://razorbillinstruments.com/wp-content/uploads/2023/06/AP006-Capacitor-performance-v2-1-Web.pdf) document. It is recommended you read this as it explains how to get the best performance out of your device.***

***For force sensors like on the FC100, Razorbill also notes that alpha, the gain of the sensor, is also temperature dependent. Below, alpha290K is 1555 NpF for our device and T is in Kelvin.***
<p align="center">
<img width="744" height="66" alt="image" src="https://github.com/user-attachments/assets/88256fc6-7fca-4ae9-a1e4-4b87c77bbb97" />
</p>

## Mounting Your Sample

*Check out Razorbill's wesbite as they have some nice documentation on sample mounting.*
(https://razorbillinstruments.com/step-by-step-guide-to-sample-mounting/)

We used the following epoxies in our experiments:

1. [Stycast 2850FT & CAT 23LV](https://datasheets.tdx.henkel.com/LOCTITE-STYCAST-2850FT-CAT-23LV-en_GL.pdf)
2. [H20E Silver Epoxy](https://www.tedpella.com/technote_html/16014_H20E_TN.pdf)

The Stycast 2850FT and CAT 23LV is a 2-part epoxy is not specifically designed for cryogenic use, though it used by many researchers for this application and behaves well. It is also cheaper than specialty cryogenic epoxies. It is used to glue to and electricaly isolate the sample from holders.

The H20E 2-part epoxy is used connect gold bonding wires to the sample from the wiring platform. 

**(A) Mounting Procedure (with the basic sample plates and optional spacers):**

1. Shape your sample, typically into a matchstick shape or have it necked through machining and etching.

> Samples are generaly a few mm in length, and ~100 x 300 µm in cross section.
   
3. Place your sample plates on the FC100 and figure out the best spacing based on the geometry of your sample.

> At this point you must decide whether you are going to use the upper mounting plates. Using the upper mounting plates offers higher strain homogeneity. You will have to sand your titanium spacers to match the thickness of your epoxy between you  + sample. This protects your sample when the upper plate is tightend down. You may decide to buy spacer sphere particles to mix into your epoxy and this will give an accurate distance between your sample and sample plates. You can also use cotton fibers or paint and cure an initial layer of epoxy. This is less accurate and will and it will require you to do some extra work to match the thicknesses while sanding the titanium spacers. If mounting without the top sample plates, it is generally easiest to paint a very thin layer of Stycast and Catalyst epoxy on the sample plates and then cure it. You can remove the sample plates when you do this. It is enough to cure ONLY the sample plates for 30 to 60 minutes at 80C as the application is very thin. If using cotton fibers or spacer spheres, it is generally easiest to mount the sample with the holders tightend down and generally you will not cure until the sample is mounted. ***If you do not have a very fine brush, using a plucked eyelash works very well and allows for very fine application. Apply the epoxy slowly and gentley so you do not shift the sample when its aligned.***

4. After mounting the sample using any of the various different methods, cure your mounted by either waiting 24 hours or can accelerate it by putting it in an oven for 2 to 4 hours at 65C. If curing at anything other than ambient temperature, make sure to short each piezo stacks with resistors.

5. Connecting the gold bonding wires is tough and will require practice and patience. You can solder the gold wires on one end to the pads on the wiring platform using a leaded solder. You do not need to bring your iron to a very hot temperature as the pads are very small and be quick. After, attach wiring platform to the strain cell.

6. Gentley bend the other end of the gold wires to their respective spots on the mounted sample. Prepare the epoxy and apply slowly and precisely where the ends of the wires meet the sample. After application, cure the entire cell in an oven at 80C for three hours. Again, make sure to short each piezo stacks with resistors.

## Connecting the Strain Cell to the Probe

In order to put the FC100 into the cryostat, you must attach it to a probe. Razorbill has a [PPMS P450 Probe Conversion Kit](https://razorbillinstruments.com/ppms-integration/) or they offer their new [CRYOINSERT](https://razorbillinstruments.com/cryoinsert-razorbill-instruments-cryostat-probe-for-ppms-and-dynacool-cryostats/) which is compatible with the FC100. 

The P450 probe has 4 connector sockets on the octogonal black box on the end. There are two connections for power supply and we have attached two BNC female connectors for connections the cell's capacitor. 

Useful links:
- [PPMS Insert User Guide](https://razorbillinstruments.com/wp-content/uploads/2023/11/PPMS1-User-guide-v6.1-Web.pdf)
- [P450 Conversion Guide](https://razorbillinstruments.com//wp-content/uploads/2020/04/PPMS1-Installation-guide-v5.pdf)

***For the P450 Probe***
1. If using the wiring platfrom, first connect the miniature male 4 pin header style connector to the respective female socket labled1. Make sure the bevel on both ends line up.
   
2. Attach the puck/bump guard to the FC100 using the two required screw.

3. Feed the four wires on the end of the FC100 through the thermal link plate. ***The thermal link plate has a chamfered edge that needs to be oriented to face downward when inserted into the cryostat.*** Then feed the end of the wires through the two holes on the end of the probe. Mount the cell to the probe with the four required screw. There are 4 holes on the end of the strain cell.

<p align="center">
<img width="185" height="146" alt="image" src="https://github.com/user-attachments/assets/09db11f7-5f36-444f-9735-0fefb05b2713" />
</p>

5. Connect to the wires from the end of the strain cell to their respective connectors in the probe. The connections are color coded. The probe is ready to be inserted into the chamber.

## RP100 Power Supply

The RP100 power supply is designed by Razorbill to work specifically with their strain cells. It is a 4 quadrant power supply meaning that its two channels are able to source and sink up to 6mA while with a voltage output of ±210V. On the front, there are four indicator lights. The ones above each output connectors are solid green when the output is on and steady or flash when the channel is slewing. The back side has has a USB type B port for serial communication to a computer and a C13 mains connector with a switch below it.

When connecting to the probe, channel 1 is connected to the compression stack and channel 2 is connected to the tension stack with the two provided cables.

SCPI interpreted by the power supply are explained in the documentation from razorbill.
(https://razorbillinstruments.com/wp-content/uploads/2018/10/RP100-Manual-v6.1-1.pdf)

## Keysight E4980AL LCR Meter

The E4980AL LCR meter is used in this setup to read a capacitance reading from the FC100 strain cell. As stated above in the [FC100 section](https://github.com/ercduma/Rutgers-LAQM-Strain-Setup/edit/main/README.md#fc100-strain-cell) the capacitance is inversely proportional the tensile force applied to the sample.

The front of the LCR meter had four BNC female terminals. The terminals Hcur and Hpot must be connected to the high terminal on the P450 probe while Lcur and Lpot must be connected to the low terminal.

The back of the LCR meter has a C13 mains connector and several other inputs for computer control. In our lab, we specifically use the GPIB connector for communication with the device. 

You can use find manuals online on how to use the device and on SCPI commands.
(https://www.cmc.ca/wp-content/uploads/2019/07/E4980A-User-Guide.pdf)


## Keithley 2182A Nanovoltmeter and 6221 Current Source combo

The Keithley 2182A and 6221 operate like a single instrument when connected. It has the capability to take low resistance measurements without much power dissipation in the device/sample under test. 

To connect the two devices, you must use RS-232 and trigger link connections on the back side. The current source will have a triax cable to alligator clip terminations for excitation and the nanovoltmeter has a low thermal input cable with alligator clips connected for voltage readings. 

The two together have the capability to measure resistances from 10 nano-ohms to 100 Mega-Ohms. The delta mode has the ability to make accurate low resistance measurements by eliminating the effects of thermal offsets and reduces noise down to 30nV peak-to-peak noise  for each reading; Multiple readings can be averaged for greater noise reduction.

In our setup, we use the GPIB connection in the back of the current source to communicate with the two devices. 

Manuals can be found online for each device and for the SCPI commands that the devices use. 

## Python Scripts

There are two python scripts that are useful.

<details>
<summary>strain.py</summary>
The [strain.py](https://github.com/ercduma/Rutgers-LAQM-Strain-Setup/blob/main/strain.py) file is the main script for running the experiments. The experiment is controlled with specific commands that are written in a specifc format. The top of the file explaines the supported commands.

Below the first section of comments, you will see

```python
host = 'HOST_IP_ADDRESS'
port = 10823

filename = 'test.csv'

volt_avg_count = 10
MAX_FAILURES = 6
FAILURE_RESET_TIME = 10
FAILURES_BEFORE_TIMEOUT = 3
```
The IP address must be changed to be the IPv4 address of your PPMS computer hosting the server. You can also change the port number. The file name to can be changes and must end in '.csv'.

> Your csv file will output data points under the header row: 'Time(s)', 'LoopTime(s)', 'Temperature(K)', 'TempStatus', 'Voltage', 'LcrCap(pF)', 'LcrD', 'LcrExcitation(V)', 'RP100_V1(V)', 'RP100_V2(V)'. 'Time(s)' is the program time when a measurement was taken. 'LoopTime(s)' is how long a measurement took and is usefult for debugging. 'Temperature(K)' is your chamber temperature and 'TempStatus' is useful for debugging. 'Voltage' is the voltage across your sample from the nanovolt meter which you can convert to ohms based on the injected current. 'LcrCap(pF)' is your force feedback in capacitance, 'LcrD' is a loss factor, and 'LcrExcitation(V)' is useful for debugging. 'RP100_V1(V)' and 'RP100_V2(V)' are voltages read from the measurement circuit on the RP100 and is mainly used for debugging. 

volt_avg_amount refers to the number of measurments you want to average from the keithley combo. 

The other 3 parameters are for the error handling and don't need to be changed.

Below this you will see a program array. The program must be written inside the program array.

```python
program = [
[<command name 1>, <parameters>, <mode>],
[<command name 2>, <parameters>, <mode>],
[<command name 3>, <parameters>, <mode>],
[<command name 4>, <parameters>, <mode>],
.
.
.
.
[<command name N>, <parameters>, <mode>]
]

```

Assuming channel 1 and 2 on the RP100 are connected to compression and tension stack respectively and the starting temperature is at 300K and with 0V on each stack, an example experiment might run in this order.:
1. Bring chamber down to 2K while taking measurements
   - 300K to 50K is at 5K per minute
   - 50K to 10K is 2K per minute
   - 10K to 2K is 1K per minute
3. Wait for 1 hour while measuring every 30 seconds. 
4. Compress the sample under test in increments of 50 volts using the full range of the device and take measurements after waiting 3 minutes after each increment.
5. Bring back the stack voltages to zero volts without measuring.
6. Bring the temperature back to 300K at 2K per minute without measuring.

The program will look like the following:
```python
program = [
['set_temp', [50, 5], 'measure'],
['set_temp', [10, 2], 'measure'],
['set_temp', [2, 1], 'measure'],
['hold', [3600, 30], 'measure'],
['set_voltage', [[0,0], 180], 'measure'],
['set_voltage', [[50,0], 180], 'measure'],
['set_voltage', [[50,-50], 180], 'measure'],
['set_voltage', [[100,-50], 180], 'measure'],
['set_voltage', [[100,-100], 180], 'measure'],
['set_voltage', [[150,-100], 180], 'measure'],
['set_voltage', [[150,-150], 180], 'measure'],
['set_voltage', [[200,-150], 180], 'measure'],
['set_voltage', [[200,-200], 180], 'measure'],
['set_voltage', [[100,-100], 180], 'wait'],
['set_voltage', [[0,0], 180], 'wait'],
['set_temp', [300, 2], 'wait'],
]
```
***In real life, you wouldn't run your experiment like this with huge voltage jumps. You can see that if you do smaller increments, the program can grow very large. The script will be updated in the future to condense many lines of small voltage increments to 1 line.***

Below this, you will see the instrument addressses. You will have to change the addresses based to what is set up on your instruments. If you use NI-VISA implementation and have the NI MAX program, you can easily find all of the addresses of your connected instruments in the Devices and Interfaces tab. 
   
</details>


<details>
<summary>rp100_check.py</summary>
This is a basic program that can list the recognized instruments connected to the computer.
The program will fail after listing the resources if the address of the power supply is not correct. Once you change the variable to the correct address, the program will be able to read a voltage output of the power supply. It will then set the voltages back to zero and turn off the outputs.

If in any case the main program fails, it may for some reason not set the output voltages of the power supply to zero. In that case, you can run this program to set the voltages to zero. You can also make your own basic program to do this. 
</details>

## Running a Experiment

***It is highly recommeneded that both data computers are connected to the LAN through an ethernet connection. WIFI IS UNRELIABLE AND ANY MISSED PACKETS IN THE COMMUNICATION BETWEEN THE SERVER HOST AND THE CLIENT RESOLVE IN A PROGRAM CRASH.***

1. After all the instruments are connected properly and the FC100 is installed in the chamber, open the MultiVu program.
2. In a powershell window, run
   ```python
      python -m MultiPyVu
   ```
> This requires you to have python and the MultiPyVu module installed on the host computer.

   This will pop up a GUI with you computer's IP and the communication port. You can change      the port directly here as the box is editable. This IP address and port must match the        ones in strain.py program. You can press the start button and then open the server. 

3. Go to your data computer and after making your program, execute the strain.py script in the terminal. Your experiment will begin to run immediately. The terminal will also print out some information as the program runs.

4. After the program ends, you will be able to find your named .csv file with all of your data. You will also see some log files that are generated by MultiPyVu on both computers which are useful for debugging for some program failures.   

