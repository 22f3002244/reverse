import random
import string
from datetime import datetime, timedelta

# In-memory OTP storage (in production, use Redis or database)
otp_store = {}

def generate_otp(length=6):
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=length))

def create_otp(user_id, contact_type, contact_value):
    """
    Create and store an OTP for a user
    contact_type: 'email' or 'phone'
    contact_value: the email or phone to verify
    """
    otp_code = generate_otp()
    expiry_time = datetime.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
    
    otp_store[user_id] = {
        'otp': otp_code,
        'contact_type': contact_type,
        'contact_value': contact_value,
        'expiry': expiry_time,
        'attempts': 0,
        'max_attempts': 3
    }
    
    return otp_code

def verify_otp(user_id, otp_code):
    """
    Verify the OTP for a user
    Returns: (success, message, otp_data)
    """
    if user_id not in otp_store:
        return False, "OTP not found. Please request a new one.", None
    
    otp_data = otp_store[user_id]
    
    # Check expiry
    if datetime.now() > otp_data['expiry']:
        del otp_store[user_id]
        return False, "OTP has expired. Please request a new one.", None
    
    # Check attempts
    if otp_data['attempts'] >= otp_data['max_attempts']:
        del otp_store[user_id]
        return False, "Maximum attempts exceeded. Please request a new OTP.", None
    
    # Verify OTP
    if otp_data['otp'] == otp_code:
        # OTP is correct, remove it from store
        contact_data = {
            'contact_type': otp_data['contact_type'],
            'contact_value': otp_data['contact_value']
        }
        del otp_store[user_id]
        return True, "OTP verified successfully!", contact_data
    else:
        # Wrong OTP, increment attempts
        otp_data['attempts'] += 1
        remaining = otp_data['max_attempts'] - otp_data['attempts']
        return False, f"Invalid OTP. {remaining} attempts remaining.", None

def get_otp_details(user_id):
    """Get OTP details for a user (for display purposes)"""
    if user_id not in otp_store:
        return None
    return otp_store[user_id]

def mask_contact(contact_value, contact_type):
    """Mask email or phone for display"""
    if contact_type == 'email':
        # john.doe@example.com -> jo***@example.com
        parts = contact_value.split('@')
        username = parts[0]
        masked = username[:2] + '***' + '@' + parts[1]
        return masked
    elif contact_type == 'phone':
        # +91 98765 43210 -> +91 ****43210
        return contact_value[:4] + '****' + contact_value[-5:]
    return contact_value
