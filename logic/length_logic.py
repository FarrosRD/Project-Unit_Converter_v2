def convert_length(value, from_unit, to_unit):
    # Base unit: Meter
    units = {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Micrometer": 1e-6,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254
    }
    if from_unit not in units or to_unit not in units: return 0.0
    return value * (units[from_unit] / units[to_unit])