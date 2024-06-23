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
- Navigate to "OAuth & Permissions" in the features section present in sidebar. Scroll down to "Scopes" and add the following bot token scopes
  
  - ```chat:write```  = to post messages.
  - ```files:read```  = to read files.
  - ```files:write``` = to write messages.
  - ```app_mentions:read```  = to read messages that directly mention the bot.
  - ```channels:history``` = view messages and other content in public channels that the bot has been added to.
- Scroll up and install the app to your workspace. Copy the OAuth token provided. Then Click allow.
- Click on event subscriptions in the sidebar and turn on the Enable events toggle.
- Enter your ngrok URL in the request URL followed by '/slack/events' like given below ```https://your_public_ngrok_url/slack/events``` and get it verified by returning the challenge request from your Flask app. (slack_bot_handler.py)
- Scroll down to 'Subscribe to bot events' and Add the following Bot user events.
  - ```app_mention```  = Subscibe to message events that mentions your bot.
  - ```message.channels```  = Subscibe to messages posted on your channels.
  - ```message.groups``` = Subscibe to messages posted on your channels.
- Go to "Socket Mode" in your app settings and enable it. Generate an App-Level Token with the scope ```connections:write``` and copy it.
- Save changes and reinstall the app into the workspace.

### 4. Running the bot
- Enter your contents in the .env file. The .env file must look like below after finishing your entries.
  ```shell script
  OPENAI_API_KEY = "your_openai_key"
  SLACK_BOT_TOKEN = "your_slack_app_oauth_token"
  SLACK_APP_TOKEN = "your_slack_applevel_token"
  ```
- Run the Flask server.
  ```shell script
  python slack_bot_handler.py
  ```
  Note: The Flask app's port must match your ngrok URL's port.
- Go to your Slack and in one of your channels invite the pdf bot to the channel.
  ```shell script
  /invite @your_bot_name
  ```
- Upload a PDF file and ask a question in your Slack workspace. The bot should respond with answers.
  Note: If you do not see any results, or facing issues try restarting the Flask server.
  
  
  
