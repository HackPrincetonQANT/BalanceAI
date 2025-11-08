"""
Example usage script showing all backend features with detailed output.
This demonstrates manual API calls and showcases the full capabilities.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print('='*70)


def print_json(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))


def main():
    print_header("🚀 BalanceAI Backend - Feature Demonstration")
    
    # Example 1: Health Check
    print_header("1️⃣  Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print_json(response.json())
    
    # Example 2: Reset Data
    print_header("2️⃣  Reset Data (Clean Slate)")
    response = requests.post(f"{BASE_URL}/reset")
    print(f"Status Code: {response.status_code}")
    print_json(response.json())
    
    # Example 3: Send a transaction
    print_header("3️⃣  Send Transaction #1 - Coffee Shop")
    transaction = {
        "amount": 5.75,
        "merchant": "Starbucks Coffee",
        "timestamp": datetime.now().isoformat()
    }
    response = requests.post(
        f"{BASE_URL}/transaction",
        json=transaction,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status Code: {response.status_code}")
    print_json(response.json())
    
    # Example 4: Send another transaction
    print_header("4️⃣  Send Transaction #2 - Grocery Store")
    transaction = {
        "id": "custom_txn_001",
        "amount": 89.45,
        "merchant": "Whole Foods Market"
    }
    response = requests.post(
        f"{BASE_URL}/transaction",
        json=transaction,
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status Code: {response.status_code}")
    print_json(response.json())
    
    # Example 5: Send more transactions for better predictions
    print_header("5️⃣  Send Multiple Transactions")
    transactions = [
        {"amount": 12.50, "merchant": "McDonald's Restaurant"},
        {"amount": 35.20, "merchant": "Olive Garden"},
        {"amount": 45.00, "merchant": "Shell Gas Station"},
        {"amount": 19.99, "merchant": "Netflix"},
    ]
    
    for txn in transactions:
        response = requests.post(
            f"{BASE_URL}/transaction",
            json=txn,
            headers={'Content-Type': 'application/json'}
        )
        result = response.json()
        print(f"✅ ${txn['amount']:.2f} at {txn['merchant']} -> {result['transaction']['category']}")
    
    # Example 6: Get all transactions
    print_header("6️⃣  View All Transactions")
    response = requests.get(f"{BASE_URL}/transactions")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total Transactions: {data['count']}\n")
    
    for i, txn in enumerate(data['transactions'], 1):
        print(f"{i}. ${txn['amount']:>7.2f} | {txn['merchant']:<30} | {txn['category']:<15} | {txn['id']}")
    
    # Example 7: Get prediction
    print_header("7️⃣  Next Purchase Prediction")
    response = requests.get(f"{BASE_URL}/predict")
    print(f"Status Code: {response.status_code}")
    prediction = response.json()
    print_json(prediction)
    print(f"\n💡 Insight: {prediction['reasoning']}")
    
    # Example 8: Error handling - Missing field
    print_header("8️⃣  Error Handling Demo - Missing Field")
    response = requests.post(
        f"{BASE_URL}/transaction",
        json={"amount": 10.00},  # Missing merchant
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status Code: {response.status_code}")
    print_json(response.json())
    
    # Example 9: Category breakdown
    print_header("9️⃣  Category Breakdown")
    response = requests.get(f"{BASE_URL}/transactions")
    data = response.json()
    
    categories = {}
    for txn in data['transactions']:
        cat = txn['category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'total': 0}
        categories[cat]['count'] += 1
        categories[cat]['total'] += txn['amount']
    
    print(f"{'Category':<20} {'Count':<10} {'Total Spent':<15} {'Avg/Transaction'}")
    print("-" * 70)
    for cat, stats in sorted(categories.items(), key=lambda x: x[1]['total'], reverse=True):
        avg = stats['total'] / stats['count']
        print(f"{cat:<20} {stats['count']:<10} ${stats['total']:<14.2f} ${avg:.2f}")
    
    print_header("✨ Demo Complete!")
    print("All features demonstrated successfully!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the backend server")
        print("Please make sure the server is running:")
        print("  python backend.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
