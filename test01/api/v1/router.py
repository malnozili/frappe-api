import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Dict, Any
import json


class APIRouter:
    """Main API router for handling requests and authentication"""
    
    def __init__(self):
        self.endpoints = {
            # Authentication endpoints
            "auth": {
                "login": "test01.api.v1.endpoints.user.login",
                "register": "test01.api.v1.endpoints.user.register_user",
                "logout": "test01.api.v1.endpoints.user.logout"
            },
            # User management endpoints
            "user": {
                "profile": "test01.api.v1.endpoints.user.get_user_profile",
                "update_profile": "test01.api.v1.endpoints.user.update_user_profile",
                "change_password": "test01.api.v1.endpoints.user.change_password"
            },
            # Example data endpoints
            "example": {
                "get": "test01.api.v1.endpoints.example.get_example_data",
                "create": "test01.api.v1.endpoints.example.create_example_data",
                "update": "test01.api.v1.endpoints.example.update_example_data",
                "delete": "test01.api.v1.endpoints.example.delete_example_data",
                "search": "test01.api.v1.endpoints.example.search_example_data"
            },
            # System endpoints
            "system": {
                "health": "test01.api.v1.endpoints.system.health_check",
                "info": "test01.api.v1.endpoints.system.get_system_info",
                "docs": "test01.api.v1.endpoints.system.get_api_documentation",
                "logs": "test01.api.v1.endpoints.system.get_error_logs"
            }
        }
    
    def route_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
        """
        Route API request to appropriate endpoint
        
        Args:
            endpoint (str): API endpoint path
            method (str): HTTP method
            data (Dict): Request data
            
        Returns:
            Dict: API response
        """
        try:
            # Parse endpoint path
            parts = endpoint.strip("/").split("/")
            
            if len(parts) < 2:
                return self._error_response("Invalid endpoint path")
            
            category = parts[0]
            action = parts[1]
            
            # Validate endpoint exists
            if category not in self.endpoints or action not in self.endpoints[category]:
                return self._error_response(f"Endpoint not found: {endpoint}")
            
            # Get method path
            method_path = self.endpoints[category][action]
            
            # Handle authentication for protected endpoints
            if not self._is_public_endpoint(category, action):
                auth_result = self._authenticate_request()
                if not auth_result["success"]:
                    return auth_result
            
            # Execute method
            if data:
                result = frappe.call(method_path, **data)
            else:
                result = frappe.call(method_path)
            
            return result
            
        except Exception as e:
            frappe.log_error(f"API Router Error: {str(e)}")
            return self._error_response(str(e))
    
    def _is_public_endpoint(self, category: str, action: str) -> bool:
        """Check if endpoint is public (no authentication required)"""
        public_endpoints = {
            "auth": ["login", "register"],
            "system": ["health", "info"]
        }
        
        return category in public_endpoints and action in public_endpoints[category]
    
    def _authenticate_request(self) -> Dict:
        """Authenticate API request using API key"""
        try:
            # Get authorization header
            auth_header = frappe.request.headers.get("Authorization")
            
            if not auth_header or not auth_header.startswith("token "):
                return self._error_response("Missing or invalid authorization header", 401)
            
            # Extract API key and secret
            token = auth_header.replace("token ", "")
            if ":" not in token:
                return self._error_response("Invalid token format", 401)
            
            api_key, api_secret = token.split(":", 1)
            
            # Validate API key
            if not frappe.db.exists("API Key", {"api_key": api_key, "api_secret": api_secret}):
                return self._error_response("Invalid API credentials", 401)
            
            # Get user from API key
            api_key_doc = frappe.get_doc("API Key", {"api_key": api_key})
            
            # Set user in session
            frappe.set_user(api_key_doc.user)
            
            return {"success": True}
            
        except Exception as e:
            frappe.log_error(f"Authentication Error: {str(e)}")
            return self._error_response("Authentication failed", 401)
    
    def _error_response(self, message: str, status_code: int = 400) -> Dict:
        """Generate error response"""
        return {
            "success": False,
            "error": message,
            "status_code": status_code,
            "timestamp": now_datetime().isoformat()
        }


# Global router instance
api_router = APIRouter()


@frappe.whitelist(allow_guest=True)
def handle_api_request(endpoint: str, method: str = "GET", data: str = None) -> Dict:
    """
    Main API request handler
    
    Args:
        endpoint (str): API endpoint path
        method (str): HTTP method
        data (str): JSON string of request data
        
    Returns:
        Dict: API response
    """
    try:
        # Parse data if provided
        parsed_data = None
        if data:
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Invalid JSON data",
                    "timestamp": now_datetime().isoformat()
                }
        
        # Route request
        return api_router.route_request(endpoint, method, parsed_data)
        
    except Exception as e:
        frappe.log_error(f"API Request Handler Error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def get_available_endpoints() -> Dict:
    """
    Get list of available API endpoints
    
    Returns:
        Dict: Available endpoints
    """
    try:
        return {
            "success": True,
            "data": {
                "endpoints": api_router.endpoints,
                "base_url": frappe.utils.get_url(),
                "api_version": "v1"
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in get_available_endpoints: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }
