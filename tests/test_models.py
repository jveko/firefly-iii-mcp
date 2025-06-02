# ABOUTME: This file contains basic validation tests for all Firefly III data models.
# ABOUTME: It ensures that models can be instantiated correctly and validate input data.

"""Tests for Firefly III data models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from firefly_iii_mcp.models import (
    Account, Transaction, TransactionSplit, Category, TagModel, Budget, Currency,
    ShortAccountTypeProperty, TransactionTypeProperty, AccountRoleProperty,
    AutoBudgetType, AutoBudgetPeriod,
    AccountRead, AccountSingleResponse, AccountArrayResponse
)


class TestEnums:
    """Test enum values are valid."""
    
    def test_account_type_enum(self):
        """Test account type enum values."""
        assert ShortAccountTypeProperty.ASSET == "asset"
        assert ShortAccountTypeProperty.EXPENSE == "expense"
        assert ShortAccountTypeProperty.LIABILITY == "liability"
    
    def test_transaction_type_enum(self):
        """Test transaction type enum values."""
        assert TransactionTypeProperty.WITHDRAWAL == "withdrawal"
        assert TransactionTypeProperty.DEPOSIT == "deposit"
        assert TransactionTypeProperty.TRANSFER == "transfer"
    
    def test_account_role_enum(self):
        """Test account role enum values."""
        assert AccountRoleProperty.DEFAULT_ASSET == "defaultAsset"
        assert AccountRoleProperty.SAVING_ASSET == "savingAsset"


class TestAccount:
    """Test Account model validation."""
    
    def test_minimal_account_creation(self):
        """Test creating account with minimal required fields."""
        account = Account(
            name="Test Account",
            type=ShortAccountTypeProperty.ASSET
        )
        assert account.name == "Test Account"
        assert account.type == ShortAccountTypeProperty.ASSET
        assert account.active is True  # Default value
    
    def test_account_with_all_fields(self):
        """Test creating account with all fields."""
        account = Account(
            name="Full Account",
            type=ShortAccountTypeProperty.ASSET,
            active=True,
            order=1,
            account_role=AccountRoleProperty.DEFAULT_ASSET,
            currency_code="USD",
            current_balance="1000.00",
            notes="Test notes",
            account_number="123456789",
            iban="DE89370400440532013000"
        )
        assert account.name == "Full Account"
        assert account.currency_code == "USD"
        assert account.current_balance == "1000.00"
        assert account.iban == "DE89370400440532013000"
    
    def test_account_missing_required_fields(self):
        """Test validation errors for missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            Account()
        
        errors = exc_info.value.errors()
        field_names = [error['loc'][0] for error in errors]
        assert 'name' in field_names
        assert 'type' in field_names


class TestTransactionSplit:
    """Test TransactionSplit model validation."""
    
    def test_minimal_transaction_split(self):
        """Test creating transaction split with minimal required fields."""
        split = TransactionSplit(
            amount="100.00",
            source_id="1",
            destination_id="2",
            date=datetime.now(),
            description="Test transaction",
            type=TransactionTypeProperty.WITHDRAWAL
        )
        assert split.amount == "100.00"
        assert split.description == "Test transaction"
        assert split.type == TransactionTypeProperty.WITHDRAWAL
    
    def test_transaction_split_with_names(self):
        """Test using account names instead of IDs."""
        split = TransactionSplit(
            amount="50.00",
            source_name="Checking Account",
            destination_name="Grocery Store",
            date=datetime.now(),
            description="Grocery shopping",
            type=TransactionTypeProperty.WITHDRAWAL
        )
        assert split.source_name == "Checking Account"
        assert split.destination_name == "Grocery Store"


class TestTransaction:
    """Test Transaction wrapper model."""
    
    def test_transaction_with_single_split(self):
        """Test transaction with one split."""
        split = TransactionSplit(
            amount="100.00",
            source_id="1",
            destination_id="2",
            date=datetime.now(),
            description="Test transaction",
            type=TransactionTypeProperty.WITHDRAWAL
        )
        transaction = Transaction(transactions=[split])
        assert len(transaction.transactions) == 1
        assert transaction.transactions[0].amount == "100.00"
    
    def test_transaction_with_multiple_splits(self):
        """Test transaction with multiple splits."""
        split1 = TransactionSplit(
            amount="50.00",
            source_id="1",
            destination_id="2",
            date=datetime.now(),
            description="Split 1",
            type=TransactionTypeProperty.WITHDRAWAL
        )
        split2 = TransactionSplit(
            amount="30.00",
            source_id="1",
            destination_id="3",
            date=datetime.now(),
            description="Split 2",
            type=TransactionTypeProperty.WITHDRAWAL
        )
        transaction = Transaction(
            transactions=[split1, split2],
            group_title="Split Transaction"
        )
        assert len(transaction.transactions) == 2
        assert transaction.group_title == "Split Transaction"


class TestSimpleModels:
    """Test simple models: Category, TagModel, Budget, Currency."""
    
    def test_category_creation(self):
        """Test creating category."""
        category = Category(name="Groceries")
        assert category.name == "Groceries"
    
    def test_tag_creation(self):
        """Test creating tag."""
        tag = TagModel(tag="important")
        assert tag.tag == "important"
    
    def test_budget_creation(self):
        """Test creating budget."""
        budget = Budget(name="Monthly Budget")
        assert budget.name == "Monthly Budget"
        assert budget.active is True
    
    def test_currency_creation(self):
        """Test creating currency."""
        currency = Currency(
            code="USD",
            name="US Dollar",
            symbol="$"
        )
        assert currency.code == "USD"
        assert currency.name == "US Dollar"
        assert currency.symbol == "$"
        assert currency.decimal_places == 2  # Default value


class TestResponseModels:
    """Test response wrapper models."""
    
    def test_account_read_model(self):
        """Test AccountRead model."""
        account = Account(name="Test", type=ShortAccountTypeProperty.ASSET)
        account_read = AccountRead(
            type="accounts",
            id="123",
            attributes=account
        )
        assert account_read.type == "accounts"
        assert account_read.id == "123"
        assert account_read.attributes.name == "Test"
    
    def test_account_single_response(self):
        """Test single account response."""
        account = Account(name="Test", type=ShortAccountTypeProperty.ASSET)
        account_read = AccountRead(
            type="accounts",
            id="123",
            attributes=account
        )
        response = AccountSingleResponse(data=account_read)
        assert response.data.attributes.name == "Test"
    
    def test_account_array_response(self):
        """Test array account response."""
        account1 = Account(name="Test1", type=ShortAccountTypeProperty.ASSET)
        account2 = Account(name="Test2", type=ShortAccountTypeProperty.EXPENSE)
        
        read1 = AccountRead(type="accounts", id="1", attributes=account1)
        read2 = AccountRead(type="accounts", id="2", attributes=account2)
        
        response = AccountArrayResponse(data=[read1, read2])
        assert len(response.data) == 2
        assert response.data[0].attributes.name == "Test1"
        assert response.data[1].attributes.name == "Test2"