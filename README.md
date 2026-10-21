# AI Document Processing & Workflow Hub

A backend API built with Python, FastAPI, PostgreSQL, and Local AI (Ollama) to upload documents, extract text, and generate automated summaries.

## Features
* FastAPI Backend: Fast REST API with interactive documentation (Swagger UI).
* PDF Processing: Automatic text extraction using pdfplumber.
* Local AI: Generates executive summaries using local LLMs (Ollama / Llama 3).
* Database: Persistent data storage using PostgreSQL and SQLAlchemy.

## Tech Stack
* Python, FastAPI, SQLAlchemy
* PostgreSQL, Redis
* Ollama, pdfplumber
* Docker & Docker Compose

## Quick Start

Clone the repository:
git clone https://github.com/AlexandrosZlatos/ai-document-hub.git
cd ai-document-hub

Start Database (Docker):
docker compose up -d

Install Dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Run the App:
uvicorn app.main:app --reload

Test the API:
Open your browser at: http://127.0.0.1:8000/docs