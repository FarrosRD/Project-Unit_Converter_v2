def convert_data(value, from_unit, to_unit):
    # Base unit: Byte
    units = {
        "Byte": 1.0,
        "Kilobyte": 1024.0,
        "Megabyte": 1024.0**2,
        "Gigabyte": 1024.0**3,
        "Terabyte": 1024.0**4,
        "Petabyte": 1024.0**5
    }
    if from_unit not in units or to_unit not in units: return 0.0
    return value * (units[from_unit] / units[to_unit])