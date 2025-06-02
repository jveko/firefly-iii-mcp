# Firefly III MCP Server Implementation Plan

## Overview

This plan provides a step-by-step approach to building a Model Context Protocol (MCP) server for Firefly III. The implementation is broken down into small, iterative chunks that build on each other, ensuring no big jumps in complexity.

## Implementation Phases

### Phase 1: Foundation (Steps 1-5)
Establish the project structure, basic server setup, and connectivity.

### Phase 2: Core Resources (Steps 6-10)
Implement primary resources with full CRUD operations.

### Phase 3: Extended Resources (Steps 11-15)
Add remaining resource types and advanced features.

### Phase 4: Enhancement & Polish (Steps 16-20)
Add caching, batch operations, shortcuts, and finalize for distribution.

---

## Detailed Implementation Steps

### Step 1: Project Setup and Structure

```text
Create the initial project structure with FastMCP and basic dependencies. Set up the package structure following Python best practices with proper module organization. Configure uv for package management, ruff for linting, and pyright for type checking. Create the basic package files including __init__.py and __main__.py.
```

### Step 2: Basic MCP Server with Health Check

```text
Implement a minimal FastMCP server that starts and responds to health checks. Create the server.py file with a basic FastMCP application. Add a simple health check tool that returns "OK" to verify the server is running. Configure logging and basic error handling. Make the server runnable via python -m firefly_iii_mcp.
```

### Step 3: Firefly III Client Foundation

```text
Create an httpx-based client for communicating with the Firefly III API. Implement the client.py module with a FireflyClient class that handles authentication via environment variables (FIREFLY_URL and FIREFLY_TOKEN). Add proper error handling for connection issues and authentication failures. Include request/response logging for debugging. Test the client with a simple API call.
```

### Step 4: Connection Management Tools

```text
Add MCP tools for connection management and testing. Implement check_connection tool that verifies API connectivity and authentication. Add get_server_info tool that retrieves Firefly III version and capabilities. Create configure_auth tool to help diagnose configuration issues. Ensure proper error messages guide users to fix common setup problems.
```

### Step 5: Data Models and Type Definitions

```text
Create Pydantic models for Firefly III data structures. Start with core models like Account, Transaction, Category, and Tag. Define proper type hints and validation rules. Create response wrapper models for API responses. Ensure models handle optional fields and API variations properly.
```

### Step 6: Accounts Resource Implementation

```text
Implement the accounts MCP tool with full CRUD operations. Create a tool that accepts action parameter (get, list, create, update, delete) and routes to appropriate methods. Implement pagination for list operations. Add proper parameter validation and error handling. Test all operations against the Firefly III API.
```

### Step 7: Transactions Resource Implementation

```text
Implement the transactions MCP tool, the most complex resource in Firefly III. Handle the complex transaction structure with splits, metadata, and related data. Implement proper date handling and amount formatting. Add support for all transaction types (withdrawal, deposit, transfer). Ensure proper validation of required fields.
```

### Step 8: Categories Resource Implementation

```text
Add the categories MCP tool with full functionality. Implement category hierarchy support (parent/child relationships). Add proper handling for income vs expense categories. Include category rules and automation features. Test category assignment to transactions.
```

### Step 9: Budgets Resource Implementation

```text
Implement the budgets MCP tool with budget management features. Add support for budget limits and auto-budgets. Implement budget period handling (daily, weekly, monthly, etc.). Include available amount calculations. Add budget vs actual comparison functionality.
```

### Step 10: Tags Resource Implementation

```text
Create the tags MCP tool for transaction tagging. Implement tag creation, update, and deletion. Add tag assignment to transactions. Include tag-based filtering and search. Test bulk tag operations.
```

### Step 11: Bills and Recurring Transactions

```text
Implement bills and recurring transaction management. Add the bills MCP tool with full CRUD operations. Include bill matching and automatic transaction creation. Add support for recurring transaction rules. Test bill payment tracking and predictions.
```

### Step 12: Additional Resources Bundle 1

```text
Implement a bundle of simpler resources including: currencies (with exchange rates), attachments (file upload/download), webhooks (event subscriptions), and preferences (user settings). Each should have its own MCP tool with appropriate actions. Focus on completeness over complexity.
```

### Step 13: Additional Resources Bundle 2

```text
Add remaining resource tools including: piggy banks (savings goals), rules and rule groups (automation), links (transaction relationships), and object groups. Ensure each tool follows the established pattern with action-based routing.
```

### Step 14: Search and Filtering Enhancement

```text
Implement advanced search functionality across resources. Create a unified search tool that queries multiple resource types. Add date range filtering, amount filtering, and text search. Include proper result formatting and grouping. Test complex search scenarios.
```

### Step 15: Reports and Analytics Tools

```text
Add reporting and analytics capabilities. Implement tools for balance reports, income/expense summaries, and category breakdowns. Add support for custom date ranges and grouping options. Include chart data generation for visualization. Test with various account configurations.
```

### Step 16: Caching Implementation

```text
Add intelligent caching to improve performance. Implement cache.py with TTL-based caching for reference data (accounts, categories, tags). Add cache invalidation on mutations. Make cache configurable via environment variables. Test cache behavior under various scenarios.
```

### Step 17: Batch Operations

```text
Implement batch operations for efficiency. Add batch transaction creation/update capabilities. Implement batch category and tag assignment. Include proper error handling for partial failures. Return detailed results for each operation in the batch.
```

### Step 18: Convenience Shortcuts

```text
Create shortcut tools for common operations. Implement transfer_between_accounts for simple transfers. Add quick_expense for rapid expense entry. Create account_balance for current balance queries. Add monthly_summary for quick financial overviews. Include budget_status for budget checking.
```

### Step 19: Error Handling and Validation

```text
Enhance error handling throughout the application. Implement comprehensive input validation for all tools. Add proper error transformation from Firefly III to MCP format. Include helpful error messages with suggested fixes. Test error scenarios extensively.
```

### Step 20: Distribution Preparation

```text
Prepare the package for PyPI distribution. Update pyproject.toml with proper metadata and dependencies. Create comprehensive README with quickstart guide. Add CLI entry point for easy server startup. Include example configurations and usage patterns. Test installation in a clean environment.
```

---

## Code Generation Prompts

Below are the specific prompts for implementing each step. Each prompt builds on the previous ones and integrates the new functionality into the existing codebase.

### Prompt 1: Project Setup and Structure

```text
Create the initial project structure for firefly-iii-mcp using uv as the package manager. Set up the following structure:

firefly_iii_mcp/
├── __init__.py
├── __main__.py
├── server.py
├── client.py
├── tools.py
├── models.py
├── cache.py
├── utils.py
└── shortcuts.py

Configure pyproject.toml with:
- Python >= 3.11
- Dependencies: fastmcp, httpx, pydantic
- Dev dependencies: ruff, pyright, pytest
- Package metadata for PyPI distribution
- Entry point: firefly-iii-mcp

Create __init__.py with proper version export and __main__.py that imports and runs the server. Add ABOUTME comments to each file explaining its purpose.
```

### Prompt 2: Basic MCP Server with Health Check

```text
Implement a basic FastMCP server in server.py that:
1. Creates a FastMCP instance named "firefly-iii-mcp"
2. Adds a health_check tool that returns {"status": "ok", "service": "firefly-iii-mcp"}
3. Configures basic logging with INFO level
4. Handles startup and shutdown events
5. Can be run via python -m firefly_iii_mcp

The health_check tool should have proper documentation and no parameters. Make sure the server starts on the default MCP port and is ready to accept connections.
```

### Prompt 3: Firefly III Client Foundation

```text
Create a Firefly III API client in client.py that:
1. Uses httpx for async HTTP requests
2. Reads FIREFLY_URL and FIREFLY_TOKEN from environment variables
3. Implements a FireflyClient class with:
   - Configurable base URL and auth token
   - Automatic auth header injection
   - Request/response logging
   - Error handling for common HTTP errors
   - Methods: get(), post(), put(), patch(), delete()
4. Raises custom exceptions for auth errors, connection errors, and API errors

Test the client by adding a simple test_connection method that calls the /api/v1/about endpoint.
```

### Prompt 4: Connection Management Tools

```text
Add connection management tools to tools.py:

1. check_connection tool:
   - Tests API connectivity and authentication
   - Returns connection status, API version, and user info
   - Provides helpful error messages for common issues

2. get_server_info tool:
   - Retrieves Firefly III version, API version, and capabilities
   - Returns structured information about the server

3. configure_auth tool:
   - Checks environment variables
   - Validates URL format
   - Tests token authentication
   - Returns diagnostic information

Wire these tools into the MCP server in server.py. Each tool should handle errors gracefully and provide actionable feedback.
```

### Prompt 5: Data Models and Type Definitions

```text
Create Pydantic models in models.py for core Firefly III resources:

1. Base models:
   - FireflyModel (base with id, created_at, updated_at)
   - ListResponse (generic pagination wrapper)
   - ErrorResponse (API error structure)

2. Core resource models:
   - Account (with type, currency, balance, etc.)
   - Transaction (complex with splits, currency, metadata)
   - Category (with hierarchy support)
   - Tag (simple with name and rules)
   - Budget (with limits and periods)

3. Enums for:
   - AccountType (asset, expense, revenue, etc.)
   - TransactionType (withdrawal, deposit, transfer)
   - BudgetPeriod (daily, weekly, monthly, etc.)

Ensure all models have proper field validation and handle optional fields correctly.
```

### Prompt 6: Accounts Resource Implementation

```text
Implement the accounts tool in tools.py with action-based routing:

@mcp.tool()
async def accounts(
    action: str,  # "get", "list", "create", "update", "delete"
    id: Optional[str] = None,
    name: Optional[str] = None,
    type: Optional[str] = None,
    currency_code: Optional[str] = None,
    opening_balance: Optional[float] = None,
    account_number: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    **kwargs
):
    """Manage accounts in Firefly III"""

Implement all actions:
- get: Retrieve single account by ID
- list: List accounts with pagination
- create: Create new account with validation
- update: Update existing account
- delete: Delete account (with safety check)

Add this tool to the server and test all operations. Include proper error handling and parameter validation.
```

### Prompt 7: Transactions Resource Implementation

```text
Implement the transactions tool handling Firefly III's complex transaction model:

@mcp.tool()
async def transactions(
    action: str,
    id: Optional[str] = None,
    type: Optional[str] = None,
    description: Optional[str] = None,
    amount: Optional[float] = None,
    source_id: Optional[str] = None,
    destination_id: Optional[str] = None,
    category_id: Optional[str] = None,
    date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    page: int = 1,
    limit: int = 50,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    **kwargs
):
    """Manage transactions in Firefly III"""

Handle:
- Transaction splits (multiple sources/destinations)
- Proper date formatting (ISO 8601)
- Amount handling with currency
- Tag and category assignment
- Filtering by date range for list action

Ensure transfers are handled correctly with both source and destination accounts.
```

### Prompt 8: Categories Resource Implementation

```text
Add the categories tool with hierarchy support:

@mcp.tool()
async def categories(
    action: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    parent_id: Optional[str] = None,
    notes: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    **kwargs
):
    """Manage categories in Firefly III"""

Implement:
- Category creation with parent/child relationships
- Listing with hierarchy information
- Update category properties and parent
- Delete with child category handling
- Category statistics (transaction count, total spent)

Add validation to prevent circular hierarchies and ensure income/expense category separation.
```

### Prompt 9: Budgets Resource Implementation

```text
Implement the budgets tool with period management:

@mcp.tool()
async def budgets(
    action: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    amount: Optional[float] = None,
    period: Optional[str] = None,  # daily, weekly, monthly, etc.
    auto_budget_type: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    **kwargs
):
    """Manage budgets in Firefly III"""

Include:
- Budget creation with limits
- Budget period configuration
- Auto-budget settings
- Available amount calculations
- Budget vs actual comparisons
- Budget limit history

Add a special "status" action that shows budget performance for the current period.
```

### Prompt 10: Tags Resource Implementation

```text
Add the tags tool for transaction organization:

@mcp.tool()
async def tags(
    action: str,
    id: Optional[str] = None,
    tag: Optional[str] = None,
    description: Optional[str] = None,
    date: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    **kwargs
):
    """Manage tags in Firefly III"""

Implement:
- Tag CRUD operations
- Tag rules for automatic assignment
- Bulk tag operations on transactions
- Tag-based transaction filtering
- Tag usage statistics

Include validation for tag uniqueness and handle tag merging scenarios.
```

### Prompt 11: Bills and Recurring Transactions

```text
Implement bills and recurring transaction tools:

@mcp.tool()
async def bills(
    action: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    date: Optional[str] = None,
    repeat_freq: Optional[str] = None,
    skip: Optional[int] = None,
    active: Optional[bool] = None,
    **kwargs
):
    """Manage bills and recurring transactions"""

Add:
- Bill creation with amount ranges
- Recurring frequency configuration
- Bill matching rules
- Next occurrence calculations
- Payment tracking
- Bill activation/deactivation

Include a "check" action to find transactions that might match bills.
```

### Prompt 12: Additional Resources Bundle 1

```text
Implement tools for currencies, attachments, webhooks, and preferences:

1. currencies tool:
   - List available currencies
   - Get exchange rates
   - Set default currency

2. attachments tool:
   - Upload attachments to transactions
   - List attachments
   - Download attachment data
   - Delete attachments

3. webhooks tool:
   - Create webhook subscriptions
   - List active webhooks
   - Test webhook delivery
   - Delete webhooks

4. preferences tool:
   - Get user preferences
   - Update preferences
   - Reset to defaults

Each tool should follow the action-based pattern. Handle file uploads for attachments using base64 encoding.
```

### Prompt 13: Additional Resources Bundle 2

```text
Add remaining resource tools:

1. piggy_banks tool:
   - Create savings goals
   - Add/remove money
   - Track progress
   - Link to accounts

2. rules tool:
   - Create automation rules
   - Test rules against transactions
   - Enable/disable rules
   - Manage rule groups

3. links tool:
   - Create transaction relationships
   - List linked transactions
   - Update link types
   - Remove links

4. object_groups tool:
   - Group related objects
   - Manage group membership
   - Set group properties

Ensure each tool integrates properly with existing resources and maintains data consistency.
```

### Prompt 14: Search and Filtering Enhancement

```text
Create an advanced search tool that queries across multiple resources:

@mcp.tool()
async def search(
    query: Optional[str] = None,
    resources: Optional[List[str]] = None,  # ["transactions", "accounts", "categories"]
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    tags: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    accounts: Optional[List[str]] = None,
    limit: int = 50,
    **kwargs
):
    """Search across Firefly III resources"""

Implement:
- Full-text search across descriptions and notes
- Multi-resource results with proper typing
- Advanced filtering combinations
- Result ranking by relevance
- Faceted search results

Return results grouped by resource type with counts.
```

### Prompt 15: Reports and Analytics Tools

```text
Add reporting tools for financial analysis:

1. balance_report tool:
   - Account balances over time
   - Net worth calculations
   - Balance trends

2. income_expense_report tool:
   - Income vs expense by period
   - Category breakdowns
   - Top expenses/income sources

3. category_report tool:
   - Spending by category
   - Category trends
   - Budget vs actual by category

4. cash_flow_report tool:
   - Cash flow analysis
   - Future projections
   - Bill payment schedule

Each report should support custom date ranges, grouping options, and return data suitable for charting.
```

### Prompt 16: Caching Implementation

```text
Implement caching in cache.py to improve performance:

1. Create a CacheManager class with:
   - TTL-based expiration
   - Memory-based storage
   - Key generation from requests
   - Cache statistics

2. Add caching to:
   - Account lists (5 min TTL)
   - Categories (5 min TTL)
   - Tags (5 min TTL)
   - Currencies (1 hour TTL)
   - Server info (1 hour TTL)

3. Implement cache invalidation:
   - Clear related caches on mutations
   - Selective invalidation by resource
   - Manual cache clearing tool

4. Make cache configurable via environment:
   - FIREFLY_CACHE_TTL (default: 300)
   - FIREFLY_CACHE_ENABLED (default: true)

Wire caching into the client transparently.
```

### Prompt 17: Batch Operations

```text
Add batch operation support for efficiency:

@mcp.tool()
async def batch_operations(
    operations: List[Dict[str, Any]],
    continue_on_error: bool = False,
    **kwargs
):
    """Execute multiple operations in a single call"""

Support batch operations for:
1. Transaction creation/updates
2. Category assignments
3. Tag operations
4. Account updates

Each operation in the batch should specify:
- resource: The resource type
- action: The operation to perform
- params: Parameters for the operation

Return results with:
- Success/failure status per operation
- Error details for failures
- Summary statistics

Implement proper transaction handling and rollback capabilities.
```

### Prompt 18: Convenience Shortcuts

```text
Create shortcut tools in shortcuts.py for common operations:

1. transfer_between_accounts:
   - Simplified internal transfers
   - Auto-creates transaction with proper type
   - Handles currency conversion

2. quick_expense:
   - Create expense with minimal params
   - Auto-select default expense account
   - Optional category quick-select

3. account_balance:
   - Get current balance for account
   - Include pending transactions
   - Currency conversion option

4. monthly_summary:
   - Income/expense for a month
   - Top categories
   - Account balance changes

5. budget_status:
   - Current period budget vs actual
   - Remaining budget amounts
   - Overspending alerts

Each shortcut should significantly simplify common workflows while maintaining data integrity.
```

### Prompt 19: Error Handling and Validation

```text
Enhance error handling throughout the application:

1. Create custom exceptions in utils.py:
   - FireflyAuthError
   - FireflyValidationError
   - FireflyNotFoundError
   - FireflyServerError
   - FireflyRateLimitError

2. Add comprehensive validation:
   - Parameter type checking
   - Required field validation
   - Business rule validation
   - Format validation (dates, amounts)

3. Implement error transformation:
   - Map Firefly errors to MCP errors
   - Include helpful error messages
   - Add suggested fixes
   - Include request context

4. Add error recovery:
   - Automatic retry for transient errors
   - Rate limit backoff
   - Connection pooling

Update all tools to use the enhanced error handling consistently.
```

### Prompt 20: Distribution Preparation

```text
Prepare the package for PyPI distribution:

1. Update pyproject.toml:
   - Complete metadata (author, description, keywords)
   - Classifiers for PyPI
   - Entry points for CLI
   - Version management
   - Dependency specifications

2. Create comprehensive README.md:
   - Installation instructions
   - Quick start guide
   - Environment setup
   - Basic usage examples
   - Link to full documentation

3. Add CLI entry point:
   - firefly-iii-mcp command
   - --version flag
   - --config flag for alt config
   - Proper signal handling

4. Create example configurations:
   - .env.example file
   - Docker compose example
   - Systemd service file

5. Add GitHub Actions workflow:
   - Test on multiple Python versions
   - Lint and type check
   - Build and publish to PyPI

Test the complete installation process in a fresh environment.
```

---

## Integration Points

Each step builds on the previous ones:

1. Steps 1-5 establish the foundation that all other steps depend on
2. Steps 6-10 implement core resources that are referenced by later features
3. Steps 11-15 add remaining resources and advanced features
4. Steps 16-20 enhance performance and prepare for production use

The code is always integrated and functional after each step, with no orphaned code or incomplete features.

## Testing Strategy

After each implementation step:
1. Unit test new functionality
2. Integration test with existing features
3. Manual test via MCP client
4. Verify no regressions in previous functionality

## Success Metrics

- All 155 Firefly III endpoints accessible
- Sub-second response for cached operations
- Clear error messages for common issues
- 90%+ test coverage
- Successful PyPI publication
- Working installation via pip/uv