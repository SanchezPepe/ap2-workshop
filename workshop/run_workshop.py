#!/usr/bin/env python3
"""
AP2 Workshop Runner

Quick workshop to learn AP2 payment authorization.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def print_banner():
    print("""
╔════════════════════════════════════════════════════════╗
║                                                        ║
║          AP2 Workshop - Secure Agent Payments          ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    """)


def test_authorization():
    """Test the AP2 authorization functions."""
    print("\n" + "=" * 50)
    print("Testing AP2 Authorization Functions")
    print("=" * 50)

    try:
        from shopper_agent.agent import (
            initiate_booking,
            request_user_authorization,
            confirm_payment,
        )

        # Test initiate_booking (pre-built)
        print("\n[1/3] Creating booking mandate...")
        booking = initiate_booking("FL001", "Test User")
        mandate_id = booking["mandate_id"]
        print(f"  ✓ Mandate: {mandate_id}")

        # Test request_user_authorization (TODO 1)
        print("\n[2/3] Testing request_user_authorization()...")
        auth = request_user_authorization(
            mandate_id=mandate_id,
            merchant_name="flight_merchant",
            amount="$952.00",
            description="Flight booking",
            line_items=["Flight FL001 - $850.00", "Taxes - $102.00"],
        )

        if auth is None:
            print("  ❌ Function returns None - implement TODO 1")
            return False

        if "prompt_to_user" not in auth:
            print("  ❌ Missing 'prompt_to_user' in response")
            return False

        print("  ✓ Authorization prompt generated")
        print(auth["prompt_to_user"])

        # Test confirm_payment (TODO 2)
        print("\n[3/3] Testing confirm_payment()...")
        confirmation = confirm_payment(mandate_id, approved=True)

        if confirmation is None:
            print("  ❌ Function returns None - implement TODO 2")
            return False

        if "authorization_token" not in confirmation:
            print("  ❌ Missing 'authorization_token' in response")
            return False

        print(f"  ✓ Token: {confirmation['authorization_token']}")

        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def run_demo():
    """Run the complete AP2 demo flow."""
    print("\n" + "=" * 50)
    print("AP2 Payment Flow Demo")
    print("=" * 50)

    try:
        from shopper_agent.agent import (
            search_merchant_flights,
            initiate_booking,
            request_user_authorization,
            confirm_payment,
        )

        print("\n[Step 1] Searching flights SFO → CDG...")
        results = search_merchant_flights("SFO", "CDG")
        for f in results["results"]:
            print(f"  {f['flight_id']}: {f['airline']} - {f['price']}")

        print("\n[Step 2] Booking FL001...")
        booking = initiate_booking("FL001", "Demo User")
        print(f"  Mandate: {booking['mandate_id']}")
        print(f"  Total: {booking['payment']['total']}")

        print("\n[Step 3] Requesting authorization...")
        auth = request_user_authorization(
            mandate_id=booking["mandate_id"],
            merchant_name=booking["merchant"],
            amount=booking["payment"]["total"],
            description="Flight booking",
            line_items=booking["line_items"],
        )

        if auth and "prompt_to_user" in auth:
            print(auth["prompt_to_user"])
        else:
            print("  ❌ request_user_authorization not implemented")
            return

        print("\n[Step 4] User confirms payment...")
        confirmation = confirm_payment(booking["mandate_id"], approved=True)

        if confirmation and "authorization_token" in confirmation:
            print(f"  ✓ Status: {confirmation['status']}")
            print(f"  ✓ Token: {confirmation['authorization_token']}")
        else:
            print("  ❌ confirm_payment not implemented")
            return

        print("\n" + "=" * 50)
        print("🎉 BOOKING COMPLETE!")
        print("=" * 50)
        print("""
Key AP2 Concepts Demonstrated:
1. User saw exactly what they were paying for
2. User explicitly approved the payment
3. Cryptographic token proves user intent
4. No silent charges possible
        """)

    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    print_banner()

    print("Options:")
    print("  1. Test your implementation")
    print("  2. Run complete demo")
    print("  3. Exit")

    choice = input("\nSelect (1-3): ").strip()

    if choice == "1":
        test_authorization()
    elif choice == "2":
        run_demo()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
