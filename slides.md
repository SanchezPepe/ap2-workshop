# Agent Payments Protocol (AP2)
## Enabling Secure Agent Commerce

---

# What Problem Does AP2 Solve?

In the emerging **Agent Economy**, AI agents need to:

- Browse and compare products/services
- Negotiate on behalf of users
- **Make payments** securely

**The Challenge:** How do we trust an AI to spend our money?

- What if the agent "hallucinates" a purchase?
- Who is accountable if something goes wrong?
- How do we prove the user actually authorized it?

---

# Introducing AP2

**Agent Payments Protocol (AP2)** is an open protocol that enables:

- **Secure** agent-to-agent payments
- **Verifiable** user authorization
- **Accountable** transactions with audit trails

> "AP2 builds trust through cryptographic proof of intent"

---

# The Protocol Stack

```
┌─────────────────────────────────────────┐
│   AP2 - Agent Payments Protocol         │  Payments & Mandates
│   "Agents communicate about payments"   │
├─────────────────────────────────────────┤
│   A2A - Agent-to-Agent Protocol         │  Tasks & Messages
│   "Agents communicate with agents"      │
├─────────────────────────────────────────┤
│   MCP - Model Context Protocol          │  Tools & APIs
│   "Agents communicate with data"        │
├─────────────────────────────────────────┤
│   ADK - Agent Development Kit           │  Build & Deploy
│   "Framework for building agents"       │
└─────────────────────────────────────────┘
```

---

# AP2 Roles

| Role | Description | Example |
|------|-------------|---------|
| **Shopper** | Acts on user's behalf to make purchases | Travel booking agent |
| **Merchant** | Sells goods or services | Airline ticket agent |
| **Credentials Provider** | Manages user payment methods | Digital wallet agent |
| **Payment Processor** | Handles actual transactions | Payment gateway agent |

---

# How AP2 Works

```
   User                Shopper Agent           Merchant Agent
    │                       │                        │
    │  "Book flight to     │                        │
    │   Paris"             │                        │
    │──────────────────────>│                        │
    │                       │   Search flights       │
    │                       │───────────────────────>│
    │                       │                        │
    │                       │   Flight options       │
    │                       │<───────────────────────│
    │   Here are options    │                        │
    │<──────────────────────│                        │
    │                       │                        │
    │   "Book option 2"     │                        │
    │──────────────────────>│                        │
    │                       │                        │
    │   ┌─────────────────────────────────────────┐  │
    │   │         AP2 PAYMENT FLOW                │  │
    │   │  1. Create Payment Mandate              │  │
    │   │  2. User Authorization (cryptographic)  │  │
    │   │  3. Process Payment                     │  │
    │   │  4. Return Confirmation                 │  │
    │   └─────────────────────────────────────────┘  │
    │                       │                        │
    │   Booking confirmed!  │                        │
    │<──────────────────────│                        │
```

---

# Guiding Principles

### 1. Openness & Interoperability
Any compliant agent works with any compliant merchant

### 2. User Control & Privacy
User is **always** the ultimate authority

### 3. Verifiable Intent
Cryptographic proof of authorization - no "hallucinated" purchases

### 4. Clear Accountability
Non-repudiable audit trail for dispute resolution

---

# AgentCard with AP2 Extension

Agents declare AP2 support in their AgentCard:

```json
{
  "name": "Travel Booking Agent",
  "capabilities": {
    "extensions": [
      {
        "uri": "https://github.com/google-agentic-commerce/ap2/tree/v0.1",
        "params": {
          "roles": ["shopper"]
        }
      }
    ]
  },
  "skills": [
    { "id": "book_flight", "name": "Book Flight" },
    { "id": "book_hotel", "name": "Book Hotel" }
  ]
}
```

---

# Demo Time!

We'll build:

1. **Shopper Agent** - Books travel on user's behalf
2. **Merchant Agent** - Sells flight tickets
3. **A2A Communication** - Agents discover and talk to each other
4. **AP2 Payment Flow** - Secure payment authorization

---

# Resources

| Resource | Link |
|----------|------|
| AP2 Protocol | https://ap2-protocol.org |
| ADK Documentation | https://google.github.io/adk-docs |
| A2A Quickstart | https://google.github.io/adk-docs/a2a |
| ADK Samples | https://github.com/google/adk-samples |
| AP2 GitHub | https://github.com/google-agentic-commerce/ap2 |

---

# Questions?

