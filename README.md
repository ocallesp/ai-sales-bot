# AI Sales Bot

## Overview
AI Sales Bot is a full-stack web application that provides an interactive chat interface for customers to inquire about products, while offering an admin dashboard to analyze user sentiment and manage inventory. The project features a chatbot powered by natural language processing (NLP) to detect user sentiment and respond with product information, alongside an admin panel for monitoring user interactions and updating products. This application was built in a few hours using prompt engineering to accelerate development, demonstrating rapid prototyping with AI assistance.

## Features
- **Customer Chat Interface**: Users can ask about products (e.g., "Do you have a laptop?"), and the bot responds with product details and applicable discounts.
- **Sentiment Analysis**: The bot analyzes user messages for sentiment (positive, neutral, negative) using an NLP model.
- **Admin Dashboard**:
  - Displays monthly sentiment analysis of user messages.
  - Lists all chat messages with timestamps and sentiments.
  - Shows the current product inventory.
  - Allows adding new products via a form.
- **Authentication**: The admin dashboard is protected with basic HTTP authentication.
- **Responsive UI**: Built with Angular Material for a clean and user-friendly interface.

## Technologies Used
- **Frontend**:
  - Angular (TypeScript) for the client-side application.
  - Angular Material for UI components.
- **Backend**:
  - FastAPI (Python) for the API server.
  - SQLite for the database.
  - Transformers.py (Hugging Face) for sentiment analysis using the `distilbert-base-uncased-finetuned-sst-2-english` model.
- **Version Control**:
  - Git for source code management.

## Project Structure