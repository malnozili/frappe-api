# Test App API Documentation

## Overview

This document provides comprehensive documentation for the Test App REST API built on the Frappe Framework. The API follows RESTful principles and provides a standardized interface for interacting with the application.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)
8. [Development](#development)

## Getting Started

### Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### API Version

The current API version is `v1.0.0`

### Content Type

All requests should use `application/json` content type.

## Authentication

The API uses API Key authentication. You need to include your API key in the Authorization header for protected endpoints.

### Getting API Key

1. **Register a new user** (if you don't have an account):
   ```bash
   POST /api/method/test.api.v1.endpoints.user.register_user
   ```

2. **Login to get API key**:
   ```bash
   POST /api/method/test.api.v1.endpoints.user.login
   ```

### Using API Key

Include your API key in the Authorization header:

```
Authorization: token api_key:api_secret
```

Example:
```
Authorization: token abc123def456:xyz789uvw012
```

## API Endpoints

### Authentication Endpoints

#### Login
```http
POST /api/method/test.api.v1.endpoints.user.login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": "user@example.com",
    "full_name": "John Doe",
    "api_key": "abc123def456",
    "api_secret": "xyz789uvw012"
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

#### Register
```http
POST /api/method/test.api.v1.endpoints.user.register_user
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "full_name": "Jane Doe",
  "password": "password123",
  "mobile_no": "+1234567890"
}
```

#### Logout
```http
POST /api/method/test.api.v1.endpoints.user.logout
```

*Requires authentication*

### User Management Endpoints

#### Get User Profile
```http
GET /api/method/test.api.v1.endpoints.user.get_user_profile
```

*Requires authentication*

#### Update User Profile
```http
PUT /api/method/test.api.v1.endpoints.user.update_user_profile
```

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "mobile_no": "+1234567890"
}
```

*Requires authentication*

#### Change Password
```http
PUT /api/method/test.api.v1.endpoints.user.change_password
```

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword"
}
```

*Requires authentication*

### Example Data Endpoints

#### Get Example Data
```http
GET /api/method/test.api.v1.endpoints.example.get_example_data
```

**Query Parameters:**
- `name` (optional): Specific record name

#### Create Example Data
```http
POST /api/method/test.api.v1.endpoints.example.create_example_data
```

**Request Body:**
```json
{
  "title": "Sample Title",
  "description": "Sample description"
}
```

#### Update Example Data
```http
PUT /api/method/test.api.v1.endpoints.example.update_example_data
```

**Request Body:**
```json
{
  "name": "record_name",
  "title": "Updated Title",
  "description": "Updated description"
}
```

#### Delete Example Data
```http
DELETE /api/method/test.api.v1.endpoints.example.delete_example_data
```

**Request Body:**
```json
{
  "name": "record_name"
}
```

#### Search Example Data
```http
GET /api/method/test.api.v1.endpoints.example.search_example_data
```

**Query Parameters:**
- `query` (required): Search query
- `limit` (optional): Maximum results (default: 10)

### System Endpoints

#### Health Check
```http
GET /api/method/test.api.v1.endpoints.system.health_check
```

*Public endpoint - no authentication required*

#### Get System Info
```http
GET /api/method/test.api.v1.endpoints.system.get_system_info
```

*Public endpoint - no authentication required*

#### Get API Documentation
```http
GET /api/method/test.api.v1.endpoints.system.get_api_documentation
```

*Requires authentication*

## Response Format

All API responses follow a standardized format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Optional success message",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

### Common Error Messages

- `"Missing required fields"` - Required parameters are missing
- `"Invalid API credentials"` - API key is invalid or expired
- `"Record not found"` - Requested record doesn't exist
- `"Insufficient permissions"` - User doesn't have required permissions

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default limit**: 100 requests per hour per user per endpoint
- **Window**: 1 hour (3600 seconds)
- **Headers**: Rate limit information is included in response headers

## Examples

### Complete Authentication Flow

1. **Register a new user:**
```bash
curl -X POST http://localhost:8000/api/method/test.api.v1.endpoints.user.register_user \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "password123"
  }'
```

2. **Login to get API key:**
```bash
curl -X POST http://localhost:8000/api/method/test.api.v1.endpoints.user.login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

3. **Use API key for authenticated requests:**
```bash
curl -X GET http://localhost:8000/api/method/test.api.v1.endpoints.user.get_user_profile \
  -H "Authorization: token your_api_key:your_api_secret"
```

### Working with Example Data

1. **Create a new record:**
```bash
curl -X POST http://localhost:8000/api/method/test.api.v1.endpoints.example.create_example_data \
  -H "Content-Type: application/json" \
  -H "Authorization: token your_api_key:your_api_secret" \
  -d '{
    "title": "My First Record",
    "description": "This is a test record"
  }'
```

2. **Get all records:**
```bash
curl -X GET http://localhost:8000/api/method/test.api.v1.endpoints.example.get_example_data \
  -H "Authorization: token your_api_key:your_api_secret"
```

3. **Search records:**
```bash
curl -X GET "http://localhost:8000/api/method/test.api.v1.endpoints.example.search_example_data?query=test&limit=5" \
  -H "Authorization: token your_api_key:your_api_secret"
```

## Development

### Project Structure

```
test/
├── api/
│   ├── __init__.py
│   ├── utils.py
│   └── v1/
│       ├── __init__.py
│       ├── router.py
│       └── endpoints/
│           ├── __init__.py
│           ├── example.py
│           ├── user.py
│           └── system.py
├── templates/
│   └── pages/
│       ├── api_docs.py
│       └── api_docs.html
├── www/
│   ├── swagger.json
│   └── swagger.html
└── API_README.md
```

### Adding New Endpoints

1. Create a new endpoint file in `test/api/v1/endpoints/`
2. Define your endpoint functions with proper decorators
3. Add the endpoint to the router in `test/api/v1/router.py`
4. Update the Swagger documentation in `test/www/swagger.json`
5. Test your endpoint

### Example Endpoint

```python
@frappe.whitelist(allow_guest=True)
def my_new_endpoint(param1: str, param2: str = None) -> Dict:
    """
    My new endpoint description
    
    Args:
        param1 (str): Required parameter
        param2 (str, optional): Optional parameter
        
    Returns:
        Dict: Response data
    """
    try:
        # Your logic here
        result = {"param1": param1, "param2": param2}
        
        return {
            "success": True,
            "data": result,
            "timestamp": now_datetime().isoformat()
        }
        
    except Exception as e:
        frappe.log_error(f"API Error in my_new_endpoint: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": now_datetime().isoformat()
        }
```

### Testing

1. **Unit Tests**: Create tests in `test/test/`
2. **Integration Tests**: Test API endpoints with real requests
3. **Comprehensive API Tests**: Run `python test_all_apis.py` for full test suite
4. **Quick API Tests**: Run `python quick_api_test.py [endpoint]` for individual tests
5. **HTTP API Tests**: Run `./test_api_curl.sh [option]` for curl-based testing
6. **Swagger UI**: Use the interactive documentation at `/assets/test/swagger.html`

#### Available Test Scripts

**1. Comprehensive Test Suite (`test_all_apis.py`)**
```bash
# Run all tests
python test_all_apis.py

# This script tests:
# - Router structure and functionality
# - System endpoints (health, info, docs)
# - Authentication endpoints (register, login)
# - User management endpoints (profile, update, password)
# - Example data endpoints (CRUD operations)
# - Error handling
# - Cleanup of test data
```

**2. Quick Test Script (`quick_api_test.py`)**
```bash
# Test specific endpoints
python quick_api_test.py health        # Test health check
python quick_api_test.py system        # Test system info
python quick_api_test.py example       # Test example data
python quick_api_test.py register      # Test user registration
python quick_api_test.py login         # Test user login
python quick_api_test.py router        # Test router functionality
python quick_api_test.py docs          # Test API documentation
python quick_api_test.py list          # List all endpoints
python quick_api_test.py all           # Run all quick tests
```

**3. HTTP Test Script (`test_api_curl.sh`)**
```bash
# Test via HTTP requests
./test_api_curl.sh system      # Test system endpoints
./test_api_curl.sh auth        # Test authentication
./test_api_curl.sh user        # Test user management
./test_api_curl.sh example     # Test example data
./test_api_curl.sh error       # Test error handling
./test_api_curl.sh router      # Test router functionality
./test_api_curl.sh endpoints   # Show available endpoints
./test_api_curl.sh all         # Run all tests
```

### Deployment

1. **Install the app** in your Frappe bench
2. **Build assets**: `bench build --app test`
3. **Restart services**: `bench restart`
4. **Access documentation**: Visit `/api-docs` on your site

## Support

For API support and questions:

- **Email**: m.nozili@fintechsys.net
- **Documentation**: Visit `/api-docs` on your site
- **Swagger UI**: Visit `/assets/test/swagger.html`

## License

This API is licensed under the MIT License. See the LICENSE file for details.
