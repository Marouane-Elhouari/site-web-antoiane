from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from extensions import db, bcrypt
from modeles import User, Liquid
from forms import RegistrationForm, LoginForm, AntoineCalculationForm
import re
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'antoine-secret-key-2024'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    return User.query.get(int(user_id))

# Custom template filter for chemical formulas
@app.template_filter('format_formula')
def format_formula(formula):
    """Convert chemical formulas to HTML with subscripts"""
    if not formula:
        return formula
    # Replace numbers with <sub> tags
    return re.sub(r'(\d+)', r'<sub>\1</sub>', formula)

# ── MySQL connection ─────────────────────────────────────────────────────────────────────────────────────
db_pass = os.getenv('DB_PASSWORD')

# Hna ghadi n-st3mlo l-variable db_pass blast l-password mktoub
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+mysqlconnector://root:{db_pass}@localhost:3306/antoine_data'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt.init_app(app)
 
 
# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    """Home page - professional landing page"""
    return render_template('index.html')
 
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('calculator'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'error')
            return render_template('register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'error')
            return render_template('register.html', form=form)

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        
        # Login the user after registration
        login_user(user)
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('calculator'))

    return render_template('register.html', form=form)
 
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calculator'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f'Welcome back, {user.fname}!', 'success')
                return redirect(url_for('calculator'))
            else:
                flash('Invalid username or password.', 'error')
        except Exception as e:
            flash('Login failed. Please try again.', 'error')

    return render_template('login.html', form=form)
 
 
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
 
 
@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    """Calculator page with Antoine equation form"""
    form = AntoineCalculationForm()
    liquids = Liquid.query.order_by(Liquid.name).all()
    form.liquid_id.choices = [
        (liq.id, f"{liq.name}  ({liq.chemical_formula or '—'})")
        for liq in liquids
    ]

    result = None
    selected_liquid = None

    # Handle pre-selected liquid from chemicals page
    if request.args.get('liquid_id'):
        try:
            preselected_id = int(request.args.get('liquid_id'))
            form.liquid_id.data = preselected_id
            selected_liquid = Liquid.query.get(preselected_id)
        except (ValueError, TypeError):
            pass

    if form.validate_on_submit():
        T = form.temperature.data
        liquid = Liquid.query.get(form.liquid_id.data)

        if liquid is None:
            flash('Liquid not found in database.', 'error')

        elif T < liquid.temperature_min or T > liquid.temperature_max:
            flash(
                f'Temperature is outside the experimental range for {liquid.name}. '
                f'Valid range: {liquid.temperature_min}°C → {liquid.temperature_max}°C.',
                'error'
            )
        else:
            # Antoine: log10(P) = A - B / (C + T)   →  P in mmHg, T in °C
            log_P = liquid.antoine_a - liquid.antoine_b / (liquid.antoine_c + T)
            P_mmHg = 10 ** log_P

            selected_liquid = liquid
            result = {
                'T':      T,
                'P_mmHg': round(P_mmHg,    4),
                'P_bar':  round(P_mmHg * 0.00133322, 6),
                'P_kPa':  round(P_mmHg * 0.133322,   4),
                'P_atm':  round(P_mmHg / 760.0,       6),
                'logP':   round(log_P, 5),
                'A': liquid.antoine_a,
                'B': liquid.antoine_b,
                'C': liquid.antoine_c,
            }
            
            # Store result in session and redirect to results page
            session['calculation_result'] = result
            session['selected_liquid_id'] = liquid.id
            return redirect(url_for('results'))

    return render_template('antoine.html', form=form, result=result,
                           selected_liquid=selected_liquid,
                           fname=session.get('fname'))


@app.route('/antoine')
@login_required
def antoine():
    """Redirect to calculator page"""
    return redirect(url_for('calculator'))


@app.route('/results')
@login_required
def results():
    """Display calculation results"""
    result = session.get('calculation_result')
    selected_liquid_id = session.get('selected_liquid_id')
    
    if not result or not selected_liquid_id:
        flash('No calculation results found.', 'warning')
        return redirect(url_for('calculator'))
    
    selected_liquid = Liquid.query.get(selected_liquid_id)
    
    # Clear session data
    session.pop('calculation_result', None)
    session.pop('selected_liquid_id', None)
    
    return render_template('results.html', result=result, selected_liquid=selected_liquid)
 
 
@app.route('/chemicals')
@login_required
def chemicals():
    """Display all chemical compounds from liquids table"""
    try:
        liquids = Liquid.query.order_by(Liquid.name).all()
        return render_template('liquids.html', liquids=liquids)
    except Exception as e:
        flash(f'Error loading chemicals: {str(e)}', 'error')
        return redirect(url_for('calculator'))


@app.route('/admin_users')
@login_required
def admin_users():
    """Display all registered users"""
    try:
        users = User.query.order_by(User.date_created.desc()).all()
        return render_template('admin_users.html', users=users)
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return redirect(url_for('antoine'))


def init_db():
    """Initialize database with sample compounds if they don't exist"""
    with app.app_context():
        # Sample compounds data
        compounds = [
            {
                'name': 'Water',
                'chemical_formula': 'H2O',
                'cas_number': '7732-18-5',
                'molecular_weight': 18.015,
                'boiling_point': 100.0,
                'antoine_a': 8.07131,
                'antoine_b': 1730.63,
                'antoine_c': 233.426,
                'temperature_min': 1.0,
                'temperature_max': 100.0,
                'description': 'Pure water'
            },
            {
                'name': 'Ethanol',
                'chemical_formula': 'C2H5OH',
                'cas_number': '64-17-5',
                'molecular_weight': 46.069,
                'boiling_point': 78.37,
                'antoine_a': 8.20417,
                'antoine_b': 1642.89,
                'antoine_c': 230.300,
                'temperature_min': -57.0,
                'temperature_max': 80.0,
                'description': 'Ethyl alcohol'
            },
            {
                'name': 'Methanol',
                'chemical_formula': 'CH3OH',
                'cas_number': '67-56-1',
                'molecular_weight': 32.042,
                'boiling_point': 64.7,
                'antoine_a': 7.89750,
                'antoine_b': 1474.08,
                'antoine_c': 232.148,
                'temperature_min': -16.0,
                'temperature_max': 91.0,
                'description': 'Methyl alcohol'
            },
            {
                'name': 'Acetone',
                'chemical_formula': 'C3H6O',
                'cas_number': '67-64-1',
                'molecular_weight': 58.080,
                'boiling_point': 56.05,
                'antoine_a': 7.02447,
                'antoine_b': 1161.00,
                'antoine_c': 224.000,
                'temperature_min': -32.0,
                'temperature_max': 77.0,
                'description': 'Dimethyl ketone'
            },
            {
                'name': 'Benzene',
                'chemical_formula': 'C6H6',
                'cas_number': '71-43-2',
                'molecular_weight': 78.114,
                'boiling_point': 80.1,
                'antoine_a': 6.87764,
                'antoine_b': 1196.76,
                'antoine_c': 219.161,
                'temperature_min': 5.5,
                'temperature_max': 150.0,
                'description': 'Aromatic hydrocarbon'
            }
        ]
        
        added_count = 0
        skipped_count = 0
        
        for compound_data in compounds:
            # Check if compound already exists
            existing = Liquid.query.filter_by(name=compound_data['name']).first()
            
            if existing is None:
                # Create new compound
                compound = Liquid(**compound_data)
                db.session.add(compound)
                added_count += 1
                print(f"Added: {compound_data['name']}")
            else:
                # Skip existing compound
                skipped_count += 1
                print(f"Skipped (already exists): {compound_data['name']}")
        
        # Commit changes
        db.session.commit()
        
        print(f"\nDatabase initialization complete:")
        print(f"  Added: {added_count} new compounds")
        print(f"  Skipped: {skipped_count} existing compounds")
        print(f"  Total compounds in database: {Liquid.query.count()}")


@app.route('/init_db')
def init_db_route():
    """Route to initialize database (for development/testing)"""
    try:
        init_db()
        return "Database initialized successfully! Check console for details.", 200
    except Exception as e:
        return f"Error initializing database: {str(e)}", 500


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        # Tables already exist in MySQL — no create_all needed
        pass
    app.run(debug=True)