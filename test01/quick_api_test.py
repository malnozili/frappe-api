#!/usr/bin/env python3
"""
Quick API Test Script for test01 App

This script provides quick testing of individual API endpoints.
Usage: python quick_api_test.py [endpoint_name]
"""

import frappe
import sys
import json
from typing import Dict, Any


def test_health_check():
    """Test health check endpoint"""
    print("Testing Health Check...")
    try:
        result = frappe.call("test01.api.v1.endpoints.system.health_check")
        if result.get("success"):
            print("✅ Health check passed")
            health_data = result.get("data", {})
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Database: {health_data.get('database', 'unknown')}")
            print(f"   Redis: {health_data.get('redis', 'unknown')}")
        else:
            print(f"❌ Health check failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Health check exception: {str(e)}")


def test_system_info():
    """Test system info endpoint"""
    print("Testing System Info...")
    try:
        result = frappe.call("test01.api.v1.endpoints.system.get_system_info")
        if result.get("success"):
            print("✅ System info retrieved")
            data = result.get("data", {})
            print(f"   Site: {data.get('site_info', {}).get('site_name', 'unknown')}")
            print(f"   Python: {data.get('server_info', {}).get('python_version', 'unknown')[:20]}...")
        else:
            print(f"❌ System info failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ System info exception: {str(e)}")


def test_example_data():
    """Test example data endpoints"""
    print("Testing Example Data...")
    
    # Get all data
    try:
        result = frappe.call("test01.api.v1.endpoints.example.get_example_data")
        if result.get("success"):
            data = result.get("data", [])
            print(f"✅ Retrieved {len(data)} example records")
        else:
            print(f"❌ Get example data failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Get example data exception: {str(e)}")
    
    # Create test record
    try:
        result = frappe.call("test01.api.v1.endpoints.example.create_example_data",
                           title="Quick Test Record",
                           description="Created by quick test script")
        if result.get("success"):
            print("✅ Created test record")
            record_name = result.get("data", {}).get("name")
            if record_name:
                print(f"   Record name: {record_name}")
        else:
            print(f"❌ Create record failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Create record exception: {str(e)}")
    
    # Search data
    try:
        result = frappe.call("test01.api.v1.endpoints.example.search_example_data",
                           query="test",
                           limit=5)
        if result.get("success"):
            data = result.get("data", [])
            print(f"✅ Search found {len(data)} results")
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Search exception: {str(e)}")


def test_user_registration():
    """Test user registration"""
    print("Testing User Registration...")
    try:
        result = frappe.call("test01.api.v1.endpoints.user.register_user",
                           email="quick_test@example.com",
                           full_name="Quick Test User",
                           password="TestPassword123!",
                           mobile_no="+1234567890")
        if result.get("success"):
            print("✅ User registered successfully")
        else:
            print(f"❌ Registration failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Registration exception: {str(e)}")


def test_user_login():
    """Test user login"""
    print("Testing User Login...")
    try:
        result = frappe.call("test01.api.v1.endpoints.user.login",
                           email="quick_test@example.com",
                           password="TestPassword123!")
        if result.get("success"):
            print("✅ Login successful")
            login_data = result.get("data", {})
            if login_data.get("api_key"):
                print("   API key generated")
        else:
            print(f"❌ Login failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Login exception: {str(e)}")


def test_router():
    """Test router functionality"""
    print("Testing Router...")
    try:
        from api.v1.router import api_router
        
        # Test valid endpoint
        result = api_router.route_request("system/health", "GET")
        if result.get("success"):
            print("✅ Router valid endpoint test passed")
        else:
            print(f"❌ Router valid endpoint failed: {result.get('error', 'Unknown error')}")
        
        # Test invalid endpoint
        result = api_router.route_request("invalid/endpoint", "GET")
        if not result.get("success"):
            print("✅ Router invalid endpoint test passed")
        else:
            print("❌ Router should have rejected invalid endpoint")
            
    except Exception as e:
        print(f"❌ Router test exception: {str(e)}")


def test_api_documentation():
    """Test API documentation endpoint"""
    print("Testing API Documentation...")
    try:
        result = frappe.call("test01.api.v1.endpoints.system.get_api_documentation")
        if result.get("success"):
            print("✅ API documentation retrieved")
            data = result.get("data", {})
            endpoints = data.get("endpoints", [])
            print(f"   Found {len(endpoints)} documented endpoints")
        else:
            print(f"❌ API documentation failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ API documentation exception: {str(e)}")


def list_endpoints():
    """List all available endpoints"""
    print("Available Endpoints:")
    print("=" * 50)
    
    try:
        from api.v1.router import api_router
        
        for category, endpoints in api_router.endpoints.items():
            print(f"\n{category.upper()}:")
            for endpoint, path in endpoints.items():
                print(f"  - {endpoint}: {path}")
                
    except Exception as e:
        print(f"❌ Failed to list endpoints: {str(e)}")


def show_help():
    """Show help information"""
    print("Quick API Test Script")
    print("=" * 50)
    print("Usage: python quick_api_test.py [endpoint]")
    print("\nAvailable endpoints:")
    print("  health        - Test health check")
    print("  system        - Test system info")
    print("  example       - Test example data operations")
    print("  register      - Test user registration")
    print("  login         - Test user login")
    print("  router        - Test router functionality")
    print("  docs          - Test API documentation")
    print("  list          - List all available endpoints")
    print("  all           - Run all tests")
    print("  help          - Show this help")


def run_all_tests():
    """Run all quick tests"""
    print("Running All Quick Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("System Info", test_system_info),
        ("Example Data", test_example_data),
        ("User Registration", test_user_registration),
        ("User Login", test_user_login),
        ("Router", test_router),
        ("API Documentation", test_api_documentation)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        test_func()


def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    endpoint = sys.argv[1].lower()
    
    if endpoint == "health":
        test_health_check()
    elif endpoint == "system":
        test_system_info()
    elif endpoint == "example":
        test_example_data()
    elif endpoint == "register":
        test_user_registration()
    elif endpoint == "login":
        test_user_login()
    elif endpoint == "router":
        test_router()
    elif endpoint == "docs":
        test_api_documentation()
    elif endpoint == "list":
        list_endpoints()
    elif endpoint == "all":
        run_all_tests()
    elif endpoint == "help":
        show_help()
    else:
        print(f"Unknown endpoint: {endpoint}")
        show_help()


if __name__ == "__main__":
    main()
