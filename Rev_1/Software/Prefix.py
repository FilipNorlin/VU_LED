import math


class PrefixAdder:
    def __init__(self):
        self.prefixes = {
            -12: "p",
            -9: "n",
            -6: "u",
            -3: "m",
            0: "",  # No prefix for base unit
            3: "k",
            6: "M",
            9: "G",
            12: "T",
            # Add more prefixes as needed
        }

    def add_prefix(self, value, unit):
        # Determine the appropriate prefix based on the magnitude of the value
        magnitude = 0 if value == 0 else int(math.floor(math.log10(abs(value)) / 3) * 3)
        prefix = self.prefixes.get(magnitude, "10^" + str(magnitude))

        # Adjust the value based on the magnitude and return it with the prefix
        adjusted_value = round(value / (10**magnitude), 3)
        return str(f"{adjusted_value}{prefix}{unit}")
