import math
from Prefix import PrefixAdder
from Converters import DB, Divider, Resistance

pfix = PrefixAdder()


class Input:
    def __init__(self, voltage, resistor, name):
        self.voltage = voltage  # Use the property setter for validation
        self.resistor = resistor
        self.name = name

    # Getter for voltage
    @property
    def voltage(self):
        return self._voltage

    # Setter for voltage
    @voltage.setter
    def voltage(self, value):
        if not isinstance(value, float):
            raise ValueError("Voltage must be a float.")
        if value < 0:
            raise ValueError("Voltage cannot be negative.")
        self._voltage = value

    # Getter for resistor
    @property
    def resistor(self):
        return self._resistor

    # Setter for resistor
    @resistor.setter
    def resistor(self, value):
        if not isinstance(value, float):
            raise ValueError("Resistance must be a float.")
        if value <= 0:
            raise ValueError("Resistance must be positive.")
        self._resistor = value

    # Getter for name
    @property
    def name(self):
        return self._name

    # Setter for name
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        self._name = value

    def __str__(self):
        return f"Input(name={self._name}, voltage={self._voltage} V, resistor={self._resistor} Ω)"


class Non_inverted_summer:
    """
    A class for implementing a non-inverting summer.
    """

    def __init__(self, Rf, Rg):
        self.Rf = Rf
        self.Rg = Rg
        self._inputs = []

    # Getter for inputs
    @property
    def inputs(self):
        return self._inputs

    # Method to add inputs
    def add_input(self, V, R, name):
        """
        Adds an input to the summer.
        """
        new_input = Input(V, R, name)
        self._inputs.append(new_input)

    # Method to update an existing input by name
    def update_input(self, name, voltage=None, resistor=None, new_name=None):
        for inpt in self._inputs:
            if inpt.name == name:
                if voltage is not None:
                    inpt.voltage = voltage
                if resistor is not None:
                    inpt.resistor = resistor
                if new_name is not None:
                    inpt.name = new_name
                return
        raise ValueError(f"Input with name '{name}' not found.")

    def get_vout(self):
        resistors = []
        voltages = []
        for inpt in self._inputs:
            voltages.append(inpt.voltage)
            resistors.append(inpt.resistor)

        Req = Resistance.parallel(resistors)

        gain = 1 + self.Rf / self.Rg
        V_plus = sum(inpt.voltage / inpt.resistor for inpt in self._inputs) * Req

        return gain * V_plus

    def __str__(self):
        return (
            f"Non_inverted_summer(Rf={self.Rf} Ω, Rg={self.Rg} Ω, "
            f"inputs={len(self._inputs)})"
        )


# Example usage
if __name__ == "__main__":
    # Create an instance of Non_inverted_summer
    summer = Non_inverted_summer(Rf=1000, Rg=1000)

    # Add inputs
    summer.add_input(V=5.0, R=1000.0, name="Input 1")
    summer.add_input(V=3.3, R=2200.0, name="Input 2")
    summer.add_input(V=1.5, R=1500.0, name="Input 3")

    # Update an input
    summer.update_input(name="Input 2", voltage=4.0, resistor=2000.0)

    # Print Vout
    print(pfix.add_prefix(summer.get_vout(), "V"))

    # Display the summer
    print(summer)

    # Display all inputs
    for input_obj in summer.inputs:
        print(input_obj)
