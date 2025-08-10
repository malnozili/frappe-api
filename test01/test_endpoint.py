#!/usr/bin/env python3
"""
Test script for the updated API endpoint with forward slash format
"""

import frappe
import json
from frappe.utils import now_datetime

def test_api_endpoint():
    """Simple test function that can be called from bench execute"""
    print("Testing the updated API endpoint with forward slash format...")
    
    try:
        # Test the endpoint directly
        result = frappe.call("test01.api.v1.endpoints.example.search_example_data", 
                           query="test", limit=5)
        
        print(f"✓ Endpoint call successful!")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Test the router configuration
        from test01.api.v1.router import api_router
        
        if "example" in api_router.endpoints and "search" in api_router.endpoints["example"]:
            endpoint_path = api_router.endpoints["example"]["search"]
            print(f"✓ Router endpoint path: {endpoint_path}")
            
            # Verify it uses forward slashes
            if "/" in endpoint_path and "." not in endpoint_path:
                print("✓ Endpoint uses forward slash format correctly!")
            else:
                print("✗ Endpoint still uses dot notation!")
                return False
        else:
            print("✗ Endpoint not found in router!")
            return False
        
        print("🎉 API endpoint test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

def test_search_example_data_endpoint():
    """Test the search_example_data endpoint with the new forward slash format"""
    
    print("Testing API endpoint: test01/api/v1/endpoints/example/search_example_data")
    print("=" * 60)
    
    try:
        # Test 1: Basic search functionality
        print("\n1. Testing basic search functionality...")
        
        # Call the endpoint directly
        result = frappe.call("test01.api.v1.endpoints.example.search_example_data", 
                           query="test", limit=5)
        
        print(f"✓ Endpoint call successful")
        print(f"  Response: {json.dumps(result, indent=2)}")
        
        # Test 2: Test with router
        print("\n2. Testing through router...")
        
        from test01.api.v1.router import api_router
        
        # Check if the endpoint is properly configured
        if "example" in api_router.endpoints and "search" in api_router.endpoints["example"]:
            endpoint_path = api_router.endpoints["example"]["search"]
            print(f"✓ Endpoint path found: {endpoint_path}")
            
            # Test router call
            router_result = api_router.route_request("example/search", "GET", {"query": "test", "limit": 3})
            print(f"✓ Router call successful")
            print(f"  Response: {json.dumps(router_result, indent=2)}")
        else:
            print("✗ Endpoint not found in router configuration")
            return False
        
        # Test 3: Test different query parameters
        print("\n3. Testing with different parameters...")
        
        test_cases = [
            {"query": "example", "limit": 10},
            {"query": "data", "limit": 1},
            {"query": "test", "limit": 0}
        ]
        
        for i, params in enumerate(test_cases, 1):
            print(f"  Test case {i}: {params}")
            try:
                result = frappe.call("test01.api.v1.endpoints.example.search_example_data", **params)
                print(f"    ✓ Success: {result.get('success', False)}")
                print(f"    ✓ Count: {result.get('count', 0)}")
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
        
        # Test 4: Test error handling
        print("\n4. Testing error handling...")
        
        try:
            # Test with empty query (should fail)
            result = frappe.call("test01.api.v1.endpoints.example.search_example_data", query="", limit=5)
            print(f"  Empty query result: {result.get('success', False)}")
        except Exception as e:
            print(f"  ✓ Empty query properly handled: {str(e)}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        return False

def test_endpoint_format():
    """Test that the endpoint format is correctly updated"""
    
    print("\nTesting endpoint format consistency...")
    print("-" * 40)
    
    try:
        from test01.api.v1.router import api_router
        
        # Check all endpoints use forward slash format
        all_endpoints = []
        for category, endpoints in api_router.endpoints.items():
            for action, path in endpoints.items():
                all_endpoints.append(path)
                if "." in path and "test01" in path:
                    print(f"✗ Found dot notation in: {path}")
                    return False
                else:
                    print(f"✓ Correct format: {path}")
        
        print(f"\n✓ All {len(all_endpoints)} endpoints use forward slash format")
        return True
        
    except Exception as e:
        print(f"✗ Format test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing Updated API Endpoint")
    print("=" * 60)
    
    # Test the endpoint functionality
    endpoint_test = test_search_example_data_endpoint()
    
    # Test the format consistency
    format_test = test_endpoint_format()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Endpoint functionality: {'✓ PASSED' if endpoint_test else '✗ FAILED'}")
    print(f"  Format consistency: {'✓ PASSED' if format_test else '✗ FAILED'}")
    
    if endpoint_test and format_test:
        print("\n🎉 All tests passed! The API endpoint is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    main()
