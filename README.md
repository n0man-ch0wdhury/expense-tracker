# BudgetScope API Usage Guide

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Categories](#categories)
4. [Transactions](#transactions)
5. [Budgets](#budgets)
6. [Summary and Dashboard](#summary-and-dashboard)
7. [Error Handling](#error-handling)

## Authentication

BudgetScope uses JWT (JSON Web Token) for authentication. All API requests (except registration and login) require a valid JWT token.

### Obtaining Tokens

**Endpoint**: `POST /api/token/`

**Request Body**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refreshing Tokens

Access tokens expire after 7 days (as configured in .env). Use the refresh token to get a new access token.

**Endpoint**: `POST /api/token/refresh/`

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using the Token

Include the access token in the Authorization header for all protected API requests:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Users

### Register a New User

**Endpoint**: `POST /api/users/`

**Request Body**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Get Current User Profile

**Endpoint**: `GET /api/users/me/`

**Authentication**: Required

**Response**: `200 OK`
```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

## Categories

Categories are used to organize transactions and budgets. The system includes default categories and allows users to create custom ones.

### List All Categories

**Endpoint**: `GET /api/categories/`

**Authentication**: Required

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Salary",
    "type": "income",
    "is_default": true,
    "user": null
  },
  {
    "id": 2,
    "name": "Groceries",
    "type": "expense",
    "is_default": true,
    "user": null
  },
  {
    "id": 3,
    "name": "Freelance Work",
    "type": "income",
    "is_default": false,
    "user": 1
  }
]
```

### Filter Categories by Type

**Endpoints**: 
- `GET /api/categories/income/`
- `GET /api/categories/expense/`

**Authentication**: Required

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Salary",
    "type": "income",
    "is_default": true,
    "user": null
  },
  {
    "id": 3,
    "name": "Freelance Work",
    "type": "income",
    "is_default": false,
    "user": 1
  }
]
```

### Create a Custom Category

**Endpoint**: `POST /api/categories/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "Side Project",
  "type": "income"
}
```

**Response**: `201 Created`
```json
{
  "id": 4,
  "name": "Side Project",
  "type": "income",
  "is_default": false,
  "user": 1
}
```

### Update a Category

**Endpoint**: `PUT /api/categories/{id}/`

**Authentication**: Required

**Request Body**:
```json
{
  "name": "Updated Category Name",
  "type": "income"
}
```

**Response**: `200 OK`
```json
{
  "id": 4,
  "name": "Updated Category Name",
  "type": "income",
  "is_default": false,
  "user": 1
}
```

### Delete a Category

**Endpoint**: `DELETE /api/categories/{id}/`

**Authentication**: Required

**Response**: `204 No Content`

## Transactions

Transactions represent income and expenses in the system.

### List All Transactions

**Endpoint**: `GET /api/transactions/`

**Authentication**: Required

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "amount": "1500.00",
    "description": "Monthly salary",
    "date": "2023-11-01",
    "type": "income",
    "category": 1,
    "created_at": "2023-11-01T10:00:00Z",
    "updated_at": "2023-11-01T10:00:00Z"
  },
  {
    "id": 2,
    "amount": "120.50",
    "description": "Weekly groceries",
    "date": "2023-11-05",
    "type": "expense",
    "category": 2,
    "created_at": "2023-11-05T15:30:00Z",
    "updated_at": "2023-11-05T15:30:00Z"
  }
]
```

### Filter Transactions

The transactions endpoint supports various filters:

- **By Date Range**: `GET /api/transactions/?start_date=2023-11-01&end_date=2023-11-30`
- **By Type**: `GET /api/transactions/?type=income` or `GET /api/transactions/?type=expense`
- **By Category**: `GET /api/transactions/?category=1`
- **By Search Term**: `GET /api/transactions/?search=groceries`

You can also use dedicated endpoints for income and expense transactions:

- `GET /api/transactions/income/`
- `GET /api/transactions/expense/`

### Create a Transaction

**Endpoint**: `POST /api/transactions/`

**Authentication**: Required

**Request Body**:
```json
{
  "amount": 75.25,
  "description": "Dinner with friends",
  "date": "2023-11-10",
  "type": "expense",
  "category": 5
}
```

**Response**: `201 Created`
```json
{
  "id": 3,
  "amount": "75.25",
  "description": "Dinner with friends",
  "date": "2023-11-10",
  "type": "expense",
  "category": 5,
  "created_at": "2023-11-10T20:15:00Z",
  "updated_at": "2023-11-10T20:15:00Z"
}
```

### Update a Transaction

**Endpoint**: `PUT /api/transactions/{id}/`

**Authentication**: Required

**Request Body**:
```json
{
  "amount": 80.00,
  "description": "Dinner with friends and dessert",
  "date": "2023-11-10",
  "type": "expense",
  "category": 5
}
```

**Response**: `200 OK`
```json
{
  "id": 3,
  "amount": "80.00",
  "description": "Dinner with friends and dessert",
  "date": "2023-11-10",
  "type": "expense",
  "category": 5,
  "created_at": "2023-11-10T20:15:00Z",
  "updated_at": "2023-11-10T20:30:00Z"
}
```

### Delete a Transaction

**Endpoint**: `DELETE /api/transactions/{id}/`

**Authentication**: Required

**Response**: `204 No Content`

## Budgets

Budgets allow users to set spending limits for specific categories in a given month.

### List All Budgets

**Endpoint**: `GET /api/budgets/`

**Authentication**: Required

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "amount": "500.00",
    "month": 11,
    "year": 2023,
    "category": 2,
    "spent_amount": "120.50",
    "remaining_amount": "379.50",
    "percentage_used": 24.1
  },
  {
    "id": 2,
    "amount": "200.00",
    "month": 11,
    "year": 2023,
    "category": 5,
    "spent_amount": "80.00",
    "remaining_amount": "120.00",
    "percentage_used": 40.0
  }
]
```

### Create a Budget

**Endpoint**: `POST /api/budgets/`

**Authentication**: Required

**Request Body**:
```json
{
  "amount": 300.00,
  "month": 11,
  "year": 2023,
  "category": 3
}
```

**Response**: `201 Created`
```json
{
  "id": 3,
  "amount": "300.00",
  "month": 11,
  "year": 2023,
  "category": 3,
  "spent_amount": "0.00",
  "remaining_amount": "300.00",
  "percentage_used": 0.0
}
```

### Update a Budget

**Endpoint**: `PUT /api/budgets/{id}/`

**Authentication**: Required

**Request Body**:
```json
{
  "amount": 350.00,
  "month": 11,
  "year": 2023,
  "category": 3
}
```

**Response**: `200 OK`
```json
{
  "id": 3,
  "amount": "350.00",
  "month": 11,
  "year": 2023,
  "category": 3,
  "spent_amount": "0.00",
  "remaining_amount": "350.00",
  "percentage_used": 0.0
}
```

### Delete a Budget

**Endpoint**: `DELETE /api/budgets/{id}/`

**Authentication**: Required

**Response**: `204 No Content`

## Summary and Dashboard

### Monthly Summary

Get a summary of income, expenses, and balance for a specific month.

**Endpoint**: `GET /api/summary/?month=11&year=2023`

**Authentication**: Required

**Response**: `200 OK`
```json
{
  "month": 11,
  "year": 2023,
  "total_income": "1500.00",
  "total_expenses": "200.50",
  "balance": "1299.50",
  "income_by_category": [
    {
      "category": "Salary",
      "amount": "1500.00"
    }
  ],
  "expenses_by_category": [
    {
      "category": "Groceries",
      "amount": "120.50"
    },
    {
      "category": "Dining Out",
      "amount": "80.00"
    }
  ]
}
```

### Dashboard

Get an overview of financial data including recent transactions, budget status, and monthly trends.

**Endpoint**: `GET /api/dashboard/`

**Authentication**: Required

**Response**: `200 OK`
```json
{
  "current_month_summary": {
    "month": 11,
    "year": 2023,
    "total_income": "1500.00",
    "total_expenses": "200.50",
    "balance": "1299.50"
  },
  "recent_transactions": [
    {
      "id": 3,
      "amount": "80.00",
      "description": "Dinner with friends and dessert",
      "date": "2023-11-10",
      "type": "expense",
      "category": 5
    },
    {
      "id": 2,
      "amount": "120.50",
      "description": "Weekly groceries",
      "date": "2023-11-05",
      "type": "expense",
      "category": 2
    }
  ],
  "budget_status": [
    {
      "id": 1,
      "category": "Groceries",
      "amount": "500.00",
      "spent": "120.50",
      "remaining": "379.50",
      "percentage": 24.1
    },
    {
      "id": 2,
      "category": "Dining Out",
      "amount": "200.00",
      "spent": "80.00",
      "remaining": "120.00",
      "percentage": 40.0
    }
  ],
  "monthly_trends": {
    "income": [
      {"month": 9, "year": 2023, "amount": "1500.00"},
      {"month": 10, "year": 2023, "amount": "1500.00"},
      {"month": 11, "year": 2023, "amount": "1500.00"}
    ],
    "expenses": [
      {"month": 9, "year": 2023, "amount": "950.75"},
      {"month": 10, "year": 2023, "amount": "1050.25"},
      {"month": 11, "year": 2023, "amount": "200.50"}
    ]
  }
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `204 No Content`: Request succeeded with no content to return
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or token expired
- `403 Forbidden`: Authenticated but not authorized to access the resource
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a message explaining the error:

```json
{
  "detail": "Error message describing the issue"
}
```

For validation errors, the response includes field-specific error messages:

```json
{
  "amount": ["This field is required."],
  "category": ["Invalid pk '999' - object does not exist."]
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10, max: 100)

Paginated responses include:

```json
{
  "count": 42,
  "next": "http://example.com/api/transactions/?page=2",
  "previous": null,
  "results": [
    // items for the current page
  ]
}
```

## Sorting and Ordering

Many endpoints support sorting with the `ordering` parameter:

- `GET /api/transactions/?ordering=date`: Sort by date (ascending)
- `GET /api/transactions/?ordering=-date`: Sort by date (descending)
- `GET /api/transactions/?ordering=amount`: Sort by amount (ascending)
- `GET /api/transactions/?ordering=-amount`: Sort by amount (descending)

Multiple fields can be specified: `ordering=type,-date`