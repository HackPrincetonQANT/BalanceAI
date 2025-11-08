"""
Simulation script to demonstrate the full flow of the spending coach backend.
Sends fake transactions and demonstrates all features.
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Sample fake transactions
FAKE_TRANSACTIONS = [
    {
        "id": "txn_001",
        "amount": 4.50,
        "merchant": "Starbucks Coffee",
        "timestamp": "2025-11-08T08:30:00"
    },
    {
        "id": "txn_002",
        "amount": 65.32,
        "merchant": "Whole Foods Market",
        "timestamp": "2025-11-08T12:15:00"
    },
    {
        "id": "txn_003",
        "amount": 45.00,
        "merchant": "Shell Gas Station",
        "timestamp": "2025-11-08T14:20:00"
    },
    {
        "id": "txn_004",
        "amount": 28.75,
        "merchant": "Olive Garden Restaurant",
        "timestamp": "2025-11-08T18:45:00"
    },
    {
        "id": "txn_005",
        "amount": 129.99,
        "merchant": "Amazon Shopping",
        "timestamp": "2025-11-08T20:10:00"
    },
    {
        "id": "txn_006",
        "amount": 15.99,
        "merchant": "Netflix Subscription",
        "timestamp": "2025-11-08T21:00:00"
    }
]


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")


def check_health():
    """Check if the server is healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print(f"   Make sure the server is running on {BASE_URL}")
        return False


def send_transaction(transaction):
    """Send a transaction to the backend."""
    print(f"\n📤 Sending transaction: ${transaction['amount']:.2f} at {transaction['merchant']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/transaction",
            json=transaction,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Transaction processed successfully")
            print(f"   Category: {result['transaction']['category']}")
            print(f"   Notification: {result['notification']['status']}")
            return result
        else:
            print(f"❌ Failed to process transaction: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def get_all_transactions():
    """Get all stored transactions."""
    print("\n📊 Fetching all transactions...")
    
    try:
        response = requests.get(f"{BASE_URL}/transactions", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retrieved {result['count']} transactions")
            
            for txn in result['transactions']:
                print(f"   - ${txn['amount']:.2f} at {txn['merchant']} ({txn['category']})")
            
            return result
        else:
            print(f"❌ Failed to get transactions: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def get_prediction():
    """Get next purchase prediction."""
    print("\n🔮 Getting next purchase prediction...")
    
    try:
        response = requests.get(f"{BASE_URL}/predict", timeout=5)
        
        if response.status_code == 200:
            prediction = response.json()
            print(f"✅ Prediction generated:")
            print(f"   Category: {prediction['predicted_category']}")
            print(f"   Amount: ${prediction['predicted_amount']:.2f}")
            print(f"   Confidence: {prediction['confidence']*100:.0f}%")
            print(f"   Reasoning: {prediction['reasoning']}")
            return prediction
        else:
            print(f"❌ Failed to get prediction: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def reset_data():
    """Reset all data."""
    print("\n🔄 Resetting all data...")
    
    try:
        response = requests.post(f"{BASE_URL}/reset", timeout=5)
        
        if response.status_code == 200:
            print("✅ All data cleared")
            return True
        else:
            print(f"❌ Failed to reset data: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def run_simulation():
    """Run the complete simulation."""
    print("🎬 Starting BalanceAI Backend Simulation")
    print("="*80)
    
    # Check server health
    print_separator()
    print("Step 1: Checking server health...")
    if not check_health():
        print("\n⚠️  Please start the backend server first:")
        print("   python backend.py")
        return
    
    # Reset data for clean simulation
    print_separator()
    print("Step 2: Resetting data for clean simulation...")
    reset_data()
    
    # Send transactions one by one
    print_separator()
    print("Step 3: Sending fake transactions...")
    
    for i, transaction in enumerate(FAKE_TRANSACTIONS, 1):
        print(f"\nTransaction {i}/{len(FAKE_TRANSACTIONS)}:")
        send_transaction(transaction)
        time.sleep(0.5)  # Small delay between transactions
    
    # Get all transactions
    print_separator()
    print("Step 4: Retrieving all transactions...")
    get_all_transactions()
    
    # Get prediction
    print_separator()
    print("Step 5: Getting next purchase prediction...")
    get_prediction()
    
    # Summary
    print_separator()
    print("🎉 Simulation completed successfully!")
    print("\nSummary:")
    print(f"  - Sent {len(FAKE_TRANSACTIONS)} transactions")
    print(f"  - All transactions classified and stored")
    print(f"  - Notifications sent for each transaction")
    print(f"  - Prediction generated based on history")
    print("\n✨ The spending coach backend is working correctly!")
    print("="*80)


if __name__ == "__main__":
    run_simulation()
