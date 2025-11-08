from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.before_request
def log_request():
    """Log each incoming request with method and path"""
    logger.info(f"{request.method} {request.path}")


@app.route('/events/transaction', methods=['POST'])
def transaction_event():
    """Stub endpoint for transaction events"""
    return jsonify({"transaction_id": "mock123"}), 200


@app.route('/notifications/reply', methods=['POST'])
def notification_reply():
    """Stub endpoint for notification replies"""
    return jsonify({"ok": True}), 200


@app.route('/user/<user_id>/summary', methods=['GET'])
def user_summary(user_id):
    """Stub endpoint for user summary"""
    return jsonify({"recent": [], "predictions": {}}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
