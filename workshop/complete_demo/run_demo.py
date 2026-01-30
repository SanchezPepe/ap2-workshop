#!/usr/bin/env python3
"""
AP2 Complete Demo Runner

This script demonstrates the complete AP2 protocol flow
with fully working shopper and merchant agents.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def print_banner():
    """Print the demo banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            AP2 - Agent Payments Protocol Demo                ║
║                                                              ║
║    Demonstrating secure agent commerce with ADK + A2A        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def print_protocol_stack():
    """Print the protocol stack diagram."""
    print("""
Protocol Stack:
┌─────────────────────────────────────┐
│  AP2  - Payments (this demo)        │
├─────────────────────────────────────┤
│  A2A  - Agent Communication         │
├─────────────────────────────────────┤
│  MCP  - Tools & APIs                │
├─────────────────────────────────────┤
│  ADK  - Agent Framework             │
└─────────────────────────────────────┘
    """)


def demo_flow():
    """Run the interactive demo flow."""
    from shopper_agent.agent import shopper_agent
    from shared.ap2_types import AP2_EXTENSION_URI

    print("\n" + "=" * 60)
    print("DEMO: Travel Booking with AP2 Payment Authorization")
    print("=" * 60)

    print(f"\nAP2 Extension URI: {AP2_EXTENSION_URI}")
    print(f"Shopper Agent: {shopper_agent.name}")
    print(f"Agent Description: {shopper_agent.description}")

    print("\n" + "-" * 60)
    print("Available Tools:")
    print("-" * 60)
    for tool in shopper_agent.tools:
        print(f"  • {tool.name}")

    print("\n" + "-" * 60)
    print("Demo Scenario: Book a flight to Paris")
    print("-" * 60)

    from shopper_agent.agent import (
        search_merchant_flights,
        initiate_booking,
        request_user_authorization,
        confirm_payment,
    )

    print("\n[Step 1] Searching for flights SFO → CDG...")
    results = search_merchant_flights("SFO", "CDG", "2025-03-15")
    print(f"Found {len(results['results'])} flights:\n")

    for flight in results["results"]:
        print(f"  {flight['flight_id']}: {flight['airline']}")
        print(f"    {flight['departure']} → {flight['arrival']}")
        print(f"    Price: {flight['price']} ({flight['class']})")
        print()

    print("\n[Step 2] User selects FL001, initiating booking...")
    booking = initiate_booking("FL001", "Demo User")
    print(f"Mandate created: {booking['mandate_id']}")
    print(f"Total: {booking['payment']['total']}")

    print("\n[Step 3] Requesting user authorization (AP2 flow)...")
    auth_request = request_user_authorization(
        mandate_id=booking["mandate_id"],
        merchant_name=booking["merchant"],
        amount=booking["payment"]["total"],
        description="Flight booking",
        line_items=booking["line_items"],
    )
    print(auth_request["prompt_to_user"])

    print("\n[Step 4] User confirms payment...")
    confirmation = confirm_payment(booking["mandate_id"], approved=True)
    print(f"Status: {confirmation['status']}")
    print(f"Authorization Token: {confirmation['authorization_token']}")

    print("\n[Step 5] Token sent to merchant, booking confirmed!")
    print("\n" + "=" * 60)
    print("AP2 DEMO COMPLETE")
    print("=" * 60)
    print("""
Key Takeaways:
1. User explicitly authorized the payment (no silent charges)
2. Cryptographic token proves user intent
3. Clear audit trail for accountability
4. Interoperable between any AP2-compliant agents
    """)


def run_interactive_agent():
    """Run the shopper agent in interactive mode."""
    print("\nStarting interactive agent session...")
    print("Run: adk web shopper_agent")
    print("Then navigate to http://localhost:8000 in your browser")


def main():
    """Main entry point."""
    print_banner()
    print_protocol_stack()

    print("\nDemo Options:")
    print("  1. Run automated demo flow")
    print("  2. Show how to run interactive agent")
    print("  3. Exit")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        demo_flow()
    elif choice == "2":
        run_interactive_agent()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
