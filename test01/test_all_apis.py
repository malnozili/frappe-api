#!/usr/bin/env python3
"""
Comprehensive API Test Script for test01 App

This script tests all API endpoints in the test01 application including:
- Authentication endpoints (login, register, logout)
- User management endpoints (profile, update, change password)
- Example data endpoints (CRUD operations)
- System endpoints (health check, system info, documentation)
- Router functionality
- Error handling
"""

import frappe
import json
import time
from typing import Dict, List, Any
from frappe.utils import now_datetime


class APITester:
    """Comprehensive API testing class"""
    
    def __init__(self):
        self.test_results = []
        self.test_user = None
        self.api_key = None
        self.api_secret = None
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "data": data,
            "timestamp": now_datetime().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if data and not success:
            print(f"   Error details: {data}")
    
    def test_router_structure(self):
        """Test the API router structure"""
        print("\n" + "="*60)
        print("TESTING API ROUTER STRUCTURE")
        print("="*60)
        
        try:
            from test01.api.v1.router import api_router
            
            # Test router exists
            self.log_test("Router Import", True, "Router imported successfully")
            
            # Test endpoints structure
            expected_categories = ["auth", "user", "example", "system"]
            for category in expected_categories:
                if category in api_router.endpoints:
                    self.log_test(f"Category {category}", True, f"Category {category} exists")
                else:
                    self.log_test(f"Category {category}", False, f"Category {category} missing")
            
            # Test specific endpoints
            expected_endpoints = {
                "auth": ["login", "register", "logout"],
                "user": ["profile", "update_profile", "change_password"],
                "example": ["get", "create", "update", "delete", "search"],
                "system": ["health", "info", "docs", "logs"]
            }
            
            for category, endpoints in expected_endpoints.items():
                for endpoint in endpoints:
                    if category in api_router.endpoints and endpoint in api_router.endpoints[category]:
                        self.log_test(f"Endpoint {category}/{endpoint}", True, f"Endpoint exists")
                    else:
                        self.log_test(f"Endpoint {category}/{endpoint}", False, f"Endpoint missing")
            
        except Exception as e:
            self.log_test("Router Structure", False, f"Router structure test failed: {str(e)}")
    
    def test_system_endpoints(self):
        """Test system endpoints (public)"""
        print("\n" + "="*60)
        print("TESTING SYSTEM ENDPOINTS")
        print("="*60)
        
        # Test health check
        try:
            result = frappe.call("test01.api.v1.endpoints.system.health_check")
            if result.get("success"):
                self.log_test("Health Check", True, "System health check passed")
                health_data = result.get("data", {})
                self.log_test("Health Status", True, f"Status: {health_data.get('status', 'unknown')}")
            else:
                self.log_test("Health Check", False, f"Health check failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Health Check", False, f"Health check exception: {str(e)}")
        
        # Test system info
        try:
            result = frappe.call("test01.api.v1.endpoints.system.get_system_info")
            if result.get("success"):
                self.log_test("System Info", True, "System info retrieved successfully")
            else:
                self.log_test("System Info", False, f"System info failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("System Info", False, f"System info exception: {str(e)}")
        
        # Test API documentation
        try:
            result = frappe.call("test01.api.v1.endpoints.system.get_api_documentation")
            if result.get("success"):
                self.log_test("API Documentation", True, "API documentation retrieved successfully")
            else:
                self.log_test("API Documentation", False, f"API documentation failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("API Documentation", False, f"API documentation exception: {str(e)}")
    
    def test_authentication_endpoints(self):
        """Test authentication endpoints"""
        print("\n" + "="*60)
        print("TESTING AUTHENTICATION ENDPOINTS")
        print("="*60)
        
        # Test user registration
        test_email = f"test_user_{int(time.time())}@example.com"
        test_password = "TestPassword123!"
        
        try:
            result = frappe.call("test01.api.v1.endpoints.user.register_user",
                               email=test_email,
                               full_name="Test User",
                               password=test_password,
                               mobile_no="+1234567890")
            
            if result.get("success"):
                self.log_test("User Registration", True, f"User {test_email} registered successfully")
                self.test_user = test_email
            else:
                self.log_test("User Registration", False, f"Registration failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("User Registration", False, f"Registration exception: {str(e)}")
        
        # Test user login
        if self.test_user:
            try:
                result = frappe.call("test01.api.v1.endpoints.user.login",
                                   email=test_email,
                                   password=test_password)
                
                if result.get("success"):
                    self.log_test("User Login", True, "User login successful")
                    login_data = result.get("data", {})
                    self.api_key = login_data.get("api_key")
                    self.api_secret = login_data.get("api_secret")
                    
                    if self.api_key and self.api_secret:
                        self.log_test("API Key Generation", True, "API key and secret generated")
                    else:
                        self.log_test("API Key Generation", False, "API key or secret missing")
                else:
                    self.log_test("User Login", False, f"Login failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                self.log_test("User Login", False, f"Login exception: {str(e)}")
    
    def test_user_management_endpoints(self):
        """Test user management endpoints (requires authentication)"""
        print("\n" + "="*60)
        print("TESTING USER MANAGEMENT ENDPOINTS")
        print("="*60)
        
        if not self.api_key or not self.api_secret:
            self.log_test("User Management", False, "Skipped - No API credentials available")
            return
        
        # Test get user profile
        try:
            result = frappe.call("test01.api.v1.endpoints.user.get_user_profile")
            if result.get("success"):
                self.log_test("Get User Profile", True, "User profile retrieved successfully")
            else:
                self.log_test("Get User Profile", False, f"Get profile failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Get User Profile", False, f"Get profile exception: {str(e)}")
        
        # Test update user profile
        try:
            result = frappe.call("test01.api.v1.endpoints.user.update_user_profile",
                               full_name="Updated Test User",
                               mobile_no="+9876543210")
            if result.get("success"):
                self.log_test("Update User Profile", True, "User profile updated successfully")
            else:
                self.log_test("Update User Profile", False, f"Update profile failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Update User Profile", False, f"Update profile exception: {str(e)}")
        
        # Test change password
        try:
            result = frappe.call("test01.api.v1.endpoints.user.change_password",
                               current_password="TestPassword123!",
                               new_password="NewTestPassword456!")
            if result.get("success"):
                self.log_test("Change Password", True, "Password changed successfully")
            else:
                self.log_test("Change Password", False, f"Change password failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Change Password", False, f"Change password exception: {str(e)}")
    
    def test_example_data_endpoints(self):
        """Test example data endpoints"""
        print("\n" + "="*60)
        print("TESTING EXAMPLE DATA ENDPOINTS")
        print("="*60)
        
        # Test get example data
        try:
            result = frappe.call("test01.api.v1.endpoints.example.get_example_data")
            if result.get("success"):
                self.log_test("Get Example Data", True, "Example data retrieved successfully")
                data = result.get("data", [])
                self.log_test("Data Count", True, f"Retrieved {len(data)} records")
            else:
                self.log_test("Get Example Data", False, f"Get data failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Get Example Data", False, f"Get data exception: {str(e)}")
        
        # Test create example data
        test_title = f"Test Record {int(time.time())}"
        test_description = "This is a test record created by the API test script"
        
        try:
            result = frappe.call("test01.api.v1.endpoints.example.create_example_data",
                               title=test_title,
                               description=test_description)
            if result.get("success"):
                self.log_test("Create Example Data", True, f"Record '{test_title}' created successfully")
                created_data = result.get("data", {})
                record_name = created_data.get("name")
                if record_name:
                    self.log_test("Record Name", True, f"Record name: {record_name}")
                else:
                    self.log_test("Record Name", False, "Record name not returned")
            else:
                self.log_test("Create Example Data", False, f"Create failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Create Example Data", False, f"Create exception: {str(e)}")
        
        # Test search example data
        try:
            result = frappe.call("test01.api.v1.endpoints.example.search_example_data",
                               query="test",
                               limit=5)
            if result.get("success"):
                self.log_test("Search Example Data", True, "Search completed successfully")
                search_data = result.get("data", [])
                self.log_test("Search Results", True, f"Found {len(search_data)} results")
            else:
                self.log_test("Search Example Data", False, f"Search failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            self.log_test("Search Example Data", False, f"Search exception: {str(e)}")
        
        # Test update example data (if we have a record name)
        if 'record_name' in locals():
            try:
                result = frappe.call("test01.api.v1.endpoints.example.update_example_data",
                                   name=record_name,
                                   title=f"Updated {test_title}",
                                   description="This record was updated by the API test script")
                if result.get("success"):
                    self.log_test("Update Example Data", True, f"Record '{record_name}' updated successfully")
                else:
                    self.log_test("Update Example Data", False, f"Update failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                self.log_test("Update Example Data", False, f"Update exception: {str(e)}")
            
            # Test delete example data
            try:
                result = frappe.call("test01.api.v1.endpoints.example.delete_example_data",
                                   name=record_name)
                if result.get("success"):
                    self.log_test("Delete Example Data", True, f"Record '{record_name}' deleted successfully")
                else:
                    self.log_test("Delete Example Data", False, f"Delete failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                self.log_test("Delete Example Data", False, f"Delete exception: {str(e)}")
    
    def test_router_functionality(self):
        """Test the router functionality"""
        print("\n" + "="*60)
        print("TESTING ROUTER FUNCTIONALITY")
        print("="*60)
        
        try:
            from test01.api.v1.router import api_router
            
            # Test valid endpoint
            result = api_router.route_request("system/health", "GET")
            if result.get("success"):
                self.log_test("Router Valid Endpoint", True, "Router handled valid endpoint correctly")
            else:
                self.log_test("Router Valid Endpoint", False, f"Router failed on valid endpoint: {result.get('error', 'Unknown error')}")
            
            # Test invalid endpoint
            result = api_router.route_request("invalid/endpoint", "GET")
            if not result.get("success"):
                self.log_test("Router Invalid Endpoint", True, "Router correctly rejected invalid endpoint")
            else:
                self.log_test("Router Invalid Endpoint", False, "Router should have rejected invalid endpoint")
            
            # Test endpoint with data
            result = api_router.route_request("example/search", "GET", {"query": "test", "limit": 3})
            if result.get("success"):
                self.log_test("Router With Data", True, "Router handled endpoint with data correctly")
            else:
                self.log_test("Router With Data", False, f"Router failed with data: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.log_test("Router Functionality", False, f"Router test exception: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n" + "="*60)
        print("TESTING ERROR HANDLING")
        print("="*60)
        
        # Test invalid login
        try:
            result = frappe.call("test01.api.v1.endpoints.user.login",
                               email="invalid@example.com",
                               password="wrong_password")
            if not result.get("success"):
                self.log_test("Invalid Login", True, "Invalid login correctly rejected")
            else:
                self.log_test("Invalid Login", False, "Invalid login should have been rejected")
        except Exception as e:
            self.log_test("Invalid Login", False, f"Invalid login exception: {str(e)}")
        
        # Test missing required fields
        try:
            result = frappe.call("test01.api.v1.endpoints.example.create_example_data", title="")
            if not result.get("success"):
                self.log_test("Missing Required Fields", True, "Missing fields correctly rejected")
            else:
                self.log_test("Missing Required Fields", False, "Missing fields should have been rejected")
        except Exception as e:
            self.log_test("Missing Required Fields", False, f"Missing fields exception: {str(e)}")
        
        # Test invalid search parameters
        try:
            result = frappe.call("test01.api.v1.endpoints.example.search_example_data",
                               query="",
                               limit=-1)
            if not result.get("success"):
                self.log_test("Invalid Search Parameters", True, "Invalid parameters correctly rejected")
            else:
                self.log_test("Invalid Search Parameters", False, "Invalid parameters should have been rejected")
        except Exception as e:
            self.log_test("Invalid Search Parameters", False, f"Invalid parameters exception: {str(e)}")
    
    def test_cleanup(self):
        """Clean up test data"""
        print("\n" + "="*60)
        print("CLEANING UP TEST DATA")
        print("="*60)
        
        # Clean up test user if created
        if self.test_user:
            try:
                # Delete test user if exists
                if frappe.db.exists("User", self.test_user):
                    frappe.delete_doc("User", self.test_user, force=True)
                    self.log_test("Cleanup Test User", True, f"Test user {self.test_user} deleted")
                else:
                    self.log_test("Cleanup Test User", True, f"Test user {self.test_user} not found")
            except Exception as e:
                self.log_test("Cleanup Test User", False, f"Failed to delete test user: {str(e)}")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
        
        if failed_tests > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        # Save detailed report
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            "results": self.test_results,
            "timestamp": now_datetime().isoformat()
        }
        
        try:
            with open("api_test_report.json", "w") as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"\nDetailed report saved to: api_test_report.json")
        except Exception as e:
            print(f"\nFailed to save report: {str(e)}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive API Tests")
        print("="*60)
        
        # Run all test suites
        self.test_router_structure()
        self.test_system_endpoints()
        self.test_authentication_endpoints()
        self.test_user_management_endpoints()
        self.test_example_data_endpoints()
        self.test_router_functionality()
        self.test_error_handling()
        self.test_cleanup()
        
        # Generate report
        success = self.generate_report()
        
        if success:
            print("\n🎉 All tests passed! Your API is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check the implementation.")
        
        return success


def main():
    """Main function to run the API tests"""
    try:
        tester = APITester()
        success = tester.run_all_tests()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
