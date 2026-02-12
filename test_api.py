"""
Test script for Cal.com API endpoints

This script tests the get-upcoming-appointments endpoint.
Make sure the API server is running before executing this script.
"""
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = "https://customer-support-cal-com-api.onrender.com"
API_AUTH_TOKEN = os.getenv("API_AUTH_TOKEN")

# Headers
headers = {
    "Authorization": f"Bearer {API_AUTH_TOKEN}",
    "Content-Type": "application/json"
}


def test_get_upcoming_appointments():
    """Test the get-upcoming-appointments endpoint"""
    print("=" * 60)
    print("Testing: GET UPCOMING APPOINTMENTS")
    print("=" * 60)
    
    endpoint = f"{API_BASE_URL}/get-upcoming-appointments"
    
    # Test data - modify with actual email
    payload = {
        "team_id": 189647,
        "patient_email": "paul@gmail.com",  # Change this to test email
        "limit": 10
    }
    
    print(f"\n📤 Sending request to: {endpoint}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}\n")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"\n📥 Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                appointments = data.get("appointments", [])
                print(f"\n✅ Found {len(appointments)} upcoming appointment(s)")
                return True
            else:
                print("\n❌ Request failed")
                return False
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running!")
        print("   Run: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_clinic_info():
    """Test the clinic-info endpoint"""
    print("\n" + "=" * 60)
    print("Testing: CLINIC INFO")
    print("=" * 60)
    
    endpoint = f"{API_BASE_URL}/clinic-info"
    
    print(f"\n📤 Sending GET request to: {endpoint}\n")
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"\n📥 Response:")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_knowledge_base():
    """Test the query-knowledge-base endpoint"""
    print("\n" + "=" * 60)
    print("Testing: KNOWLEDGE BASE")
    print("=" * 60)
    
    endpoint = f"{API_BASE_URL}/query-knowledge-base"
    
    print(f"\n📤 Sending POST request to: {endpoint}\n")
    
    try:
        response = requests.post(endpoint, headers=headers, json={})
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"\n📥 Response:")
        data = response.json()
        if data.get("success"):
            content = data.get("content", "")
            print(f"Content length: {len(content)} characters")
            print(f"First 500 characters:\n{content[:500]}...")
        else:
            print(json.dumps(data, indent=2))
        
        return response.status_code == 200
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 Cal.com API Test Suite")
    print(f"🔗 API URL: {API_BASE_URL}")
    print(f"🔑 Auth Token: {'✅ Loaded' if API_AUTH_TOKEN else '❌ Missing'}\n")
    
    if not API_AUTH_TOKEN:
        print("❌ ERROR: API_AUTH_TOKEN not found in .env file!")
        exit(1)
    
    # Run tests
    results = []
    
    results.append(("Upcoming Appointments", test_get_upcoming_appointments()))
    results.append(("Clinic Info", test_clinic_info()))
    results.append(("Knowledge Base", test_knowledge_base()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
