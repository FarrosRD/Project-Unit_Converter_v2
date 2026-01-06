def convert_area(value, from_unit, to_unit):
    # Base unit: Square Meter
    units = {
        "Square Meter": 1.0,
        "Square Kilometer": 1000000.0,
        "Square Centimeter": 0.0001,
        "Square Millimeter": 0.000001,
        "Hectare": 10000.0,
        "Acre": 4046.856,
        "Square Mile": 2589988.11,
        "Square Foot": 0.092903
    }
    if from_unit not in units or to_unit not in units: return 0.0
    return value * (units[from_unit] / units[to_unit])