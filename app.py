from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import signal
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Qloo API configuration
QLOO_API_KEY = os.getenv('QLOO_API_KEY')
QLOO_BASE_URL = "https://hackathon.api.qloo.com"

class TravelRecommender:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def get_qloo_recommendations(self, location, category="restaurants"):
        """Get recommendations from Qloo Taste AI API with retry logic"""
        headers = {
            "Authorization": f"Bearer {QLOO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Set timeout to prevent hanging requests
        timeout = 10
        
        # Retry logic for intermittent issues
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Search for the location first
                search_url = f"{QLOO_BASE_URL}/search"
                search_params = {
                    "query": location,
                    "category": "cities"
                }
                
                search_response = requests.get(search_url, headers=headers, params=search_params, timeout=timeout)
                search_response.raise_for_status()
                search_data = search_response.json()
                
                if not search_data.get('results'):
                    return {"error": f"Location '{location}' not found. Please check the spelling or try a different city name."}
                
                # Get the first result (most relevant)
                location_id = search_data['results'][0]['id']
                
                # Get recommendations for the location
                rec_url = f"{QLOO_BASE_URL}/recommendations"
                rec_params = {
                    "entity_id": location_id,
                    "category": category,
                    "limit": 10
                }
                
                rec_response = requests.get(rec_url, headers=headers, params=rec_params, timeout=timeout)
                rec_response.raise_for_status()
                rec_data = rec_response.json()
                
                return rec_data
                
            except requests.exceptions.RequestException as e:
                error_msg = str(e)
                if attempt < max_retries - 1:  # Don't retry on last attempt
                    continue  # Retry
                else:
                    # Final attempt failed
                    if "401" in error_msg:
                        return {"error": "Qloo API temporarily unavailable (rate limit or service issue). Please try again in a few moments."}
                    elif "timeout" in error_msg.lower():
                        return {"error": "Qloo API request timed out. Please try again."}
                    else:
                        return {"error": f"Qloo API error: {error_msg}"}
    
    def get_gpt_recommendations(self, location, preferences, duration):
        """Get personalized recommendations using GPT"""
        prompt = f"""
        Provide quick travel tips for {location}. Duration: {duration}. Preferences: {preferences}.
        
        Return JSON with 2-3 items per category:
        {{
            "destination_info": {{
                "name": "{location}",
                "best_time_to_visit": "brief info",
                "weather_info": "brief info", 
                "cultural_highlights": "brief info"
            }},
            "food_recommendations": [
                {{
                    "name": "Restaurant name",
                    "cuisine": "cuisine type",
                    "description": "brief description",
                    "price_range": "price level",
                    "must_try_dishes": ["dish1", "dish2"],
                    "location": "area"
                }}
            ],
            "experience_recommendations": [
                {{
                    "name": "Experience name",
                    "category": "category",
                    "description": "brief description",
                    "duration": "time needed",
                    "best_time": "when to go",
                    "tips": "quick tip"
                }}
            ],
            "hidden_gems": [
                {{
                    "name": "Place name",
                    "type": "type",
                    "description": "brief description",
                    "location": "location"
                }}
            ],
            "travel_tips": ["tip1", "tip2", "tip3"]
        }}
        
        Keep responses concise and specific to {location}.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a travel expert. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800,
                timeout=10
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            # Clean up the response to ensure it's valid JSON
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
            
        except Exception as e:
            return {"error": f"GPT API error: {str(e)}"}

# Initialize the recommender
recommender = TravelRecommender()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get travel recommendations"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        preferences = data.get('preferences', '')
        duration = data.get('duration', '')
        
        if not location:
            return jsonify({"error": "Location is required"}), 400
        
        # Get Qloo recommendations first (faster)
        qloo_restaurants = recommender.get_qloo_recommendations(location, "restaurants")
        
        # Combine Qloo recommendations
        qloo_recommendations = {
            "restaurants": qloo_restaurants
        }
        
        # Try GPT with aggressive timeout (15 seconds max)
        gpt_recommendations = None
        gpt_error = None
        
        def gpt_call():
            nonlocal gpt_recommendations, gpt_error
            try:
                gpt_recommendations = recommender.get_gpt_recommendations(location, preferences, duration)
            except Exception as e:
                gpt_error = str(e)
        
        # Run GPT in a thread with timeout
        gpt_thread = threading.Thread(target=gpt_call)
        gpt_thread.daemon = True
        gpt_thread.start()
        gpt_thread.join(timeout=15)  # 15 second timeout
        
        if gpt_thread.is_alive():
            # GPT is taking too long, use fallback
            gpt_recommendations = {
                "error": "Qloo API temporarily unavailable - using fallback recommendations",
                "destination_info": {
                    "name": location,
                    "best_time_to_visit": "Check local tourism websites",
                    "weather_info": "Check weather apps for current conditions",
                    "cultural_highlights": "Explore local attractions and museums"
                },
                "food_recommendations": [],
                "experience_recommendations": [],
                "hidden_gems": [],
                "travel_tips": [
                    "Always check local tourism websites for the latest information",
                    "Consider booking popular attractions in advance",
                    "Learn a few basic phrases in the local language"
                ]
            }
        elif gpt_error:
            # GPT failed with error
            gpt_recommendations = {
                "error": f"GPT API error: {gpt_error}",
                "destination_info": {
                    "name": location,
                    "best_time_to_visit": "Check local tourism websites",
                    "weather_info": "Check weather apps for current conditions",
                    "cultural_highlights": "Explore local attractions and museums"
                },
                "food_recommendations": [],
                "experience_recommendations": [],
                "hidden_gems": [],
                "travel_tips": [
                    "Always check local tourism websites for the latest information",
                    "Consider booking popular attractions in advance",
                    "Learn a few basic phrases in the local language"
                ]
            }
        
        # Combine recommendations
        combined_recommendations = {
            "gpt_recommendations": gpt_recommendations,
            "qloo_recommendations": qloo_recommendations,
            "generated_at": datetime.now().isoformat()
        }
        
        return jsonify(combined_recommendations)
        
    except Exception as e:
        # Return a proper JSON response even on error
        return jsonify({
            "gpt_recommendations": {
                "error": f"Server temporarily unavailable: {str(e)}",
                "destination_info": {
                    "name": location,
                    "best_time_to_visit": "Check local tourism websites",
                    "weather_info": "Check weather apps for current conditions",
                    "cultural_highlights": "Explore local attractions and museums"
                },
                "food_recommendations": [],
                "experience_recommendations": [],
                "hidden_gems": [],
                "travel_tips": [
                    "Always check local tourism websites for the latest information",
                    "Consider booking popular attractions in advance",
                    "Learn a few basic phrases in the local language"
                ]
            },
            "qloo_recommendations": {
                "restaurants": {"error": "Unable to fetch restaurant recommendations"}
            },
            "generated_at": datetime.now().isoformat()
        }), 500

@app.route('/api/qloo-search', methods=['GET'])
def qloo_search():
    """API endpoint to search locations using Qloo"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        headers = {
            "Authorization": f"Bearer {QLOO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        search_url = f"{QLOO_BASE_URL}/search"
        search_params = {
            "query": query,
            "category": "cities"
        }
        
        response = requests.get(search_url, headers=headers, params=search_params, timeout=10)
        response.raise_for_status()
        
        return jsonify(response.json())
        
    except Exception as e:
        return jsonify({"error": f"Search error: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 