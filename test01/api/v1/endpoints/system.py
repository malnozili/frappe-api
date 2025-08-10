import frappe
from frappe import _
from frappe.utils import now_datetime, get_url
from typing import Dict, List, Optional
import json
import platform
import sys


@frappe.whitelist(allow_guest=True)
def health_check() -> Dict:
    """
    System health check endpoint
    
    Returns:
        Dict: System health status
    """
    try:
        # Check database connection
        db_status = "healthy"
        try:
            frappe.db.sql("SELECT 1")
        except Exception:
            db_status = "unhealthy"
        
        # Check Redis connection
        redis_status = "healthy"
        try:
            frappe.cache().ping()
        except Exception:
            redis_status = "unhealthy"
        
        # Get system info
        system_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "frappe_version": "14.0.0",
            "app_version": "1.0.0"
        }
        
        # Overall health
        overall_health = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"
        
        return {
            "success": True,
            "data": {
                "status": overall_health,
                "database": db_status,
                "redis": redis_status,
                "system_info": system_info,
                "timestamp": now_datetime().isoformat()
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in health_check: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def get_system_info() -> Dict:
    """
    Get detailed system information
    
    Returns:
        Dict: System information
    """
    try:
        # Get site info
        site_info = {
            "site_name": frappe.local.site,
            "site_url": get_url(),
            "site_path": frappe.get_site_path()
        }
        
        # Get app info
        apps = frappe.get_all("Installed Application", fields=["app_name", "app_version"])
        app_info = {app.app_name: app.app_version for app in apps}
        
        # Get database info
        db_info = {
            "database_type": frappe.conf.db_type,
            "database_name": frappe.conf.db_name,
            "database_host": frappe.conf.db_host
        }
        
        # Get server info
        server_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor()
        }
        
        return {
            "success": True,
            "data": {
                "site": site_info,
                "apps": app_info,
                "database": db_info,
                "server": server_info,
                "timestamp": now_datetime().isoformat()
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in get_system_info: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def get_api_documentation() -> Dict:
    """
    Get API documentation and available endpoints
    
    Returns:
        Dict: API documentation
    """
    try:
        # Define API endpoints
        endpoints = {
            "authentication": {
                "login": {
                    "method": "POST",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.login",
                    "description": "Authenticate user and get API token",
                    "parameters": {
                        "email": "string (required)",
                        "password": "string (required)"
                    }
                },
                "register": {
                    "method": "POST",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.register_user",
                    "description": "Register a new user",
                    "parameters": {
                        "email": "string (required)",
                        "full_name": "string (required)",
                        "password": "string (required)",
                        "mobile_no": "string (optional)"
                    }
                },
                "logout": {
                    "method": "POST",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.logout",
                    "description": "Logout current user",
                    "authentication": "required"
                }
            },
            "user_management": {
                "get_profile": {
                    "method": "GET",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.get_user_profile",
                    "description": "Get current user profile",
                    "authentication": "required"
                },
                "update_profile": {
                    "method": "PUT",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.update_user_profile",
                    "description": "Update user profile",
                    "parameters": {
                        "full_name": "string (optional)",
                        "mobile_no": "string (optional)"
                    },
                    "authentication": "required"
                },
                "change_password": {
                    "method": "PUT",
                    "endpoint": "/api/method/test01.api.v1.endpoints.user.change_password",
                    "description": "Change user password",
                    "parameters": {
                        "current_password": "string (required)",
                        "new_password": "string (required)"
                    },
                    "authentication": "required"
                }
            },
            "example_data": {
                "get_data": {
                    "method": "GET",
                    "endpoint": "/api/method/test01.api.v1.endpoints.example.get_example_data",
                    "description": "Get example data",
                    "parameters": {
                        "name": "string (optional)"
                    }
                },
                "create_data": {
                    "method": "POST",
                    "endpoint": "/api/method/test01.api.v1.endpoints.example.create_example_data",
                    "description": "Create new example record",
                    "parameters": {
                        "title": "string (required)",
                        "description": "string (optional)"
                    }
                },
                "update_data": {
                    "method": "PUT",
                    "endpoint": "/api/method/test01.api.v1.endpoints.example.update_example_data",
                    "description": "Update example record",
                    "parameters": {
                        "name": "string (required)",
                        "title": "string (optional)",
                        "description": "string (optional)"
                    }
                },
                "delete_data": {
                    "method": "DELETE",
                    "endpoint": "/api/method/test01.api.v1.endpoints.example.delete_example_data",
                    "description": "Delete example record",
                    "parameters": {
                        "name": "string (required)"
                    }
                },
                "search_data": {
                    "method": "GET",
                    "endpoint": "/api/method/test01/api/v1/endpoints/example/search_example_data",
                    "description": "Search example records",
                    "parameters": {
                        "query": "string (required)",
                        "limit": "integer (optional, default: 10)"
                    }
                }
            },
            "system": {
                "health_check": {
                    "method": "GET",
                    "endpoint": "/api/method/test01.api.v1.endpoints.system.health_check",
                    "description": "System health check"
                },
                "system_info": {
                    "method": "GET",
                    "endpoint": "/api/method/test01.api.v1.endpoints.system.get_system_info",
                    "description": "Get system information"
                }
            }
        }
        
        return {
            "success": True,
            "data": {
                "api_version": "v1",
                "base_url": get_url(),
                "endpoints": endpoints,
                "authentication": {
                    "type": "API Key",
                    "header": "Authorization: token api_key:api_secret"
                },
                "response_format": {
                    "success": "boolean",
                    "data": "object/array",
                    "error": "string (if success is false)",
                    "timestamp": "ISO 8601 datetime"
                }
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in get_api_documentation: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist()
def get_error_logs(limit: int = 50) -> Dict:
    """
    Get recent error logs (admin only)
    
    Args:
        limit (int, optional): Number of logs to retrieve (default: 50)
        
    Returns:
        Dict: Error logs
        
    Raises:
        frappe.PermissionError: If user doesn't have admin access
    """
    try:
        # Check admin permissions
        if not frappe.has_permission("System Manager"):
            frappe.throw(_("Insufficient permissions"), frappe.PermissionError)
        
        # Get error logs
        logs = frappe.get_all(
            "Error Log",
            fields=["name", "method", "error", "creation", "seen"],
            limit=limit,
            order_by="creation desc"
        )
        
        return {
            "success": True,
            "data": {
                "logs": logs,
                "count": len(logs)
            },
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in get_error_logs: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }
