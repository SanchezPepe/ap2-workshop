#!/usr/bin/env python3
"""
AP2 Workshop Demo Runner

This script tests and demonstrates the workshop agents.
Use this to verify your implementation at each stage.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def print_banner():
    """Print the workshop banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         AP2 Workshop - Agent Payments Protocol               ║
║                                                              ║
║         Building Secure Agent Commerce with ADK              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def test_ap2_types():
    """Test the AP2 types implementation."""
    print("\n" + "=" * 60)
    print("Testing AP2 Types Implementation")
    print("=" * 60)

    try:
        from shared.ap2_types import (
            PaymentStatus,
            LineItem,
            PaymentMandate,
            create_ap2_extension,
        )

        # Test LineItem
        print("\n[Test 1] Creating LineItem...")
        item = LineItem(
            description="Test Flight",
            quantity=1,
            unit_price=100.00,
            currency="USD"
        )
        print(f"  ✓ LineItem created: {item.description}")
        print(f"  ✓ Total: ${item.total:.2f}")

        # Test PaymentMandate
        print("\n[Test 2] Creating PaymentMandate...")
        mandate = PaymentMandate(
            shopper_agent_id="test_shopper",
            merchant_agent_id="test_merchant",
            user_id="user_123",
            line_items=[item],
        )
        print(f"  ✓ Mandate created: {mandate.mandate_id[:8]}...")
        print(f"  ✓ Status: {mandate.status.value}")

        # Test total_amount
        print("\n[Test 3] Testing total_amount property...")
        print(f"  ✓ Total amount: ${mandate.total_amount:.2f}")

        # Test authorize
        print("\n[Test 4] Testing authorize() method...")
        mandate.authorize("test_token_12345")
        print(f"  ✓ Status after auth: {mandate.status.value}")
        print(f"  ✓ Token stored: {mandate.user_authorization_token[:10]}...")

        # Test to_summary
        print("\n[Test 5] Testing to_summary() method...")
        summary = mandate.to_summary()
        print(f"  ✓ Summary generated with {len(summary)} fields")

        print("\n" + "-" * 60)
        print("✅ All AP2 Types tests passed!")
        print("-" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Check your ap2_types.py implementation")
        return False


def test_shopper_tools():
    """Test the shopper agent tools."""
    print("\n" + "=" * 60)
    print("Testing Shopper Agent Tools")
    print("=" * 60)

    try:
        from shopper_agent.agent import (
            get_user_preferences,
            get_payment_methods,
            search_merchant_flights,
            initiate_booking,
            request_user_authorization,
            confirm_payment,
        )

        # Test get_user_preferences
        print("\n[Test 1] get_user_preferences()...")
        prefs = get_user_preferences()
        if prefs and "user_id" in prefs:
            print(f"  ✓ User: {prefs.get('name', 'Unknown')}")
        else:
            print("  ❌ Missing user_id in response")
            return False

        # Test get_payment_methods
        print("\n[Test 2] get_payment_methods()...")
        methods = get_payment_methods()
        if methods and "payment_methods" in methods:
            print(f"  ✓ Found {len(methods['payment_methods'])} payment methods")
        else:
            print("  ❌ Missing payment_methods in response")
            return False

        # Test search_merchant_flights
        print("\n[Test 3] search_merchant_flights('SFO', 'CDG')...")
        results = search_merchant_flights("SFO", "CDG")
        if results and "results" in results:
            print(f"  ✓ Found {len(results['results'])} flights")
        else:
            print("  ❌ Missing results in response")
            return False

        # Test initiate_booking
        print("\n[Test 4] initiate_booking('FL001', 'Test User')...")
        booking = initiate_booking("FL001", "Test User")
        if booking and "mandate_id" in booking:
            mandate_id = booking["mandate_id"]
            print(f"  ✓ Mandate created: {mandate_id}")
        else:
            print("  ❌ Missing mandate_id in response")
            return False

        # Test request_user_authorization
        print("\n[Test 5] request_user_authorization()...")
        auth = request_user_authorization(
            mandate_id=mandate_id,
            merchant_name="test_merchant",
            amount="$100.00",
            description="Test booking",
            line_items=["Test item - $100.00"],
        )
        if auth and "prompt_to_user" in auth:
            print(f"  ✓ Authorization prompt generated")
        else:
            print("  ❌ Missing prompt_to_user in response")
            return False

        # Test confirm_payment
        print("\n[Test 6] confirm_payment()...")
        confirmation = confirm_payment(mandate_id, approved=True)
        if confirmation and "authorization_token" in confirmation:
            print(f"  ✓ Token: {confirmation['authorization_token'][:16]}...")
        else:
            print("  ❌ Missing authorization_token in response")
            return False

        print("\n" + "-" * 60)
        print("✅ All Shopper Tools tests passed!")
        print("-" * 60)
        return True

    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("   Make sure all functions are implemented (not just 'pass')")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def test_shopper_agent():
    """Test that the shopper agent is properly configured."""
    print("\n" + "=" * 60)
    print("Testing Shopper Agent Configuration")
    print("=" * 60)

    try:
        from shopper_agent.agent import shopper_agent

        if shopper_agent is None:
            print("\n❌ shopper_agent is None")
            print("   Uncomment and complete the Agent() definition")
            return False

        print(f"\n  ✓ Agent name: {shopper_agent.name}")
        print(f"  ✓ Model: {shopper_agent.model}")
        print(f"  ✓ Tools: {len(shopper_agent.tools)} configured")

        for tool in shopper_agent.tools:
            print(f"    - {tool.name}")

        print("\n" + "-" * 60)
        print("✅ Shopper Agent configured correctly!")
        print("-" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def run_demo_flow():
    """Run the complete demo flow."""
    print("\n" + "=" * 60)
    print("Running Complete AP2 Demo Flow")
    print("=" * 60)

    try:
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
        booking = initiate_booking("FL001", "Workshop User")
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
        print("🎉 AP2 DEMO COMPLETE!")
        print("=" * 60)
        print("""
Key Takeaways:
1. User explicitly authorized the payment (no silent charges)
2. Cryptographic token proves user intent
3. Clear audit trail for accountability
4. Interoperable between any AP2-compliant agents
        """)
        return True

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        return False


def main():
    """Main entry point."""
    print_banner()

    print("\nWorkshop Test Options:")
    print("  1. Test AP2 Types (Phase 2)")
    print("  2. Test Shopper Tools (Phase 3)")
    print("  3. Test Shopper Agent (Phase 4)")
    print("  4. Run Complete Demo Flow")
    print("  5. Run All Tests")
    print("  6. Exit")

    choice = input("\nSelect option (1-6): ").strip()

    if choice == "1":
        test_ap2_types()
    elif choice == "2":
        test_shopper_tools()
    elif choice == "3":
        test_shopper_agent()
    elif choice == "4":
        run_demo_flow()
    elif choice == "5":
        print("\nRunning all tests...\n")
        t1 = test_ap2_types()
        t2 = test_shopper_tools()
        t3 = test_shopper_agent()

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  AP2 Types:      {'✅ PASS' if t1 else '❌ FAIL'}")
        print(f"  Shopper Tools:  {'✅ PASS' if t2 else '❌ FAIL'}")
        print(f"  Shopper Agent:  {'✅ PASS' if t3 else '❌ FAIL'}")

        if t1 and t2 and t3:
            print("\n🎉 All tests passed! Ready for the demo.")
            run_demo_flow()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()
