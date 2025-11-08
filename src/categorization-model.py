import asyncio
import json
import os
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

# Define predefined product categories
CATEGORIES = [
    "Electronics",
    "Home & Kitchen",
    "Clothing & Accessories",
    "Sports & Outdoors",
    "Health & Beauty",
    "Pet Supplies",
    "Office Products",
    "Toys & Games",
    "Grocery & Food",
    "Home Improvement",
    "Miscellaneous"
]

async def categorize_product(runner, product_name):
    """
    Categorize a single product using Dedalus AI with structured JSON output.

    Expected input: Product name string
    Expected output: Dict with category, confidence, reason, ask_user fields
    """
    prompt = f"""You are a product taxonomy classifier. Map the product to exactly one category from this list:

{", ".join(CATEGORIES)}

Rules:
- Choose the most specific fit among the list (do NOT invent new categories).
- If multiple plausible categories exist, pick the one that best reflects the primary intended use.
- If confidence < 0.6, output "Miscellaneous" and set ask_user=true.
- Never include brand names or marketing fluff in the category.

Product to categorize: {product_name}

Return ONLY valid JSON:
{{
  "category": "<one of the categories above>",
  "confidence": <float 0..1>,
  "reason": "<=12 words, short why",
  "ask_user": <true|false>
}}"""

    response = await runner.run(
        input=prompt,
        model="openai/gpt-5-mini"
    )

    # Parse JSON response
    try:
        result = json.loads(response.final_output)
        return result
    except json.JSONDecodeError:
        # Fallback if model doesn't return valid JSON
        return {
            "category": "Miscellaneous",
            "confidence": 0.0,
            "reason": "Failed to parse response",
            "ask_user": True
        }

async def main():
    """
    Load Amazon mock data and categorize all products using Dedalus AI.

    Expected input: JSON file with Amazon transactions containing products
    Expected output: Category classification for all products with confidence scores
    """
    # Load JSON data
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'simplify_mock_amazon.json')

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Initialize Dedalus client
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    # Track results
    all_results = []
    total_products = sum(len(transaction['products']) for transaction in data['transactions'])

    print(f"Processing {total_products} products across {len(data['transactions'])} transactions...")
    print("=" * 80)

    # Loop through all transactions and products
    for transaction in data['transactions']:
        transaction_id = transaction['id']

        for product in transaction['products']:
            product_name = product['name']
            product_price = product['price']['total']

            print(f"\nTransaction: {transaction_id}")
            print(f"Product: {product_name}")
            print(f"Price: ${product_price}")

            # Categorize product
            result = await categorize_product(runner, product_name)

            # Display result
            print(f"Category: {result['category']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Reason: {result['reason']}")
            if result['ask_user']:
                print("⚠️  LOW CONFIDENCE - Manual review recommended")
            print("-" * 80)

            # Store result
            all_results.append({
                "transaction_id": transaction_id,
                "product_name": product_name,
                "price": product_price,
                **result
            })

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total products processed: {len(all_results)}")

    # Count by category
    category_counts = {}
    for result in all_results:
        category = result['category']
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\nProducts by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")

    # Flag low confidence items
    low_confidence = [r for r in all_results if r['ask_user']]
    if low_confidence:
        print(f"\n⚠️  {len(low_confidence)} product(s) flagged for manual review")

if __name__ == "__main__":
    asyncio.run(main())