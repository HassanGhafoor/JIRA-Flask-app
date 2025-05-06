from flask import Blueprint, request, jsonify
import requests
import boto3

webhook = Blueprint('webhook', __name__)

def get_secret_from_ssm(param_name):
    ssm = boto3.client('ssm', region_name='eu-north-1')
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response['Parameter']['Value']

@webhook.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'pull_request' and data['action'] == 'opened':
        title = data['pull_request']['title']
        user = data['pull_request']['user']['login']

        jira_url = "https://hassanghafoortts.atlassian.net/rest/api/2/issue"
        jira_user = get_secret_from_ssm('/jira/user')
        jira_token = get_secret_from_ssm('/jira/token')
        project_key = "SCRUM"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": f"PR Opened by {user}: {title}",
                "description": "Automatically created from GitHub webhook",
                "issuetype": {"name": "Task"}
            }
        }

        response = requests.post(jira_url, json=payload, auth=(jira_user, jira_token), headers=headers)

        if response.status_code == 201:
            return jsonify({"message": "Jira issue created"}), 201
        else:
            return jsonify({"error": response.text}), 400

    return jsonify({"message": "Ignored event"}), 200
