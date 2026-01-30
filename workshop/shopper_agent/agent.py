"""
Shopper Agent - Travel Booking Assistant

This agent helps users find and book travel using the AP2 protocol
for secure payment authorization.

WORKSHOP: Complete the two TODO functions to implement AP2 authorization.
"""

import os
import sys
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk import Agent
from google.adk.tools import FunctionTool

from shared.ap2_types import PaymentStatus, create_ap2_extension


# ============================================================================
# User Session (Simulated)
# ============================================================================

USER_SESSION = {
    "user_id": "user_12345",
    "name": "Demo User",
    "payment_methods": [
        {"type": "card", "last_four": "4242", "brand": "Visa"},
        {"type": "card", "last_four": "5555", "brand": "Mastercard"},
    ],
}

PENDING_MANDATES: dict[str, dict] = {}


# ============================================================================
# Pre-built Tools (provided for you)
# ============================================================================

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


def search_merchant_flights(
    origin: str,
    destination: str,
    date: str | None = None,
    travel_class: str | None = None,
) -> dict[str, Any]:
    """Search for flights via the merchant agent."""
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


def initiate_booking(flight_id: str, passenger_name: str) -> dict[str, Any]:
    """Initiate a flight booking - merchant creates payment mandate."""
    import uuid
    mandate_id = str(uuid.uuid4())[:8]

    return {
        "status": "mandate_created",
        "message": "Merchant created payment mandate - user authorization required",
        "mandate_id": f"MND-{mandate_id}",
        "merchant": "flight_merchant_agent",
        "booking_details": {"flight_id": flight_id, "passenger": passenger_name},
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


# ============================================================================
# AP2 AUTHORIZATION - IMPLEMENT THESE TWO FUNCTIONS
# ============================================================================

def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    """
    TODO 1: Request user authorization for a payment.

    This is the core of AP2 - showing the user what they're paying for
    and getting their explicit approval.

    Steps:
    1. Store the mandate in PENDING_MANDATES with status "pending_user_input"
    2. Return a response with:
       - status: "authorization_required"
       - mandate_id: the mandate ID
       - prompt_to_user: formatted payment details (see example below)
       - requires_user_action: True

    Example prompt_to_user format:
    ========================================
            AP2 PAYMENT AUTHORIZATION
    ========================================
    Merchant: {merchant_name}
    Amount: {amount}

    Items:
      - {item1}
      - {item2}

    Description: {description}
    ========================================
    """
    # IMPLEMENT HERE:
    pass


def confirm_payment(mandate_id: str, approved: bool = True) -> dict[str, Any]:
    """
    TODO 2: Confirm or reject a payment authorization.

    This generates the cryptographic proof of user intent.

    Steps:
    1. Check if mandate_id exists in PENDING_MANDATES
       - If not found, return {"status": "error", "message": "..."}

    2. If not approved:
       - Set mandate status to "rejected"
       - Return {"status": "rejected", "message": "...", "mandate_id": ...}

    3. If approved:
       - Generate token: hashlib.sha256(f"{mandate_id}:{USER_SESSION['user_id']}:{time.time()}".encode()).hexdigest()[:32]
       - Update mandate status to "authorized"
       - Store token in mandate
       - Return {"status": "authorized", "authorization_token": token, ...}
    """
    import hashlib
    import time

    # IMPLEMENT HERE:
    pass


# ============================================================================
# Agent Configuration (provided for you)
# ============================================================================

# Create tools
get_user_preferences_tool = FunctionTool(func=get_user_preferences)
get_payment_methods_tool = FunctionTool(func=get_payment_methods)
search_merchant_flights_tool = FunctionTool(func=search_merchant_flights)
initiate_booking_tool = FunctionTool(func=initiate_booking)
request_user_authorization_tool = FunctionTool(func=request_user_authorization)
confirm_payment_tool = FunctionTool(func=confirm_payment)

# Create the agent
shopper_agent = Agent(
    model="gemini-2.0-flash",
    name="travel_shopper_agent",
    description="A travel booking assistant using AP2 for secure payments",
    instruction="""You are a travel booking assistant. Help users find and book flights
    using the AP2 protocol for secure payments.

    Workflow:
    1. Search for flights with search_merchant_flights
    2. When user selects a flight, use initiate_booking
    3. Request authorization with request_user_authorization
    4. After user confirms, use confirm_payment to generate the auth token

    AP2 Principles:
    - NEVER make payments without explicit user authorization
    - ALWAYS show payment details before requesting approval
    - The user is ALWAYS in control
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

root_agent = shopper_agent
