# RAG-based Customer Complaint Chatbot

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** based chatbot that:

- Interacts with customers to collect complaint details in a natural conversational flow.
- Creates complaint records using a RESTful API.
- Generates a unique complaint ID for each complaint.
- Retrieves complaint details when provided with a complaint ID.
- Provides contextual answers using a knowledge base (e.g. customer service policies, FAQs).

---

## Folder Struture

1. chatbot.py # Chatbot logic (RAG, conversation flow with api calling)
2. main.py # FastAPI app for complaint API routes
3. rag.py # Sample text files for RAG knowledge base
4. models.py # DB models and connection setup (SQLite)
5. test.py # Testing chatbot 
6. requirements.txt # Python dependencies


## Steps to try it out:

# Clone the Repository
- git clone https://github.com/pranaybobde/rag_chat_bot_customer_service.git
- cd rag_chat_bot_customer_service

# Install UV virtual Environment
- curl -LsSf https://astral.sh/uv/install.sh | sh   # Install uv for macos/ubuntu
- powershell -c "irm https://astral.sh/uv/install.ps1 | more"   # Install for windows

# Create virtual Environment
- uv venv leo
- source venv/bin/activate   # Linux/macOS
- venv\Scripts\activate      # Windows

# Install Dependencies
- pip install -r requirements.txt

# Run main.py
- python main.py    # For complaint registration and details fetching routes

# Run test.py
- python test.py    # For testing end-to-end chatbot with complaint registration and details fetching

# Interact with Bot
- http://0.0.0.0:8005/static/index.html  (after running main.py and test.py server)
