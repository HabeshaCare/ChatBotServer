---

# LLM Server Setup

This repository contains a Python-based LLM (Language Model) server. Follow the steps below to set up and run the server locally.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3
- Python virtual environment (venv)
- Docker (optional)

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/HabeshaCare/ChatBotServer.git
   cd ChatBotServer
   ```

2. **Run Setup Script:**
   Execute the setup script to install dependencies and set up the virtual environment.
   ```bash
   ./setup
   ```
   The server will run on `http://localhost:5000`.

## Using Docker (Alternative)

Alternatively, you can use Docker to run the server:

1. **Build Docker Image:**
   ```bash
   docker build -t chatbotserver .
   ```

2. **Run Docker Container:**
   ```bash
   docker run -p 5000:5000 chatbotserver
   ```

   The server will run on `http://localhost:5000`.

## Asking LLM

The server exposes a single endpoint to ask the LLM:

- **Endpoint:** `/ask`
- **Method:** POST
- **Usage:** Send a POST request to `http://localhost:5000/ask` with a JSON payload containing the question.
   Example:
   ```json
   {
       "query": "What is the meaning of life?"
   }
   ```

   The server will respond with the LLM's answer.

---
