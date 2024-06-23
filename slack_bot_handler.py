from qa import CustomQAChain
import os
import logging
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
import requests
import warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('slack_handler')


SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
event_id_set = set()

slack_client = WebClient(token=SLACK_BOT_TOKEN)
socket_mode_client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=slack_client)
bot_user_id = slack_client.auth_test()['user_id']

cqa = CustomQAChain()
app = Flask(__name__)

def download_file(file):
    """
        Downloads the pdf file to the local directory.
    """
    file_id = file.get('id')
    result = slack_client.files_info(file=file_id)
    file_url = result['file']['url_private_download']

    response = requests.get(file_url, headers={'Authorization': 'Bearer %s' % SLACK_BOT_TOKEN})
    pdf_content = response.content
    
    with open("downloaded_file.pdf", "wb") as f:
        f.write(pdf_content)

@app.route('/slack/events', methods=['POST'])
def slack_handler():

    """
        Handles slack events, gathers response from gpt and posts it on slack channel.
    """

    event = request.json
    event_id = event['event_id']
    event_data = event['event']

    if event_data.get('user') == bot_user_id or event_id in event_id_set:
        return jsonify({'status': 'ok'})
    else:
        try:

            filee = None
            event_id_set.add(event_id)
            questions = event_data.get('text').split(',')
            files = event_data.get('files')

            filee = files[0] if files else None

            if filee and filee.get('filetype') == 'pdf':

                download_file(filee)
            
                docs = cqa.load_pdf()
                cqa.create_collection(docs)
                contexts = cqa.query_collection(questions)
                response = cqa.call_gpt(questions, contexts)

                slack_client.chat_postMessage(
                                    channel=event_data['channel'],
                                    text= f'{str(response)}'
                            )
                return jsonify({'status': 'ok'})
            else:
                logger.info(f"No files found or No pdf file found")
                return jsonify({'status': "ok"})
                
        except Exception as e:
            logger.error(f"Error handling the event: {e}")
            return jsonify({'status': 'Event Handler ERROR'})


if __name__ == '__main__':
    app.run(port= 5000)


