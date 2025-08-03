🧠 Multi-Agent API (CrewAI + Gemini + FastAPI)
A multi-agent backend using CrewAI, FastAPI, Gemini API, and Redis with multilingual query support and session-based memory.

🚀 Features
🤖 CrewAI agents: SupportAgent, DashboardAgent

🌍 Multilingual query support (via Gemini API)

🧠 Session-based memory (via Redis)

⚡ FastAPI-powered REST API

🐳 Docker support for easy deployment

🔧 Required Environment Variables
Add the following in a .env file or set them in your environment:

MONGO_URI

DB_NAME

REDIS_URL

GEMINI_API_KEY

📬 API Endpoints
GET /support/query
GET /dashboard/query
Query Parameters:

q: Your natural language query

Headers:

session-id: Unique session ID to track context

Example Request:

perl
Copy
Edit
GET /support/query?q=Get%20priya%20sharma%20details
session-id: abc123
# 🐳 Docker Setup

# Build image
docker build -t multi-agent-api .

# Run container with .env
docker run -p 10000:10000 --env-file .env multi-agent-api
# Local Deployment
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app.main:app --reload
