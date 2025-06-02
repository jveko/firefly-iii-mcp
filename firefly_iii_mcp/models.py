# ABOUTME: This file defines Pydantic models for all Firefly III data structures.
# ABOUTME: It provides type safety and validation for API requests and responses.

"""Data models and type definitions for Firefly III resources."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


# Core enums
class ShortAccountTypeProperty(str, Enum):
    """Account types in Firefly III."""
    ASSET = "asset"
    EXPENSE = "expense"
    IMPORT = "import"
    REVENUE = "revenue"
    CASH = "cash"
    LIABILITY = "liability"
    LIABILITIES = "liabilities"
    INITIAL_BALANCE = "initial-balance"
    RECONCILIATION = "reconciliation"


class TransactionTypeProperty(str, Enum):
    """Transaction types in Firefly III."""
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    RECONCILIATION = "reconciliation"
    OPENING_BALANCE = "opening balance"


class AccountRoleProperty(str, Enum):
    """Account roles for asset accounts."""
    DEFAULT_ASSET = "defaultAsset"
    SHARED_ASSET = "sharedAsset"
    SAVING_ASSET = "savingAsset"
    CC_ASSET = "ccAsset"
    CASH_WALLET_ASSET = "cashWalletAsset"


class AutoBudgetType(str, Enum):
    """Auto budget types."""
    NONE = "none"
    RESET = "reset"
    ROLLOVER = "rollover"


class AutoBudgetPeriod(str, Enum):
    """Auto budget periods."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEAR = "half-year"
    YEARLY = "yearly"


# Base response models
class Meta(BaseModel):
    """Pagination metadata for API responses."""
    pagination: Optional[Dict[str, Any]] = None


class BaseRead(BaseModel):
    """Base class for API resource reads with type/id/attributes pattern."""
    type: str
    id: str
    attributes: Dict[str, Any]


# Response wrapper models
class BaseResponse(BaseModel):
    """Base response model with data and metadata."""
    data: Any
    meta: Optional[Meta] = None


class BaseArrayResponse(BaseResponse):
    """Array response with multiple resources."""
    data: List[BaseRead]


class BaseSingleResponse(BaseResponse):
    """Single resource response."""
    data: BaseRead


# Core data models
class Account(BaseModel):
    """Firefly III Account model."""
    model_config = ConfigDict(populate_by_name=True)
    # Required fields
    name: str = Field(..., description="Account name")
    type: ShortAccountTypeProperty = Field(..., description="Account type")
    
    # Optional fields
    active: bool = Field(default=True, description="Whether the account is active")
    order: Optional[int] = Field(default=None, description="Display order")
    account_role: Optional[AccountRoleProperty] = Field(default=None, description="Account role for asset accounts")
    
    # Currency fields
    currency_id: Optional[str] = Field(default=None, description="Currency ID")
    currency_code: Optional[str] = Field(default=None, description="Currency code")
    currency_symbol: Optional[str] = Field(default=None, description="Currency symbol", alias="currencySymbol")
    currency_decimal_places: Optional[int] = Field(default=None, description="Currency decimal places", alias="currencyDecimalPlaces")
    
    # Native currency fields
    native_currency_id: Optional[str] = Field(default=None, description="Native currency ID", alias="nativeCurrencyId")
    native_currency_code: Optional[str] = Field(default=None, description="Native currency code", alias="nativeCurrencyCode")
    native_currency_symbol: Optional[str] = Field(default=None, description="Native currency symbol", alias="nativeCurrencySymbol")
    native_currency_decimal_places: Optional[int] = Field(default=None, description="Native currency decimal places", alias="nativeCurrencyDecimalPlaces")
    
    # Balance fields (read-only)
    current_balance: Optional[str] = Field(default=None, description="Current balance", alias="currentBalance")
    current_balance_date: Optional[datetime] = Field(default=None, description="Current balance date", alias="currentBalanceDate")
    
    # Native balance fields (read-only) 
    native_current_balance: Optional[str] = Field(default=None, description="Current balance in native currency", alias="nativeCurrentBalance")
    native_current_balance_date: Optional[datetime] = Field(default=None, description="Current balance date in native currency", alias="nativeCurrentBalanceDate")
    
    # Configuration fields
    virtual_balance: Optional[str] = Field(default=None, description="Virtual balance", alias="virtualBalance")
    opening_balance: Optional[str] = Field(default=None, description="Opening balance", alias="openingBalance")
    opening_balance_date: Optional[datetime] = Field(default=None, description="Opening balance date", alias="openingBalanceDate")
    
    # Account details
    notes: Optional[str] = Field(default=None, description="Account notes")
    account_number: Optional[str] = Field(default=None, description="Account number", alias="accountNumber")
    iban: Optional[str] = Field(default=None, description="IBAN")
    bic: Optional[str] = Field(default=None, description="BIC")
    
    # Location data
    latitude: Optional[float] = Field(default=None, description="Latitude")
    longitude: Optional[float] = Field(default=None, description="Longitude")
    zoom_level: Optional[int] = Field(default=None, description="Zoom level", alias="zoomLevel")
    
    # Liability-specific fields
    liability_type: Optional[str] = Field(default=None, description="Liability type", alias="liabilityType")
    liability_amount: Optional[str] = Field(default=None, description="Liability amount", alias="liabilityAmount")
    liability_start_date: Optional[datetime] = Field(default=None, description="Liability start date", alias="liabilityStartDate")
    
    # Interest fields
    interest: Optional[str] = Field(default=None, description="Interest rate")
    interest_period: Optional[str] = Field(default=None, description="Interest period", alias="interestPeriod")
    
    # Credit card specific
    credit_card_type: Optional[str] = Field(default=None, description="Credit card type", alias="creditCardType")
    monthly_payment_date: Optional[datetime] = Field(default=None, description="Monthly payment date", alias="monthlyPaymentDate")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class TransactionSplit(BaseModel):
    """Individual transaction split within a transaction group."""
    model_config = ConfigDict(populate_by_name=True)
    # Required fields
    amount: str = Field(..., description="Transaction amount")
    source_id: Optional[str] = Field(default=None, description="Source account ID", alias="sourceId")
    destination_id: Optional[str] = Field(default=None, description="Destination account ID", alias="destinationId")
    date: datetime = Field(..., description="Transaction date")
    description: str = Field(..., description="Transaction description")
    type: TransactionTypeProperty = Field(..., description="Transaction type")
    
    # Alternative to IDs - names
    source_name: Optional[str] = Field(default=None, description="Source account name", alias="sourceName")
    destination_name: Optional[str] = Field(default=None, description="Destination account name", alias="destinationName")
    
    # Currency fields
    currency_id: Optional[str] = Field(default=None, description="Currency ID", alias="currencyId")
    currency_code: Optional[str] = Field(default=None, description="Currency code", alias="currencyCode")
    currency_symbol: Optional[str] = Field(default=None, description="Currency symbol", alias="currencySymbol")
    currency_name: Optional[str] = Field(default=None, description="Currency name", alias="currencyName")
    currency_decimal_places: Optional[int] = Field(default=None, description="Currency decimal places", alias="currencyDecimalPlaces")
    
    # Native currency fields
    native_currency_id: Optional[str] = Field(default=None, description="Native currency ID", alias="nativeCurrencyId")
    native_currency_code: Optional[str] = Field(default=None, description="Native currency code", alias="nativeCurrencyCode")
    native_currency_symbol: Optional[str] = Field(default=None, description="Native currency symbol", alias="nativeCurrencySymbol")
    native_currency_name: Optional[str] = Field(default=None, description="Native currency name", alias="nativeCurrencyName")
    native_currency_decimal_places: Optional[int] = Field(default=None, description="Native currency decimal places", alias="nativeCurrencyDecimalPlaces")
    native_amount: Optional[str] = Field(default=None, description="Amount in native currency", alias="nativeAmount")
    
    # Foreign currency fields
    foreign_currency_id: Optional[str] = Field(default=None, description="Foreign currency ID", alias="foreignCurrencyId")
    foreign_currency_code: Optional[str] = Field(default=None, description="Foreign currency code", alias="foreignCurrencyCode")
    foreign_currency_symbol: Optional[str] = Field(default=None, description="Foreign currency symbol", alias="foreignCurrencySymbol")
    foreign_currency_decimal_places: Optional[int] = Field(default=None, description="Foreign currency decimal places", alias="foreignCurrencyDecimalPlaces")
    foreign_amount: Optional[str] = Field(default=None, description="Foreign amount", alias="foreignAmount")
    
    # Related resources (can use ID or name)
    budget_id: Optional[str] = Field(default=None, description="Budget ID", alias="budgetId")
    budget_name: Optional[str] = Field(default=None, description="Budget name", alias="budgetName")
    category_id: Optional[str] = Field(default=None, description="Category ID", alias="categoryId") 
    category_name: Optional[str] = Field(default=None, description="Category name", alias="categoryName")
    bill_id: Optional[str] = Field(default=None, description="Bill ID", alias="billId")
    bill_name: Optional[str] = Field(default=None, description="Bill name", alias="billName")
    
    # Tags and metadata
    tags: Optional[List[str]] = Field(default_factory=list, description="Transaction tags")
    notes: Optional[str] = Field(default=None, description="Transaction notes")
    
    # Transaction state
    reconciled: bool = Field(default=False, description="Whether transaction is reconciled")
    
    # External references
    internal_reference: Optional[str] = Field(default=None, description="Internal reference", alias="internalReference")
    external_id: Optional[str] = Field(default=None, description="External ID", alias="externalId")
    external_url: Optional[str] = Field(default=None, description="External URL", alias="externalUrl")
    
    # Location data
    latitude: Optional[float] = Field(default=None, description="Latitude")
    longitude: Optional[float] = Field(default=None, description="Longitude")
    zoom_level: Optional[int] = Field(default=None, description="Zoom level", alias="zoomLevel")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class Transaction(BaseModel):
    """Firefly III Transaction wrapper model."""
    model_config = ConfigDict(populate_by_name=True)
    # Core field
    transactions: List[TransactionSplit] = Field(..., description="List of transaction splits")
    
    # Optional transaction group fields
    group_title: Optional[str] = Field(default=None, description="Group title for split transactions", alias="groupTitle")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class Category(BaseModel):
    """Firefly III Category model."""
    # Required fields
    name: str = Field(..., description="Category name")
    
    # Optional fields
    notes: Optional[str] = Field(default=None, description="Category notes")
    
    # Currency information (read-only)
    spent: Optional[List[Dict[str, Any]]] = Field(default=None, description="Spending data by currency")
    earned: Optional[List[Dict[str, Any]]] = Field(default=None, description="Earning data by currency")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class TagModel(BaseModel):
    """Firefly III Tag model (named TagModel to avoid conflict with 'tag' field)."""
    # Required fields
    tag: str = Field(..., description="Tag name")
    
    # Optional fields
    date: Optional[datetime] = Field(default=None, description="Date the tag applies to")
    description: Optional[str] = Field(default=None, description="Tag description")
    
    # Location data
    latitude: Optional[float] = Field(default=None, description="Latitude")
    longitude: Optional[float] = Field(default=None, description="Longitude")
    zoom_level: Optional[int] = Field(default=None, description="Zoom level", alias="zoomLevel")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class Budget(BaseModel):
    """Firefly III Budget model."""
    # Required fields
    name: str = Field(..., description="Budget name")
    
    # Optional fields
    active: bool = Field(default=True, description="Whether the budget is active")
    notes: Optional[str] = Field(default=None, description="Budget notes")
    order: Optional[int] = Field(default=None, description="Display order")
    
    # Auto-budget configuration
    auto_budget_type: Optional[AutoBudgetType] = Field(default=None, description="Auto budget type", alias="autoBudgetType")
    auto_budget_currency_id: Optional[str] = Field(default=None, description="Auto budget currency ID", alias="autoBudgetCurrencyId")
    auto_budget_currency_code: Optional[str] = Field(default=None, description="Auto budget currency code", alias="autoBudgetCurrencyCode")
    auto_budget_amount: Optional[str] = Field(default=None, description="Auto budget amount", alias="autoBudgetAmount")
    auto_budget_period: Optional[AutoBudgetPeriod] = Field(default=None, description="Auto budget period", alias="autoBudgetPeriod")
    
    # Spending data (read-only)
    spent: Optional[List[Dict[str, Any]]] = Field(default=None, description="Spending data by currency")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


class Currency(BaseModel):
    """Firefly III Currency model."""
    # Required fields
    code: str = Field(..., description="Currency code")
    name: str = Field(..., description="Currency name")
    symbol: str = Field(..., description="Currency symbol")
    
    # Optional fields
    enabled: bool = Field(default=True, description="Whether the currency is enabled")
    default: bool = Field(default=False, description="Whether this is the default currency")
    native: bool = Field(default=False, description="Whether this is the native currency")
    decimal_places: int = Field(default=2, description="Number of decimal places", alias="decimalPlaces")
    
    # Timestamps (read-only)
    created_at: Optional[datetime] = Field(default=None, description="Creation timestamp", alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp", alias="updatedAt")


# Typed response models for each resource
class AccountRead(BaseRead):
    """Account resource read model."""
    type: str = Field(default="accounts", description="Resource type")
    attributes: Account


class TransactionRead(BaseRead):
    """Transaction resource read model."""
    type: str = Field(default="transactions", description="Resource type")
    attributes: Transaction


class CategoryRead(BaseRead):
    """Category resource read model."""
    type: str = Field(default="categories", description="Resource type")
    attributes: Category


class TagRead(BaseRead):
    """Tag resource read model."""
    type: str = Field(default="tags", description="Resource type")
    attributes: TagModel


class BudgetRead(BaseRead):
    """Budget resource read model."""
    type: str = Field(default="budgets", description="Resource type")
    attributes: Budget


class CurrencyRead(BaseRead):
    """Currency resource read model."""
    type: str = Field(default="currencies", description="Resource type")
    attributes: Currency


# Array response models
class AccountArrayResponse(BaseArrayResponse):
    """Multiple accounts response."""
    data: List[AccountRead]


class TransactionArrayResponse(BaseArrayResponse):
    """Multiple transactions response."""
    data: List[TransactionRead]


class CategoryArrayResponse(BaseArrayResponse):
    """Multiple categories response."""
    data: List[CategoryRead]


class TagArrayResponse(BaseArrayResponse):
    """Multiple tags response."""
    data: List[TagRead]


class BudgetArrayResponse(BaseArrayResponse):
    """Multiple budgets response."""
    data: List[BudgetRead]


class CurrencyArrayResponse(BaseArrayResponse):
    """Multiple currencies response."""
    data: List[CurrencyRead]


# Single response models
class AccountSingleResponse(BaseSingleResponse):
    """Single account response."""
    data: AccountRead


class TransactionSingleResponse(BaseSingleResponse):
    """Single transaction response."""
    data: TransactionRead


class CategorySingleResponse(BaseSingleResponse):
    """Single category response."""
    data: CategoryRead


class TagSingleResponse(BaseSingleResponse):
    """Single tag response."""
    data: TagRead


class BudgetSingleResponse(BaseSingleResponse):
    """Single budget response."""
    data: BudgetRead


class CurrencySingleResponse(BaseSingleResponse):
    """Single currency response."""
    data: CurrencyRead
