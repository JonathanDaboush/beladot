"""
Aggregate imports for ORM models so SQLAlchemy's Base.metadata is fully populated
at runtime for migrations, testing, and app startup.

Import modules that declare tables and relationships referenced across the app
and tests. Keep this list in sync with new models as they are added.
"""

# Core
from .user import User

# Catalog
from .category import Category
from .subcategory import Subcategory
from .product import Product
from .product_variant import ProductVariant

# Images / reviews (optional, extend as needed)
from .product_image import ProductImage
from .product_comment import ProductComment
from .product_review import ProductReview
from .product_rating import ProductRating


# Cart / order (optional, extend as needed)
from .cart import Cart
from .cart_item import CartItem
from .order import Order
from .order_item import OrderItem

# Wishlist
from .wishlist import Wishlist
from .wishlist_item import WishlistItem

# Employee / Manager / Department
from .department import Department
from .employee import Employee
from .manager import Manager
from .shift import Shift
from .employee_payment import EmployeePayment
from .employee_pto import EmployeePTO
from .employee_sickday import EmployeeSickday

# Snapshots
from .address_snapshot import AddressSnapshot
from .employee_snapshot import EmployeeSnapshot
from .user_snapshot import UserSnapshot
from .payment_snapshot import PaymentSnapshot
from .paystub_snapshot import PaystubSnapshot
from .pto_snapshot import PTOSnapshot
from .sickday_snapshot import SickdaySnapshot
from .seller_snapshot import SellerSnapshot
from .shipping_snapshot import ShippingSnapshot
from .refund_snapshot import RefundSnapshot
from .reimbursement_snapshot import ReimbursementSnapshot

# Shipping
from .shipment import Shipment
from .shipment_item import ShipmentItem
from .shipment_event import ShipmentEvent
from .shipment_address import ShipmentAddress
from .shipment_issue import ShipmentIssue
from .return_shipment import ReturnShipment

# Components
from .employee_component import EmployeeComponent
from .seller_component import SellerComponent
from .customer_component import CustomerComponent

# Finance
from .payment import Payment
from .refund import Refund
from .refund_request import RefundRequest
from .refund_ledger import RefundLedger
from .reimbursement import Reimbursement
from .ledger import Ledger
from .seller_payout import SellerPayout
from .sellers_expense import SellersExpense
from .finance_employee import FinanceEmployee
from .user_finance import UserFinance

# Misc
from .incident import Incident
from .shift_request import ShiftRequest
from .customer_shipment import CustomerShipment
from .seller_review_response import SellerReviewResponse
from .product_variant_image import ProductVariantImage

# NOTE: Imports above are for SQLAlchemy model registration side effects only.
#       This is intentional and required for Base.metadata population.
#       See file docstring for details. Do not remove unless model registration changes.
