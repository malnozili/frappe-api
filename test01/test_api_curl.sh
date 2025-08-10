#!/bin/bash

# API Test Script using curl for test01 App
# This script tests all API endpoints using HTTP requests

BASE_URL="http://localhost:8000"
API_KEY=""
API_SECRET=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ PASS${NC} $message"
    elif [ "$status" = "FAIL" ]; then
        echo -e "${RED}❌ FAIL${NC} $message"
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ️  INFO${NC} $message"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  WARN${NC} $message"
    fi
}

# Function to make API call and check response
test_api_call() {
    local test_name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_status="$5"
    
    echo "Testing: $test_name"
    
    # Prepare curl command
    local curl_cmd="curl -s -X $method"
    
    # Add headers
    curl_cmd="$curl_cmd -H 'Content-Type: application/json'"
    
    # Add authentication if available
    if [ ! -z "$API_KEY" ] && [ ! -z "$API_SECRET" ]; then
        curl_cmd="$curl_cmd -H 'Authorization: token $API_KEY:$API_SECRET'"
    fi
    
    # Add data if provided
    if [ ! -z "$data" ]; then
        curl_cmd="$curl_cmd -d '$data'"
    fi
    
    # Add URL
    curl_cmd="$curl_cmd '$BASE_URL/api/method/$endpoint'"
    
    # Execute curl command
    local response=$(eval $curl_cmd)
    local http_status=$?
    
    if [ $http_status -eq 0 ]; then
        # Check if response contains success
        if echo "$response" | grep -q '"success":true'; then
            print_status "PASS" "$test_name - API call successful"
            echo "   Response: $(echo "$response" | jq -r '.message // .data // "Success"' 2>/dev/null || echo "Success")"
        else
            print_status "FAIL" "$test_name - API call failed"
            echo "   Error: $(echo "$response" | jq -r '.error // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")"
        fi
    else
        print_status "FAIL" "$test_name - HTTP request failed (status: $http_status)"
    fi
    
    echo ""
}

# Function to test system endpoints
test_system_endpoints() {
    echo "=========================================="
    echo "TESTING SYSTEM ENDPOINTS"
    echo "=========================================="
    
    test_api_call "Health Check" "POST" "test01.api.v1.endpoints.system.health_check" "" "200"
    test_api_call "System Info" "POST" "test01.api.v1.endpoints.system.get_system_info" "" "200"
    test_api_call "API Documentation" "POST" "test01.api.v1.endpoints.system.get_api_documentation" "" "200"
}

# Function to test authentication endpoints
test_auth_endpoints() {
    echo "=========================================="
    echo "TESTING AUTHENTICATION ENDPOINTS"
    echo "=========================================="
    
    # Test user registration
    local test_email="test_user_$(date +%s)@example.com"
    local registration_data="{\"email\":\"$test_email\",\"full_name\":\"Test User\",\"password\":\"test123\",\"mobile_no\":\"+1234567890\"}"
    
    test_api_call "User Registration" "POST" "test01.api.v1.endpoints.user.register_user" "$registration_data" "200"
    
    # Test user login
    local login_data="{\"email\":\"$test_email\",\"password\":\"test123\"}"
    local login_response=$(curl -s -X POST \
        -H 'Content-Type: application/json' \
        -d "$login_data" \
        "$BASE_URL/api/method/test01.api.v1.endpoints.user.login")
    
    if echo "$login_response" | grep -q '"success":true'; then
        print_status "PASS" "User Login - Login successful"
        
        # Extract API key and secret
        API_KEY=$(echo "$login_response" | jq -r '.data.api_key' 2>/dev/null)
        API_SECRET=$(echo "$login_response" | jq -r '.data.api_secret' 2>/dev/null)
        
        if [ ! -z "$API_KEY" ] && [ ! -z "$API_SECRET" ]; then
            print_status "INFO" "API Key generated: ${API_KEY:0:10}..."
            print_status "INFO" "API Secret generated: ${API_SECRET:0:10}..."
        else
            print_status "WARN" "API key or secret not found in response"
        fi
    else
        print_status "FAIL" "User Login - Login failed"
        echo "   Error: $(echo "$login_response" | jq -r '.error // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")"
    fi
    
    echo ""
}

# Function to test user management endpoints
test_user_endpoints() {
    echo "=========================================="
    echo "TESTING USER MANAGEMENT ENDPOINTS"
    echo "=========================================="
    
    if [ -z "$API_KEY" ] || [ -z "$API_SECRET" ]; then
        print_status "WARN" "Skipping user management tests - No API credentials available"
        echo ""
        return
    fi
    
    test_api_call "Get User Profile" "POST" "test01.api.v1.endpoints.user.get_user_profile" "" "200"
    
    local update_data="{\"full_name\":\"Updated Test User\",\"mobile_no\":\"+9876543210\"}"
    test_api_call "Update User Profile" "POST" "test01.api.v1.endpoints.user.update_user_profile" "$update_data" "200"
    
    local password_data="{\"current_password\":\"test123\",\"new_password\":\"new_test_password_456\"}"
    test_api_call "Change Password" "POST" "test01.api.v1.endpoints.user.change_password" "$password_data" "200"
}

# Function to test example data endpoints
test_example_endpoints() {
    echo "=========================================="
    echo "TESTING EXAMPLE DATA ENDPOINTS"
    echo "=========================================="
    
    test_api_call "Get Example Data" "POST" "test01.api.v1.endpoints.example.get_example_data" "" "200"
    
    local create_data="{\"title\":\"Curl Test Record\",\"description\":\"Created by curl test script\"}"
    test_api_call "Create Example Data" "POST" "test01.api.v1.endpoints.example.create_example_data" "$create_data" "200"
    
    local search_data="{\"query\":\"test\",\"limit\":5}"
    test_api_call "Search Example Data" "POST" "test01.api.v1.endpoints.example.search_example_data" "$search_data" "200"
}

# Function to test error handling
test_error_handling() {
    echo "=========================================="
    echo "TESTING ERROR HANDLING"
    echo "=========================================="
    
    # Test invalid login
    local invalid_login_data="{\"email\":\"invalid@example.com\",\"password\":\"wrong_password\"}"
    local invalid_response=$(curl -s -X POST \
        -H 'Content-Type: application/json' \
        -d "$invalid_login_data" \
        "$BASE_URL/api/method/test01.api.v1.endpoints.user.login")
    
    if echo "$invalid_response" | grep -q '"success":false'; then
        print_status "PASS" "Invalid Login - Correctly rejected"
    else
        print_status "FAIL" "Invalid Login - Should have been rejected"
    fi
    
    # Test missing required fields
    local missing_fields_response=$(curl -s -X POST \
        -H 'Content-Type: application/json' \
        -d "{}" \
        "$BASE_URL/api/method/test01.api.v1.endpoints.example.create_example_data")
    
    if echo "$missing_fields_response" | grep -q '"success":false'; then
        print_status "PASS" "Missing Required Fields - Correctly rejected"
    else
        print_status "FAIL" "Missing Required Fields - Should have been rejected"
    fi
    
    echo ""
}

# Function to test router functionality
test_router() {
    echo "=========================================="
    echo "TESTING ROUTER FUNCTIONALITY"
    echo "=========================================="
    
    # Test router endpoint
    local router_data="{\"endpoint\":\"system/health\",\"method\":\"GET\"}"
    test_api_call "Router Valid Endpoint" "POST" "test01.api.v1.router.handle_api_request" "$router_data" "200"
    
    local invalid_router_data="{\"endpoint\":\"invalid/endpoint\",\"method\":\"GET\"}"
    local invalid_router_response=$(curl -s -X POST \
        -H 'Content-Type: application/json' \
        -d "$invalid_router_data" \
        "$BASE_URL/api/method/test01.api.v1.router.handle_api_request")
    
    if echo "$invalid_router_response" | grep -q '"success":false'; then
        print_status "PASS" "Router Invalid Endpoint - Correctly rejected"
    else
        print_status "FAIL" "Router Invalid Endpoint - Should have been rejected"
    fi
    
    echo ""
}

# Function to show available endpoints
show_endpoints() {
    echo "=========================================="
    echo "AVAILABLE API ENDPOINTS"
    echo "=========================================="
    
    echo "System Endpoints:"
    echo "  - test01.api.v1.endpoints.system.health_check"
    echo "  - test01.api.v1.endpoints.system.get_system_info"
    echo "  - test01.api.v1.endpoints.system.get_api_documentation"
    echo ""
    
    echo "Authentication Endpoints:"
    echo "  - test01.api.v1.endpoints.user.register_user"
    echo "  - test01.api.v1.endpoints.user.login"
    echo "  - test01.api.v1.endpoints.user.logout"
    echo ""
    
    echo "User Management Endpoints:"
    echo "  - test01.api.v1.endpoints.user.get_user_profile"
    echo "  - test01.api.v1.endpoints.user.update_user_profile"
    echo "  - test01.api.v1.endpoints.user.change_password"
    echo ""
    
    echo "Example Data Endpoints:"
    echo "  - test01.api.v1.endpoints.example.get_example_data"
    echo "  - test01.api.v1.endpoints.example.create_example_data"
    echo "  - test01.api.v1.endpoints.example.update_example_data"
    echo "  - test01.api.v1.endpoints.example.delete_example_data"
    echo "  - test01.api.v1.endpoints.example.search_example_data"
    echo ""
    
    echo "Router Endpoints:"
    echo "  - test01.api.v1.router.handle_api_request"
    echo "  - test01.api.v1.router.get_available_endpoints"
    echo ""
}

# Function to show help
show_help() {
    echo "API Test Script using curl"
    echo "=========================="
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  system      - Test system endpoints"
    echo "  auth        - Test authentication endpoints"
    echo "  user        - Test user management endpoints"
    echo "  example     - Test example data endpoints"
    echo "  error       - Test error handling"
    echo "  router      - Test router functionality"
    echo "  endpoints   - Show available endpoints"
    echo "  all         - Run all tests"
    echo "  help        - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 system"
    echo "  $0 auth"
    echo "  $0 all"
}

# Main function
main() {
    local option="${1:-help}"
    
    case $option in
        "system")
            test_system_endpoints
            ;;
        "auth")
            test_auth_endpoints
            ;;
        "user")
            test_user_endpoints
            ;;
        "example")
            test_example_endpoints
            ;;
        "error")
            test_error_handling
            ;;
        "router")
            test_router
            ;;
        "endpoints")
            show_endpoints
            ;;
        "all")
            test_system_endpoints
            test_auth_endpoints
            test_user_endpoints
            test_example_endpoints
            test_error_handling
            test_router
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Warning: jq is not installed. Some features may not work properly."
    echo "Install jq with: sudo apt-get install jq (Ubuntu/Debian) or brew install jq (macOS)"
    echo ""
fi

# Run main function
main "$@"
