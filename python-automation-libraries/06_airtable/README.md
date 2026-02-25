# 06 — pyairtable: Automating Real-World Workflows

`pyairtable` is the modern Python client for the Airtable REST API.
Automate CRM sync, content calendars, inventory, and any Airtable-powered workflow.

## Setup

1. Get your Personal Access Token: https://airtable.com/create/tokens
2. Copy `.env.example` to `.env` and fill in your credentials
3. Run examples

## Run the Examples

```bash
python basic_crud.py       # Requires real Airtable credentials
python sync_workflow.py    # Requires real Airtable credentials
python content_calendar.py # Requires real Airtable credentials
```

> **Note:** Examples include a mock mode so you can run them without credentials
> and see the expected behavior.

## Key Concepts

- `Api(token)` — authenticates with your Personal Access Token
- `api.table(base_id, table_name)` — reference a specific table
- `.all(formula="...")` — fetch all matching records (handles pagination)
- `.create({...})` — insert a new record
- `.update(record_id, {...})` — update specific fields
- `.delete(record_id)` — remove a record
- Airtable formula syntax: `Status = 'Active'`, `AND(...)`, `OR(...)`
