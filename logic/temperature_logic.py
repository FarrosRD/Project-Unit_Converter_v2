def convert_temperature(value, from_unit, to_unit):
    # Base Unit: Celcius
    if from_unit == to_unit: return value
    
    if from_unit == "Fahrenheit": temp_c = (value - 32) * 5/9
    elif from_unit == "Kelvin": temp_c = value - 273.15
    else: temp_c = value

    if to_unit == "Fahrenheit": return (temp_c * 9/5) + 32
    elif to_unit == "Kelvin": return temp_c + 273.15
    return temp_c