def convert_mass(value, from_unit, to_unit):
    # Base unit: Gram
    units = {
        "Gram": 1.0,
        "Kilogram": 1000.0,
        "Milligram": 0.001,
        "Metric Ton": 1000000.0,
        "Pound": 453.592,
        "Ounce": 28.3495
    }
    if from_unit not in units or to_unit not in units: return 0.0
    return value * (units[from_unit] / units[to_unit])