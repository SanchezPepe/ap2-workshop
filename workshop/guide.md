# AP2 Workshop Guide

**Duration:** 20 minutes | **TODOs:** 2 functions

---

## What You'll Learn

AP2 ensures AI agents **never charge users without explicit approval**. You'll implement the two core authorization functions.

---

## Setup (2 min)

```bash
cd workshop
pip install -r requirements.txt
```

---

## The Two Functions You'll Implement

Open `shopper_agent/agent.py` and find the two TODO sections:

### TODO 1: `request_user_authorization()`

Shows the user what they're paying for and asks for approval.

```python
def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    # 1. Store in PENDING_MANDATES
    PENDING_MANDATES[mandate_id] = {
        "mandate_id": mandate_id,
        "merchant": merchant_name,
        "amount": amount,
        "description": description,
        "line_items": line_items,
        "status": "pending_user_input",
    }

    # 2. Return authorization prompt
    return {
        "status": "authorization_required",
        "mandate_id": mandate_id,
        "prompt_to_user": f"""
========================================
        AP2 PAYMENT AUTHORIZATION
========================================
Merchant: {merchant_name}
Amount: {amount}

Items:
{chr(10).join(f'  - {item}' for item in line_items)}

Description: {description}
========================================
        """,
        "requires_user_action": True,
    }
```

### TODO 2: `confirm_payment()`

Generates cryptographic proof of user approval.

```python
def confirm_payment(mandate_id: str, approved: bool = True) -> dict[str, Any]:
    import hashlib
    import time

    # 1. Check mandate exists
    if mandate_id not in PENDING_MANDATES:
        return {"status": "error", "message": f"Mandate {mandate_id} not found"}

    mandate = PENDING_MANDATES[mandate_id]

    # 2. Handle rejection
    if not approved:
        mandate["status"] = "rejected"
        return {"status": "rejected", "message": "User rejected", "mandate_id": mandate_id}

    # 3. Generate authorization token
    token_data = f"{mandate_id}:{USER_SESSION['user_id']}:{time.time()}"
    token = hashlib.sha256(token_data.encode()).hexdigest()[:32]

    mandate["status"] = "authorized"
    mandate["authorization_token"] = token

    return {
        "status": "authorized",
        "mandate_id": mandate_id,
        "authorization_token": token,
        "user_id": USER_SESSION["user_id"],
    }
```

---

## Test Your Code

```bash
python run_workshop.py
# Select option 1 to test
```

Expected output:
```
✓ Mandate: MND-abc123
✓ Authorization prompt generated
✓ Token: a1b2c3d4e5f6...

✅ All tests passed!
```

---

## Run the Demo

```bash
python run_workshop.py
# Select option 2 for full demo
```

---

## Key Takeaways

| Principle | Your Implementation |
|-----------|---------------------|
| **No silent charges** | `request_user_authorization()` shows all details |
| **Explicit approval** | User must confirm before payment |
| **Proof of intent** | `confirm_payment()` generates cryptographic token |

---

## Why This Matters

Without AP2:
- Agent could charge $10,000 for a $100 flight
- User has no proof they didn't authorize it
- No accountability

With AP2:
- User sees exact amount before approving
- Cryptographic token proves user intent
- Full audit trail

---

## Next Steps

- Explore `complete_demo/` for the full working example
- Read `ap2-protocol.md` for protocol details
- Try `adk web shopper_agent` for interactive mode
