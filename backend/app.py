# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# AWS credentials and Q App ID
# ACCESS_KEY = 'XXX'
ACCESS_KEY = 'XXX'
# SECRET_KEY = 'XXX+XX'
SECRET_KEY = 'XXX'
# APP_ID = 'XXX'
APP_ID = 'XXXX'

client = boto3.client(
    'qbusiness',
    region_name='us-east-1',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message', '').strip()
    files      = request.files.getlist('attachments')

    # Build base parameters
    params = {
        "applicationId": APP_ID,
        "userMessage":  user_input
    }

    # If there's at least one file, add attachments and Creator mode
    if files and any(f.filename for f in files):
        attachments = []
        for f in files:
            attachments.append({
                "name": f.filename,
                "data": f.read()
            })
        params["attachments"] = attachments
        params["chatMode"]    = "CREATOR_MODE"

    try:
        resp = client.chat_sync(**params)
    except Exception as e:
        return jsonify({'reply': f'Backend error: {e}'}), 500

    # In Creator mode, systemMessage.content holds the answer
    sys_msg = resp.get('systemMessage', {})
    if isinstance(sys_msg, dict):
        reply = sys_msg.get('content', '[No content returned]')
    else:
        # sometimes systemMessage is a string
        reply = sys_msg or '[No response returned]'

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(port=5000)
