# WanderWise - AI Travel Companion

A production-ready travel recommender web application that combines the power of GPT and Qloo Taste AI API to provide personalized travel recommendations for food, experiences, and hidden gems.

## 🚀 Features

- **AI-Powered Recommendations**: Uses GPT-4o-mini to generate personalized travel recommendations
- **Qloo Taste AI Integration**: Leverages Qloo's API for restaurant and food recommendations
- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **Comprehensive Travel Guide**: Includes food, experiences, hidden gems, and travel tips
- **Personalization**: Tailored recommendations based on trip duration, budget, and preferences
- **Production Ready**: Includes error handling, health checks, and proper API structure

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: OpenAI GPT-4o-mini
- **API Integration**: Qloo Taste AI API
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Qloo Taste AI API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd qloo_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
cp env_example.txt .env
```

Edit the `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
QLOO_API_KEY=your_qloo_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 API Endpoints

### Main Endpoints
- `GET /` - Main application page
- `POST /api/recommendations` - Get travel recommendations
- `GET /api/qloo-search` - Search locations using Qloo API
- `GET /health` - Health check endpoint

### Request Format for Recommendations
```json
{
    "location": "Tokyo, Japan",
    "duration": "Short trip (4-7 days)",
    "preferences": "I love trying local street food and visiting historical sites"
}
```

### Response Format
```json
{
    "gpt_recommendations": {
        "destination_info": {
            "name": "Tokyo, Japan",
            "best_time_to_visit": "...",
            "weather_info": "...",
            "cultural_highlights": "..."
        },
        "food_recommendations": [...],
        "experience_recommendations": [...],
        "hidden_gems": [...],
        "travel_tips": [...]
    },
    "qloo_recommendations": {...},
    "generated_at": "2024-01-01T12:00:00"
}
```

## 🏗️ Project Structure

```
qloo_project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Main application template
└── .env                  # Environment variables (create this)
```

## 🎯 How It Works

1. **User Input**: Users provide their destination, trip duration, budget, and preferences
2. **AI Processing**: The app sends the request to GPT-4 for personalized recommendations
3. **Qloo Integration**: Simultaneously fetches restaurant recommendations from Qloo Taste AI
4. **Data Combination**: Merges both AI and Qloo recommendations for comprehensive results
5. **Beautiful Display**: Presents results in an organized, visually appealing format

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `QLOO_API_KEY`: Your Qloo Taste AI API key
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode

### Customization
You can customize the GPT prompt in `app.py` to modify the recommendation format and style.

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider using:
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Docker**: Create a Dockerfile for containerized deployment
- **Cloud Platforms**: Deploy to Heroku, AWS, or Google Cloud Platform

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly set in the `.env` file
2. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Conflicts**: Change the port in `app.py` if port 5000 is already in use

### Debug Mode
Set `FLASK_DEBUG=True` in your `.env` file for detailed error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for the Qloo API hackathon.

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- Qloo for Taste AI API
- Font Awesome for icons
- Google Fonts for typography

## 📞 Support

For support or questions, please open an issue in the repository.

---

**Happy Traveling! 🌍✈️** 
