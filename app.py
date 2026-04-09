from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from getmac import get_mac_address
from extensions import db, bcrypt
from modeles import User, Liquid, UserLog
from forms import RegistrationForm, LoginForm, VerificationForm, AntoineCalculationForm, ForgotPasswordForm, ResetPasswordForm
import re
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'antoine-secret-key-2024'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_SUPPRESS_SEND'] = False  # Enable actual email sending
app.config['MAIL_DEBUG'] = True  # Enable debugging information

mail = Mail(app)

# Initialize Flask-Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day"]
)

# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    """Custom error handler for rate limit exceeded"""
    return render_template('429.html'), 429

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
# Jbed l-URL d connection (Reference l-MYSQL_URL li ghadi n-diro f Railway)
db_url = os.getenv('MYSQL_URL')

if db_url:
    # 1. Beddel mysql:// l mysql+mysqlconnector:// (bach t-khdem b l-driver dyalk)
    # 2. Zid /antoine_data f l-akhir bach i-3ref l-database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace('mysql://', 'mysql+mysqlconnector://').split('?')[0] + '/antoine_data'
else:
    # Hada l-code dyal Local (ila knti k-t-tisti f PC dyalk)
    db_pass = os.getenv('DB_PASSWORD')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{db_pass}@localhost:3306/antoine_data'
db.init_app(app)
bcrypt.init_app(app)
 
 
# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    """Home page - professional landing page"""
    return render_template('index.html')
 
 
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
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
        verification_code = str(random.randint(100000, 999999))
        
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pw,
            verification_code=verification_code
        )
        db.session.add(user)
        db.session.commit()
        
        # Send verification email
        try:
            # Debug: Check mail configuration
            print(f"Mail Server: {app.config['MAIL_SERVER']}")
            print(f"Mail Port: {app.config['MAIL_PORT']}")
            print(f"Mail Username: {app.config['MAIL_USERNAME']}")
            print(f"Recipient: {user.email}")
            
            msg = Message(
                'Email Verification - Antoine Calculator',
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email],
                body=f'''Hello {user.fname},

Thank you for registering! Your verification code is:

{verification_code}

Please enter this code on the verification page to activate your account.

Best regards,
Antoine Calculator Team'''
            )
            
            print("Attempting to send email...")
            mail.send(msg)
            print("Email sent successfully!")
            
            flash('Registration successful! Please check your email for verification code.', 'success')
            return redirect(url_for('verify'))
            
        except Exception as e:
            # Enhanced error logging
            print(f"Email sending failed: {type(e).__name__}: {str(e)}")
            print(f"Error details: {repr(e)}")
            
            # Common Gmail SMTP errors
            if "SMTPAuthenticationError" in str(e):
                error_msg = "Gmail authentication failed. Check your App Password in .env file."
            elif "SMTPRecipientsRefused" in str(e):
                error_msg = "Email address refused. Check recipient email format."
            elif "SMTPServerDisconnected" in str(e):
                error_msg = "SMTP server disconnected. Check internet connection."
            elif "smtplib.SMTPException" in str(e):
                error_msg = "SMTP error. Check Gmail App Password and 2FA settings."
            else:
                error_msg = f"Email sending failed: {str(e)}"
            
            flash(f'Registration saved but {error_msg}', 'warning')
            return redirect(url_for('verify'))

    return render_template('register.html', form=form)


@app.route('/verify', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def verify():
    """Verify user email with OTP code"""
    if current_user.is_authenticated and current_user.is_verified:
        return redirect(url_for('calculator'))
    
    form = VerificationForm()
    if form.validate_on_submit():
        # Find user by verification code
        user = User.query.filter_by(verification_code=form.verification_code.data).first()
        
        if user:
            user.is_verified = True
            user.verification_code = None  # Clear the verification code
            db.session.commit()
            
            flash('Email verified successfully! Please login to continue.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code. Please try again.', 'error')
    
    return render_template('verify.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calculator'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            ip_address = get_remote_address()
            mac_address = get_mac_address(ip=request.remote_addr, network_request=True)
            username_attempted = form.username.data
            
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                if not user.is_verified:
                    # Log failed attempt due to unverified email
                    log_entry = UserLog(
                        user_id=user.id,
                        ip_address=ip_address,
                        mac_address=mac_address,
                        action='Login Failed - Email Not Verified'
                    )
                    db.session.add(log_entry)
                    db.session.commit()
                    
                    flash('Please verify your email before logging in. Check your inbox for the verification code.', 'warning')
                    return redirect(url_for('verify'))
                
                # Log successful login
                log_entry = UserLog(
                    user_id=user.id,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action='Login Success'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                login_user(user)
                flash(f'Welcome back, {user.fname}!', 'success')
                return redirect(url_for('home'))
            else:
                # Determine specific failure reason for better logging
                if user:
                    # User exists but password is wrong
                    action = 'Login Failed - Wrong Password'
                else:
                    # User doesn't exist
                    action = f'Login Failed - User Not Found (Username: {username_attempted})'
                
                # Log failed attempt
                log_entry = UserLog(
                    user_id=user.id if user else None,  # None if user doesn't exist
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action=action
                )
                db.session.add(log_entry)
                db.session.commit()
                
                flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
        except Exception as e:
            # Log system error
            log_entry = UserLog(
                user_id=None,
                ip_address=get_remote_address(),
                mac_address=get_mac_address(ip=request.remote_addr, network_request=True),
                action=f'Login Failed - System Error (Username: {form.username.data})'
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('Login failed. Please try again.', 'error')

    return render_template('login.html', form=form)
 
 
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/forgot-password', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def forgot_password():
    """Handle forgot password requests"""
    if current_user.is_authenticated:
        return redirect(url_for('calculator'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            ip_address = get_remote_address()
            mac_address = get_mac_address(ip=request.remote_addr, network_request=True)
            
            if user:
                # Generate 6-digit reset code
                reset_code = str(random.randint(100000, 999999))
                reset_expiration = datetime.utcnow() + timedelta(minutes=10)
                
                # Update user record
                user.reset_code = reset_code
                user.reset_expiration = reset_expiration
                db.session.commit()
                
                # Log password reset request
                log_entry = UserLog(
                    user_id=user.id,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action='Password Reset Requested'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                # Send reset email
                msg = Message(
                    'Password Reset Code - Antoine Calculator',
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[user.email],
                    body=f'''Hello {user.fname},

You requested to reset your password. Your reset code is:

{reset_code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Antoine Calculator Team'''
                )
                mail.send(msg)
                
                flash('Password reset code has been sent to your email. Please check your inbox.', 'success')
                return redirect(url_for('reset_password'))
            else:
                # Log attempt with non-existent email
                log_entry = UserLog(
                    user_id=None,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action=f'Password Reset Attempt - Email Not Found: {form.email.data}'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                # Don't reveal if email exists or not
                flash('If an account with that email exists, a reset code has been sent.', 'info')
                return redirect(url_for('reset_password'))
                
        except Exception as e:
            flash('An error occurred. Please try again later.', 'error')
    
    return render_template('forgot_password.html', form=form)


@app.route('/reset-password', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def reset_password():
    """Handle password reset with code verification"""
    if current_user.is_authenticated:
        return redirect(url_for('calculator'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            ip_address = get_remote_address()
            mac_address = get_mac_address(ip=request.remote_addr, network_request=True)
            
            # Find user by reset code
            user = User.query.filter_by(reset_code=form.reset_code.data).first()
            
            if user and user.reset_expiration and user.reset_expiration > datetime.utcnow():
                # Code is valid and not expired
                # Hash new password
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                
                # Update user record
                user.password_hash = hashed_password
                user.is_verified = True  # Auto-verify email since user accessed reset via email
                user.reset_code = None  # Clear reset code
                user.reset_expiration = None  # Clear expiration
                db.session.commit()
                
                # Log successful password reset
                log_entry = UserLog(
                    user_id=user.id,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action='Password Reset Successful - Auto Verified'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                # Auto-login user and redirect to calculator
                login_user(user)
                flash('Your password has been successfully reset and your account is now verified! Welcome back!', 'success')
                return redirect(url_for('calculator'))
                
            elif user and user.reset_expiration and user.reset_expiration <= datetime.utcnow():
                # Code exists but expired
                # Log expired code attempt
                log_entry = UserLog(
                    user_id=user.id,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action='Password Reset Failed - Code Expired'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                flash('The reset code has expired. Please request a new one.', 'error')
                
            else:
                # Invalid code
                # Log invalid code attempt
                log_entry = UserLog(
                    user_id=None,
                    ip_address=ip_address,
                    mac_address=mac_address,
                    action=f'Password Reset Failed - Invalid Code: {form.reset_code.data}'
                )
                db.session.add(log_entry)
                db.session.commit()
                
                flash('Invalid reset code. Please check your email and try again.', 'error')
                
        except Exception as e:
            # Log system error
            log_entry = UserLog(
                user_id=None,
                ip_address=get_remote_address(),
                mac_address=get_mac_address(ip=request.remote_addr, network_request=True),
                action='Password Reset Failed - System Error'
            )
            db.session.add(log_entry)
            db.session.commit()
            
            flash('An error occurred. Please try again later.', 'error')
    
    return render_template('reset_password.html', form=form)
 
 
@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    """Calculator page with Antoine equation form - only for verified users"""
    if not current_user.is_verified:
        flash('Please verify your email to access the calculator.', 'warning')
        return redirect(url_for('verify'))
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

    # Extract vapor_pressure from result if available
    vapor_pressure = None
    if result and 'P_mmHg' in result:
        vapor_pressure = result['P_mmHg']
    
    return render_template('antoine.html', form=form, result=result,
                           selected_liquid=selected_liquid,
                           vapor_pressure=vapor_pressure,
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
    
    # Extract vapor_pressure from result if available
    vapor_pressure = None
    if result and 'P_mmHg' in result:
        vapor_pressure = result['P_mmHg']
    
    return render_template('results.html', result=result, selected_liquid=selected_liquid, vapor_pressure=vapor_pressure)
 
 
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    with app.app_context():
        # Tables already exist in MySQL — no create_all needed
        pass
    app.run(debug=True)