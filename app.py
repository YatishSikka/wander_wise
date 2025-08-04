from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime

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
        """Get recommendations from Qloo Taste AI API"""
        headers = {
            "Authorization": f"Bearer {QLOO_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Set timeout to prevent hanging requests
        timeout = 10
        
        # Search for the location first
        search_url = f"{QLOO_BASE_URL}/search"
        search_params = {
            "query": location,
            "category": "cities"
        }
        
        try:
            search_response = requests.get(search_url, headers=headers, params=search_params, timeout=timeout)
            search_response.raise_for_status()
            search_data = search_response.json()
            
            if not search_data.get('results'):
                return {"error": f"Location '{location}' not found"}
            
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
            return {"error": f"Qloo API error: {str(e)}"}
    
    def get_gpt_recommendations(self, location, preferences, duration):
        """Get personalized recommendations using GPT"""
        prompt = f"""
        You are a knowledgeable travel expert. Provide detailed recommendations for {location} based on the following preferences:
        
        Travel Duration: {duration}
        Preferences: {preferences}
        
        Please provide recommendations in the following JSON format with 5-8 recommendations in each category:
        {{
            "destination_info": {{
                "name": "{location}",
                "best_time_to_visit": "string",
                "weather_info": "string",
                "cultural_highlights": "string"
            }},
            "food_recommendations": [
                {{
                    "name": "Restaurant/Cafe name",
                    "cuisine": "Type of cuisine",
                    "description": "Why it's worth visiting",
                    "price_range": "Budget/Mid-range/Luxury",
                    "must_try_dishes": ["dish1", "dish2", "dish3"],
                    "location": "Area/neighborhood"
                }}
            ],
            "experience_recommendations": [
                {{
                    "name": "Experience name",
                    "category": "Cultural/Adventure/Food/Nightlife/etc",
                    "description": "What makes this experience special",
                    "duration": "How long it takes",
                    "best_time": "When to do it",
                    "tips": "Pro tips for the best experience"
                }}
            ],
            "hidden_gems": [
                {{
                    "name": "Hidden gem name",
                    "type": "Restaurant/Attraction/Experience",
                    "description": "Why it's a hidden gem",
                    "location": "Where to find it"
                }}
            ],
            "travel_tips": [
                "Tip 1",
                "Tip 2",
                "Tip 3",
                "Tip 4",
                "Tip 5",
                "Tip 6"
            ]
        }}
        
        Make sure the recommendations are specific to {location} and consider the user's preferences and duration. Focus on authentic local experiences and must-try items. Provide 5-8 recommendations in each category to ensure fast response times.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a travel expert specializing in personalized travel recommendations. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
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
        
        # Get GPT recommendations
        gpt_recommendations = recommender.get_gpt_recommendations(location, preferences, duration)
        
        # Get Qloo recommendations for restaurants only (to avoid timeout)
        qloo_restaurants = recommender.get_qloo_recommendations(location, "restaurants")
        
        # Combine Qloo recommendations
        qloo_recommendations = {
            "restaurants": qloo_restaurants
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