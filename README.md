# BalanceAI

A minimal backend for a real-time spending coach that processes transactions, classifies them, and sends notifications.

## Features

- 💳 **Transaction Processing**: Accept and process transaction data via REST API
- 🤖 **Automatic Classification**: Classify transactions into categories (dining, groceries, transportation, etc.)
- 💾 **In-Memory Storage**: Store transaction history for analysis
- 📱 **Mock Notifications**: Send iMessage-style notifications for each transaction
- 🔮 **Purchase Prediction**: Predict next purchase category and amount based on history

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the Backend Server

```bash
python backend.py
```

The server will start on `http://localhost:5000`

### Run the Simulation

In a separate terminal, run the simulation script to test the full flow:

```bash
python simulate.py
```

This will:
1. Check server health
2. Send 6 fake transactions
3. Retrieve all stored transactions
4. Generate a prediction for the next purchase

### Run the Example Usage Script

For a more detailed demonstration with comprehensive output:

```bash
python example_usage.py
```

This script showcases:
- All API endpoints with detailed responses
- Transaction classification examples
- Error handling
- Category breakdown and analytics
- Purchase predictions

## API Endpoints

### POST /transaction
Accept and process a new transaction.

**Request Body:**
```json
{
  "id": "txn_123",
  "amount": 45.50,
  "merchant": "Starbucks",
  "timestamp": "2025-11-08T10:30:00"
}
```

**Response:**
```json
{
  "status": "success",
  "transaction": {
    "id": "txn_123",
    "amount": 45.50,
    "merchant": "Starbucks",
    "category": "dining",
    "timestamp": "2025-11-08T10:30:00"
  },
  "notification": {
    "status": "sent",
    "message": "💰 New dining transaction: $45.50 at Starbucks"
  }
}
```

### GET /transactions
Retrieve all stored transactions.

**Response:**
```json
{
  "count": 3,
  "transactions": [...]
}
```

### GET /predict
Get a prediction for the next purchase.

**Response:**
```json
{
  "predicted_category": "dining",
  "predicted_amount": 35.25,
  "confidence": 0.45,
  "reasoning": "Based on 6 transactions, dining is your most frequent category"
}
```

### GET /health
Health check endpoint.

### POST /reset
Clear all stored transactions (for testing).

## Architecture

- **Backend Server** (`backend.py`): Flask-based REST API server
- **Transaction Classifier**: Rule-based placeholder for AI agent classification
- **Notification System**: Mock iMessage-style notification function
- **Prediction Engine**: Simple prediction based on transaction history
- **Simulation Script** (`simulate.py`): Demonstrates the complete flow

## Example Transaction Categories

The classifier recognizes the following categories:
- `dining` - Restaurants, cafes, food establishments
- `groceries` - Supermarkets and grocery stores
- `transportation` - Gas stations and fuel
- `shopping` - Retail stores and online shopping
- `entertainment` - Streaming services and subscriptions
- `other` - Uncategorized transactions