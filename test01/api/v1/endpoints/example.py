import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Dict, List, Optional
import json


@frappe.whitelist(allow_guest=True)
def get_example_data(name: str = None) -> Dict:
    """
    Get example data from the system
    
    Args:
        name (str, optional): Name of the specific record to retrieve
        
    Returns:
        Dict: Example data or list of records
        
    Raises:
        frappe.ValidationError: If validation fails
        frappe.DoesNotExistError: If record not found
    """
    try:
        # For testing purposes, return mock data
        mock_data = [
            {
                "name": "example_001",
                "title": "Sample Record 1",
                "description": "This is a sample record for testing",
                "creation": "2024-01-01 00:00:00.000000",
                "modified": "2024-01-01 00:00:00.000000"
            },
            {
                "name": "example_002", 
                "title": "Sample Record 2",
                "description": "Another sample record for testing",
                "creation": "2024-01-01 00:00:00.000000",
                "modified": "2024-01-01 00:00:00.000000"
            }
        ]
        
        if name:
            # Get specific record
            record = next((item for item in mock_data if item["name"] == name), None)
            if not record:
                frappe.throw(_("Record not found"), frappe.DoesNotExistError)
            
            return {
                "success": True,
                "data": record,
                "timestamp": now_datetime().isoformat()
            }
        else:
            # Get all records
            return {
                "success": True,
                "data": mock_data,
                "count": len(mock_data),
                "timestamp": now_datetime().isoformat()
            }
            
    except Exception as e:
        frappe.log_error(f"API Error in get_example_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def create_example_data(title: str, description: str = None) -> Dict:
    """
    Create a new example record
    
    Args:
        title (str): Title of the record
        description (str, optional): Description of the record
        
    Returns:
        Dict: Created record data
        
    Raises:
        frappe.ValidationError: If validation fails
    """
    try:
        # Validate required fields
        if not title:
            frappe.throw(_("Title is required"), frappe.ValidationError)
        
        # For testing purposes, create mock record
        import time
        record_name = f"example_{int(time.time())}"
        
        new_record = {
            "name": record_name,
            "title": title,
            "description": description or "",
            "creation": now_datetime().isoformat(),
            "modified": now_datetime().isoformat()
        }
        
        return {
            "success": True,
            "data": new_record,
            "message": _("Record created successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in create_example_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def update_example_data(name: str, title: str = None, description: str = None) -> Dict:
    """
    Update an existing example record
    
    Args:
        name (str): Name of the record to update
        title (str, optional): New title
        description (str, optional): New description
        
    Returns:
        Dict: Updated record data
        
    Raises:
        frappe.ValidationError: If validation fails
        frappe.DoesNotExistError: If record not found
    """
    try:
        # For testing purposes, simulate update
        if not name:
            frappe.throw(_("Record name is required"), frappe.ValidationError)
        
        # Simulate updated record
        updated_record = {
            "name": name,
            "title": title or "Updated Title",
            "description": description or "Updated Description",
            "creation": "2024-01-01 00:00:00.000000",
            "modified": now_datetime().isoformat()
        }
        
        return {
            "success": True,
            "data": updated_record,
            "message": _("Record updated successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in update_example_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def delete_example_data(name: str) -> Dict:
    """
    Delete an example record
    
    Args:
        name (str): Name of the record to delete
        
    Returns:
        Dict: Deletion confirmation
        
    Raises:
        frappe.ValidationError: If validation fails
        frappe.DoesNotExistError: If record not found
    """
    try:
        # For testing purposes, simulate deletion
        if not name:
            frappe.throw(_("Record name is required"), frappe.ValidationError)
        
        # Simulate successful deletion
        
        return {
            "success": True,
            "message": _("Record deleted successfully"),
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in delete_example_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }


@frappe.whitelist(allow_guest=True)
def search_example_data(query: str, limit: int = 10) -> Dict:
    """
    Search example records by title or description
    
    Args:
        query (str): Search query
        limit (int, optional): Maximum number of results (default: 10)
        
    Returns:
        Dict: Search results
        
    Raises:
        frappe.ValidationError: If validation fails
    """
    try:
        # Validate query
        if not query:
            frappe.throw(_("Search query is required"), frappe.ValidationError)
        
        # For testing purposes, search in mock data
        mock_data = [
            {
                "name": "example_001",
                "title": "Sample Record 1",
                "description": "This is a sample record for testing",
                "creation": "2024-01-01 00:00:00.000000"
            },
            {
                "name": "example_002", 
                "title": "Sample Record 2",
                "description": "Another sample record for testing",
                "creation": "2024-01-01 00:00:00.000000"
            }
        ]
        
        # Simple search in mock data
        results = []
        for item in mock_data:
            if (query.lower() in item["title"].lower() or 
                query.lower() in item["description"].lower()):
                results.append(item)
        
        # Apply limit
        results = results[:limit]
        
        return {
            "success": True,
            "data": results,
            "count": len(results),
            "query": query,
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in search_example_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }
