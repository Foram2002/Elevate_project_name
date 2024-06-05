import tkinter as tk
from tkinter import ttk, messagebox

class MeasurementConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Measurement Converter")
        
        self.create_widgets()

    def create_widgets(self):
        self.conversion_type_label = tk.Label(self.root, text="Select Conversion Type:")
        self.conversion_type_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.conversion_type = ttk.Combobox(self.root, values=["Length", "Weight", "Volume", "Temperature"])
        self.conversion_type.grid(row=0, column=1, padx=10, pady=10)
        self.conversion_type.current(0)
        
        self.from_unit_label = tk.Label(self.root, text="From Unit:")
        self.from_unit_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.from_unit = ttk.Combobox(self.root)
        self.from_unit.grid(row=1, column=1, padx=10, pady=10)
        
        self.to_unit_label = tk.Label(self.root, text="To Unit:")
        self.to_unit_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.to_unit = ttk.Combobox(self.root)
        self.to_unit.grid(row=2, column=1, padx=10, pady=10)
        
        self.value_label = tk.Label(self.root, text="Value:")
        self.value_label.grid(row=3, column=0, padx=10, pady=10)
        
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(row=3, column=1, padx=10, pady=10)
        
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert)
        self.convert_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        self.result_label = tk.Label(self.root, text="Result:")
        self.result_label.grid(row=5, column=0, padx=10, pady=10)
        
        self.result = tk.Label(self.root, text="")
        self.result.grid(row=5, column=1, padx=10, pady=10)
        
        self.conversion_type.bind("<<ComboboxSelected>>", self.update_units)
        self.update_units()

    def update_units(self, event=None):
        conversion_type = self.conversion_type.get()
        units = {
            "Length": ["meters", "kilometers", "miles", "yards", "feet", "inches"],
            "Weight": ["grams", "kilograms", "pounds", "ounces"],
            "Volume": ["liters", "milliliters", "gallons", "cups"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
        }
        self.from_unit["values"] = units[conversion_type]
        self.to_unit["values"] = units[conversion_type]
        self.from_unit.current(0)
        self.to_unit.current(1)

    def convert(self):
        conversion_type = self.conversion_type.get()
        from_unit = self.from_unit.get()
        to_unit = self.to_unit.get()
        value = self.value_entry.get()

        try:
            value = float(value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        if conversion_type == "Length":
            result = self.convert_length(value, from_unit, to_unit)
        elif conversion_type == "Weight":
            result = self.convert_weight(value, from_unit, to_unit)
        elif conversion_type == "Volume":
            result = self.convert_volume(value, from_unit, to_unit)
        elif conversion_type == "Temperature":
            result = self.convert_temperature(value, from_unit, to_unit)
        else:
            messagebox.showerror("Invalid Conversion Type", "Please select a valid conversion type.")
            return

        self.result.config(text=f"{result:.2f} {to_unit}")

    def convert_length(self, value, from_unit, to_unit):
        length_units = {
            "meters": 1,
            "kilometers": 1000,
            "miles": 1609.34,
            "yards": 0.9144,
            "feet": 0.3048,
            "inches": 0.0254
        }
        return value * length_units[from_unit] / length_units[to_unit]

    def convert_weight(self, value, from_unit, to_unit):
        weight_units = {
            "grams": 1,
            "kilograms": 1000,
            "pounds": 453.592,
            "ounces": 28.3495
        }
        return value * weight_units[from_unit] / weight_units[to_unit]

    def convert_volume(self, value, from_unit, to_unit):
        volume_units = {
            "liters": 1,
            "milliliters": 0.001,
            "gallons": 3.78541,
            "cups": 0.24
        }
        return value * volume_units[from_unit] / volume_units[to_unit]

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif to_unit == "Kelvin":
                return value + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (value - 32) * 5/9
            elif to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return value - 273.15
            elif to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32
        return value

def main():
    root = tk.Tk()
    app = MeasurementConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
