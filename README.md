# Fintastic

:money_with_wings: Fintastic is just a proof of concept of a fintech backend

## Quick start

- Download the repository
- Generate an environment file from the existing one `.env.example`
- Run the server with `make up` 

## Usage

Run server
`make up`

Stop server
`make down`

Run tests
`make test`

## Documentation
### Users
With this endpoint you will be able to create users

#### Create user

**POST** `/api/v1/users/`

| Name | Type | Description |
|---|---|---|
| name | String | Name of the user |
| email | String | Email of the user |
| age | Integer | Age of the user |

Example

```json
{
  "name": "Jane Doe",
  "email": "jane@email.com",
  "age": 23
}
```

Response

```json
{
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@email.com",
    "age": 23
}
```


### Transactions
Manage bank transactions made in a bank account


### Create transactions

**POST** `/api/v1/transactions/`

| Name | Type | Description |
|---|---|---|
| reference | String | Reference of the transaction |
| account | String | Account number |
| date | String | Date of the transaction |
| amount | String | Amount of the transaction |
| type | Enum: [inflow, outflow] | Type of the transaction. Must be positive if is _inflow_ and negative if _outflow_|
| category | String | Category where the transaction is categorized |
| user_id | Integer | User related with the transaction |


Example with single transaction

```json
{
  "reference": "000001",
  "account": "S00001",
  "date": "2020-01-01",
  "amount": "21.13",
  "type": "inflow",
  "category": "payment",
  "user_id": 1
}
```

Response

```json
{
  "reference": "000001",
  "account": "S00001",
  "date": "2020-01-01",
  "amount": "21.13",
  "type": "inflow",
  "category": "payment",
  "user_id": 1
}
```

Example with bulk creation

```json
[
  {
    "reference": "000001",
    "account": "S55555",
    "date": "2020-01-01",
    "amount": "21.13",
    "type": "inflow",
    "category": "payment",
    "user_id": 1
  },
  {
    "reference": "000002",
    "account": "S55555",
    "date": "2020-01-01",
    "amount": "-21.13",
    "type": "outflow",
    "category": "restaurant",
    "user_id": 1
  }
]
```

Response

```json
[
  {
    "reference": "000001",
    "account": "S55555",
    "date": "2020-01-01",
    "amount": "21.13",
    "type": "inflow",
    "category": "payment",
    "user_id": 1
  },
  {
    "reference": "000002",
    "account": "S55555",
    "date": "2020-01-01",
    "amount": "-21.13",
    "type": "outflow",
    "category": "restaurant",
    "user_id": 1
  }
]
```

### Get user balance

Given an user id, we are be able to see a summary by account that shows the balance of the account, total inflow and total outflows

**GET** `/api/v1/transactions/{user-id}`

Response

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "account": "S00099",
            "balance": "-294.52",
            "total_inflow": "0.00",
            "total_outflow": "-294.52"
        },
        {
            "account": "S55555",
            "balance": "24.52",
            "total_inflow": "105.65",
            "total_outflow": "-81.13"
        }
    ]
}
```


#### Filter results
We can filter the results by date using the params **date_before** and **date_after**

Examples

`/api/v1/transactions/1?date_after=2020-01-02`

`/api/v1/transactions/1?date_before=2020-01-02`

`/api/v1/transactions/1?date_after=2020-01-02&date_before=2020-05-02`

### Get user summary
We are able to see a user's summary by category that shows the sum of amounts per transaction category

**GET** `/api/v1/transactions/{user-id}/summary`

Response

```json
{
    "inflow": {
        "salary": 2500.72,
        "savings": 150.72
    },
    "outflow": {
        "groceries": -51.13,
        "other": -51.13,
        "rent": -560.0
    }
}
```
