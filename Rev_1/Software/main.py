import math
from Prefix import PrefixAdder
from Converters import DB, Divider

pfix = PrefixAdder()

db_values = [-2, -6, -10, -18, -30, -40]
voltage_values = []


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

for db in db_values:
    voltage = DB.to_lin(db, vref)
    voltage_values.append(voltage)

    # print(f"{pfix.add_prefix(db, 'dB')}: \t {pfix.add_prefix(voltage, 'V')}")


resistors = resistor_network(vref, 1e6, voltage_values)
print(pfix.add_prefix(vref, "V"))

for i in range(len(resistors) - 1):
    print(
        f"{pfix.add_prefix(db_values[i], 'dB')}: \t {pfix.add_prefix(voltage_values[i], 'V')}: \t {pfix.add_prefix(resistors[i + 1], 'ohm')}"
    )
