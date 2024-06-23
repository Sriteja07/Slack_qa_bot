# Slack QA Bot
An AI-powered Slack bot for PDF Querying.

This repo provides an AI-powered Slack bot that allows users to upload PDF documents and ask questions. The bot processes the PDFs and retrieves answers based on the provided context using OpenAI's GPT-3.5 model.

## Features

- Upload PDF documents directly in a Slack channel containing the bot
- Ask questions about the content of the PDF
- Get accurate and context-based answers

## Setup

### 1. Code Setup
- 1. Clone the Repository
     
  ```shell script
  git clone https://github.com/Sriteja07/Slack_qa_bot.git
  cd Slack_qa_bot
  ```
  
- 2. Create and activate a virtual environment
     
  ```shell script
  python3 -m venv venv
  source  venv\Scripts\activate
  ```
  
- 3. Install dependencies
     
  ```shell script
  pip install -r requirements.txt
  ```

### 2. Server Setup
- 1. Download the ngrok from [here](https://ngrok.com/download)
- 2. Get your authtoken from [here](https://dashboard.ngrok.com/get-started/your-authtoken)
- 3. Open your ngrok shell and config your authtoken like below
     ```shell script
       ngrok config add-authtoken $YOUR_AUTHTOKEN
       ```
     
  


