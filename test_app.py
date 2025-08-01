#!/usr/bin/env python3
"""
Test script for WanderWise Travel Recommender
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Make sure it's running on localhost:5000")
        return False

def test_recommendations_endpoint():
    """Test the recommendations endpoint"""
    test_data = {
        "location": "Tokyo, Japan",
        "duration": "Short trip (4-7 days)",
        "preferences": "I love trying local street food and visiting historical sites"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/recommendations',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recommendations endpoint working")
            print(f"   Generated at: {data.get('generated_at', 'N/A')}")
            
            # Check if GPT recommendations are present
            if 'gpt_recommendations' in data:
                gpt_data = data['gpt_recommendations']
                if 'error' in gpt_data:
                    print(f"⚠️  GPT API Error: {gpt_data['error']}")
                else:
                    print("✅ GPT recommendations generated successfully")
            
            # Check if Qloo recommendations are present
            if 'qloo_recommendations' in data:
                qloo_data = data['qloo_recommendations']
                if 'error' in qloo_data:
                    print(f"⚠️  Qloo API Error: {qloo_data['error']}")
                else:
                    print("✅ Qloo recommendations generated successfully")
            
            return True
        else:
            print(f"❌ Recommendations endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application")
        return False
    except Exception as e:
        print(f"❌ Error testing recommendations: {str(e)}")
        return False

def test_qloo_search_endpoint():
    """Test the Qloo search endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/qloo-search?q=Tokyo')
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Qloo search endpoint working")
            return True
        else:
            print(f"❌ Qloo search endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application")
        return False
    except Exception as e:
        print(f"❌ Error testing Qloo search: {str(e)}")
        return False

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    qloo_key = os.getenv('QLOO_API_KEY')
    
    if openai_key and openai_key != 'your_openai_api_key_here':
        print("✅ OpenAI API key is set")
    else:
        print("❌ OpenAI API key is not set or is default value")
    
    if qloo_key and qloo_key != 'your_qloo_api_key_here':
        print("✅ Qloo API key is set")
    else:
        print("❌ Qloo API key is not set or is default value")
    
    return bool(openai_key and qloo_key and 
                openai_key != 'your_openai_api_key_here' and 
                qloo_key != 'your_qloo_api_key_here')

def main():
    """Run all tests"""
    print("🚀 Testing WanderWise Travel Recommender")
    print("=" * 50)
    
    # Check environment
    env_ok = check_environment()
    print()
    
    # Test endpoints
    health_ok = test_health_endpoint()
    print()
    
    if health_ok:
        search_ok = test_qloo_search_endpoint()
        print()
        
        rec_ok = test_recommendations_endpoint()
        print()
        
        # Summary
        print("=" * 50)
        print("📊 Test Summary:")
        print(f"   Environment: {'✅' if env_ok else '❌'}")
        print(f"   Health Check: {'✅' if health_ok else '❌'}")
        print(f"   Qloo Search: {'✅' if search_ok else '❌'}")
        print(f"   Recommendations: {'✅' if rec_ok else '❌'}")
        
        if all([env_ok, health_ok, search_ok, rec_ok]):
            print("\n🎉 All tests passed! Your application is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
    else:
        print("❌ Application is not running. Please start it first with 'python app.py'")

if __name__ == "__main__":
    main() 