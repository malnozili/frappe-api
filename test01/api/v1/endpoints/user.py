import frappe
from frappe import _
from frappe.utils import now_datetime, get_url
from typing import Dict, List, Optional
import json


@frappe.whitelist(allow_guest=True)
def login(email: str, password: str) -> Dict:
    """
    Authenticate user and return session token
    
    Args:
        email (str): User email
        password (str): User password
        
    Returns:
        Dict: Authentication result with token
        
    Raises:
        frappe.AuthenticationError: If authentication fails
    """
    try:
        # Validate required fields
        if not email or not password:
            frappe.throw(_("Email and password are required"), frappe.ValidationError)
        
        # Authenticate user
        try:
            frappe.local.login_manager.authenticate(email, password)
            user = frappe.get_doc("User", frappe.session.user)
        except Exception as auth_error:
            frappe.throw(_("Invalid email or password"), frappe.AuthenticationError)
        
        # Generate API key for the user
        api_key = frappe.generate_hash()
        api_secret = frappe.generate_hash()
        
        # Create or update API key
        if frappe.db.exists("API Key", {"user": user.name}):
            api_key_doc = frappe.get_doc("API Key", {"user": user.name})
            api_key_doc.api_key = api_key
            api_key_doc.api_secret = api_secret
            api_key_doc.save()
        else:
            api_key_doc = frappe.new_doc("API Key")
            api_key_doc.user = user.name
            api_key_doc.api_key = api_key
            api_key_doc.api_secret = api_secret
            api_key_doc.insert()
        
        return {
            "success": True,
            "message": _("Login successful"),
            "data": {
                "user": user.name,
                "full_name": user.full_name,
                "api_key": api_key,
                "api_secret": api_secret
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in login: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def get_user_profile() -> Dict:
    """
    Get current user profile information
    
    Returns:
        Dict: User profile data
        
    Raises:
        frappe.AuthenticationError: If user not authenticated
    """
    try:
        user = frappe.get_doc("User", frappe.session.user)
        
        return {
            "success": True,
            "data": {
                "name": user.name,
                "full_name": user.full_name,
                "email": user.email,
                "mobile_no": user.mobile_no,
                "user_image": user.user_image,
                "last_active": user.last_active,
                "last_known_versions": user.last_known_versions
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in get_user_profile: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def update_user_profile(full_name: str = None, mobile_no: str = None) -> Dict:
    """
    Update current user profile
    
    Args:
        full_name (str, optional): New full name
        mobile_no (str, optional): New mobile number
        
    Returns:
        Dict: Updated profile data
        
    Raises:
        frappe.AuthenticationError: If user not authenticated
        frappe.ValidationError: If validation fails
    """
    try:
        user = frappe.get_doc("User", frappe.session.user)
        
        if full_name is not None:
            user.full_name = full_name
        if mobile_no is not None:
            user.mobile_no = mobile_no
            
        user.save()
        
        return {
            "success": True,
            "data": {
                "name": user.name,
                "full_name": user.full_name,
                "email": user.email,
                "mobile_no": user.mobile_no,
                "user_image": user.user_image
            },
            "message": _("Profile updated successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in update_user_profile: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def change_password(current_password: str, new_password: str) -> Dict:
    """
    Change user password
    
    Args:
        current_password (str): Current password
        new_password (str): New password
        
    Returns:
        Dict: Password change confirmation
        
    Raises:
        frappe.AuthenticationError: If current password is incorrect
        frappe.ValidationError: If validation fails
    """
    try:
        # Validate required fields
        if not current_password or not new_password:
            frappe.throw(_("Current password and new password are required"), frappe.ValidationError)
        
        # Verify current password
        user = frappe.get_doc("User", frappe.session.user)
        if not user.check_password(current_password):
            frappe.throw(_("Current password is incorrect"), frappe.AuthenticationError)
        
        # Update password
        user.new_password = new_password
        user.save()
        
        return {
            "success": True,
            "message": _("Password changed successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in change_password: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def logout() -> Dict:
    """
    Logout current user and invalidate session
    
    Returns:
        Dict: Logout confirmation
    """
    try:
        # Clear session
        frappe.local.login_manager.logout()
        
        return {
            "success": True,
            "message": _("Logged out successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in logout: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def register_user(email: str, full_name: str, password: str, mobile_no: str = None) -> Dict:
    """
    Register a new user
    
    Args:
        email (str): User email
        full_name (str): User full name
        password (str): User password
        mobile_no (str, optional): User mobile number
        
    Returns:
        Dict: Registration result
        
    Raises:
        frappe.ValidationError: If validation fails
    """
    try:
        # Validate required fields
        if not email or not full_name or not password:
            frappe.throw(_("Email, full name, and password are required"), frappe.ValidationError)
        
        # Check if user already exists
        if frappe.db.exists("User", {"email": email}):
            frappe.throw(_("User with this email already exists"), frappe.ValidationError)
        
        # Create new user
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = full_name.split()[0] if full_name else ""
        user.last_name = " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else ""
        user.full_name = full_name
        user.mobile_no = mobile_no
        user.new_password = password
        user.send_welcome_email = 0
        user.insert()
        
        return {
            "success": True,
            "message": _("User registered successfully"),
            "data": {
                "name": user.name,
                "email": user.email,
                "full_name": user.full_name
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in register_user: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }
