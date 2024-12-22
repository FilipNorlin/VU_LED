import math


class DB:
    def to_dB(gain, ref):
        if gain > 0:
            return float(20 * math.log10(gain / ref))
        print("Gain has to be over 0")
        return

    def to_lin(dB, ref):
        return float(math.pow(ref * 10, dB / 20))


class Resistance:
    @staticmethod
    def series(resistors):
        r_tot = 0

        for r in resistors:
            r_tot += r

        return r_tot

    @staticmethod
    def parallel(resistors):
        r_tot = 0

        for r in resistors:
            r_tot += 1 / r

        return 1 / r_tot


class Charge:

    @staticmethod
    def discharge_v(V, R, C, t):
        return V * math.pow(math.e, -(t / (R * C)))

    @staticmethod
    def discharge_t(V_start, V_end, R, C, I_cap):
        if I_cap is None:
            return -R * C * math.log(V_end / V_start)
        return (C * (V_end - V_start)) / I_cap

    @staticmethod
    def charge_v(V, R, C, t):
        return V * (1 - math.pow(math.e, -(t / (R * C))))

    @staticmethod
    def charge_t(V_start, V_end, R, C):
        return -R * C * math.log(1 - (V_start / V_end))

    @staticmethod
    def charge_R(V_start, V_end, C, t):
        return t / (-C * math.log(V_start / V_end))


class Divider:
    def voltage(R1, R2, Vin):
        return (Vin * R2) / (R1 + R2)

    def voltage_solve_for(Vout, Vin, R1, R2):
        if Vout is None:
            return (Vin * R2) / (R1 + R2)
        if Vin is None:
            return (Vout * (R1 + R2)) / R2
        if R1 is None:
            return R2 * ((Vin / Vout) - 1)
        if R2 is None:
            return (Vout * R1) / (Vin - Vout)
