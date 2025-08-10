import frappe
from frappe import _


def get_context(context):
    """Get context for API documentation page"""
    context.title = _("API Documentation")
    context.breadcrumbs = [
        {"label": _("Home"), "route": "/"},
        {"label": _("API Documentation"), "route": "/api-docs"}
    ]
    
    # Get API information
    context.api_info = {
        "title": "test01 App API",
        "version": "v1.0.0",
        "description": "REST API for the test01 Frappe application",
        "base_url": frappe.utils.get_url(),
        "swagger_url": frappe.utils.get_url("/assets/test01/swagger.json"),
        "swagger_ui_url": frappe.utils.get_url("/assets/test01/swagger.html")
    }
    
    # Get available endpoints
    try:
        from test01.api.v1.router import api_router
        context.endpoints = api_router.endpoints
    except ImportError:
        context.endpoints = {}
    
    return context
