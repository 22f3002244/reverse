from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import SessionLocal
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("auth/register.html")

    db = SessionLocal()
    data = request.form

    existing_user = db.query(User).filter(User.email == data["email"]).first()
    if existing_user:
        flash("Email already registered", "danger")
        return redirect(url_for("auth.register"))

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        phone_no=data.get("phone_no"),
        city=data.get("city"),
        is_lister=False
    )

    db.add(user)
    db.commit()

    flash("Registration successful. Please login.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/business-register", methods=["GET", "POST"])
def business_register():
    if request.method == "GET":
        return render_template("auth/business_register.html")

    db = SessionLocal()
    data = request.form

    existing_user = db.query(User).filter(User.email == data["email"]).first()
    if existing_user:
        flash("Email already registered", "danger")
        return redirect(url_for("auth.business_register"))

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        phone_no=data.get("phone_no"),
        city=data.get("city"),
        org_name=data.get("org_name"),
        is_lister=True
    )

    db.add(user)
    db.commit()

    flash("Business registration successful. Please login.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    db = SessionLocal()
    data = request.form

    user = db.query(User).filter(User.email == data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.login"))

    # TODO: session / JWT (next step)
    flash("Login successful", "success")
    return redirect("/")  # dashboard/home

@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("auth/forgot.html")

    db = SessionLocal()
    email = request.form["email"]

    user = db.query(User).filter(User.email == email).first()
    if not user:
        flash("Email not found", "danger")
        return redirect(url_for("auth.forgot_password"))

    # TODO: send email with reset token
    flash("Password reset link sent (mock)", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/update-password", methods=["GET", "POST"])
def update_password():
    if request.method == "GET":
        return render_template("auth/update.html")

    db = SessionLocal()
    data = request.form

    user = db.query(User).filter(User.email == data["email"]).first()
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("auth.update_password"))

    if data["new_password"] != data["confirm_password"]:
        flash("Passwords do not match", "danger")
        return redirect(url_for("auth.update_password"))

    user.password = generate_password_hash(data["new_password"])
    db.commit()

    flash("Password updated successfully", "success")
    return redirect(url_for("auth.login"))

