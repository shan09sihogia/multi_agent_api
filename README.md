# 🧠 Multi-Agent Backend API (CrewAI + Gemini + FastAPI)

A powerful production-ready multi-agent backend powered by **CrewAI**, **FastAPI**, **Redis**, and **Gemini API**. This system supports multilingual queries, intelligent agents, and session-based memory — all optimized for smart decision-making and fast response.

---

## 🚀 Features

- 🤖 Two intelligent agents: `SupportAgent` and `DashboardAgent` (via CrewAI)
- 🌍 Multilingual query support (via Google Gemini API)
- 🧠 Session-based memory management (via Redis)
- ⚡ RESTful APIs built using FastAPI
- 🐳 Docker support for simple and consistent deployment

---

## 📦 Tech Stack

- **Python** & **FastAPI**
- **CrewAI** for multi-agent architecture
- **Gemini Pro API** (Google AI)
- **Redis (Upstash)** for context/session tracking
- **MongoDB Atlas** as the backend database
- **Docker** for containerization
- **Render** for cloud deployment

---

## 🌐 Live Demo

Base URL: [`https://multi-agent-api-bcev.onrender.com`](https://multi-agent-api-bcev.onrender.com)

Example Endpoint:

```http
GET /support/query?q=Get%20Priya%20Sharma%20details
Headers:
session-id: abc123
