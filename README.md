# Antoine Equation Calculator

A web application for calculating vapor pressure of liquids using the Antoine equation.

## The Antoine Equation

The Antoine equation relates vapor pressure to temperature for pure substances:

```
log₁₀(P_sat) = A - B/(T + C)
```

Where:
- `P_sat` is the saturation vapor pressure
- `T` is the temperature (typically in °C)
- `A, B, C` are substance-specific coefficients

## Features

- Interactive web interface for vapor pressure calculations
- Pre-loaded Antoine parameters for common compounds
- Real-time calculation with detailed results
- Modern, responsive design

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Enter the temperature in °C
2. Input the Antoine parameters (A, B, C) for your compound
   - You can click on common compounds to auto-fill their parameters
3. Click "Calculate P_sat" to get the vapor pressure

## Common Compounds

The app includes Antoine parameters for:
- Water
- Ethanol
- Methanol
- Benzene
- Toluene
- Acetone
- Hexane

## API Endpoints

- `GET /` - Main web interface
- `POST /calculate` - Calculate vapor pressure
- `GET /common_compounds` - Get Antoine parameters for common compounds

## Note

The Antoine equation is valid only within specific temperature ranges for each compound. The app displays the valid temperature range for each pre-loaded compound.
