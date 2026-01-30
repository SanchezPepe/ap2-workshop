"""
Shopper Agent - Travel Booking Assistant

This agent acts as a shopper in the AP2 protocol, helping users
find and book travel arrangements by communicating with merchant agents.

WORKSHOP: You will complete this agent by implementing the tools and agent definition.
"""

import os
import sys
from typing import Any

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk import Agent
from google.adk.tools import FunctionTool

from shared.ap2_types import (
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
# Shopper Tools - IMPLEMENT THESE
# ============================================================================

def get_user_preferences() -> dict[str, Any]:
    """
    Get the current user's travel preferences.

    Returns:
        User preferences and profile information
    """
    # TODO 1: Return a dictionary containing:
    # - user_id (from USER_SESSION)
    # - name (from USER_SESSION)
    # - preferences dict with:
    #   - preferred_class: "economy"
    #   - preferred_airlines: ["SkyHigh Airlines", "Premium Air"]
    #   - max_layovers: 1
    #   - seat_preference: "aisle"
    # - payment_methods_available: count of payment methods

    # IMPLEMENT HERE:
    pass


def get_payment_methods() -> dict[str, Any]:
    """
    Get the user's available payment methods.

    Returns:
        List of payment methods (masked for security)
    """
    # TODO 2: Return the user's payment methods
    # Iterate through USER_SESSION["payment_methods"] and create a list with:
    # - index (position in list)
    # - type (card type)
    # - display (formatted as "{brand} ending in {last_four}")
    #
    # Return: {"status": "success", "payment_methods": [...], "default_method": 0}

    # IMPLEMENT HERE:
    pass


def search_merchant_flights(
    origin: str,
    destination: str,
    date: str | None = None,
    travel_class: str | None = None,
) -> dict[str, Any]:
    """
    Search for flights via the merchant agent.

    In a full A2A implementation, this would call the remote merchant agent.
    For this demo, we'll simulate the merchant's response.

    Args:
        origin: Origin airport code
        destination: Destination airport code
        date: Travel date (YYYY-MM-DD)
        travel_class: Preferred class

    Returns:
        Flight search results from merchant
    """
    # TODO 3: Return simulated flight search results
    # Create a list of 3 flight options with:
    # - flight_id (FL001, FL002, FL003)
    # - airline
    # - route (formatted as "{origin} → {destination}")
    # - departure time
    # - arrival time
    # - price (as string like "$850.00")
    # - class
    #
    # Return dict with: status, source, search query, results list, message

    # IMPLEMENT HERE:
    pass


def initiate_booking(
    flight_id: str,
    passenger_name: str,
) -> dict[str, Any]:
    """
    Initiate a flight booking with the merchant.

    This starts the AP2 payment flow by requesting a payment mandate
    from the merchant agent.

    Args:
        flight_id: The flight to book
        passenger_name: Name for the booking

    Returns:
        Payment mandate details requiring user authorization
    """
    # TODO 4: Simulate the merchant creating a payment mandate
    #
    # 1. Generate a mandate_id using: str(uuid.uuid4())[:8]
    # 2. Return a dict with:
    #    - status: "mandate_created"
    #    - message: explaining mandate was created
    #    - mandate_id: formatted as "MND-{id}"
    #    - merchant: "flight_merchant_agent"
    #    - booking_details: {flight_id, passenger}
    #    - payment: {subtotal, taxes, total, currency}
    #    - line_items: list of formatted item strings
    #    - next_step: instruction to use request_user_authorization

    import uuid

    # IMPLEMENT HERE:
    pass


def request_user_authorization(
    mandate_id: str,
    merchant_name: str,
    amount: str,
    description: str,
    line_items: list[str],
) -> dict[str, Any]:
    """
    Request user authorization for a payment mandate.

    This simulates the AP2 authorization flow where the user must
    explicitly approve a payment before it can proceed.

    Args:
        mandate_id: The mandate ID from the merchant
        merchant_name: Name of the merchant requesting payment
        amount: Total amount to be charged
        description: Description of the purchase
        line_items: List of items being purchased

    Returns:
        Authorization status and prompt for user
    """
    # TODO 5: Implement the authorization request flow
    #
    # 1. Store the pending mandate in PENDING_MANDATES dict with:
    #    - mandate_id, merchant, amount, description, line_items
    #    - status: "pending_user_input"
    #
    # 2. Return a dict with:
    #    - status: "authorization_required"
    #    - mandate_id
    #    - prompt_to_user: A formatted string showing the payment details
    #    - requires_user_action: True
    #
    # The prompt should look like:
    # ========================================
    #         AP2 PAYMENT AUTHORIZATION
    # ========================================
    # Merchant: {merchant_name}
    # Amount: {amount}
    # Items:
    #   - {item1}
    #   - {item2}
    # ========================================

    # IMPLEMENT HERE:
    pass


def confirm_payment(mandate_id: str, approved: bool = True) -> dict[str, Any]:
    """
    Confirm or reject a payment authorization.

    This simulates the user's response to an authorization request.

    Args:
        mandate_id: The mandate to confirm/reject
        approved: Whether the user approves the payment

    Returns:
        Authorization token if approved, rejection if not
    """
    # TODO 6: Implement the payment confirmation
    #
    # 1. Check if mandate_id exists in PENDING_MANDATES
    #    - If not, return error status
    #
    # 2. If not approved:
    #    - Update mandate status to "rejected"
    #    - Return rejection response
    #
    # 3. If approved:
    #    - Generate an authorization token using:
    #      token_data = f"{mandate_id}:{USER_SESSION['user_id']}:{time.time()}"
    #      authorization_token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
    #    - Update mandate status to "authorized"
    #    - Store the token in the mandate
    #    - Return success with token

    import hashlib
    import time

    # IMPLEMENT HERE:
    pass


# ============================================================================
# Create the Shopper Agent - COMPLETE THIS
# ============================================================================

# TODO 7: Create FunctionTool instances for each tool
# Example: get_user_preferences_tool = FunctionTool(func=get_user_preferences)

# UNCOMMENT AND COMPLETE:
# get_user_preferences_tool = FunctionTool(func=get_user_preferences)
# get_payment_methods_tool = ...
# search_merchant_flights_tool = ...
# initiate_booking_tool = ...
# request_user_authorization_tool = ...
# confirm_payment_tool = ...


# TODO 8: Create the shopper agent
# Use Agent() with:
# - model: "gemini-2.0-flash"
# - name: "travel_shopper_agent"
# - description: A helpful description
# - instruction: Detailed instructions for the agent's behavior
# - tools: List of all the FunctionTools created above

# UNCOMMENT AND COMPLETE:
# shopper_agent = Agent(
#     model="gemini-2.0-flash",
#     name="travel_shopper_agent",
#     description="...",
#     instruction="""...""",
#     tools=[
#         # Add your tools here
#     ],
# )

# Placeholder until you complete the agent
shopper_agent = None

# Export the agent
root_agent = shopper_agent
