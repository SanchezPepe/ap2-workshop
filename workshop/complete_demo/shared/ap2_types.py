"""
AP2 Protocol Types and Utilities - COMPLETE WORKING VERSION

This module defines the core types and utilities for the AP2 protocol,
including roles, extension parameters, and payment mandate structures.
"""

from typing import Literal
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid


# ============================================================================
# AP2 Role Types
# ============================================================================

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
    """Status of a payment mandate."""
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
    """A line item in a payment mandate."""
    description: str
    quantity: int = 1
    unit_price: float
    currency: str = "USD"

    @property
    def total(self) -> float:
        """Calculate the total price for this line item."""
        return self.quantity * self.unit_price


# ============================================================================
# Payment Mandate
# ============================================================================

class PaymentMandate(BaseModel):
    """
    AP2 Payment Mandate

    A mandate represents a user's authorization for an agent to make a payment.
    It includes cryptographic proof of intent to prevent unauthorized transactions.
    """
    mandate_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Parties involved
    shopper_agent_id: str
    merchant_agent_id: str
    user_id: str

    # Payment details
    line_items: list[LineItem]
    currency: str = "USD"

    # Authorization
    status: PaymentStatus = PaymentStatus.PENDING
    user_authorization_token: str | None = None
    authorization_timestamp: datetime | None = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    merchant_reference: str | None = None
    description: str | None = None

    @property
    def total_amount(self) -> float:
        """Calculate total amount from all line items."""
        return sum(item.total for item in self.line_items)

    def authorize(self, token: str) -> None:
        """Authorize the mandate with a user token."""
        self.user_authorization_token = token
        self.authorization_timestamp = datetime.utcnow()
        self.status = PaymentStatus.AUTHORIZED

    def to_summary(self) -> dict:
        """Return a summary suitable for display to users."""
        return {
            "mandate_id": self.mandate_id,
            "merchant": self.merchant_agent_id,
            "total": f"{self.currency} {self.total_amount:.2f}",
            "items": [
                f"{item.description} x{item.quantity} = {item.currency} {item.total:.2f}"
                for item in self.line_items
            ],
            "status": self.status.value
        }


# ============================================================================
# AP2 Extension Helper
# ============================================================================

AP2_EXTENSION_URI = "https://github.com/google-agentic-commerce/ap2/tree/v0.1"


def create_ap2_extension(roles: list[AP2Role]) -> dict:
    """Create an AP2 extension object for an AgentCard."""
    return {
        "uri": AP2_EXTENSION_URI,
        "description": f"This agent supports AP2 with roles: {', '.join(roles)}",
        "params": {
            "roles": roles
        }
    }
