"""
Shopper Agent - COMPLETE SOLUTION

This is the complete implementation of the shopper agent for reference.
"""

import os
import sys
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk import Agent
from google.adk.tools import FunctionTool

from solutions.ap2_types_complete import (
    PaymentMandate,
    PaymentStatus,
    create_ap2_extension,
)


# ============================================================================
# User Session & Authorization (Simulated)
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
# Shopper Tools - COMPLETE IMPLEMENTATIONS
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


def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    """Request user authorization for a payment mandate."""
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


# ============================================================================
# Create the Shopper Agent
# ============================================================================

get_user_preferences_tool = FunctionTool(func=get_user_preferences)
get_payment_methods_tool = FunctionTool(func=get_payment_methods)
search_merchant_flights_tool = FunctionTool(func=search_merchant_flights)
initiate_booking_tool = FunctionTool(func=initiate_booking)
request_user_authorization_tool = FunctionTool(func=request_user_authorization)
confirm_payment_tool = FunctionTool(func=confirm_payment)

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

root_agent = shopper_agent
