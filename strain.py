import csv
import time
import random
import pyvisa
import numpy as npy
import MultiPyVu as mpv
import pandas as pd
import matplotlib.pyplot as plt # imports matplotlib from plt library for liveplotting
from matplotlib.animation import FuncAnimation
#from instrument2 import Instrument



'''
Supported Commands:

1. set_temp: [setpoint_K, rate_K_per_min]
   - Sets the temperature of the system to a target value (in Kelvin) at a specified ramp rate.
   - Mode:
       'wait'    : Wait until temperature is steady, no measurement is taken.
       'measure' : Wait until temperature is steady, then take measurements repeatedly.

2. set_voltage: [[ch1_V, ch2_V], wait_time_s]
   - Sets the voltages of the RP100 channels 1 and 2 to specified values.
   - Waits for the specified number of seconds after setting the voltage.
   - Mode:
       'wait'    : Only wait for the time to elapse, no measurement.
       'measure' : Wait for the time to elapse, then take measurement(s).

3. hold: [hold_time_s, delta_t_s]
   - Holds the current temperature and voltages for a specified duration.
   - delta_t_s is the interval between measurements during the hold.
   - Mode:
       'wait'    : Simply hold, no measurements taken.
       'measure' : Take repeated measurements during the hold period.
'''



host = '128.6.234.242'
port = 10823

filename = 'PtSn4_3.csv'

volt_avg_count = 10
MAX_FAILURES = 6
FAILURE_RESET_TIME = 10
FAILURES_BEFORE_TIMEOUT = 3


program = [
    ['hold', [4000, 2], 'measure'],
    ['hold', [60, 0], 'wait'], 
    ['set_voltage', [[1,0], 120], 'measure'],
    ['set_voltage', [[2,0], 120], 'measure'],
    ['set_voltage', [[3,0], 120], 'measure'],
    ['set_voltage', [[4,0], 120], 'measure'],
    ['set_voltage', [[5,0], 120], 'measure'],
    ['set_voltage', [[6,0], 120], 'measure'],
    ['set_voltage', [[7,0], 120], 'measure'],
    ['set_voltage', [[8,0], 120], 'measure'],
    ['set_voltage', [[9,0], 120], 'measure'],
    ['set_voltage', [[10,0], 120], 'measure'],
    ['set_voltage', [[11,0], 120], 'measure'],
    ['set_voltage', [[12,0], 120], 'measure'],
    ['set_voltage', [[13,0], 120], 'measure'],
    ['set_voltage', [[14,0], 120], 'measure'],
    ['set_voltage', [[15,0], 120], 'measure'],
    ['set_voltage', [[16,0], 120], 'measure'],
    ['set_voltage', [[17,0], 120], 'measure'],
    ['set_voltage', [[18,0], 120], 'measure'],
    ['set_voltage', [[19,0], 120], 'measure'],
    ['set_voltage', [[20,0], 120], 'measure'],
    ['set_voltage', [[21,0], 120], 'measure'],
    ['set_voltage', [[22,0], 120], 'measure'],
    ['set_voltage', [[23,0], 120], 'measure'],
    ['set_voltage', [[24,0], 120], 'measure'],
    ['set_voltage', [[25,0], 120], 'measure'],
    ['set_voltage', [[26,0], 120], 'measure'],
    ['set_voltage', [[27,0], 120], 'measure'],
    ['set_voltage', [[28,0], 120], 'measure'],
    ['set_voltage', [[29,0], 120], 'measure'],
    ['set_voltage', [[30,0], 120], 'measure'],
    ['set_voltage', [[31,0], 120], 'measure'],
    ['set_voltage', [[32,0], 120], 'measure'],
    ['set_voltage', [[33,0], 120], 'measure'],
    ['set_voltage', [[34,0], 120], 'measure'],
    ['set_voltage', [[35,0], 120], 'measure'],
    ['set_voltage', [[36,0], 120], 'measure'],
    ['set_voltage', [[37,0], 120], 'measure'],
    ['set_voltage', [[38,0], 120], 'measure'],
    ['set_voltage', [[39,0], 120], 'measure'],
    ['set_voltage', [[40,0], 120], 'measure'],    
    ['set_voltage', [[0,0], 240], 'measure'],
    ['hold', [60, 0], 'wait'],
    ['set_temp',[100, 1], 'measure'],
    ['hold', [3600, 2], 'measure'],
    ['hold', [60, 0], 'wait'],
    ['set_voltage', [[1,0], 120], 'measure'],
    ['set_voltage', [[2,0], 120], 'measure'],
    ['set_voltage', [[3,0], 120], 'measure'],
    ['set_voltage', [[4,0], 120], 'measure'],
    ['set_voltage', [[5,0], 120], 'measure'],
    ['set_voltage', [[6,0], 120], 'measure'],
    ['set_voltage', [[7,0], 120], 'measure'],
    ['set_voltage', [[8,0], 120], 'measure'],
    ['set_voltage', [[9,0], 120], 'measure'],
    ['set_voltage', [[10,0], 120], 'measure'],
    ['set_voltage', [[11,0], 120], 'measure'],
    ['set_voltage', [[12,0], 120], 'measure'],
    ['set_voltage', [[13,0], 120], 'measure'],
    ['set_voltage', [[14,0], 120], 'measure'],
    ['set_voltage', [[15,0], 120], 'measure'],
    ['set_voltage', [[16,0], 120], 'measure'],
    ['set_voltage', [[17,0], 120], 'measure'],
    ['set_voltage', [[18,0], 120], 'measure'],
    ['set_voltage', [[19,0], 120], 'measure'],
    ['set_voltage', [[20,0], 120], 'measure'],
    ['set_voltage', [[21,0], 120], 'measure'],
    ['set_voltage', [[22,0], 120], 'measure'],
    ['set_voltage', [[23,0], 120], 'measure'],
    ['set_voltage', [[24,0], 120], 'measure'],
    ['set_voltage', [[25,0], 120], 'measure'],
    ['set_voltage', [[26,0], 120], 'measure'],
    ['set_voltage', [[27,0], 120], 'measure'],
    ['set_voltage', [[28,0], 120], 'measure'],
    ['set_voltage', [[29,0], 120], 'measure'],
    ['set_voltage', [[30,0], 120], 'measure'],
    ['set_voltage', [[31,0], 120], 'measure'],
    ['set_voltage', [[32,0], 120], 'measure'],
    ['set_voltage', [[33,0], 120], 'measure'],
    ['set_voltage', [[34,0], 120], 'measure'],
    ['set_voltage', [[35,0], 120], 'measure'],
    ['set_voltage', [[36,0], 120], 'measure'],
    ['set_voltage', [[37,0], 120], 'measure'],
    ['set_voltage', [[38,0], 120], 'measure'],
    ['set_voltage', [[39,0], 120], 'measure'],
    ['set_voltage', [[40,0], 120], 'measure'],    
    ['set_voltage', [[0,0], 240], 'measure']
]


# ------------------------------------------------------------------
# Instrument addresses
# ------------------------------------------------------------------
RP100_ADDR = 'ASRL4::INSTR'
METER_ADDR = 'GPIB0::21::INSTR'
KEITHLEY_ADDR = 'GPIB0::16::INSTR'

# ------------------------------------------------------------------
# VISA resource setup
# ------------------------------------------------------------------
rm = pyvisa.ResourceManager()
power_supply = rm.open_resource(RP100_ADDR)
meter = rm.open_resource(METER_ADDR)
keithley = rm.open_resource(KEITHLEY_ADDR)

# ------------------------------------------------------------------
# LCR meter configuration
# ------------------------------------------------------------------
meter.write('FREQ 100000')
meter.write('FUNC:IMP:TYPE CPD')
meter.write('VOLT:LEV 1')
meter.write('APER LONG,3')

# ------------------------------------------------------------------
# RP100 power supply configuration
# ------------------------------------------------------------------
power_supply.write('OUTP1 1')
power_supply.write('OUTP2 1')
power_supply.write('SOUR1:VOLT:SLEW 100')
power_supply.write('SOUR2:VOLT:SLEW 100')

# ------------------------------------------------------------------
# Keithley configuration
# ------------------------------------------------------------------
keithley.write('*RST') #restores 6221 defaults
keithley.write("TRAC:CLE") 
keithley.write('SYST:COMM:SER:SEND "REN"')

#setup2182A
voltrange = 0.01 
keithley.write('SYST:COMM:SER:SEND "VOLT:RANG %f"' % voltrange) #sets 2V range for 2182a 
rate = 1
keithley.write('SYST:COMM:SER:SEND "VOLT:NPLC %f"' % rate) #Set rate to 1PLC for 2182a

#setup6221Delta
keithley.write('*RST') #restores 6221 defaults
keithley.write('SOUR:DELT:HIGH 1e-3') #sets high source current value to 1mA
keithley.write('SOUR:DELT:COUN 1') #Sets Delta count to 65536
keithley.write('SOUR:CURR:RANGE:AUTO 1')
keithley.write('TRAC:POIN 1') #sets buffer to 65536 points
keithley.write('SOUR:DELT:ARM') #Arms Delta

# ------------------------------------------------------------------
# Measurement helper functions
# ------------------------------------------------------------------
def get_lcr_capacitance():
    reply = meter.query('FETCH?')
    chunks = reply.split(',')
    cap_pf = float(chunks[0]) * 1e12  # convert F → pF
    d = float(chunks[1])
    return cap_pf, d

def get_lcr_exvolt():
    return float(meter.query('FETC:SMON:VAC?'))

def get_rp100_volt():
    v1 = float(power_supply.query('MEAS1:VOLT?'))
    v2 = float(power_supply.query('MEAS2:VOLT?'))
    return v1,v2

def set_rp100_volt(channel, temp, volt):
    if temp > 250:
        lower, upper = -20, 120
    elif temp > 100:
        lower, upper = (-50 + 0.2 * (temp - 100)), 120
    elif temp >= 10:
        lower = -200 + (5/3) * (temp - 10)
        upper = 200 - (8/9) * (temp - 20)
    else:
        lower, upper = -200, 200

    volt_clamp = min(max(volt, lower), upper)
    power_supply.write(f'SOUR{channel}:VOLT {volt_clamp}')

# ------------------------------------------------------------------
# Temperature error handling
# ------------------------------------------------------------------
def reset_client_connection(client, failures):
    print("\nConnection failure detected. Resetting client...")
    reset_attempts = 0
    while reset_attempts < FAILURES_BEFORE_TIMEOUT:
        try:
            client.close()
            client = mpv.Client(host, port)
        except:
            pass
        time.sleep(FAILURE_RESET_TIME)
        try:
            client.open()
            print("Client reconnected successfully.")
            return client, 0
        except Exception:
            reset_attempts += 1
            print(f"Reconnect attempt {reset_attempts} failed.")
    raise RuntimeError("Failed to reconnect to MultiPyVu client after multiple attempts.")

def safe_get_temperature_with_failures(client, last_temp, failures):
    try:
        temp, status = client.get_temperature()
        if temperature_invalid(temp, last_temp):
            raise ValueError
        failures = 0
        return temp, status, failures, client
    except Exception:
        failures += 1
        if failures >= MAX_FAILURES:
            client, failures = reset_client_connection(client, failures)
        return None, None, failures, client

def temperature_invalid(temp, last_temp):
    if temp <= 0.0:
        return True
    if last_temp is not None and abs(temp - last_temp) > 20:
        return True
    return False

# ------------------------------------------------------------------
# Keithley measurement helper
# ------------------------------------------------------------------
def take_keithley_measurement():
    volt_avg = []
    for i in range(volt_avg_count):
        keithley.write('INIT:IMM') #starts delta measurements
        keithley.query('SENS:DATA?')
        temp_var = str(keithley.query('TRAC:DATA?')).replace('+','')
        var2 = float(temp_var.split(',')[0])
        volt_avg.append(var2)
        time.sleep(0.05)
    return sum(volt_avg)/len(volt_avg)


# ------------------------------------------------------------------
# Data acquisition
# ------------------------------------------------------------------
with open(filename, 'w', newline='') as file:

    writer = csv.writer(file)
    writer.writerow([
        'Time(s)', 'LoopTime(s)', 'Temperature(K)', 'TempStatus',
        'Voltage',
        'LcrCap(pF)', 'LcrD', 'LcrExcitation(V)',
        'RP100_V1(V)', 'RP100_V2(V)'
    ])

    start_time = time.time()
    last_valid_temp = None
    failures = 0

    client = mpv.Client(host, port)
    client.open()

    try:

        for command, params, mode in program:


            # --------------------------------------------------
            # SET TEMPERATURE
            # --------------------------------------------------
            if command == 'set_temp':
                target, rate = params
                print(f"\n-> Set temperature: {target} K at {rate} K/min")
                client.set_temperature(target, rate, client.temperature.approach_mode.fast_settle)
                mask = client.temperature.waitfor

                while True:
                    loop_start = time.time()
                    temp, status, failures, client = safe_get_temperature_with_failures(client, last_valid_temp, failures)
                    if temp is None:
                        continue
                    last_valid_temp = temp
                    print(f"T = {temp:.2f} K")
                    if mode == 'wait' and client.is_steady(mask):
                        break
                    if mode == 'measure':
                        meas = take_keithley_measurement()
                        v1, v2 = get_rp100_volt()
                        cap, d = get_lcr_capacitance()
                        exvolt = get_lcr_exvolt()
                        now = time.time()
                        writer.writerow([
                            now - start_time, now - loop_start, temp, status,
                            meas, cap, d, exvolt, v1, v2
                        ])
                    time.sleep(2)

            # --------------------------------------------------
            # SET VOLTAGE
            # --------------------------------------------------
            elif command == 'set_voltage':
                [v_ch, wait_time] = params
                ch1, ch2 = v_ch
                print(f"\n-> Set voltage: Ch1 = {ch1} V, Ch2 = {ch2} V, wait {wait_time} s")
                set_rp100_volt(1, last_valid_temp or 300, ch1)
                set_rp100_volt(2, last_valid_temp or 300, ch2)
                time.sleep(wait_time)

                if mode == 'measure':
                    loop_start = time.time()
                    temp, status, failures, client = safe_get_temperature_with_failures(client, last_valid_temp, failures)
                    if temp is None:
                        continue

                    meas = take_keithley_measurement()
                    v1, v2 = get_rp100_volt()
                    cap, d = get_lcr_capacitance()
                    exvolt = get_lcr_exvolt()
                    now = time.time()
                    writer.writerow([
                        now - start_time, now - loop_start, temp, status,
                        meas, cap, d, exvolt, v1, v2
                    ])

            # --------------------------------------------------
            # HOLD
            # --------------------------------------------------
            elif command == 'hold':
                hold_time, dt = params
                print(f"\n-> Hold {hold_time}s (delta t = {dt}s)")
                t0 = time.time()
                while time.time() - t0 < hold_time:
                    loop_start = time.time()
                    temp, status, failures, client = safe_get_temperature_with_failures(client, last_valid_temp, failures)
                    if temp is None:
                        continue
                    last_valid_temp = temp
                    meas = take_keithley_measurement()
                    v1, v2 = get_rp100_volt()
                    cap, d = get_lcr_capacitance()
                    exvolt = get_lcr_exvolt()
                    now = time.time()
                    writer.writerow([
                        now - start_time, now - loop_start, temp, status,
                        meas, cap, d, exvolt, v1, v2
                    ])
                    if dt > 0:
                        time.sleep(dt)

    finally:
        client.close_client()

# ------------------------------------------------------------------
# Hardware shutdown
# ------------------------------------------------------------------
keithley.write('*RST') #restores 6221 defaults
keithley.write("TRAC:CLE") 
power_supply.write('SOUR1:VOLT 0')
power_supply.write('SOUR2:VOLT 0')
time.sleep(5)
power_supply.write('OUTP1 0')
power_supply.write('OUTP2 0')

keithley.close()
power_supply.close()
meter.close()
rm.close()