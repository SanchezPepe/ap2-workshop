# AP2 Demo Script

**Duration:** 5-10 minutes
**Audience:** Developers, Product Managers, anyone interested in agent commerce

---

## Setup Before Demo

```bash
cd demo
pip install -r requirements.txt
```

---

## Opening (30 sec)

> "Today I'll show you **AP2 - the Agent Payments Protocol**. It solves a critical problem: **How can we trust AI agents to spend our money?**"

---

## The Problem (1 min)

> "Without AP2, an AI agent could:"

- Charge $10,000 for a $100 flight
- Make purchases you never approved
- Leave no proof of what happened

> "AP2 fixes this by requiring **explicit user authorization** with **cryptographic proof**."

---

## Run the Demo

```bash
python run_demo.py
# Select option 1
```

---

## Step-by-Step Narration

### Step 1: Search Flights

> "The user asks their agent to book a flight to Paris. The agent searches available flights."

**Highlight:** Agent finds 3 flights with prices.

---

### Step 2: Initiate Booking

> "User selects FL001. The merchant creates a **Payment Mandate** - this is like a digital invoice."

**Highlight:**
- Mandate ID: `MND-xxxxx`
- Total: `$952.00`

> "Notice the merchant **cannot charge yet**. They need user authorization first."

---

### Step 3: Authorization Request (KEY MOMENT)

> "Here's the core of AP2. The agent shows the user **exactly** what they're paying for."

**Highlight the authorization prompt:**
```
========================================
        AP2 PAYMENT AUTHORIZATION
========================================
Merchant: flight_merchant_agent
Amount: $952.00

Items:
  - Flight FL001: SFO → CDG - $850.00
  - Taxes and fees - $102.00
========================================
```

> "The user sees the merchant, amount, and itemized charges. **No hidden fees. No surprises.**"

---

### Step 4: User Confirms

> "The user clicks APPROVE. The system generates a **cryptographic authorization token**."

**Highlight:**
- Status: `authorized`
- Token: `95ac3183cd78ea0e...`

> "This token is **proof** that the user approved this specific payment. It can be audited later if there's a dispute."

---

### Step 5: Booking Complete

> "The token is sent to the merchant, who can now process the payment. Booking confirmed!"

---

## Key Takeaways (30 sec)

Show the summary:

| Principle | How AP2 Implements It |
|-----------|----------------------|
| **No silent charges** | User sees all details before approving |
| **Explicit consent** | User must click APPROVE |
| **Proof of intent** | Cryptographic token with timestamp |
| **Audit trail** | mandate_id → user_id → token |

---

## Closing (30 sec)

> "AP2 makes agent commerce **trustworthy**. Users stay in control. Merchants get proof of authorization. And when something goes wrong, there's a clear audit trail."

> "Questions?"

---

## Common Questions

### "How is the token generated?"
```python
token = sha256(f"{mandate_id}:{user_id}:{timestamp}").hexdigest()
```
It combines the mandate, user, and time - proving WHO approved WHAT and WHEN.

### "What if the agent tries to bypass authorization?"
The merchant won't accept payment without a valid token. No token = no charge.

### "Is this a real protocol?"
AP2 is built on Google's ADK (Agent Development Kit) and A2A (Agent-to-Agent) protocol. It's designed for production use.

### "Can I try it?"
Yes! Workshop available at: `workshop/guide.md`

---

## Quick Commands Reference

```bash
# Run demo
cd demo && python run_demo.py

# Run workshop
cd workshop && python run_workshop.py

# Test workshop implementation
python run_workshop.py  # Select option 1
```
