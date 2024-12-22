from Converters import DB, Divider

# Given values
Vcc = 5  # V
R1 = 10000  # ohms (top resistor)


# Desired voltages
V1 = 3.0  # V
V2 = 1.75  # V
V3 = 0.21  # V


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


# Set the current by Setting R2

R2 = Divider.voltage_solve_for(V1, Vcc, R1, None)
print(R2)

I = Vcc / (R1 + R2)
print(I)

# Set R3

R3 = V2 / I
R2 = R2 - R3

# Set R4

R4 = V3 / I
R3 = R3 - R4

print()
print(R1)
print(R2)
print(R3)
print(R4)

print(resistor_network(Vcc, 10000, [V1, V2, V3]))
