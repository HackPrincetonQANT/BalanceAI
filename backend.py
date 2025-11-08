"""
Minimal backend for a real-time spending coach.
Provides endpoints for transaction processing, classification, and notifications.
"""
from flask import Flask, request, jsonify
from datetime import datetime
from typing import List, Dict, Any
import random

app = Flask(__name__)

# In-memory storage for transactions
transactions: List[Dict[str, Any]] = []


def classify_transaction(transaction: Dict[str, Any]) -> str:
    """
    Placeholder agent function to classify transactions.
    
    Args:
        transaction: Transaction data containing amount, merchant, etc.
    
    Returns:
        str: Category of the transaction
    """
    # Simple rule-based classification (placeholder for AI agent)
    merchant = transaction.get('merchant', '').lower()
    amount = transaction.get('amount', 0)
    
    # Check groceries first (before more general food-related terms)
    if any(word in merchant for word in ['grocery', 'supermarket', 'whole foods', 'trader joe', 'safeway', 'kroger', 'publix']):
        return 'groceries'
    # Check dining/restaurants
    elif any(word in merchant for word in ['restaurant', 'cafe', 'coffee', 'food', 'dine', 'dining', 'starbucks', 'mcdonald', 'burger', 'pizza', 'kitchen', 'grill', 'garden', 'bistro', 'tavern']):
        return 'dining'
    # Check transportation
    elif any(word in merchant for word in ['gas', 'fuel', 'shell', 'exxon', 'chevron', 'bp', 'mobil']):
        return 'transportation'
    # Check entertainment
    elif any(word in merchant for word in ['netflix', 'spotify', 'subscription', 'hulu', 'disney', 'prime video', 'apple tv']):
        return 'entertainment'
    # Check shopping (should be after more specific categories)
    elif any(word in merchant for word in ['amazon', 'store', 'shop', 'target', 'walmart', 'mall']):
        return 'shopping'
    else:
        return 'other'


def send_imessage_notification(message: str, transaction: Dict[str, Any]) -> Dict[str, str]:
    """
    Mock function to send iMessage-style notifications.
    
    Args:
        message: Notification message to send
        transaction: Transaction data that triggered the notification
    
    Returns:
        dict: Notification status
    """
    # Mock notification - in production, this would integrate with push notification service
    notification = {
        'status': 'sent',
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'recipient': 'user@example.com',
        'transaction_id': transaction.get('id', 'unknown')
    }
    
    print(f"📱 iMessage Notification: {message}")
    print(f"   Transaction: ${transaction.get('amount', 0):.2f} at {transaction.get('merchant', 'Unknown')}")
    
    return notification


def predict_next_purchase() -> Dict[str, Any]:
    """
    Simple prediction function for next purchase.
    
    Returns:
        dict: Predicted next purchase details
    """
    if not transactions:
        return {
            'predicted_category': 'unknown',
            'predicted_amount': 0.0,
            'confidence': 0.0,
            'reasoning': 'No transaction history available'
        }
    
    # Simple prediction based on most common category and average amount
    categories = [t.get('category', 'other') for t in transactions]
    amounts = [t.get('amount', 0) for t in transactions]
    
    # Find most common category
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    most_common_category = max(category_counts, key=category_counts.get)
    
    # Calculate average amount for that category
    category_amounts = [t.get('amount', 0) for t in transactions 
                       if t.get('category') == most_common_category]
    avg_amount = sum(category_amounts) / len(category_amounts) if category_amounts else 0
    
    return {
        'predicted_category': most_common_category,
        'predicted_amount': round(avg_amount, 2),
        'confidence': round(category_counts[most_common_category] / len(transactions), 2),
        'reasoning': f'Based on {len(transactions)} transactions, {most_common_category} is your most frequent category'
    }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/transaction', methods=['POST'])
def accept_transaction():
    """
    Accept and process a transaction.
    
    Expected JSON format:
    {
        "id": "txn_123",
        "amount": 45.50,
        "merchant": "Starbucks",
        "timestamp": "2025-11-08T10:30:00"
    }
    """
    try:
        transaction_data = request.get_json()
        
        if not transaction_data:
            return jsonify({'error': 'No transaction data provided'}), 400
        
        # Validate required fields
        required_fields = ['amount', 'merchant']
        for field in required_fields:
            if field not in transaction_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add metadata
        transaction_data['id'] = transaction_data.get('id', f"txn_{len(transactions) + 1}")
        transaction_data['timestamp'] = transaction_data.get('timestamp', datetime.now().isoformat())
        
        # Classify the transaction
        category = classify_transaction(transaction_data)
        transaction_data['category'] = category
        
        # Store in memory
        transactions.append(transaction_data)
        
        # Send notification
        notification_message = f"💰 New {category} transaction: ${transaction_data['amount']:.2f} at {transaction_data['merchant']}"
        notification_result = send_imessage_notification(notification_message, transaction_data)
        
        return jsonify({
            'status': 'success',
            'transaction': transaction_data,
            'notification': notification_result
        }), 201
        
    except Exception as e:
        # Don't expose internal error details to avoid information leakage
        app.logger.error(f"Error processing transaction: {str(e)}")
        return jsonify({'error': 'Failed to process transaction'}), 500


@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all stored transactions."""
    return jsonify({
        'count': len(transactions),
        'transactions': transactions
    })


@app.route('/predict', methods=['GET'])
def predict():
    """Get prediction for next purchase."""
    prediction = predict_next_purchase()
    return jsonify(prediction)


@app.route('/reset', methods=['POST'])
def reset_data():
    """Reset all stored transactions (for testing)."""
    global transactions
    transactions = []
    return jsonify({'status': 'success', 'message': 'All transactions cleared'})


if __name__ == '__main__':
    print("🚀 Starting BalanceAI Backend Server...")
    print("📊 Endpoints available:")
    print("  POST /transaction - Accept and process transactions")
    print("  GET  /transactions - View all transactions")
    print("  GET  /predict - Get next purchase prediction")
    print("  GET  /health - Health check")
    print("  POST /reset - Clear all data")
    print("\n⚠️  WARNING: Running in development mode. Do not use in production!")
    app.run(host='0.0.0.0', port=5000, debug=True)
