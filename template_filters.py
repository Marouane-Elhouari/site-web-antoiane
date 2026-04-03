import re
from flask import Blueprint

def chemical_formula(text):
    """
    Convert chemical formulas to HTML with subscripts.
    Example: C3H6O -> C<sub>3</sub>H<sub>6</sub>O
    """
    if not text:
        return text
    
    # Find all numbers in the formula and wrap them in sub tags
    # This regex finds numbers that are part of chemical formulas
    pattern = r'(\d+)'
    formula_with_subs = re.sub(pattern, r'<sub>\1</sub>', text)
    
    return formula_with_subs

# Register the filter with Flask app
def register_filters(app):
    app.add_template_filter(chemical_formula, 'chemical_formula')
