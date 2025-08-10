import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Dict, List, Optional, Any
import json


def create_api_response(success: bool = True, data: Any = None, message: str = None, error: str = None) -> Dict:
    """
    Create standardized API response
    
    Args:
        success (bool): Whether the operation was successful
        data (Any): Response data
        message (str): Success message
        error (str): Error message
        
    Returns:
        Dict: Standardized API response
    """
    response = {
        "success": success,
        "timestamp": now_datetime().isoformat()
    }
    
    if success:
        if data is not None:
            response["data"] = data
        if message:
            response["message"] = message
    else:
        if error:
            response["error"] = error
    
    return response


def validate_required_fields(data: Dict, required_fields: List[str]) -> None:
    """
    Validate that required fields are present in request data
    
    Args:
        data (Dict): Request data
        required_fields (List[str]): List of required field names
        
    Raises:
        frappe.ValidationError: If required fields are missing
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        frappe.throw(_("Missing required fields: {0}").format(", ".join(missing_fields)), frappe.ValidationError)


def validate_permissions(doctype: str, permission: str = "read") -> None:
    """
    Validate user permissions for a doctype
    
    Args:
        doctype (str): Document type name
        permission (str): Permission to check (read, write, create, delete)
        
    Raises:
        frappe.PermissionError: If user doesn't have required permission
    """
    if not frappe.has_permission(doctype, permission):
        frappe.throw(_("Insufficient permissions for {0}").format(doctype), frappe.PermissionError)


def sanitize_data(data: Dict, allowed_fields: List[str]) -> Dict:
    """
    Sanitize data by keeping only allowed fields
    
    Args:
        data (Dict): Input data
        allowed_fields (List[str]): List of allowed field names
        
    Returns:
        Dict: Sanitized data
    """
    return {key: value for key, value in data.items() if key in allowed_fields}


def paginate_results(results: List, page: int = 1, page_size: int = 20) -> Dict:
    """
    Paginate results
    
    Args:
        results (List): List of results to paginate
        page (int): Page number (1-based)
        page_size (int): Number of items per page
        
    Returns:
        Dict: Paginated results with metadata
    """
    total = len(results)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_results = results[start_idx:end_idx]
    
    return {
        "data": paginated_results,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": end_idx < total,
            "has_prev": page > 1
        }
    }


def log_api_request(endpoint: str, method: str, user: str = None, status: str = "success", error: str = None) -> None:
    """
    Log API request for monitoring and debugging
    
    Args:
        endpoint (str): API endpoint
        method (str): HTTP method
        user (str): User making the request
        status (str): Request status (success, error)
        error (str): Error message if any
    """
    try:
        log_data = {
            "endpoint": endpoint,
            "method": method,
            "user": user or frappe.session.user,
            "status": status,
            "timestamp": now_datetime(),
            "ip_address": frappe.local.request_ip,
            "user_agent": frappe.request.headers.get("User-Agent", "")
        }
        
        if error:
            log_data["error"] = error
        
        # Create API Log entry
        api_log = frappe.new_doc("API Log")
        api_log.update(log_data)
        api_log.insert(ignore_permissions=True)
        
    except Exception as e:
        # Fallback to error log if API Log doctype doesn't exist
        frappe.log_error(f"API Request Logging Error: {str(e)}")


def handle_api_exception(func):
    """
    Decorator to handle API exceptions and return standardized responses
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except frappe.ValidationError as e:
            return create_api_response(success=False, error=str(e))
        except frappe.PermissionError as e:
            return create_api_response(success=False, error=str(e))
        except frappe.DoesNotExistError as e:
            return create_api_response(success=False, error=str(e))
        except Exception as e:
            frappe.log_error(f"API Error in {func.__name__}: {str(e)}")
            return create_api_response(success=False, error="Internal server error")
    
    return wrapper


def get_api_rate_limit_key(user: str, endpoint: str) -> str:
    """
    Generate rate limit key for API requests
    
    Args:
        user (str): User identifier
        endpoint (str): API endpoint
        
    Returns:
        str: Rate limit key
    """
    return f"api_rate_limit:{user}:{endpoint}"


def check_rate_limit(user: str, endpoint: str, max_requests: int = 100, window: int = 3600) -> bool:
    """
    Check if user has exceeded rate limit for an endpoint
    
    Args:
        user (str): User identifier
        endpoint (str): API endpoint
        max_requests (int): Maximum requests allowed
        window (int): Time window in seconds
        
    Returns:
        bool: True if within rate limit, False otherwise
    """
    try:
        key = get_api_rate_limit_key(user, endpoint)
        current_count = frappe.cache().get_value(key, 0)
        
        if current_count >= max_requests:
            return False
        
        # Increment counter
        frappe.cache().set_value(key, current_count + 1, expires_in_sec=window)
        return True
        
    except Exception:
        # If rate limiting fails, allow the request
        return True


def generate_api_key(user: str) -> Dict[str, str]:
    """
    Generate new API key and secret for a user
    
    Args:
        user (str): User identifier
        
    Returns:
        Dict: API key and secret
    """
    api_key = frappe.generate_hash()
    api_secret = frappe.generate_hash()
    
    # Create or update API key
    if frappe.db.exists("API Key", {"user": user}):
        api_key_doc = frappe.get_doc("API Key", {"user": user})
        api_key_doc.api_key = api_key
        api_key_doc.api_secret = api_secret
        api_key_doc.save()
    else:
        api_key_doc = frappe.new_doc("API Key")
        api_key_doc.user = user
        api_key_doc.api_key = api_key
        api_key_doc.api_secret = api_secret
        api_key_doc.insert()
    
    return {
        "api_key": api_key,
        "api_secret": api_secret
    }


def validate_api_key(api_key: str, api_secret: str) -> Optional[str]:
    """
    Validate API key and secret
    
    Args:
        api_key (str): API key
        api_secret (str): API secret
        
    Returns:
        Optional[str]: User identifier if valid, None otherwise
    """
    try:
        if frappe.db.exists("API Key", {"api_key": api_key, "api_secret": api_secret}):
            api_key_doc = frappe.get_doc("API Key", {"api_key": api_key})
            return api_key_doc.user
        return None
    except Exception:
        return None
