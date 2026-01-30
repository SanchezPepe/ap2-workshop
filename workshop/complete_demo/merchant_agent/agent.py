"""
Merchant Agent - Flight Booking Service (COMPLETE WORKING VERSION)

This agent acts as a merchant in the AP2 protocol, offering flight
booking services and accepting payments from shopper agents.
"""

import os
import sys
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk import Agent
from google.adk.tools import FunctionTool

from shared.ap2_types import (
    LineItem,
    PaymentMandate,
    PaymentStatus,
    create_ap2_extension,
)


# ============================================================================
# Flight Database (Mock Data)
# ============================================================================

FLIGHTS_DB = [
    {
        "flight_id": "FL001",
        "airline": "SkyHigh Airlines",
        "origin": "SFO",
        "destination": "CDG",
        "departure": "2025-03-15 10:00",
        "arrival": "2025-03-16 06:30",
        "price": 850.00,
        "class": "economy",
        "seats_available": 45,
    },
    {
        "flight_id": "FL002",
        "airline": "SkyHigh Airlines",
        "origin": "SFO",
        "destination": "CDG",
        "departure": "2025-03-15 14:30",
        "arrival": "2025-03-16 10:00",
        "price": 920.00,
        "class": "economy",
        "seats_available": 23,
    },
    {
        "flight_id": "FL003",
        "airline": "Premium Air",
        "origin": "SFO",
        "destination": "CDG",
        "departure": "2025-03-15 08:00",
        "arrival": "2025-03-15 23:30",
        "price": 1450.00,
        "class": "business",
        "seats_available": 8,
    },
    {
        "flight_id": "FL004",
        "airline": "Budget Wings",
        "origin": "SFO",
        "destination": "CDG",
        "departure": "2025-03-15 23:00",
        "arrival": "2025-03-16 18:00",
        "price": 620.00,
        "class": "economy",
        "seats_available": 120,
    },
]

BOOKINGS: dict[str, dict] = {}
PAYMENT_MANDATES: dict[str, PaymentMandate] = {}


# ============================================================================
# Merchant Tools
# ============================================================================

def search_flights(
    origin: str,
    destination: str,
    date: str | None = None,
    travel_class: str | None = None,
    max_price: float | None = None,
) -> dict[str, Any]:
    """Search for available flights."""
    results = []

    for flight in FLIGHTS_DB:
        if flight["origin"].upper() != origin.upper():
            continue
        if flight["destination"].upper() != destination.upper():
            continue
        if travel_class and flight["class"] != travel_class.lower():
            continue
        if max_price and flight["price"] > max_price:
            continue
        if date and not flight["departure"].startswith(date):
            continue
        if flight["seats_available"] > 0:
            results.append(flight)

    return {
        "status": "success",
        "query": {
            "origin": origin,
            "destination": destination,
            "date": date,
            "class": travel_class,
            "max_price": max_price,
        },
        "results_count": len(results),
        "flights": results,
    }


def get_flight_details(flight_id: str) -> dict[str, Any]:
    """Get detailed information about a specific flight."""
    for flight in FLIGHTS_DB:
        if flight["flight_id"] == flight_id:
            return {
                "status": "success",
                "flight": flight,
                "policies": {
                    "cancellation": "Free cancellation up to 24 hours before departure",
                    "baggage": "1 carry-on included, checked bags extra",
                    "changes": "Changes allowed with $75 fee",
                }
            }
    return {"status": "error", "message": f"Flight {flight_id} not found"}


def create_booking_mandate(
    flight_id: str,
    passenger_name: str,
    shopper_agent_id: str,
    user_id: str,
) -> dict[str, Any]:
    """Create an AP2 payment mandate for booking a flight."""
    flight = None
    for f in FLIGHTS_DB:
        if f["flight_id"] == flight_id:
            flight = f
            break

    if not flight:
        return {"status": "error", "message": f"Flight {flight_id} not found"}

    if flight["seats_available"] <= 0:
        return {"status": "error", "message": "No seats available on this flight"}

    line_items = [
        LineItem(
            description=f"Flight {flight_id}: {flight['origin']} → {flight['destination']}",
            quantity=1,
            unit_price=flight["price"],
            currency="USD",
        ),
        LineItem(
            description="Taxes and fees",
            quantity=1,
            unit_price=round(flight["price"] * 0.12, 2),
            currency="USD",
        ),
    ]

    mandate = PaymentMandate(
        shopper_agent_id=shopper_agent_id,
        merchant_agent_id="flight_merchant_agent",
        user_id=user_id,
        line_items=line_items,
        description=f"Flight booking for {passenger_name}",
        merchant_reference=flight_id,
    )

    PAYMENT_MANDATES[mandate.mandate_id] = mandate

    return {
        "status": "success",
        "message": "Payment mandate created - awaiting user authorization",
        "mandate": mandate.to_summary(),
        "mandate_id": mandate.mandate_id,
        "requires_authorization": True,
        "authorization_prompt": f"Do you authorize payment of USD {mandate.total_amount:.2f} for flight {flight_id}?",
    }


def process_authorized_payment(
    mandate_id: str,
    authorization_token: str,
) -> dict[str, Any]:
    """Process a payment after user authorization."""
    mandate = PAYMENT_MANDATES.get(mandate_id)

    if not mandate:
        return {"status": "error", "message": f"Mandate {mandate_id} not found"}

    if mandate.status != PaymentStatus.PENDING:
        return {"status": "error", "message": f"Mandate is not pending (status: {mandate.status.value})"}

    mandate.authorize(authorization_token)
    mandate.status = PaymentStatus.PROCESSING
    mandate.status = PaymentStatus.COMPLETED

    booking_id = f"BK{mandate.mandate_id[:8].upper()}"
    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "mandate_id": mandate_id,
        "flight_id": mandate.merchant_reference,
        "status": "confirmed",
        "total_paid": mandate.total_amount,
    }

    return {
        "status": "success",
        "message": "Payment processed and booking confirmed!",
        "booking": {
            "booking_id": booking_id,
            "flight_id": mandate.merchant_reference,
            "confirmation_code": booking_id,
            "amount_charged": f"USD {mandate.total_amount:.2f}",
            "payment_status": "completed",
        },
        "ap2_receipt": {
            "mandate_id": mandate_id,
            "authorization_timestamp": mandate.authorization_timestamp.isoformat() if mandate.authorization_timestamp else None,
            "merchant": mandate.merchant_agent_id,
            "shopper": mandate.shopper_agent_id,
        }
    }


# ============================================================================
# Create the Merchant Agent
# ============================================================================

search_flights_tool = FunctionTool(func=search_flights)
get_flight_details_tool = FunctionTool(func=get_flight_details)
create_booking_mandate_tool = FunctionTool(func=create_booking_mandate)
process_authorized_payment_tool = FunctionTool(func=process_authorized_payment)

merchant_agent = Agent(
    model="gemini-2.0-flash",
    name="flight_merchant_agent",
    description="A flight booking merchant that sells airline tickets via AP2 protocol",
    instruction="""You are a flight booking merchant agent. You help other agents
    find and book flights for their users.

    Your capabilities:
    1. Search for available flights based on origin, destination, date, and preferences
    2. Provide detailed flight information
    3. Create payment mandates for bookings (AP2 protocol)
    4. Process payments after user authorization

    When a shopper agent wants to book a flight:
    1. First help them search for available options
    2. Provide flight details when requested
    3. Create a payment mandate when they're ready to book
    4. Wait for the authorization token before processing payment
    5. Confirm the booking after successful payment

    Always be helpful and provide clear pricing information including taxes and fees.
    """,
    tools=[
        search_flights_tool,
        get_flight_details_tool,
        create_booking_mandate_tool,
        process_authorized_payment_tool,
    ],
)

root_agent = merchant_agent
