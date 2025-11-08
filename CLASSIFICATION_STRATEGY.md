# Classification Strategy - Multi-Source Ensemble Approach

**Core Philosophy:** Do ONE thing exceptionally well - transaction classification
**Method:** Use multiple classification sources and combine intelligently

---

## Why This Approach?

### For Hackathon:
- ✅ Shows technical depth (multiple API integrations)
- ✅ Demonstrates ML/AI knowledge (ensemble methods)
- ✅ Impressive accuracy through validation
- ✅ One polished feature > many half-baked features
- ✅ Clear demo narrative: "Our AI is 95% accurate because..."

### Real-World Benefits:
- Higher accuracy through consensus
- Fallback if one service fails
- Can compare/validate results
- Learn which methods work best
- Build confidence scores

---

## Classification Pipeline Architecture

### Level 1: Primary Classification (Fast)
```
Transaction → Rule-Based Engine → Quick Classification
             (< 100ms)            {need_or_want, confidence}
```

**Rule-Based Engine:**
```python
ALWAYS_NEED = ["Grocery", "Gas", "Utilities", "Healthcare", "Rent"]
ALWAYS_WANT = ["Entertainment", "Dining", "Coffee", "Shopping"]
AMOUNT_THRESHOLDS = {
    "Coffee": 10.00,  # > $10 coffee probably special
    "Dining": 50.00   # > $50 dining probably date night
}
```

**Use for:**
- Obvious categories (utilities = need)
- Training data collection
- Fallback if APIs fail

---

### Level 2: AI Classification (Dedalus MCP)
```
Transaction → Dedalus MCP Server → AI Classification
             (200-500ms)           {need_or_want, reasoning, confidence}
```

**Dedalus MCP Call:**
```python
{
  "tool": "classify_transaction",
  "model": "claude-3-5-sonnet-20241022",
  "prompt": """
    Classify this transaction as NEED or WANT:

    Merchant: Starbucks
    Amount: $5.25
    Category: Coffee/Cafe
    Time: Weekday 8:30 AM

    Context:
    - User's recent patterns: [3 coffee purchases this week]
    - Location: Near office

    NEED = Essential for daily life/work
    WANT = Discretionary, could be skipped

    Return JSON:
    {
      "need_or_want": "need" or "want",
      "confidence": 0.0-1.0,
      "reasoning": "brief explanation",
      "category": "specific category"
    }
  """
}
```

---

### Level 3: Alternative AI Sources (Validation)

**Option A: OpenAI Direct Call**
```python
import openai

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[{
    "role": "system",
    "content": "You are a financial advisor. Classify transactions as NEED or WANT."
  }, {
    "role": "user",
    "content": f"Starbucks, $5.25, weekday morning. NEED or WANT?"
  }]
)
```

**Option B: Another MCP Server**
- Financial classification MCP (if exists)
- Custom fine-tuned model
- Open-source local model

**Option C: Historical Pattern Matching**
```python
def classify_by_history(merchant, category, user_id):
    """Look at user's past replies for this merchant/category"""
    past_labels = get_user_labels(user_id, merchant=merchant)

    if len(past_labels) >= 3:
        # User has labeled this merchant before
        most_common = mode(past_labels)
        confidence = past_labels.count(most_common) / len(past_labels)
        return {"need_or_want": most_common, "confidence": confidence}

    return None  # Not enough data
```

---

### Level 4: Ensemble Decision

**Ensemble Strategy Options:**

**1. Weighted Voting (Recommended)**
```python
def ensemble_classification(transaction, user_id):
    results = []

    # Get classifications from multiple sources
    rule_result = rule_based_classify(transaction)
    results.append({"source": "rules", "classification": rule_result, "weight": 0.3})

    dedalus_result = dedalus_mcp_classify(transaction)
    results.append({"source": "dedalus", "classification": dedalus_result, "weight": 0.4})

    history_result = classify_by_history(transaction, user_id)
    if history_result:
        results.append({"source": "history", "classification": history_result, "weight": 0.3})

    # Weighted voting
    want_score = sum(r['weight'] for r in results
                     if r['classification']['need_or_want'] == 'want')
    need_score = sum(r['weight'] for r in results
                     if r['classification']['need_or_want'] == 'need')

    final_classification = 'want' if want_score > need_score else 'need'
    final_confidence = max(want_score, need_score)

    return {
        "need_or_want": final_classification,
        "confidence": final_confidence,
        "sources": results,  # For debugging/transparency
        "reasoning": get_best_reasoning(results)
    }
```

**2. Confidence-Based Priority**
```python
def classify_with_confidence_priority(sources):
    """Use highest confidence result if > 0.8, otherwise ensemble"""

    highest_confidence = max(sources, key=lambda x: x['confidence'])

    if highest_confidence['confidence'] > 0.8:
        return highest_confidence  # Trust high-confidence result
    else:
        return weighted_voting(sources)  # Use ensemble for low confidence
```

**3. Consensus Requirement**
```python
def classify_with_consensus(sources):
    """Require 2/3 sources to agree"""

    classifications = [s['classification']['need_or_want'] for s in sources]

    want_count = classifications.count('want')
    need_count = classifications.count('need')

    if want_count >= 2:
        return {'need_or_want': 'want', 'confidence': want_count / len(sources)}
    elif need_count >= 2:
        return {'need_or_want': 'need', 'confidence': need_count / len(sources)}
    else:
        # No consensus - ask user
        return {'need_or_want': 'unknown', 'confidence': 0.5, 'ask_user': True}
```

---

## Recommended Implementation for Hackathon

### Minimal Version (48 hours available):
```
1. Rule-based classifier (2 hours)
   - Simple merchant/category rules
   - Fast fallback

2. Dedalus MCP (6 hours)
   - Primary AI classification
   - Prompt engineering for accuracy

3. Simple ensemble (2 hours)
   - Combine rules + Dedalus
   - Weighted average

Total: ~10 hours of work
```

### Enhanced Version (if time permits):
```
4. Historical pattern matching (3 hours)
   - Learn from user corrections
   - Personalized over time

5. OpenAI backup (2 hours)
   - Validate Dedalus results
   - Use if Dedalus fails

Total: ~15 hours
```

---

## Module Structure

### `src/classification/`
```
classification/
├── __init__.py              # Public API
├── ensemble.py              # Ensemble logic
├── rule_based.py            # Rule engine
├── mcp_classifier.py        # Dedalus MCP calls
├── openai_classifier.py     # OpenAI backup (optional)
├── historical.py            # Pattern matching from user data
└── config.py                # Weights, thresholds, rules
```

### Public API (`classification/__init__.py`)
```python
def classify_transaction(
    merchant: str,
    amount: float,
    category: str,
    user_id: str,
    timestamp: str = None,
    use_ensemble: bool = True
) -> dict:
    """
    Main classification function.

    Returns:
    {
        "need_or_want": "want",
        "category": "Coffee",
        "confidence": 0.91,
        "reasoning": "Daily coffee is discretionary",
        "sources": [
            {"source": "rules", "result": "want", "confidence": 1.0},
            {"source": "dedalus", "result": "want", "confidence": 0.85},
            {"source": "history", "result": "want", "confidence": 0.88}
        ],
        "method": "weighted_ensemble"
    }
    """
```

---

## Demo Value

### What You Can Show Judges:

**1. Accuracy Comparison**
```
Test transaction: Starbucks $5.25

Rules Engine:    "want" (confidence: 1.0)  - Too simplistic
Dedalus MCP:     "want" (confidence: 0.85) - Good reasoning
User History:    "want" (confidence: 0.88) - Personalized
Ensemble:        "want" (confidence: 0.91) - Best of all!

"Our ensemble is 15% more confident than any single source."
```

**2. Fallback Resilience**
```
[Simulate Dedalus timeout during demo]

"Dedalus timed out, but our system still works!
→ Fell back to rules + history
→ Still got classification in 150ms
→ Confidence slightly lower (0.75) but still usable"
```

**3. Learning Over Time**
```
Day 1: Starbucks → AI says "want", user corrects to "need"
Day 2: Starbucks → Ensemble now weights history higher
Day 3: Starbucks → Automatically classified as "need" (personalized!)

"Our system learns from every user correction."
```

---

## Configuration

### `src/classification/config.py`
```python
import os

# Ensemble weights (must sum to 1.0)
ENSEMBLE_WEIGHTS = {
    "rules": float(os.getenv("CLASSIFICATION_WEIGHT_RULES", "0.2")),
    "dedalus": float(os.getenv("CLASSIFICATION_WEIGHT_DEDALUS", "0.5")),
    "openai": float(os.getenv("CLASSIFICATION_WEIGHT_OPENAI", "0.0")),  # Disabled by default
    "history": float(os.getenv("CLASSIFICATION_WEIGHT_HISTORY", "0.3"))
}

# Confidence thresholds
MIN_CONFIDENCE_TO_AUTO_CLASSIFY = 0.7   # Below this, ask user
HIGH_CONFIDENCE_THRESHOLD = 0.85        # Single source can be trusted

# Rule-based definitions
ALWAYS_NEED_CATEGORIES = [
    "Groceries", "Gas & Fuel", "Utilities", "Healthcare",
    "Insurance", "Rent", "Mortgage"
]

ALWAYS_WANT_CATEGORIES = [
    "Entertainment", "Bars & Nightlife", "Hobby Shops",
    "Luxury Goods", "Vacation", "Subscriptions"
]

CONTEXT_RULES = {
    "Coffee": {
        "weekday_morning": 0.6,  # 60% likely a need (work coffee)
        "weekend": 0.1,           # 10% likely a need (treat)
        "expensive": 0.2          # >$8 coffee = special treat
    }
}

# Historical pattern matching
MIN_HISTORY_SAMPLES = 3              # Need 3+ labels to use history
HISTORY_WEIGHT_MULTIPLIER = 1.2      # Give more weight to personalized data

# Dedalus MCP settings
DEDALUS_TIMEOUT = 5                  # Seconds before fallback
DEDALUS_RETRY = 1                    # Retry once on failure

# Demo mode
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
if DEMO_MODE:
    # In demo, show all sources working
    ENSEMBLE_WEIGHTS = {
        "rules": 0.2,
        "dedalus": 0.4,
        "openai": 0.1,
        "history": 0.3
    }
```

---

## Testing Strategy

### Unit Tests
```python
def test_rule_based_classifier():
    result = rule_based_classify("Whole Foods", 45.00, "Groceries")
    assert result["need_or_want"] == "need"
    assert result["confidence"] == 1.0

def test_ensemble_voting():
    sources = [
        {"need_or_want": "want", "confidence": 0.8, "weight": 0.3},
        {"need_or_want": "want", "confidence": 0.9, "weight": 0.5},
        {"need_or_want": "need", "confidence": 0.7, "weight": 0.2}
    ]
    result = weighted_ensemble(sources)
    assert result["need_or_want"] == "want"  # 0.8 > 0.2
```

### Integration Tests
```python
def test_full_classification_pipeline():
    result = classify_transaction(
        merchant="Starbucks",
        amount=5.25,
        category="Coffee",
        user_id="u_test"
    )

    assert "need_or_want" in result
    assert "confidence" in result
    assert "sources" in result
    assert len(result["sources"]) >= 2  # At least rules + dedalus
```

---

## Metrics to Track (Show in Demo)

```python
{
    "accuracy": 0.94,                    # % correct vs user corrections
    "avg_confidence": 0.87,              # Average confidence score
    "ensemble_agreement_rate": 0.82,     # % where all sources agree
    "dedalus_uptime": 0.98,             # API reliability
    "avg_classification_time_ms": 250,   # Speed
    "user_correction_rate": 0.06        # How often users disagree
}
```

Show this in frontend dashboard:
```
"Our AI is 94% accurate and processes transactions in 250ms"
```

---

## Implementation Priority

### Day 1 (Core):
1. Rule-based classifier - 2 hours
2. Dedalus MCP integration - 4 hours
3. Simple weighted ensemble - 2 hours
4. Wire into Flask `/api/knot/webhooks` - 1 hour

### Day 2 (Polish):
5. Historical pattern matching - 3 hours
6. Confidence-based notifications - 2 hours
7. Testing + edge cases - 2 hours

### Day 3 (Demo prep):
8. Metrics dashboard - 2 hours
9. Demo scripts - 1 hour
10. OpenAI backup (if time) - 2 hours

---

## Sample Demo Script

```
1. Show transaction coming in:
   "Here's a real transaction: Starbucks, $5.25"

2. Show classification sources:
   [Screen shows 3 sources running in parallel]
   - Rules: "want" (100ms)
   - Dedalus: "want" (350ms)
   - History: "want" (50ms)

3. Show ensemble decision:
   "Our ensemble combines all three:
    → Final: WANT (91% confidence)
    → Reasoning: Daily coffee is discretionary"

4. Show learning:
   "User corrects to NEED (work coffee)
    → System learns
    → Next Starbucks transaction auto-classified correctly"

5. Show metrics:
   "94% accuracy, 250ms average speed, 98% uptime"
```

---

## Next Steps

1. **Create the classification module structure**
2. **Implement rule-based engine** (quick win)
3. **Set up Dedalus MCP client** (core value)
4. **Build ensemble logic** (demo wow factor)
5. **Test with real transaction data**

Want me to start building the actual code for this?
