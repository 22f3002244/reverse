from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database import SessionLocal
from models import User
from services.otp_service import create_otp, verify_otp, mask_contact, get_otp_details

user_bp = Blueprint("user", __name__, url_prefix="/user")

# Mock current user (in production, use Flask-Login or JWT)
def get_current_user():
    """Get current user from session (mock implementation)"""
    # In production, replace with: return current_user from Flask-Login
    user_id = session.get('user_id')
    if not user_id:
        return None
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    return user

@user_bp.route("/change-email", methods=["GET", "POST"])
def change_email():
    """Display form to change email address"""
    user = get_current_user()
    if not user:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))
    
    if request.method == "GET":
        return render_template("auth/change-email.html", user=user)
    
    # POST request - validate and send OTP
    db = SessionLocal()
    data = request.form
    password = data.get("password")
    new_email = data.get("email")
    
    # Validate password
    if not check_password_hash(user.password, password):
        flash("Invalid password", "danger")
        return redirect(url_for("user.change_email"))
    
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == new_email,
        User.id != user.id
    ).first()
    
    if existing_user:
        flash("Email already registered", "danger")
        return redirect(url_for("user.change_email"))
    
    # Generate OTP
    otp_code = create_otp(user.id, 'email', new_email)
    
    # TODO: Send OTP via email (implement email service)
    print(f"[Mock] OTP for {new_email}: {otp_code}")
    
    # Store the new email in session temporarily
    session['pending_email'] = new_email
    session['otp_type'] = 'email'
    session.modified = True
    
    flash("OTP sent to your new email address", "info")
    return redirect(url_for("user.verify_otp_view", change_type='email'))

@user_bp.route("/change-phone", methods=["GET", "POST"])
def change_phone():
    """Display form to change phone number"""
    user = get_current_user()
    if not user:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))
    
    if request.method == "GET":
        return render_template("auth/change-contact.html", user=user)
    
    # POST request - validate and send OTP
    db = SessionLocal()
    data = request.form
    password = data.get("password")
    new_phone = data.get("phone")
    
    # Validate password
    if not check_password_hash(user.password, password):
        flash("Invalid password", "danger")
        return redirect(url_for("user.change_phone"))
    
    # Generate OTP
    otp_code = create_otp(user.id, 'phone', new_phone)
    
    # TODO: Send OTP via SMS (implement SMS service)
    print(f"[Mock] OTP for {new_phone}: {otp_code}")
    
    # Store the new phone in session temporarily
    session['pending_phone'] = new_phone
    session['otp_type'] = 'phone'
    session.modified = True
    
    flash("OTP sent to your new phone number", "info")
    return redirect(url_for("user.verify_otp_view", change_type='phone'))

@user_bp.route("/verify-otp/<change_type>", methods=["GET", "POST"])
def verify_otp_view(change_type):
    """Verify OTP for email or phone change"""
    user = get_current_user()
    if not user:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))
    
    if request.method == "GET":
        # Get OTP details for display
        otp_data = get_otp_details(user.id)
        
        if not otp_data:
            flash("OTP not found. Please request a new one.", "danger")
            return redirect(url_for("user.change_email" if change_type == 'email' else "user.change_phone"))
        
        masked_value = mask_contact(otp_data['contact_value'], otp_data['contact_type'])
        
        return render_template(
            "auth/otp.html",
            change_type=change_type,
            verification_type=otp_data['contact_type'],
            masked_target=masked_value
        )
    
    # POST request - verify OTP and update user
    db = SessionLocal()
    data = request.form
    
    # Combine OTP from form fields
    otp_code = data.get('o1', '') + data.get('o2', '') + data.get('o3', '') + \
               data.get('o4', '') + data.get('o5', '') + data.get('o6', '')
    
    # Verify OTP
    success, message, contact_data = verify_otp(user.id, otp_code)
    
    if not success:
        flash(message, "danger")
        return redirect(url_for("user.verify_otp_view", change_type=change_type))
    
    # Update user with new contact information
    if contact_data['contact_type'] == 'email':
        user.email = contact_data['contact_value']
    elif contact_data['contact_type'] == 'phone':
        user.phone_no = contact_data['contact_value']
    
    db.commit()
    
    # Clear session data
    session.pop('pending_email', None)
    session.pop('pending_phone', None)
    session.pop('otp_type', None)
    session.modified = True
    
    field_name = "Email" if contact_data['contact_type'] == 'email' else "Phone Number"
    flash(f"{field_name} updated successfully!", "success")
    return redirect("/settings")  # Redirect to settings page

@user_bp.route("/resend-otp/<change_type>", methods=["GET"])
def resend_otp_view(change_type):
    """Resend OTP"""
    user = get_current_user()
    if not user:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))
    
    otp_data = get_otp_details(user.id)
    if not otp_data:
        flash("Please initiate the change request again", "danger")
        return redirect(url_for(
            "user.change_email" if change_type == 'email' else "user.change_phone"
        ))
    
    # Generate new OTP
    new_otp = create_otp(user.id, otp_data['contact_type'], otp_data['contact_value'])
    
    # TODO: Send new OTP via email/SMS
    print(f"[Mock] Resent OTP for {otp_data['contact_value']}: {new_otp}")
    
    flash("OTP has been resent", "info")
    return redirect(url_for("user.verify_otp_view", change_type=change_type))

@user_bp.route("/settings", methods=["GET"])
def settings():
    """Display user settings page"""
    user = get_current_user()
    if not user:
        flash("Please login first", "danger")
        return redirect(url_for("auth.login"))
    
    return render_template("user/settings.html", user=user)

# Old endpoint - kept for backward compatibility
@user_bp.get("/<int:user_id>")
def get_user(user_id):
    db = SessionLocal()
    user = db.query(User).get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": f"{user.first_name} {user.last_name}",
        "email": user.email
    })
