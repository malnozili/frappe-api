#!/usr/bin/env python3
"""
test01 script to verify the API structure and basic functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test01_imports():
    """test01 that all API modules can be imported"""
    try:
        # test01 API module imports
        from test01.api import __init__ as api_init
        print("✓ API module imported successfully")
        
        from test01.api.v1 import __init__ as v1_init
        print("✓ API v1 module imported successfully")
        
        from test01.api.v1.endpoints import __init__ as endpoints_init
        print("✓ API endpoints module imported successfully")
        
        from test01.api.v1.endpoints import example, user, system
        print("✓ All endpoint modules imported successfully")
        
        from test01.api.v1.router import APIRouter, api_router
        print("✓ API router imported successfully")
        
        from test01.api.utils import create_api_response, validate_required_fields
        print("✓ API utilities imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test01_router_structure():
    """test01 the API router structure"""
    try:
        from test01.api.v1.router import api_router
        
        # Check if all expected categories exist
        expected_categories = ['auth', 'user', 'example', 'system']
        for category in expected_categories:
            if category not in api_router.endpoints:
                print(f"✗ Missing category: {category}")
                return False
            print(f"✓ Found category: {category}")
        
        # Check if endpoints exist in each category
        expected_endpoints = {
            'auth': ['login', 'register', 'logout'],
            'user': ['profile', 'update_profile', 'change_password'],
            'example': ['get', 'create', 'update', 'delete', 'search'],
            'system': ['health', 'info', 'docs', 'logs']
        }
        
        for category, endpoints in expected_endpoints.items():
            for endpoint in endpoints:
                if endpoint not in api_router.endpoints[category]:
                    print(f"✗ Missing endpoint: {category}.{endpoint}")
                    return False
                print(f"✓ Found endpoint: {category}.{endpoint}")
        
        return True
        
    except Exception as e:
        print(f"✗ Router structure test01 failed: {e}")
        return False

def test01_utility_functions():
    """test01 utility functions"""
    try:
        from test01.api.utils import create_api_response, validate_required_fields
        
        # test01 create_api_response
        response = create_api_response(success=True, data={"test01": "data"}, message="Success")
        if not response.get("success") or "test01" not in response.get("data", {}):
            print("✗ create_api_response test01 failed")
            return False
        print("✓ create_api_response test01 passed")
        
        # test01 validate_required_fields
        try:
            validate_required_fields({"field1": "value1", "field2": "value2"}, ["field1", "field2"])
            print("✓ validate_required_fields test01 passed (valid data)")
        except Exception:
            print("✗ validate_required_fields test01 failed (valid data)")
            return False
        
        try:
            validate_required_fields({"field1": "value1"}, ["field1", "field2"])
            print("✗ validate_required_fields test01 failed (should have raised exception)")
            return False
        except Exception:
            print("✓ validate_required_fields test01 passed (invalid data)")
        
        return True
        
    except Exception as e:
        print(f"✗ Utility functions test01 failed: {e}")
        return False

def test01_swagger_files():
    """test01 that Swagger files exist"""
    try:
        swagger_json_path = os.path.join(os.path.dirname(__file__), "www", "swagger.json")
        swagger_html_path = os.path.join(os.path.dirname(__file__), "www", "swagger.html")
        
        if not os.path.exists(swagger_json_path):
            print("✗ swagger.json file not found")
            return False
        print("✓ swagger.json file found")
        
        if not os.path.exists(swagger_html_path):
            print("✗ swagger.html file not found")
            return False
        print("✓ swagger.html file found")
        
        return True
        
    except Exception as e:
        print(f"✗ Swagger files test01 failed: {e}")
        return False

def main():
    """Run all test01s"""
    print("test01ing API Structure...")
    print("=" * 50)
    
    test01s = [
        ("Import test01s", test01_imports),
        ("Router Structure test01s", test01_router_structure),
        ("Utility Functions test01s", test01_utility_functions),
        ("Swagger Files test01s", test01_swagger_files)
    ]
    
    passed = 0
    total = len(test01s)
    
    for test01_name, test01_func in test01s:
        print(f"\n{test01_name}:")
        print("-" * 30)
        if test01_func():
            passed += 1
            print(f"✓ {test01_name} PASSED")
        else:
            print(f"✗ {test01_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"test01 Results: {passed}/{total} test01s passed")
    
    if passed == total:
        print("🎉 All test01s passed! API structure is ready.")
        return 0
    else:
        print("❌ Some test01s failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
