from flask import Flask
from app.webhook_listener import webhook

app = Flask(__name__)
app.register_blueprint(webhook)
