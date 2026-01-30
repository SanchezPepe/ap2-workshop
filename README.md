# AP2 Demo - Agent Payments Protocol

This repository contains a hands-on demo of the **Agent Payments Protocol (AP2)** using Google's **Agent Development Kit (ADK)**.

## What is AP2?

AP2 is an open protocol that enables secure, reliable, and interoperable agent commerce. It allows AI agents to make payments on behalf of users with:

- **Verifiable Intent** - Cryptographic proof of user authorization
- **Clear Accountability** - Non-repudiable audit trails
- **User Control** - Users always authorize payments explicitly

## Repository Structure

```
AP2/
├── slides.md                 # Presentation slides (Marp/Markdown)
├── README.md                 # This file
└── demo/
    ├── requirements.txt      # Python dependencies
    ├── .env.example          # Environment variables template
    ├── run_demo.py           # Interactive demo runner
    ├── shared/
    │   ├── __init__.py
    │   └── ap2_types.py      # AP2 protocol types and utilities
    ├── shopper_agent/
    │   ├── __init__.py
    │   ├── agent.py          # Shopper agent implementation
    │   └── agent_card.json   # A2A AgentCard with AP2 extension
    └── merchant_agent/
        ├── __init__.py
        ├── agent.py          # Merchant agent implementation
        └── agent_card.json   # A2A AgentCard with AP2 extension
```

## Quick Start

### Prerequisites

- Python 3.10+
- Google API Key (for Gemini models)

### Installation

```bash
# Clone or navigate to the repository
cd AP2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r demo/requirements.txt

# Configure environment
cp demo/.env.example demo/.env
# Edit demo/.env and add your GOOGLE_API_KEY
```

### Run the Demo

```bash
# Run the automated demo
python demo/run_demo.py

# Or run the shopper agent with ADK web UI
cd demo/shopper_agent
adk web
# Then open http://localhost:8000
```

### Run with A2A (Multi-Agent)

```bash
# Terminal 1: Start the merchant agent
cd demo/merchant_agent
adk api_server --a2a --port 8002

# Terminal 2: Start the shopper agent
cd demo/shopper_agent
adk api_server --a2a --port 8001
```

## Presentation

The `slides.md` file contains presentation slides in Markdown format. You can present them using:

- [Marp](https://marp.app/) - Markdown Presentation Ecosystem
- [Slidev](https://sli.dev/) - Presentation Slides for Developers
- Any Markdown viewer with slide support

```bash
# Using Marp CLI
npx @marp-team/marp-cli slides.md --html

# Using Marp VS Code extension
# Just open slides.md and use the preview
```

## Demo Scenario

The demo simulates a travel booking flow:

1. **User** asks to book a flight to Paris
2. **Shopper Agent** searches merchant agents for flights
3. **Merchant Agent** returns available options with prices
4. **User** selects a flight
5. **AP2 Payment Flow**:
   - Merchant creates a payment mandate
   - Shopper requests user authorization
   - User provides cryptographic authorization token
   - Payment is processed with verifiable proof of intent
6. **Booking Confirmed** with full audit trail

## AP2 Roles Demonstrated

| Role | Agent | Description |
|------|-------|-------------|
| Shopper | `travel_shopper_agent` | Acts on user's behalf |
| Merchant | `flight_merchant_agent` | Sells flight tickets |

## Key Files Explained

### `shared/ap2_types.py`
Core AP2 types including:
- `AP2Role` - Protocol roles (shopper, merchant, etc.)
- `PaymentMandate` - Authorization structure
- `PaymentStatus` - Transaction states

### `shopper_agent/agent.py`
Implements a shopper agent that:
- Searches for flights via merchant agents
- Handles AP2 payment authorization flow
- Never charges without explicit user approval

### `merchant_agent/agent.py`
Implements a merchant agent that:
- Provides flight search and booking services
- Creates payment mandates
- Processes authorized payments

## Resources

- [AP2 Protocol Documentation](https://ap2-protocol.org)
- [ADK Documentation](https://google.github.io/adk-docs)
- [A2A Protocol](https://google.github.io/adk-docs/a2a)
- [ADK Samples](https://github.com/google/adk-samples)

## License

This demo is provided for educational purposes.
