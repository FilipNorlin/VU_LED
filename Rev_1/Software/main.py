import math
from Prefix import PrefixAdder
from Converters import DB, Divider, Resistance
from Non_inverted_summer import Non_inverted_summer

pfix = PrefixAdder()
summer = Non_inverted_summer(Rf=1000, Rg=1000)

db_values = [-2, -6, -10, -18, -30, -40]
sound_voltage_values = []
led_voltage_values = []


def resistor_network(Vcc, R1, voltages):
    resistors = [R1]
    resistors.append(Divider.voltage_solve_for(voltages[0], Vcc, R1, None))
    I = Vcc / (resistors[0] + resistors[1])

    if len(voltages) > 1:
        for i in range(2, len(voltages) + 1):
            r = voltages[i - 1] / I

            resistors[i - 1] -= r
            resistors.append(r)

    return resistors


# For the pwm signal to work properly with the sawtooth signal the
# soundwave has to have a ptp voltage of (2/3 * vcc) - (1/3 * vcc).
# The soundwave has to have its amplitude offsetted by 1/3 * vcc aswell

vcc = 5
vmax = 2 / 3 * 5
vmin = 1 / 3 * 5
vref = vmax - vmin
R1 = 1e6

for db in db_values:
    voltage = DB.to_lin(db, vcc)
    sound_voltage_values.append(voltage)

resistors = resistor_network(vcc, R1, sound_voltage_values)
print(pfix.add_prefix(vcc, "V"))

for i in range(len(resistors) - 1):
    print(
        f"{pfix.add_prefix(db_values[i], 'dB')}: \t {pfix.add_prefix(sound_voltage_values[i], 'V')}: \t {pfix.add_prefix(resistors[i + 1], 'ohm')}"
    )


for db in db_values:
    voltage = DB.to_lin(db, vref)
    led_voltage_values.append(voltage)


R_goal = 10e3

resistor_divider = [10e3] * (len(led_voltage_values) - 1)
resistor_divider.append(10e3)


rtot = Resistance.parallel(resistor_divider)

print(rtot)

R1 = Divider.voltage_solve_for(led_voltage_values[0], 5, None, rtot)
print(pfix.add_prefix(R1, "Ohm"))
print(pfix.add_prefix(led_voltage_values[0], "V"))
