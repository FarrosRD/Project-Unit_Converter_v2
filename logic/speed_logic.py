def convert_speed(value, from_unit, to_unit):
    # Base unit: Meters per second
    units = {
        "Meters per second": 1.0,
        "Kilometers per hour": 1/3.6,
        "Miles per hour": 0.44704,
        "Knot": 0.514444,
        "Foot per second": 0.3048
    }
    if from_unit not in units or to_unit not in units: return 0.0
    return value * (units[from_unit] / units[to_unit])