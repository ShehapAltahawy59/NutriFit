"""
Test Script for Plan Workflow

This script demonstrates how to use the complete nutrition planning workflow
from InBody image analysis to final nutrition plan generation.
"""

import requests
import json
import time

# API base URL
BASE_URL = " https://nutrifit-agents-api.jollymoss-483cf973.uaenorth.azurecontainerapps.io"

def test_workflow_status():
    """Test workflow status endpoint"""
    print("=== Testing Workflow Status ===")
    
    try:
        response = requests.get(f"{BASE_URL}/workflow/workflow_status")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_health_check():
    """Test health check endpoint"""
    print("=== Testing Health Check ===")
    
    try:
        response = requests.get(f"{BASE_URL}/workflow/health")
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_inbody_analysis_only():
    """Test InBody analysis only"""
    print("=== Testing InBody Analysis Only ===")
    
    # Example data - replace with actual InBody image URL
    test_data = {
        "inbody_image_url": "https://inbodycanada.ca/wp-content/uploads/2020/09/270_SpecSheet_Hi-res-scaled.jpg",  # Replace with actual URL
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/workflow/test_inbody_analysis",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_complete_workflow():
    """Test complete workflow from InBody image to nutrition plan"""
    print("=== Testing Complete Workflow ===")
    
    # Example data - replace with actual values
    test_data = {
        "inbody_image_url": "https://inbodycanada.ca/wp-content/uploads/2020/09/270_SpecSheet_Hi-res-scaled.jpg",  # Replace with actual URL
        "client_country": "Egypt",
        "goals": "Weight loss and muscle building",
        "allergies": "egg",
        "injuries": "none",  # <-- NEW
        "number_of_gym_days": "5"
    }
    
    try:
        print("Starting complete workflow...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/workflow/create_complete_plan",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()

def test_individual_agents():
    """Test individual agent endpoints"""
    print("=== Testing Individual Agents ===")
    
    # Test InBody Specialist
    print("1. Testing InBody Specialist:")
    try:
        response = requests.get(f"{BASE_URL}/inbody/health")
        print(f"   Status: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Nutritionist
    print("2. Testing Nutritionist:")
    try:
        response = requests.get(f"{BASE_URL}/nutritionist/health")
        print(f"   Status: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Gym Trainer
    print("3. Testing Gym Trainer:")
    try:
        response = requests.get(f"{BASE_URL}/gym/health")
        print(f"   Status: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()

def main():
    """Main test function"""
    print("NutriFit Agents API - Workflow Test")
    print("=" * 50)
    print()
    
    # Test individual agents first
    # test_individual_agents()
    
    # # Test workflow status
    # test_workflow_status()
    
    # # Test health check
    # test_health_check()
    
    # # Test InBody analysis only (commented out as it requires actual image URL)
    # test_inbody_analysis_only()
    
    # Test complete workflow (commented out as it requires actual image URL)
    test_complete_workflow()
    
    print("Test completed!")
    

if __name__ == "__main__":
    main() 
