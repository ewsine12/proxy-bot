COUNTRIES = {
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "IN": "India",
    "JP": "Japan",
    # Add all countries as needed
}

def get_code(name):
    name = name.upper()
    for code, full in COUNTRIES.items():
        if name == code or name.upper() == full.upper():
            return code, full
    return None, None
