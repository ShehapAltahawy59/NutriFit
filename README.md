# NutriFit Agents API

A comprehensive Flask API for nutrition and fitness planning using specialized AI agents. The application is built with a modular architecture where each agent has its own dedicated file and functionality.

## Architecture

The application uses a modular structure with separate files for each agent:

```
Agents/
├── __init__.py              # Shared Azure client initialization
├── inbody_specialist.py     # InBody analysis functionality
├── nutritionist.py          # Nutrition planning functionality
├── gym_trainer.py           # Fitness training functionality
├── main_app.py              # Main Flask application with all routes
├── Nutrition_agent.py       # Main entry point
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Features

### **InBody Specialist** (`inbody_specialist.py`)
- Body composition analysis
- InBody scan result interpretation
- Metabolic health indicators
- Progress tracking guidance
- Image analysis for scan results

### **Nutritionist** (`nutritionist.py`)
- Personalized meal planning
- Dietary restriction handling
- Cultural preference consideration
- Team-based plan evaluation
- Shopping lists and meal prep strategies

### **Gym Trainer** (`gym_trainer.py`)
- Workout plan creation
- Exercise form analysis
- Fitness level adaptation
- Equipment-based recommendations
- Injury prevention guidance

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the Agents directory:

```env
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

### 3. Run the API

```bash
python Nutrition_agent.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Main Endpoints

- **GET** `/` - API documentation and usage information
- **GET** `/health` - Main health check
- **GET** `/status` - Detailed agent status

### InBody Specialist Endpoints

- **POST** `/inbody/analyze` - Comprehensive body composition analysis
- **POST** `/inbody/simple_analysis` - Quick InBody analysis
- **GET** `/inbody/health` - InBody specialist health check

### Nutritionist Endpoints

- **POST** `/nutritionist/create_plan` - Comprehensive nutrition plan with evaluation
- **POST** `/nutritionist/simple_plan` - Simple nutrition plan
- **POST** `/nutritionist/advice` - General nutrition advice
- **GET** `/nutritionist/health` - Nutritionist health check

### Gym Trainer Endpoints

- **POST** `/gym/create_workout` - Comprehensive workout plan
- **POST** `/gym/simple_workout` - Simple workout plan
- **POST** `/gym/exercise_advice` - Exercise-specific advice
- **POST** `/gym/form_check` - Exercise form analysis (requires image)
- **GET** `/gym/health` - Gym trainer health check

## Usage Examples

### InBody Analysis

```bash
curl -X POST http://localhost:5000/inbody/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
    "scan_data": "InBody scan results...",
    "goals": "Weight loss and muscle building"
  }'
```

### Nutrition Planning

```bash
curl -X POST http://localhost:5000/nutritionist/create_plan \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
    "goals": "Weight loss",
    "preferences": "Mediterranean diet",
    "restrictions": "Lactose intolerant",
    "meal_plan_type": "weekly"
  }'
```

### Workout Planning

```bash
curl -X POST http://localhost:5000/gym/create_workout \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": "Age: 30, Weight: 70kg, Height: 170cm",
    "fitness_level": "intermediate",
    "goals": "Muscle building",
    "preferences": "Strength training",
    "available_equipment": "Full gym access"
  }'
```

### Exercise Form Check

```bash
curl -X POST http://localhost:5000/gym/form_check \
  -H "Content-Type: application/json" \
  -d '{
    "exercise": "squat",
    "image_url": "https://example.com/squat-form.jpg"
  }'
```

## Python Usage

```python
import requests

# InBody Analysis
response = requests.post('http://localhost:5000/inbody/analyze', json={
    'user_info': 'Age: 30, Weight: 70kg, Height: 170cm',
    'scan_data': 'InBody scan results...',
    'goals': 'Weight loss and muscle building'
})
print(response.json())

# Nutrition Plan
response = requests.post('http://localhost:5000/nutritionist/create_plan', json={
    'user_info': 'Age: 30, Weight: 70kg, Height: 170cm',
    'goals': 'Weight loss',
    'preferences': 'Mediterranean diet',
    'restrictions': 'Lactose intolerant'
})
print(response.json())

# Workout Plan
response = requests.post('http://localhost:5000/gym/create_workout', json={
    'user_info': 'Age: 30, Weight: 70kg, Height: 170cm',
    'fitness_level': 'intermediate',
    'goals': 'Muscle building',
    'preferences': 'Strength training'
})
print(response.json())
```

## Agent Details

### InBody Specialist
- Analyzes body composition data
- Provides metabolic health insights
- Offers progress tracking guidance
- Supports image analysis for scan results

### Nutritionist + Evaluator Team
- Creates personalized meal plans
- Validates nutritional adequacy
- Considers dietary restrictions
- Provides shopping lists and prep tips

### Gym Trainer
- Designs workout routines
- Analyzes exercise form
- Adapts to fitness levels
- Provides safety guidance

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (missing required fields)
- `500`: Server error

Error responses include descriptive messages:

```json
{
    "error": "Missing required field: user_info"
}
```

## Modular Structure Benefits

1. **Separation of Concerns**: Each agent has its own file and responsibilities
2. **Maintainability**: Easy to modify individual agents without affecting others
3. **Scalability**: Can easily add new agents or modify existing ones
4. **Testing**: Each agent can be tested independently
5. **Code Reuse**: Shared Azure client initialization in `__init__.py`

## Troubleshooting

1. **Agent initialization fails**: Check Azure OpenAI credentials in `.env`
2. **Image processing errors**: Ensure image URLs are accessible
3. **Timeout errors**: Complex plans may take time; consider increasing timeouts
4. **Import errors**: Ensure all dependencies are installed correctly

## Development

To add a new agent:

1. Create a new file (e.g., `new_agent.py`)
2. Import the shared Azure client: `from . import initialize_azure_client`
3. Create the agent function and Flask routes
4. Register the blueprint in `main_app.py`
5. Update documentation and README

## Notes

- All agents use the same Azure OpenAI client from `__init__.py`
- Each agent has its own health check endpoint
- Image analysis is optional and requires valid image URLs
- The modular structure allows for easy extension and maintenance 
