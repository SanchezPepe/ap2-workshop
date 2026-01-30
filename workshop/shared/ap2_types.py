"""
AP2 Protocol Types and Utilities

This module defines the core types and utilities for the AP2 protocol,
including roles, extension parameters, and payment mandate structures.

WORKSHOP: You will complete the PaymentMandate class and helper functions.
"""

from typing import Literal
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid


# ============================================================================
# AP2 Role Types
# ============================================================================

# AP2 defines four roles that agents can play in the payment ecosystem
AP2Role = Literal["merchant", "shopper", "credentials-provider", "payment-processor"]


class AP2ExtensionParameters(BaseModel):
    """Parameters for the AP2 A2A extension."""
    roles: list[AP2Role] = Field(
        ...,
        min_length=1,
        description="The roles this agent performs in AP2"
    )


# ============================================================================
# Payment Status
# ============================================================================

class PaymentStatus(str, Enum):
    """
    Status of a payment mandate.

    Lifecycle: PENDING → AUTHORIZED → PROCESSING → COMPLETED
               (can transition to FAILED or CANCELLED at any point)
    """
    PENDING = "pending"
    AUTHORIZED = "authorized"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================================
# Payment Method
# ============================================================================

class PaymentMethod(BaseModel):
    """Represents a payment method."""
    type: str = Field(..., description="Payment method type (e.g., 'card', 'bank_transfer')")
    last_four: str | None = Field(None, description="Last four digits of card/account")
    brand: str | None = Field(None, description="Card brand or bank name")


# ============================================================================
# Line Item
# ============================================================================

class LineItem(BaseModel):
    """
    A line item in a payment mandate.

    Represents a single item being purchased with its price and quantity.
    """
    description: str
    quantity: int = 1
    unit_price: float
    currency: str = "USD"

    @property
    def total(self) -> float:
        """Calculate the total price for this line item."""
        return self.quantity * self.unit_price


# ============================================================================
# Payment Mandate - COMPLETE THIS CLASS
# ============================================================================

class PaymentMandate(BaseModel):
    """
    AP2 Payment Mandate

    A mandate represents a user's authorization for an agent to make a payment.
    It includes cryptographic proof of intent to prevent unauthorized transactions.

    WORKSHOP TODO: Complete this class by adding:
    1. The missing fields (see comments below)
    2. The authorize() method
    3. The to_summary() method
    """

    # Unique identifier for this mandate
    mandate_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 1: Add the parties involved in this transaction
    # ─────────────────────────────────────────────────────────────────────────
    # Add these fields:
    # - shopper_agent_id: str  (the agent acting on behalf of user)
    # - merchant_agent_id: str (the agent selling goods/services)
    # - user_id: str           (the human authorizing the payment)

    shopper_agent_id: str
    merchant_agent_id: str
    user_id: str

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 2: Add payment details
    # ─────────────────────────────────────────────────────────────────────────
    # - line_items: list[LineItem]  (items being purchased)
    # - currency: str = "USD"       (payment currency)

    # UNCOMMENT AND COMPLETE:
    # line_items: ...
    # currency: ...

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 3: Add authorization fields
    # ─────────────────────────────────────────────────────────────────────────
    # - status: PaymentStatus = PaymentStatus.PENDING
    # - user_authorization_token: str | None = None
    # - authorization_timestamp: datetime | None = None

    # UNCOMMENT AND COMPLETE:
    # status: ...
    # user_authorization_token: ...
    # authorization_timestamp: ...

    # ─────────────────────────────────────────────────────────────────────────
    # Metadata (provided for you)
    # ─────────────────────────────────────────────────────────────────────────
    created_at: datetime = Field(default_factory=datetime.utcnow)
    merchant_reference: str | None = None
    description: str | None = None

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 4: Add the total_amount property
    # ─────────────────────────────────────────────────────────────────────────
    # This should sum up all line items
    #
    # @property
    # def total_amount(self) -> float:
    #     """Calculate total amount from all line items."""
    #     # HINT: Use sum() with a generator expression over self.line_items
    #     pass

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 5: Implement the authorize() method
    # ─────────────────────────────────────────────────────────────────────────
    # def authorize(self, token: str) -> None:
    #     """
    #     Authorize the mandate with a user token.
    #
    #     This method should:
    #     1. Store the authorization token
    #     2. Record the current timestamp
    #     3. Update status to AUTHORIZED
    #     """
    #     pass

    # ─────────────────────────────────────────────────────────────────────────
    # TODO 6: Implement the to_summary() method
    # ─────────────────────────────────────────────────────────────────────────
    # def to_summary(self) -> dict:
    #     """
    #     Return a summary suitable for display to users.
    #
    #     Should return a dict with:
    #     - mandate_id
    #     - merchant (the merchant_agent_id)
    #     - total (formatted as "USD 123.45")
    #     - items (list of formatted line item strings)
    #     - status (the status value)
    #     """
    #     pass


# ============================================================================
# AP2 Extension Helper
# ============================================================================

# The URI that identifies AP2-compatible agents
AP2_EXTENSION_URI = "https://github.com/google-agentic-commerce/ap2/tree/v0.1"


def create_ap2_extension(roles: list[AP2Role]) -> dict:
    """
    Create an AP2 extension object for an AgentCard.

    This is used when registering an agent to declare its AP2 capabilities.

    Args:
        roles: List of AP2 roles this agent supports

    Returns:
        Extension dictionary for the agent card
    """
    return {
        "uri": AP2_EXTENSION_URI,
        "description": f"This agent supports AP2 with roles: {', '.join(roles)}",
        "params": {
            "roles": roles
        }
    }
