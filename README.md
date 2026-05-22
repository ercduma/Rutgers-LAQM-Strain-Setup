# Rutgers-LAQM-Strain-Setup
Documentation On Straining Setup

<img width="737" height="600" alt="image" src="https://github.com/user-attachments/assets/f803e9c0-7bec-48bd-a185-4abd19861b2a" />


## Overview Of Strain Cell Setup

The goal of this setup is to be able to apply force onto a conductive crystal while measuring electrical characteristics of the sample of interest. The equipment used in this setup are:


1. QD PPMS Model 6000 and EverCool II and connected desktop
2. [FC100 Strain Cell](https://razorbillinstruments.com/fc1x0-high-performance-cryogenic-stress-cell/)
3. [RP100 Power Supply](https://razorbillinstruments.com/rp100/)
4. [Keithley 2182A Nanovoltmeter and 6221 Current Source combo](https://www.tek.com/en/products/keithley/low-level-sensitive-and-specialty-instruments/series-6200-2182a)
5. [Keysight E4980AL LCR meter](https://www.keysight.com/us/en/product/E4980AL/precision-lcr-meter-20-hz-300-khz-500-khz-1-mhz.html)
6. Remote data desktop computer

The entire experiment is controlled through a python script run on the data computer. Connection between the two computers is enabled through the MultiPyVu library and the two devices must be connected to the LAN. The RP100 power supply is used to control the force applied to the sample on the FC100 strain cell. The force applied to the sample is readback through capacitance which is collected through the E4980AL LCR meter. Electrical transport is done using the Keithley 2182A nanovoltmeter and 6221 current source combo. The EverCool II chamber houses the FC100 during operation and is used to adjust temperature and to apply magnetic field. 

***This setup can be implemented using only the PPMS desktop, though we ran into some issues with mulitple GPIB connections not being recognized which drove us to use a two computer setup. Using this setup will require only slight changes in the main code file - specifically an initial line to initialize the host and then after the initial client initialization. More information can be found in the [MultiPyVu] (https://pypi.org/project/MultiPyVu/) module used in the python script. The with-blocks were not used for client reinitialization.***

## Software Requirments

They scripts requires at least python version 3.7 or higher as per the module requirements. 

The **required modules** that need to be installed are:

1. [csv](https://docs.python.org/3/library/csv.html)
2. [time](https://docs.python.org/3/library/time.html)
3. [PyVISA](https://pyvisa.readthedocs.io/en/latest/index.html)
4. [MultiPyVu](https://pypi.org/project/MultiPyVu/)

***Quantum design recommends an Anaconda distribution though installation of just the basic Cpython implementation is enough.***

**A VISA Implementation must be installed.**
The PPMS desktop most likely already has a VISA implementaion installed (likely NI-VISA) though you will need to install an implementation on the remote data computer. Also install and setup drivers for any GPIB adaptors or cards that you will use.

Initial connection with the RP100 power supply should install drivers though it would be wise to check. 

## FC100 Strain Cell

The FC100 strain cell is a high force strain cell specifically designed to be used for millimeter sized samples in a 25mm bore cyrostat like the QD PPMS EverCool II or PPMS Dynacool. The cell has a full titanium construction and is safe to be used in a magnetic field. A WP101 wiring platform from Razorbill is used for electrical connections sample of interest. 

It is wise to review and be familiar with cell's documentation before use. 

***The FC100 is designed for operation inside a cryostat under vacuum, dry air, or low-pressure helium exchange gas. During epoxy curing, the maximum  process temperature is 100 °C, but the cell must not be mechanically operated at those elevated temperatures because the structural epoxies soften and insulation degrades.***

The FC100 is used for high force applications with a ±200 N force sensor. ***At room 300 K, the FC100 can apply approximately ±170 N at zero displacement and ±45 μm displacement at zero load. At 4 K, the available force decreases to approximately ±100 N and displacement to ±25 μm because the piezoelectric stroke decreases at low temperature.***

The cells are thermally compensated to match titanium thermal expansion, minimizing unintended strain during cooling. ***However, rapid cooling and heating needs to be avoided. Razorbill recommends limiting all temperature ramps to less than 10 K/min under all circumstances.***

***The cell's piezoelectric stacks that must always remain connected to discharge resistors during heating or cooling.*** Temperature changes generate pyroelectric charge in the stacks, and failure to discharge them can permanently damage the piezos. ***When the power supply is disconnected, each pair of drive wires should be shorted together through a resistor of a few kΩ.*** The  RP100 Power Supply includes integrated discharge resistors when its output is switched off.

***The FC100 has maximum ecommended voltage limits that depend on temperature. See the offical documentation for the numbers.***

The cell must never be cooled or operated if condensation is present. Humidity shifts the capacitance calibration and can require several days in vacuum to stabilize. ***Razorbill recommends pumping the cell under vacuum for at least a day before precision measurements.***

The FC100 uses toothed sample plates to transfer large forces into the sample. ***The plate spacing is adjustable in discrete 1/3 mm increments over approximately 0.3–2.5 mm gap spacing.*** Razorbill explains in their documentation different ways to mount the sample.

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
2. Place your sample plates on the FC100 and figure out the best spacing based on the geometry of your sample.

> At this point you must decide whether you are going to use the upper mounting plates. Using the upper mounting plates offers higher strain homogeneity. You will have to sand your titanium spacers to match the thickness of your epoxy between you  + sample. This protects your sample when the upper plate is tightend down. You may decide to buy spacer sphere particles to mix into your epoxy and this will give an accurate distance between your sample and sample plates. You can also use cotton fibers or paint and cure an initial layer of epoxy. This is less accurate and will and it will require you to do some extra work to match the thicknesses while sanding the titanium spacers. If mounting without the top sample plates, it is generally easiest to paint a very thin layer of Stycast and Catalyst epoxy on the sample plates and then cure it. You can remove the sample plates when you do this. It is enough to cure ONLY the sample plates for 30 to 60 minutes at 80C as the application is very thin. If using cotton fibers or spacer spheres, it is generally easiest to mount the sample with the holders tightend down and generally you will not cure until the sample is mounted. ***If you do not have a very fine brush, using a plucked eyelash works very well and allows for very fine application.***

4. After mounting the sample using any of the various different methods, cure your mounted by either waiting 24 hours or can accelerate it by putting it in an oven for 2 to 4 hours at 65C.

5. Connecting the bonding wires is though and will require practice and patience. 



