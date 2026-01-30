# AP2 Workshop - Step by Step Guide

**Duration:** 20 minutes | **Goal:** Implement AP2 payment authorization

---

## Step 1: Setup (2 min)

```bash
# Navigate to workshop folder
cd workshop

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from google.adk import Agent; print('Ready!')"
```

---

## Step 2: Understand the Problem

**Without AP2**, an AI agent could:
- Charge $10,000 instead of $100
- Make purchases you never approved
- Leave no proof of what you authorized

**With AP2**, every payment requires:
- User sees exact amount and items
- User explicitly approves
- Cryptographic token proves intent

---

## Step 3: Open the File

Open `shopper_agent/agent.py` in your editor.

Find the section marked:
```python
# ============================================================================
# AP2 AUTHORIZATION - IMPLEMENT THESE TWO FUNCTIONS
# ============================================================================
```

You'll implement two functions:
1. `request_user_authorization()` - Shows payment details to user
2. `confirm_payment()` - Generates proof of approval

---

## Step 4: Implement TODO 1 - Request Authorization

Find `request_user_authorization()` and replace `pass` with:

```python
def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    # Step 1: Store the pending mandate
    PENDING_MANDATES[mandate_id] = {
        "mandate_id": mandate_id,
        "merchant": merchant_name,
        "amount": amount,
        "description": description,
        "line_items": line_items,
        "status": "pending_user_input",
    }

    # Step 2: Return authorization prompt for user
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

**Why this matters:** The user sees exactly what they're paying for before approving.

---

## Step 5: Implement TODO 2 - Confirm Payment

Find `confirm_payment()` and replace `pass` with:

```python
def confirm_payment(mandate_id: str, approved: bool = True) -> dict[str, Any]:
    import hashlib
    import time

    # Step 1: Check mandate exists
    if mandate_id not in PENDING_MANDATES:
        return {"status": "error", "message": f"Mandate {mandate_id} not found"}

    mandate = PENDING_MANDATES[mandate_id]

    # Step 2: Handle rejection
    if not approved:
        mandate["status"] = "rejected"
        return {"status": "rejected", "message": "User rejected", "mandate_id": mandate_id}

    # Step 3: Generate cryptographic authorization token
    token_data = f"{mandate_id}:{USER_SESSION['user_id']}:{time.time()}"
    token = hashlib.sha256(token_data.encode()).hexdigest()[:32]

    # Step 4: Update mandate and return token
    mandate["status"] = "authorized"
    mandate["authorization_token"] = token

    return {
        "status": "authorized",
        "mandate_id": mandate_id,
        "authorization_token": token,
        "user_id": USER_SESSION["user_id"],
    }
```

**Why this matters:** The token is cryptographic proof that the user approved this specific payment.

---

## Step 6: Test Your Implementation

```bash
python run_workshop.py
# Select option 1: Test your implementation
```

**Expected output:**
```
[1/3] Creating booking mandate...
  ✓ Mandate: MND-abc123

[2/3] Testing request_user_authorization()...
  ✓ Authorization prompt generated

[3/3] Testing confirm_payment()...
  ✓ Token: a1b2c3d4e5f6...

✅ All tests passed!
```

---

## Step 7: Run the Full Demo

```bash
python run_workshop.py
# Select option 2: Run complete demo
```

Watch the complete AP2 flow:
1. Search flights
2. Create booking mandate
3. **Show authorization prompt** (your TODO 1)
4. **Generate auth token** (your TODO 2)
5. Booking confirmed!

---

## What You Built

| Function | Purpose |
|----------|---------|
| `request_user_authorization()` | Shows user what they're paying for |
| `confirm_payment()` | Creates cryptographic proof of approval |

---

## Key AP2 Concepts

### 1. No Silent Charges
```
User sees: "Merchant: flight_merchant, Amount: $952.00"
User must click APPROVE before any charge
```

### 2. Cryptographic Proof
```python
token = sha256(f"{mandate_id}:{user_id}:{timestamp}").hexdigest()
# This token proves: WHO approved WHAT and WHEN
```

### 3. Audit Trail
```
mandate_id → user_id → timestamp → token
# Complete traceability for disputes
```

---

## Troubleshooting

### "Function returns None"
- Make sure you replaced `pass` with the actual code
- Check for syntax errors

### "Mandate not found"
- `request_user_authorization()` must be called before `confirm_payment()`
- Check that you're storing in `PENDING_MANDATES`

### Import errors
- Run `pip install -r requirements.txt`
- Make sure you're in the `workshop` folder

---

## Next Steps

- Explore `../demo/` for a full working example
- Check `solutions/` for reference implementations
- Read `ap2-protocol.md` for protocol details
- Try `adk web shopper_agent` for interactive mode

---

## Resources

- [AP2 Protocol](https://github.com/anthropics/ap2)
- [Google ADK](https://google.github.io/adk-docs/)
- [A2A Protocol](https://google.github.io/A2A/)
