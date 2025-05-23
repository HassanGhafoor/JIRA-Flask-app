from flask import Flask
from app.webhook_listener import webhook

app = Flask(__name__)
app.register_blueprint(webhook)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
