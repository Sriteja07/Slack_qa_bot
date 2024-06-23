# Slack QA Bot
An AI-powered Slack bot for PDF Querying.

This repo provides an AI-powered Slack bot that allows users to upload PDF documents and ask questions. The bot processes the PDFs and retrieves answers based on the provided context using OpenAI's GPT-3.5 model.

## Features

- Upload PDF documents directly in a Slack channel containing the bot
- Ask questions about the content of the PDF
- Get accurate and context-based answers

## Setup

### 1. Code Setup
- Clone the Repository
     
  ```shell script
  git clone https://github.com/Sriteja07/Slack_qa_bot.git
  cd Slack_qa_bot
  ```
  
- Create and activate a virtual environment
     
  ```shell script
  python3 -m venv venv
  source  venv\Scripts\activate
  ```
  
- Install dependencies
     
  ```shell script
  pip install -r requirements.txt
  ```

### 2. Server Setup
- Download the ngrok from [here](https://ngrok.com/download)
- Get your authtoken from [here](https://dashboard.ngrok.com/get-started/your-authtoken)
- Open your ngrok shell and config your authtoken like below
     ```shell script
       ngrok config add-authtoken $YOUR_AUTHTOKEN
     ```
- Start ngrok on the new port
     ```shell script
       ngrok http 127.0.0.1:your-port
     ```
     This will provide you with a public URL and it is needed while setting up the Event Subscription settings of the Slack Bot. Copy it and save it.

Note: First three steps are not necessary if you have already downloaded and configured ngrok in your system.

### 3. Slack Setup
- Navigate to the [Slack API site](https://api.slack.com/apps) and click 'Create New App".
- Choose "From Scratch" and provide a name for the app, and select the workspace where you want to install it.
- Navigate to "OAuth & Permissions" in the features section present in sidebar. Scroll down to "scopes: and add the following bot token scopes
  
  - ```chat:write```  = to post messages.
  - ```files:read```  = to read files.
  - ```files:write``` = to write messages.
  - ```app_mentions:read```  = to read messages that directly mention the bot.
  - ```channels:history``` = view messages and other content in public channels that the bot has been added to.
  
     
  


