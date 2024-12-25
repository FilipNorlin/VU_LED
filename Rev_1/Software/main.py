import math
from Prefix import PrefixAdder
from Converters import DB, Divider, Resistance, Charge
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


print("\n --- Log Stage --- \n")

# For the pwm signal to work properly with the sawtooth signal the
# soundwave has to have a ptp voltage of (2/3 * vcc) - (1/3 * vcc).
# The soundwave has to have its amplitude offsetted by 1/3 * vcc aswell

vcc = 5
vmax = 2 / 3 * 5
vmin = 1 / 3 * 5
vref = vmax - vmin
R1 = 1e5

for db in db_values:
    voltage = DB.to_lin(db, vcc)
    sound_voltage_values.append(voltage)

resistors = resistor_network(vcc, R1, sound_voltage_values)

for i in range(len(resistors) - 1):
    print(
        f"{pfix.add_prefix(db_values[i], 'dB')}: \t {pfix.add_prefix(sound_voltage_values[i], 'V')}: \t {pfix.add_prefix(resistors[i + 1], 'ohm')}"
    )

print()
print("-" * 50)
print()

for db in db_values:
    voltage = DB.to_lin(db, vref) + vmin
    led_voltage_values.append(voltage)

led_voltage_values[0] = 5

for i in range(len(led_voltage_values)):
    r = Divider.voltage_solve_for(led_voltage_values[i], 5, None, 10e3)
    print(
        f"{pfix.add_prefix(db_values[i], 'dB')}: \t {pfix.add_prefix(led_voltage_values[i], 'V')}: \t {pfix.add_prefix(r, 'ohm')}"
    )

print()
print("-" * 50)
print()

R1 = 47e3
R2 = 100e3

Ic = Divider.voltage(R1, R2, vcc)

# print(pfix.add_prefix(Charge.discharge_t(5, 1, 1000, 5e-6, None), "s"))
# print(pfix.add_prefix(Charge.discharge_t(vmin, vmax, None, 47e-9, Ic), "s"))

for i in range(len(led_voltage_values)):
    duty_cycle = (led_voltage_values[i] - vref) / vref * 100

    print(f"{pfix.add_prefix(db_values[i], 'db:')} \t {round(duty_cycle, 3)}%")
