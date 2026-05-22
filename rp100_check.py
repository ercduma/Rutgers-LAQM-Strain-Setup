import csv
import time
import pyvisa
import MultiPyVu as mpv


RP100_ADDR = 'ASRL4::INSTR'

rm = pyvisa.ResourceManager()

print(rm.list_resources())

power_supply = rm.open_resource(RP100_ADDR)

v1 = float(power_supply.query('MEAS1:VOLT?'))
v2 = float(power_supply.query('MEAS2:VOLT?'))

print(f'{v1}, {v2}')

power_supply.write('SOUR1:VOLT 0')
power_supply.write('SOUR2:VOLT 0')
time.sleep(5)
power_supply.write('OUTP1 0')
power_supply.write('OUTP2 0')

power_supply.close()
rm.close()
