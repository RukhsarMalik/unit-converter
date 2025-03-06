import streamlit as st

st.title("Unit Converter Web App")

# Top buttons for category selection
category = st.radio(
    "Select a Category:", 
    ["Weight", "Length", "Temperature", "Volume", "Area", "Time"],
    horizontal=True
)

# Unit options based on category
unit_options = {
    "Weight": ["grams", "kilograms", "pounds", "ounces"],
    "Length": ["meters", "kilometers", "miles", "yards", "feet", "inches"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Volume": ["liters", "milliliters", "gallons", "cups"],
    "Area": ["Square Meter", "Square Kilometer", "Acre", "Hectare"],
    "Time": ["seconds", "minutes", "hours", "days"]
}

# Conversion factors
conversion_factors = {
    'Length': {
        'meters': {'kilometers': 0.001, 'miles': 0.000621371, 'feet': 3.28084, 'yards': 1.09361, 'inches': 39.3701},
        'kilometers': {'meters': 1000, 'miles': 0.621371, 'feet': 3280.84, 'yards': 1093.61, 'inches': 39370.1},
        'miles': {'meters': 1609.34, 'kilometers': 1.60934, 'feet': 5280, 'yards': 1760, 'inches': 63360},
        'feet': {'meters': 0.3048, 'kilometers': 0.0003048, 'miles': 0.000189394, 'yards': 0.333333, 'inches': 12},
        'yards': {'meters': 0.9144, 'kilometers': 0.0009144, 'miles': 0.000568182, 'feet': 3, 'inches': 36},
        'inches': {'meters': 0.0254, 'kilometers': 0.0000254, 'miles': 0.0000157828, 'feet': 0.0833333, 'yards': 0.0277778}
    },
    'Weight': {
        'grams': {'kilograms': 0.001, 'pounds': 0.00220462, 'ounces': 0.035274},
        'kilograms': {'grams': 1000, 'pounds': 2.20462, 'ounces': 35.274},
        'pounds': {'grams': 453.592, 'kilograms': 0.453592, 'ounces': 16},
        'ounces': {'grams': 28.3495, 'kilograms': 0.0283495, 'pounds': 0.0625}
    },
    'Temperature': {
        'Celsius': {'Fahrenheit': lambda c: (c * 9/5) + 32, 'Kelvin': lambda c: c + 273.15},
        'Fahrenheit': {'Celsius': lambda f: (f - 32) * 5/9, 'Kelvin': lambda f: ((f - 32) * 5/9) + 273.15},
        'Kelvin': {'Celsius': lambda k: k - 273.15, 'Fahrenheit': lambda k: ((k - 273.15) * 9/5) + 32}
    },
    'Time': {
        'seconds': {'minutes': 1/60, 'hours': 1/3600, 'days': 1/86400},
        'minutes': {'seconds': 60, 'hours': 1/60, 'days': 1/1440},
        'hours': {'seconds': 3600, 'minutes': 60, 'days': 1/24},
        'days': {'seconds': 86400, 'minutes': 1440, 'hours': 24}
    },
    'Volume': {
        'liters': {'milliliters': 1000, 'gallons': 0.264172, 'cups': 4.22675},
        'milliliters': {'liters': 0.001, 'gallons': 0.000264172, 'cups': 0.00422675},
        'gallons': {'liters': 3.78541, 'milliliters': 3785.41, 'cups': 16},
        'cups': {'liters': 0.236588, 'milliliters': 236.588, 'gallons': 0.0625}
    }
}

# Ensure session state for 'from_unit' and 'to_unit' exists, reset if category changes
if 'category' not in st.session_state or st.session_state.category != category:
    st.session_state.category = category
    st.session_state.from_unit = unit_options[category][0]
    st.session_state.to_unit = unit_options[category][1]

# Dropdowns for 'From' and 'To' units
st.session_state.from_unit = st.selectbox(f"From ({category}):", unit_options[category], index=unit_options[category].index(st.session_state.from_unit))
st.session_state.to_unit = st.selectbox(f"To ({category}):", unit_options[category], index=unit_options[category].index(st.session_state.to_unit))

# Amount input
amount = st.number_input("Amount:", min_value=0.0, format="%.2f")

# Buttons for conversion, reset, and swap
col1, col2, col3 = st.columns(3)

convert = col1.button("Convert")
reset = col2.button("Reset")
swap = col3.button("Swap")

# Handle button actions
result = ""
steps = ""

if convert:
    if st.session_state.from_unit == st.session_state.to_unit:
        result = amount
        steps = f"No conversion needed, both units are the same: {st.session_state.from_unit}"
    else:
        try:
            if category == 'Temperature':
                result = conversion_factors[category][st.session_state.from_unit][st.session_state.to_unit](amount)
                steps = f"Converting {amount} {st.session_state.from_unit} to {st.session_state.to_unit}"
            else:
                factor = conversion_factors[category][st.session_state.from_unit.lower()][st.session_state.to_unit.lower()]
                result = amount * factor
                steps = f"Converting {amount} {st.session_state.from_unit} to {st.session_state.to_unit} using factor {factor}"
        except KeyError:
            result = "Conversion not available"
            steps = "Please select compatible units"

elif reset:
    st.session_state.from_unit = unit_options[category][0]
    st.session_state.to_unit = unit_options[category][1]
    st.rerun()

elif swap:
    st.session_state.from_unit, st.session_state.to_unit = st.session_state.to_unit, st.session_state.from_unit
    st.rerun()

# Display result
if result:
    st.subheader("Result")
    st.write(f"{amount} {st.session_state.from_unit} = {result} {st.session_state.to_unit}")

# Display conversion steps
if steps:
    st.subheader("Result Steps")
    st.write(steps)
