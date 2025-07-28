#!/usr/bin/env python3
"""
Test script for SAP SuccessFactors Employee Central Mock Server
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/successfactors/odata/v2"

def test_endpoint(method: str, url: str, data: Dict[Any, Any] = None) -> None:
    """Test an API endpoint and print the results."""
    print(f"\n🔍 Testing {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "PUT":
            response = requests.put(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"✅ Status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"📄 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run comprehensive tests of the mock server."""
    print("🚀 Starting SAP SuccessFactors Mock Server Tests")
    
    # Test health check
    test_endpoint("GET", "http://localhost:8000/health")
    
    # Test basic entity listing
    test_endpoint("GET", f"{BASE_URL}/EmpEmployment")
    
    # Test entity by single key
    test_endpoint("GET", f"{BASE_URL}/EmpEmployment('EMP001')")
    
    # Test background entity with dual keys
    test_endpoint("GET", f"{BASE_URL}/Background_Education(backgroundElementId=1,userId='EMP001')")
    
    # Test creating a new entity
    test_endpoint("POST", f"{BASE_URL}/NewTestEntity", {
        "name": "Test Employee",
        "department": "Engineering",
        "active": True
    })
    
    # Test listing the new entity
    test_endpoint("GET", f"{BASE_URL}/NewTestEntity")
    
    # Test updating an entity
    test_endpoint("PUT", f"{BASE_URL}/EmpEmployment('EMP001')", {
        "employmentStatus": "Updated"
    })
    
    # Test workflow entities
    test_endpoint("GET", f"{BASE_URL}/MyPendingWorkflow")
    
    # Test skills management entities
    test_endpoint("GET", f"{BASE_URL}/SkillEntity")
    
    # Test payroll entities
    test_endpoint("GET", f"{BASE_URL}/EmployeeTimeSheet")
    
    # Test position management
    test_endpoint("GET", f"{BASE_URL}/Position")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()
