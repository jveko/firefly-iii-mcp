# Firefly III MCP Server Specification

## Overview

This document specifies the design and implementation requirements for a Model Context Protocol (MCP) server that provides comprehensive access to Firefly III's personal finance management API. The server will expose all functionality from the Firefly III OpenAPI specification through MCP tools.

## Core Requirements

### Scope
- **Full API Coverage**: Implement all ~155 endpoints from the Firefly III OpenAPI specification v6.2.13
- **Complete Operations**: Support all 219 HTTP operations (GET, POST, PUT, PATCH, DELETE)
- **All Resources**: Cover all 28 resource types including accounts, transactions, budgets, categories, bills, etc.

### Architecture

#### Package Structure
```
firefly_iii_mcp/
├── __init__.py
├── __main__.py
├── server.py          # FastMCP server implementation
├── client.py          # Firefly III API client using httpx
├── tools.py           # MCP tool definitions
├── models.py          # Data models and types
├── cache.py           # Caching implementation
├── utils.py           # Helper functions
└── shortcuts.py       # Convenience operations
```

#### Tool Organization
- **Grouped by Resource**: One MCP tool per resource type with actions as parameters
- **Tool Naming**: Match resource names from API (e.g., `accounts`, `transactions`, `budgets`)
- **Action Parameter**: Each tool accepts an `action` parameter (get, list, create, update, delete)

Example tool signature:
```python
@mcp.tool()
async def transactions(
    action: str,  # "get", "list", "create", "update", "delete"
    **params      # Additional parameters matching Firefly III API fields
):
    """Manage transactions in Firefly III"""
```

### Authentication

#### Primary Method: Environment Variables
- `FIREFLY_URL`: Base URL of Firefly III instance (e.g., https://demo.firefly-iii.org)
- `FIREFLY_TOKEN`: Personal Access Token for authentication

#### Setup Tools
Include MCP tools for connection management:
- `check_connection`: Test authentication and connectivity
- `configure_auth`: Help diagnose configuration issues
- `get_server_info`: Retrieve Firefly III version and capabilities

### Data Handling

#### Request Format
- **Field Names**: Use exact field names from Firefly III API
- **No Transformation**: Pass parameters directly to API

#### Response Format
- **Follow API Defaults**: Return data as provided by Firefly III
- **No Flattening**: Maintain original JSON structure
- **Preserve Types**: Keep data types from API responses

#### Error Handling
- **Transform Errors**: Convert Firefly III errors to standardized MCP error format
- **Error Types**:
  - Validation errors → MCP validation error
  - Not found (404) → MCP not found error
  - Auth errors (401) → MCP auth error
  - Server errors (500) → MCP server error
- **No Detailed Messages**: Keep error responses concise

#### Pagination
- **Automatic Handling**: Implement automatic pagination for list operations
- **Configurable**: Accept `page` and `limit` parameters (default: 50 items)
- **Full Retrieval**: Option to fetch all pages automatically with `all_pages=true`

### Enhanced Features

#### 1. Caching
- **Cache Frequently Used Data**: 
  - Account lists
  - Categories
  - Tags
  - Currencies
- **TTL Configuration**: Configurable cache time-to-live (default: 5 minutes)
- **Cache Invalidation**: Clear cache on create/update/delete operations

#### 2. Batch Operations
- **Batch Transactions**: Create/update multiple transactions in one call
- **Batch Categories**: Assign categories to multiple transactions
- **Error Handling**: Return partial success with detailed error report

#### 3. Enhanced Search
- **Cross-Resource Search**: Search across transactions, accounts, categories
- **Advanced Filters**: Date ranges, amounts, descriptions
- **Unified Results**: Return results grouped by resource type

#### 4. Shortcuts/Macros
Common operations exposed as dedicated tools:
- `transfer_between_accounts`: Simplified internal transfers
- `quick_expense`: Create expense with minimal parameters
- `account_balance`: Get current balance for an account
- `monthly_summary`: Get income/expense summary for a month
- `budget_status`: Check budget vs actual for current period

### Development Stack

#### Core Dependencies
- **FastMCP**: MCP server framework
- **httpx**: Modern async HTTP client
- **pydantic**: Data validation and settings

#### Development Tools
- **Package Manager**: uv
- **Linting/Formatting**: ruff
- **Type Checking**: pyright
- **Testing**: pytest
- **Build System**: As defined in pyproject.toml

### Distribution

#### PyPI Package
- **Package Name**: `firefly-iii-mcp`
- **Import Name**: `firefly_iii_mcp`
- **CLI Command**: `firefly-iii-mcp`

#### Installation
```bash
pip install firefly-iii-mcp
# or with uv
uv add firefly-iii-mcp
```

#### Usage
```bash
# Set environment variables
export FIREFLY_URL="https://your-firefly-instance.com"
export FIREFLY_TOKEN="your-personal-access-token"

# Run the MCP server
firefly-iii-mcp

# Or use with an MCP client
# The server will be available for MCP client connections
```

### Implementation Priorities

1. **Phase 1 - Core Functionality**
   - Authentication with environment variables
   - Basic CRUD tools for key resources (accounts, transactions, categories)
   - Error transformation
   - Connection testing tools

2. **Phase 2 - All Resources**
   - Implement remaining resource tools
   - Automatic pagination
   - Response caching for reference data

3. **Phase 3 - Enhanced Features**
   - Batch operations
   - Cross-resource search
   - Convenience shortcuts
   - Performance optimizations

### Testing Requirements

- Unit tests for all tools
- Integration tests with mock Firefly III responses
- Test error handling scenarios
- Test pagination edge cases
- Cache behavior tests
- Batch operation tests

### Documentation Requirements

- README with quick start guide
- Tool reference documentation
- Environment variable configuration guide
- Example usage patterns
- Troubleshooting guide

### Security Considerations

- Never log or expose authentication tokens
- Validate all inputs before sending to API
- Use HTTPS only for API connections
- Implement rate limiting awareness
- Clear cache on authentication changes

### Performance Goals

- Sub-second response for cached data
- Efficient batch processing (minimize API calls)
- Lazy loading for large datasets
- Connection pooling for API requests
- Minimal memory footprint

## Success Criteria

The MCP server will be considered complete when:

1. All Firefly III API endpoints are accessible via MCP tools
2. Authentication works reliably with environment variables
3. Error handling provides clear, actionable feedback
4. Caching improves performance for common operations
5. Batch operations reduce API call overhead
6. Search provides unified access to financial data
7. Shortcuts simplify common workflows
8. Package is published to PyPI and installable
9. Documentation covers all features and usage patterns
10. Tests provide >90% code coverage