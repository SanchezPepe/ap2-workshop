# AP2 Workshop Guide

## Building Secure Agent Commerce with ADK

**Duration:** 45 minutes
**Prerequisites:** Python basics, ADK familiarity
**Environment:** Google Cloud Shell

---

## Workshop Overview

In this hands-on workshop, you'll build a **travel booking agent** that uses the **AP2 (Agent Payments Protocol)** to securely handle payments. By the end, you'll understand how AI agents can make payments on behalf of users with cryptographic proof of authorization.

### What You'll Build

```
┌─────────────────┐         ┌─────────────────┐
│  Shopper Agent  │ ◄─────► │ Merchant Agent  │
│  (You build)    │   AP2   │  (Reference)    │
└────────┬────────┘         └─────────────────┘
         │
         │ Authorization
         ▼
    ┌─────────┐
    │  User   │
    └─────────┘
```

---

## Phase 1: Environment Setup (5 min)

### 1.1 Clone the Workshop

```bash
# If you haven't already, clone the repository
cd ~
git clone <repository-url> ap2-workshop
cd ap2-workshop/workshop
```

### 1.2 Set Up Virtual Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.3 Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your project ID
nano .env
# Set: GOOGLE_CLOUD_PROJECT=your-project-id
```

### 1.4 Verify Setup

```bash
# Test that ADK is installed
python -c "from google.adk import Agent; print('ADK ready!')"
```

**Checkpoint:** You should see "ADK ready!" printed.

---

## Phase 2: Complete AP2 Types (10 min)

The AP2 protocol defines data structures for secure payments. You'll complete the `PaymentMandate` class.

### 2.1 Open the File

```bash
# Open the AP2 types file
code shared/ap2_types.py
# Or: nano shared/ap2_types.py
```

### 2.2 Understanding the PaymentMandate

A `PaymentMandate` is the core AP2 data structure. It contains:
- **Parties**: Who's involved (shopper, merchant, user)
- **Payment details**: What's being purchased
- **Authorization**: Cryptographic proof of user intent

### 2.3 Complete TODO 1-3: Add the Fields

Find the TODO comments and add these fields:

```python
class PaymentMandate(BaseModel):
    # ... existing code ...

    # TODO 1: Parties involved (already provided as hints)
    shopper_agent_id: str
    merchant_agent_id: str
    user_id: str

    # TODO 2: Payment details - ADD THESE:
    line_items: list[LineItem]
    currency: str = "USD"

    # TODO 3: Authorization fields - ADD THESE:
    status: PaymentStatus = PaymentStatus.PENDING
    user_authorization_token: str | None = None
    authorization_timestamp: datetime | None = None
```

### 2.4 Complete TODO 4: Add total_amount Property

```python
    @property
    def total_amount(self) -> float:
        """Calculate total amount from all line items."""
        return sum(item.total for item in self.line_items)
```

**Why this matters:** The total amount is calculated from line items, ensuring transparency about what the user is paying for.

### 2.5 Complete TODO 5: Implement authorize()

```python
    def authorize(self, token: str) -> None:
        """
        Authorize the mandate with a user token.

        This method:
        1. Stores the cryptographic token (proof of intent)
        2. Records when authorization happened
        3. Updates the mandate status
        """
        self.user_authorization_token = token
        self.authorization_timestamp = datetime.utcnow()
        self.status = PaymentStatus.AUTHORIZED
```

**Why this matters:** This is the heart of AP2 - the user's authorization is recorded with a timestamp, creating an audit trail.

### 2.6 Complete TODO 6: Implement to_summary()

```python
    def to_summary(self) -> dict:
        """Return a summary suitable for display to users."""
        return {
            "mandate_id": self.mandate_id,
            "merchant": self.merchant_agent_id,
            "total": f"{self.currency} {self.total_amount:.2f}",
            "items": [
                f"{item.description} x{item.quantity} = {item.currency} {item.total:.2f}"
                for item in self.line_items
            ],
            "status": self.status.value
        }
```

### 2.7 Test Your Implementation

```bash
python run_workshop.py
# Select option 1: Test AP2 Types
```

**Checkpoint:** All 5 tests should pass with green checkmarks.

---

## Phase 3: Build Shopper Agent Tools (15 min)

Now you'll implement the tools that your shopper agent uses to help users book flights.

### 3.1 Open the Shopper Agent File

```bash
code shopper_agent/agent.py
# Or: nano shopper_agent/agent.py
```

### 3.2 Implement get_user_preferences() - TODO 1

This tool retrieves the user's travel preferences.

```python
def get_user_preferences() -> dict[str, Any]:
    """Get the current user's travel preferences."""
    return {
        "user_id": USER_SESSION["user_id"],
        "name": USER_SESSION["name"],
        "preferences": {
            "preferred_class": "economy",
            "preferred_airlines": ["SkyHigh Airlines", "Premium Air"],
            "max_layovers": 1,
            "seat_preference": "aisle",
        },
        "payment_methods_available": len(USER_SESSION["payment_methods"]),
    }
```

### 3.3 Implement get_payment_methods() - TODO 2

This tool lists the user's saved payment methods (masked for security).

```python
def get_payment_methods() -> dict[str, Any]:
    """Get the user's available payment methods."""
    methods = []
    for i, pm in enumerate(USER_SESSION["payment_methods"]):
        methods.append({
            "index": i,
            "type": pm["type"],
            "display": f"{pm['brand']} ending in {pm['last_four']}",
        })

    return {
        "status": "success",
        "payment_methods": methods,
        "default_method": 0,
    }
```

### 3.4 Implement search_merchant_flights() - TODO 3

This tool searches for flights (simulates calling the merchant agent).

```python
def search_merchant_flights(
    origin: str,
    destination: str,
    date: str | None = None,
    travel_class: str | None = None,
) -> dict[str, Any]:
    """Search for flights via the merchant agent."""
    # Simulated flight results
    flights = [
        {
            "flight_id": "FL001",
            "airline": "SkyHigh Airlines",
            "route": f"{origin} → {destination}",
            "departure": "2025-03-15 10:00",
            "arrival": "2025-03-16 06:30",
            "price": "$850.00",
            "class": "economy",
        },
        {
            "flight_id": "FL002",
            "airline": "SkyHigh Airlines",
            "route": f"{origin} → {destination}",
            "departure": "2025-03-15 14:30",
            "arrival": "2025-03-16 10:00",
            "price": "$920.00",
            "class": "economy",
        },
        {
            "flight_id": "FL003",
            "airline": "Premium Air",
            "route": f"{origin} → {destination}",
            "departure": "2025-03-15 08:00",
            "arrival": "2025-03-15 23:30",
            "price": "$1,450.00",
            "class": "business",
        },
    ]

    return {
        "status": "success",
        "source": "flight_merchant_agent",
        "search": {"origin": origin, "destination": destination, "date": date},
        "results": flights,
        "message": f"Found {len(flights)} flights from {origin} to {destination}",
    }
```

### 3.5 Implement initiate_booking() - TODO 4

This is where AP2 kicks in! The merchant creates a payment mandate.

```python
def initiate_booking(
    flight_id: str,
    passenger_name: str,
) -> dict[str, Any]:
    """Initiate a flight booking with the merchant."""
    import uuid
    mandate_id = str(uuid.uuid4())[:8]

    return {
        "status": "mandate_created",
        "message": "Merchant created payment mandate - user authorization required",
        "mandate_id": f"MND-{mandate_id}",
        "merchant": "flight_merchant_agent",
        "booking_details": {
            "flight_id": flight_id,
            "passenger": passenger_name,
        },
        "payment": {
            "subtotal": "$850.00",
            "taxes": "$102.00",
            "total": "$952.00",
            "currency": "USD",
        },
        "line_items": [
            f"Flight {flight_id}: SFO → CDG - $850.00",
            "Taxes and fees - $102.00",
        ],
        "next_step": "Request user authorization using request_user_authorization tool",
    }
```

**Key AP2 Concept:** The merchant creates a mandate but CANNOT process payment yet. The user must authorize it first!

### 3.6 Implement request_user_authorization() - TODO 5

This tool shows the user what they're about to pay for and asks for approval.

```python
def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    """Request user authorization for a payment mandate."""
    # Store the pending mandate
    PENDING_MANDATES[mandate_id] = {
        "mandate_id": mandate_id,
        "merchant": merchant_name,
        "amount": amount,
        "description": description,
        "line_items": line_items,
        "status": "pending_user_input",
    }

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

To authorize this payment, the user should confirm.
For this demo, use the 'confirm_payment' tool with the mandate_id.
        """,
        "requires_user_action": True,
    }
```

**Key AP2 Concept:** Users see exactly what they're paying for before authorizing. No hidden charges!

### 3.7 Implement confirm_payment() - TODO 6

This generates the cryptographic authorization token.

```python
def confirm_payment(mandate_id: str, approved: bool = True) -> dict[str, Any]:
    """Confirm or reject a payment authorization."""
    if mandate_id not in PENDING_MANDATES:
        return {
            "status": "error",
            "message": f"No pending mandate found with ID {mandate_id}"
        }

    mandate = PENDING_MANDATES[mandate_id]

    if not approved:
        mandate["status"] = "rejected"
        return {
            "status": "rejected",
            "message": "User rejected the payment authorization",
            "mandate_id": mandate_id,
        }

    # Generate authorization token
    import hashlib
    import time
    token_data = f"{mandate_id}:{USER_SESSION['user_id']}:{time.time()}"
    authorization_token = hashlib.sha256(token_data.encode()).hexdigest()[:32]

    mandate["status"] = "authorized"
    mandate["authorization_token"] = authorization_token

    return {
        "status": "authorized",
        "message": "Payment authorized by user",
        "mandate_id": mandate_id,
        "authorization_token": authorization_token,
        "user_id": USER_SESSION["user_id"],
        "timestamp": time.time(),
    }
```

**Key AP2 Concept:** The authorization token is cryptographic proof that the user approved this specific payment. It can be audited later.

### 3.8 Test Your Tools

```bash
python run_workshop.py
# Select option 2: Test Shopper Tools
```

**Checkpoint:** All 6 tool tests should pass.

---

## Phase 4: Configure the Agent (10 min)

Now let's wire up the tools to create a working agent.

### 4.1 Create FunctionTools - TODO 7

Find the TODO 7 section and uncomment/complete:

```python
# Define tools
get_user_preferences_tool = FunctionTool(func=get_user_preferences)
get_payment_methods_tool = FunctionTool(func=get_payment_methods)
search_merchant_flights_tool = FunctionTool(func=search_merchant_flights)
initiate_booking_tool = FunctionTool(func=initiate_booking)
request_user_authorization_tool = FunctionTool(func=request_user_authorization)
confirm_payment_tool = FunctionTool(func=confirm_payment)
```

### 4.2 Create the Agent - TODO 8

```python
shopper_agent = Agent(
    model="gemini-2.0-flash",
    name="travel_shopper_agent",
    description="A travel booking assistant that helps users find and book flights using AP2 for secure payments",
    instruction="""You are a helpful travel booking assistant. You help users find
    and book flights by communicating with merchant agents and handling payments
    securely using the AP2 protocol.

    Your workflow for booking a flight:

    1. SEARCH: When user wants to book travel, search for flights using search_merchant_flights
    2. PRESENT: Show the user their options clearly with prices
    3. SELECT: When user chooses a flight, initiate the booking with initiate_booking
    4. AUTHORIZE: Request user authorization for the payment using request_user_authorization
    5. CONFIRM: After user confirms, use confirm_payment to generate the authorization token
    6. COMPLETE: The authorization token is sent to merchant to complete the booking

    Important AP2 principles you follow:
    - NEVER make a payment without explicit user authorization
    - ALWAYS show the user exactly what they're paying for before requesting authorization
    - The user is ALWAYS in control of their money

    Be friendly and helpful. Explain the AP2 payment process if the user asks.
    """,
    tools=[
        get_user_preferences_tool,
        get_payment_methods_tool,
        search_merchant_flights_tool,
        initiate_booking_tool,
        request_user_authorization_tool,
        confirm_payment_tool,
    ],
)

# Update the export
root_agent = shopper_agent
```

### 4.3 Test the Agent Configuration

```bash
python run_workshop.py
# Select option 3: Test Shopper Agent
```

**Checkpoint:** Agent should show 6 configured tools.

---

## Phase 5: Run the Complete Demo (5 min)

### 5.1 Run All Tests

```bash
python run_workshop.py
# Select option 5: Run All Tests
```

You should see:
```
SUMMARY
  AP2 Types:      ✅ PASS
  Shopper Tools:  ✅ PASS
  Shopper Agent:  ✅ PASS
```

### 5.2 Run the Demo Flow

The script will automatically run the complete booking flow:

1. **Search** - Find flights from SFO to Paris
2. **Select** - Choose flight FL001
3. **Mandate** - Merchant creates payment mandate
4. **Authorize** - User sees payment details and approves
5. **Token** - Cryptographic token generated
6. **Complete** - Booking confirmed!

### 5.3 Try Interactive Mode (Optional)

```bash
# Run the agent in web mode
adk web shopper_agent

# Open http://localhost:8000 in your browser
# Try: "I want to book a flight to Paris"
```

---

## Key Takeaways

### AP2 Principles You Implemented

| Principle | Implementation |
|-----------|----------------|
| **Verifiable Intent** | `authorization_token` in `confirm_payment()` |
| **Clear Accountability** | `to_summary()` and `authorization_timestamp` |
| **User Control** | `request_user_authorization()` shows all details |

### The Payment Flow

```
User Request → Search → Select → Mandate Created
                                      ↓
Token Generated ← User Approves ← Show Details
      ↓
Booking Confirmed
```

### What Makes AP2 Different

1. **No silent charges** - Every payment requires explicit user approval
2. **Proof of intent** - Cryptographic token proves authorization
3. **Audit trail** - Timestamps and references for every transaction
4. **Interoperability** - Any AP2-compliant agents can work together

---

## Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the workshop directory
cd ~/ap2-workshop/workshop

# Make sure virtual environment is active
source venv/bin/activate
```

### Tests failing
- Check that you removed `pass` from functions and added real implementations
- Make sure all field names match exactly (case-sensitive)
- Run individual tests to see specific errors

### Agent returns None
- Make sure you uncommented the `shopper_agent = Agent(...)` block
- Check that `root_agent = shopper_agent` is at the bottom

---

## Next Steps

- **Explore the merchant agent** - See how it processes mandates
- **Add more tools** - Hotel booking, car rental
- **Multi-agent setup** - Run shopper and merchant on separate ports with A2A
- **Real payment integration** - Connect to Stripe or other processors

---

## Resources

- [AP2 Protocol Specification](https://github.com/google-agentic-commerce/ap2)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://google.github.io/A2A/)
- Workshop solutions: `workshop/solutions/`
