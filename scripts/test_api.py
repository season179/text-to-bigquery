#!/usr/bin/env python3
"""
Test script for the FastAPI application.
"""
import sys
import json
import requests
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 50}")
    print(f"{title.upper()}")
    print(f"{'=' * 50}")

def test_health_check():
    """Test the health check endpoint."""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        
        print("✅ Health check successful")
        print(f"Status: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_schema_endpoints():
    """Test the schema endpoints."""
    print_section("Testing Schema Endpoints")
    
    # Test getting the schema (should be empty)
    try:
        print("Getting current schema...")
        response = requests.get(f"{BASE_URL}/schema")
        response.raise_for_status()
        print("✅ Successfully retrieved schema")
    except Exception as e:
        print(f"❌ Failed to get schema: {e}")
        return False
    
    # Create a test schema
    test_schema = {
        "description": "Test database schema",
        "tables": {
            "users": {
                "name": "users",
                "description": "User information",
                "columns": {
                    "id": {
                        "name": "id",
                        "type": "INTEGER",
                        "description": "User ID",
                        "is_primary_key": True,
                        "is_nullable": False
                    },
                    "name": {
                        "name": "name",
                        "type": "STRING",
                        "description": "User's full name",
                        "is_nullable": False
                    },
                    "email": {
                        "name": "email",
                        "type": "STRING",
                        "description": "User's email address",
                        "is_nullable": False
                    }
                },
                "primary_key": ["id"],
                "sample_queries": [
                    "SELECT * FROM users WHERE id = 1"
                ]
            }
        },
        "relationships": []
    }
    
    # Test updating the schema
    try:
        print("\nUpdating schema...")
        response = requests.put(
            f"{BASE_URL}/schema",
            json={
                "schema_data": test_schema,
                "overwrite": True
            }
        )
        response.raise_for_status()
        print("✅ Successfully updated schema")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Failed to update schema: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False
    
    # Get the updated schema
    try:
        print("\nGetting updated schema...")
        response = requests.get(f"{BASE_URL}/schema")
        response.raise_for_status()
        print("✅ Successfully retrieved updated schema")
        print("Schema:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Failed to get updated schema: {e}")
        return False
    
    return True

def test_generate_sql():
    """Test the generate SQL endpoint."""
    print_section("Testing Generate SQL Endpoint")
    
    test_query = {
        "query": "Show me all users",
        "max_tokens": 1000,
        "temperature": 0.3
    }
    
    try:
        print("Generating SQL...")
        response = requests.post(
            f"{BASE_URL}/generate-sql",
            json=test_query
        )
        response.raise_for_status()
        
        print("✅ Successfully generated SQL")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate SQL: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing FastAPI Application")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Schema Endpoints", test_schema_endpoints),
        ("Generate SQL", test_generate_sql)
    ]
    
    all_passed = True
    for name, test_func in tests:
        print(f"\n{' Starting ' + name + ' ':-^50}")
        if not test_func():
            all_passed = False
            print(f"\n❌ {name} test failed!")
        else:
            print(f"\n✅ {name} test passed!")
    
    if all_passed:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
