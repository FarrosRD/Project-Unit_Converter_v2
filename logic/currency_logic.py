import requests

API_KEY = "043f512b96c839f141e795de"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# Cache 
_rate_cache = {}

def convert_currency(value, from_currency, to_currency):
    try:
        from_code = from_currency.split(" - ")[0].strip()
        to_code = to_currency.split(" - ")[0].strip()
    except:
        from_code = from_currency
        to_code = to_currency
    
    if from_code == to_code:
        return value

    try:
        if from_code not in _rate_cache:
            response = requests.get(f"{BASE_URL}{from_code}", timeout=5)
            data = response.json()
            if data["result"] == "success":
                _rate_cache[from_code] = data["conversion_rates"]
            else:
                return 0.0
        
        rates = _rate_cache[from_code]
        rate = rates.get(to_code, 0)
        return value * rate
    except Exception:
        return 0.0